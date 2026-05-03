#!/usr/bin/env python3

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import platform
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS_DIR = REPO_ROOT / "benchmarks"
DEFAULT_PLUTO = (REPO_ROOT / "../pluto/pluto").resolve()
DEFAULT_ZIG = (REPO_ROOT / ".toolchains/zig-aarch64-macos-0.15.2/zig").resolve()
DEFAULT_CC_CANDIDATES = (
    Path("/opt/homebrew/opt/llvm/bin/clang"),
    Path("/usr/local/opt/llvm/bin/clang"),
)
DEFAULT_CXX_CANDIDATES = (
    Path("/opt/homebrew/opt/llvm/bin/clang++"),
    Path("/usr/local/opt/llvm/bin/clang++"),
)
PT_MOD = REPO_ROOT / "pt.mod"
WORK_ROOT = Path(tempfile.gettempdir()) / "pluto-bench"
TARGET_POLICY_MODE = "host-native-where-supported"
# Keep the benchmark tables and CLI output in the natural progression order.
CASE_ORDER = ("sum", "fib", "fib_tail", "harmonic")
# The chart grid uses a different order so the short-running loop cases share
# the first row and the recursion-heavy cases share the second row.
CASE_GRID_ORDER = ("sum", "harmonic", "fib", "fib_tail")
CASE_LABELS = {
    "sum": "Sum",
    "fib": "Fib",
    "fib_tail": "Fib Tail",
    "harmonic": "Harmonic",
}

LANGUAGE_ORDER = (
    "pluto",
    "c",
    "cpp",
    "swift",
    "go",
    "rust",
    "zig",
    "julia",
    "luajit",
    "node",
    "bun",
    "python",
)
LANGUAGE_LABELS = {
    "pluto": "Pluto",
    "c": "C",
    "cpp": "C++",
    "swift": "Swift",
    "go": "Go",
    "rust": "Rust",
    "zig": "Zig",
    "julia": "Julia",
    "luajit": "LuaJIT",
    "node": "Node",
    "bun": "Bun",
    "python": "Python",
}
GENERATED_CASE_FILE_SUFFIXES = {
    ".o",
    ".out",
    ".exe",
    ".pdb",
    ".ilk",
    ".obj",
    ".a",
    ".so",
    ".dylib",
    ".dll",
    ".bc",
    ".ll",
    ".s",
}
LANGUAGE_TO_SOURCE = {
    "c": "main.c",
    "cpp": "main.cpp",
    "swift": "main.swift",
    "go": "main.go",
    "rust": "main.rs",
    "zig": "main.zig",
    "julia": "main.jl",
    "luajit": "main.lua",
    "node": "main.js",
    "bun": "main.js",
    "python": "main.py",
}
LANGUAGE_TO_TOOL = {
    "c": "cc",
    "cpp": "c++",
    "swift": "swiftc",
    "go": "go",
    "rust": "rustc",
    "zig": "zig",
    "julia": "julia",
    "luajit": "luajit",
    "node": "node",
    "bun": "bun",
}
LANGUAGE_TO_VERSION_CMD = {
    "c": ["cc", "--version"],
    "cpp": ["c++", "--version"],
    "swift": ["swift", "--version"],
    "go": ["go", "version"],
    "rust": ["rustc", "--version"],
    "zig": ["zig", "version"],
    "julia": ["julia", "--version"],
    "luajit": ["luajit", "-v"],
    "node": ["node", "--version"],
    "bun": ["bun", "--version"],
    "python": [sys.executable, "--version"],
}
PYTHON_NUMPY_VERSION_CMD = [
    sys.executable,
    "-c",
    (
        "import platform; import numpy as np; "
        "print(f'Python {platform.python_version()} + NumPy {np.__version__}')"
    ),
]
LANGUAGE_COLORS = {
    "pluto": "#c2410c",
    "c": "#2563eb",
    "cpp": "#16a34a",
    "swift": "#dc2626",
    "go": "#0891b2",
    "rust": "#6d28d9",
    "zig": "#ca8a04",
    "julia": "#7c3aed",
    "luajit": "#0e7490",
    "node": "#15803d",
    "bun": "#0f172a",
    "python": "#9333ea",
}


@dataclass
class Result:
    case: str
    language: str
    version: str
    compile_ms: float | None
    run_ms: float
    peak_memory_kb: int | None
    output: str


@dataclass(frozen=True)
class CommandSpec:
    cmd: list[str]
    env: dict[str, str] | None = None


@dataclass(frozen=True)
class CaseSource:
    case: str
    case_dir: Path
    source_dir: Path
    language: str
    source_name: str


@dataclass(frozen=True)
class Toolchain:
    pluto: Path
    zig: Path
    cc: Path
    cxx: Path
    luajit: Path


def ordered_cases(cases: list[str] | set[str]) -> list[str]:
    seen = set(cases)
    ordered = [case for case in CASE_ORDER if case in seen]
    ordered.extend(sorted(case for case in seen if case not in set(CASE_ORDER)))
    return ordered


def ordered_grid_cases(cases: list[str] | set[str]) -> list[str]:
    seen = set(cases)
    ordered = [case for case in CASE_GRID_ORDER if case in seen]
    ordered.extend(sorted(case for case in seen if case not in set(CASE_GRID_ORDER)))
    return ordered


def first_line(text: str) -> str:
    return text.strip().splitlines()[0] if text.strip() else ""


def normalized_machine() -> str:
    machine = platform.machine().lower()
    return {
        "amd64": "x86_64",
        "arm64": "aarch64",
    }.get(machine, machine)


def pluto_compile_env() -> dict[str, str]:
    return {"PLUTO_TARGET_CPU": "native"}


def c_family_target_args() -> list[str]:
    machine = normalized_machine()
    if machine == "x86_64":
        return ["-march=native"]
    if machine == "aarch64":
        return ["-mcpu=native"]
    return []


def rust_target_args() -> list[str]:
    machine = normalized_machine()
    if machine in {"x86_64", "aarch64"}:
        return ["-C", "target-cpu=native"]
    return []


def swift_target_args() -> list[str]:
    machine = normalized_machine()
    if machine in {"x86_64", "aarch64"}:
        return ["-target-cpu", "native"]
    return []


def host_cpu_flags() -> set[str]:
    machine = normalized_machine()
    if machine != "x86_64":
        return set()

    if sys.platform.startswith("linux"):
        try:
            cpuinfo = Path("/proc/cpuinfo").read_text(encoding="utf-8")
        except OSError:
            return set()
        match = re.search(r"^flags\s*:\s*(.+)$", cpuinfo, re.MULTILINE)
        return {flag.lower().replace(".", "_") for flag in match.group(1).split()} if match else set()

    if sys.platform == "darwin":
        keys = (
            "machdep.cpu.features",
            "machdep.cpu.leaf7_features",
        )
        flags: set[str] = set()
        for key in keys:
            raw = probe_first_line(["sysctl", "-n", key])
            if not raw:
                continue
            flags.update(flag.lower().replace(".", "_") for flag in raw.split())
        return flags

    return set()


def go_amd64_level() -> str | None:
    flags = host_cpu_flags()
    if not flags:
        return None

    level = "v1"
    if {
        "cx16",
        "lahf_lm",
        "popcnt",
        "sse3",
        "ssse3",
        "sse4_1",
        "sse4_2",
    }.issubset(flags):
        level = "v2"
    if {
        "avx",
        "avx2",
        "bmi1",
        "bmi2",
        "f16c",
        "fma",
        "movbe",
        "osxsave",
    }.issubset(flags) and ("lzcnt" in flags or "abm" in flags):
        level = "v3"
    if {
        "avx512f",
        "avx512dq",
        "avx512cd",
        "avx512bw",
        "avx512vl",
    }.issubset(flags):
        level = "v4"
    return level


def go_compile_env() -> dict[str, str]:
    machine = normalized_machine()
    if machine == "x86_64":
        level = go_amd64_level()
        if level is not None:
            return {"GOAMD64": level}
    return {}


def target_policy_metadata() -> dict[str, object]:
    go_env = go_compile_env()
    return {
        "mode": TARGET_POLICY_MODE,
        "machine": normalized_machine(),
        "pluto": {
            "env": pluto_compile_env(),
        },
        "c": {
            "flags": c_family_target_args(),
        },
        "cpp": {
            "flags": c_family_target_args(),
        },
        "swift": {
            "flags": swift_target_args(),
        },
        "go": {
            "env": go_env,
            "mode": "native" if go_env else "default",
            "reason": None if go_env else "no portable host-native override configured",
        },
        "rust": {
            "flags": rust_target_args(),
        },
        "zig": {
            "flags": zig_compile_target_args(),
        },
    }


def normalize_version(language: str, raw: str) -> str:
    if not raw:
        return "unknown"
    if language == "pluto":
        return raw.split(" (", 1)[0]
    if language in {"c", "cpp"}:
        distro_match = re.match(r"^(Apple|Homebrew|Ubuntu)\s+clang version\s+(\S+)", raw)
        if distro_match:
            return f"{distro_match.group(1)} clang {distro_match.group(2)}"
        clang_match = re.match(r"^clang version\s+(\S+)", raw)
        if clang_match:
            return f"clang {clang_match.group(1)}"
    if language == "swift":
        marker = "Swift version "
        idx = raw.find(marker)
        if idx != -1:
            tail = raw[idx + len(marker):].split()
            if tail:
                return f"Swift {tail[0]}"
    if language == "go" and raw.startswith("go version "):
        parts = raw.split()
        if len(parts) >= 3:
            return parts[2]
    if language == "rust" and raw.startswith("rustc "):
        parts = raw.split()
        if len(parts) >= 2:
            return f"rustc {parts[1]}"
    if language == "zig":
        return f"zig {raw}"
    if language == "julia" and raw.startswith("julia version "):
        parts = raw.split()
        if len(parts) >= 3:
            return f"Julia {parts[2]}"
    if language == "luajit":
        luajit_match = re.match(r"^LuaJIT\s+(\S+)", raw)
        if luajit_match:
            return f"LuaJIT {luajit_match.group(1)}"
    if language == "node" and raw.startswith("v"):
        return f"Node {raw}"
    if language == "bun":
        return f"Bun {raw}"
    return raw


def timed_run(spec: CommandSpec, cwd: Path) -> tuple[float, subprocess.CompletedProcess[str]]:
    env = None if spec.env is None else {**os.environ, **spec.env}
    start = time.perf_counter()
    proc = subprocess.run(
        spec.cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000.0
    if proc.returncode != 0:
        details = []
        if proc.stdout.strip():
            details.append(proc.stdout.strip())
        if proc.stderr.strip():
            details.append(proc.stderr.strip())
        detail_text = "\n".join(details)
        raise RuntimeError(
            f"command failed: {' '.join(spec.cmd)}"
            + (f"\n{detail_text}" if detail_text else "")
        )
    return elapsed_ms, proc


def prepare_workdir(base: str, language: str, repeat: str | int) -> Path:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    workdir = Path(
        tempfile.mkdtemp(
            prefix=f"{base}_{language}_{repeat}_",
            dir=WORK_ROOT,
        )
    )
    if PT_MOD.exists():
        shutil.copy2(PT_MOD, workdir / PT_MOD.name)
    return workdir


def copy_case_files(source_dir: Path, workdir: Path) -> None:
    for path in source_dir.iterdir():
        if not path.is_file():
            continue
        if path.suffix in GENERATED_CASE_FILE_SUFFIXES:
            continue
        # Extensionless executables such as stray local "main" binaries should
        # not leak into temp workdirs and influence benchmark runs.
        if not path.suffix and os.access(path, os.X_OK):
            continue
        shutil.copy2(path, workdir / path.name)


def zig_compile_target_args() -> list[str]:
    machine = normalized_machine()

    if sys.platform.startswith("linux"):
        triple = {
            "x86_64": "x86_64-linux-gnu",
            "aarch64": "aarch64-linux-gnu",
        }.get(machine)
    elif sys.platform == "darwin":
        triple = {
            "x86_64": "x86_64-macos-none",
            "aarch64": "aarch64-macos-none",
        }.get(machine)
    else:
        triple = None

    if triple is None:
        return ["-mcpu", "native"]

    return ["-target", triple, "-mcpu", "native"]


def commands_for(
    source: CaseSource,
    workdir: Path,
    toolchain: Toolchain,
) -> tuple[CommandSpec | None, CommandSpec]:
    stem = Path(source.source_name).stem
    if source.language == "pluto":
        compile_cmd = CommandSpec(
            [str(toolchain.pluto), source.source_name],
            env=pluto_compile_env(),
        )
        run_cmd = CommandSpec([str(workdir / stem)])
    elif source.language == "c":
        compile_cmd = CommandSpec(
            [str(toolchain.cc), "-O3", *c_family_target_args(), source.source_name, "-o", stem],
        )
        run_cmd = CommandSpec([str(workdir / stem)])
    elif source.language == "cpp":
        compile_cmd = CommandSpec(
            [str(toolchain.cxx), "-O3", *c_family_target_args(), source.source_name, "-o", stem],
        )
        run_cmd = CommandSpec([str(workdir / stem)])
    elif source.language == "swift":
        compile_cmd = CommandSpec(
            ["swiftc", "-O", *swift_target_args(), source.source_name, "-o", stem],
        )
        run_cmd = CommandSpec([str(workdir / stem)])
    elif source.language == "go":
        compile_cmd = CommandSpec(
            ["go", "build", "-trimpath", "-o", stem, source.source_name],
            env=go_compile_env(),
        )
        run_cmd = CommandSpec([str(workdir / stem)])
    elif source.language == "rust":
        compile_cmd = CommandSpec(
            ["rustc", "-C", "opt-level=3", *rust_target_args(), source.source_name, "-o", stem],
        )
        run_cmd = CommandSpec([str(workdir / stem)])
    elif source.language == "zig":
        compile_cmd = CommandSpec(
            [
                str(toolchain.zig),
                "build-exe",
                "-O",
                "ReleaseFast",
                *zig_compile_target_args(),
                f"-femit-bin={workdir / stem}",
                source.source_name,
            ],
        )
        run_cmd = CommandSpec([str(workdir / stem)])
    elif source.language == "julia":
        compile_cmd = None
        run_cmd = CommandSpec(["julia", "--startup-file=no", source.source_name])
    elif source.language == "luajit":
        compile_cmd = None
        run_cmd = CommandSpec([str(toolchain.luajit), source.source_name])
    elif source.language == "node":
        compile_cmd = None
        run_cmd = CommandSpec(["node", source.source_name])
    elif source.language == "bun":
        compile_cmd = None
        run_cmd = CommandSpec(["bun", source.source_name])
    elif source.language == "python":
        compile_cmd = None
        run_cmd = CommandSpec([sys.executable, source.source_name])
    else:
        raise ValueError(f"unsupported language: {source.language}")
    return compile_cmd, run_cmd


def resolve_pluto(path_arg: str | None) -> Path:
    raw_path = path_arg or os.environ.get("PLUTO_BIN")
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    return DEFAULT_PLUTO


def resolve_zig(path_arg: str | None) -> Path:
    raw_path = path_arg or os.environ.get("ZIG_BIN")
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    if DEFAULT_ZIG.exists():
        return DEFAULT_ZIG
    found = shutil.which("zig")
    return Path(found).resolve() if found else DEFAULT_ZIG


def resolve_compiler(path_arg: str | None, env_name: str, candidates: tuple[Path, ...], fallback: str) -> Path:
    raw_path = path_arg or os.environ.get(env_name)
    if raw_path:
        return Path(raw_path).expanduser()
    for candidate in candidates:
        if candidate.exists():
            return candidate
    found = shutil.which(fallback)
    return Path(found) if found else candidates[0]


def resolve_cc(path_arg: str | None) -> Path:
    return resolve_compiler(path_arg, "CC_BIN", DEFAULT_CC_CANDIDATES, "cc")


def resolve_cxx(path_arg: str | None) -> Path:
    return resolve_compiler(path_arg, "CXX_BIN", DEFAULT_CXX_CANDIDATES, "c++")


def resolve_tool(path_arg: str | None, env_name: str, fallback: str) -> Path:
    raw_path = path_arg or os.environ.get(env_name)
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    found = shutil.which(fallback)
    return Path(found).resolve() if found else Path(fallback)


def resolve_luajit(path_arg: str | None) -> Path:
    return resolve_tool(path_arg, "LUAJIT_BIN", "luajit")


def language_available(language: str, toolchain: Toolchain) -> bool:
    if language == "pluto":
        return toolchain.pluto.exists()
    if language == "c":
        return toolchain.cc.exists()
    if language == "cpp":
        return toolchain.cxx.exists()
    if language == "zig":
        return toolchain.zig.exists()
    if language == "luajit":
        return toolchain.luajit.exists()
    if language == "python":
        return True
    tool = LANGUAGE_TO_TOOL.get(language)
    if tool is None:
        return False
    return shutil.which(tool) is not None


def language_version(language: str, toolchain: Toolchain) -> str:
    if language == "pluto":
        if not toolchain.pluto.exists():
            return "not found"
        proc = subprocess.run(
            [str(toolchain.pluto), "-version"],
            capture_output=True,
            text=True,
            check=False,
        )
        text = proc.stdout if proc.stdout.strip() else proc.stderr
        return normalize_version(language, first_line(text))
    if language == "c":
        if not toolchain.cc.exists():
            return "not found"
        proc = subprocess.run([str(toolchain.cc), "--version"], capture_output=True, text=True, check=False)
        text = proc.stdout if proc.stdout.strip() else proc.stderr
        return normalize_version(language, first_line(text))
    if language == "cpp":
        if not toolchain.cxx.exists():
            return "not found"
        proc = subprocess.run([str(toolchain.cxx), "--version"], capture_output=True, text=True, check=False)
        text = proc.stdout if proc.stdout.strip() else proc.stderr
        return normalize_version(language, first_line(text))
    if language == "zig":
        if not toolchain.zig.exists():
            return "not found"
        proc = subprocess.run([str(toolchain.zig), "version"], capture_output=True, text=True, check=False)
        text = proc.stdout if proc.stdout.strip() else proc.stderr
        return normalize_version(language, first_line(text))
    if language == "luajit":
        if not toolchain.luajit.exists():
            return "not found"
        proc = subprocess.run([str(toolchain.luajit), "-v"], capture_output=True, text=True, check=False)
        text = proc.stdout if proc.stdout.strip() else proc.stderr
        return normalize_version(language, first_line(text))

    cmd = LANGUAGE_TO_VERSION_CMD.get(language)
    if cmd is None:
        return "unknown"
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    text = proc.stdout if proc.stdout.strip() else proc.stderr
    return normalize_version(language, first_line(text))


def source_uses_numpy(source: CaseSource) -> bool:
    if source.language != "python":
        return False
    try:
        text = (source.source_dir / source.source_name).read_text(encoding="utf-8")
    except OSError:
        return False
    return "import numpy" in text or "from numpy" in text


def source_available(source: CaseSource, toolchain: Toolchain) -> bool:
    if source.language != "python" or not source_uses_numpy(source):
        return language_available(source.language, toolchain)
    proc = subprocess.run(
        [sys.executable, "-c", "import numpy"],
        capture_output=True,
        text=True,
        check=False,
    )
    return proc.returncode == 0


def source_version(source: CaseSource, toolchain: Toolchain) -> str:
    if source.language != "python" or not source_uses_numpy(source):
        return language_version(source.language, toolchain)
    proc = subprocess.run(
        PYTHON_NUMPY_VERSION_CMD,
        capture_output=True,
        text=True,
        check=False,
    )
    text = proc.stdout if proc.stdout.strip() else proc.stderr
    return first_line(text) or "unknown"


def probe_first_line(cmd: list[str], cwd: Path | None = None) -> str | None:
    executable = cmd[0]
    if not Path(executable).exists() and shutil.which(executable) is None:
        return None
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=False,
        )
    except OSError:
        return None
    text = proc.stdout if proc.stdout.strip() else proc.stderr
    line = first_line(text)
    return line or None


def command_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    if extra is None:
        return dict(os.environ)
    return {**os.environ, **extra}


def resolved_command_metadata(
    name: str,
    args: list[str],
    *,
    env: dict[str, str] | None = None,
) -> dict[str, str | None]:
    path = shutil.which(name, path=env.get("PATH") if env else None)
    if path is None:
        return {
            "command": name,
            "bin": None,
            "version": None,
        }
    version = probe_first_line([path, *args])
    return {
        "command": name,
        "bin": path,
        "version": version,
    }


def format_tool_metadata(tool: dict[str, object]) -> str:
    bin_path = tool.get("bin")
    version = tool.get("version")
    if bin_path and version:
        return f"{bin_path} | {version}"
    if bin_path:
        return str(bin_path)
    return f"{tool.get('command') or 'tool'} unavailable"


def pluto_llvm_metadata() -> dict[str, str | None]:
    llvm_config = resolved_command_metadata("llvm-config", ["--version"])
    version = llvm_config.get("version")
    return {
        "mode": "in-process",
        "version": f"LLVM {version}" if version else None,
        "source": "llvm-config" if llvm_config.get("bin") else None,
        "bin": llvm_config.get("bin"),
    }


def format_pluto_llvm_metadata(tool: dict[str, object]) -> str:
    mode = tool.get("mode") or "in-process"
    version = tool.get("version") or "unknown LLVM"
    bin_path = tool.get("bin")
    source = tool.get("source")
    if bin_path and source:
        return f"{mode} {version} | {source} {bin_path}"
    return f"{mode} {version}"


def find_git_repo_root(start: Path) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return None


def git_repo_metadata(start: Path) -> dict[str, str | bool | None] | None:
    repo_root = find_git_repo_root(start)
    if repo_root is None:
        return None

    commit = probe_first_line(["git", "-C", str(repo_root), "rev-parse", "HEAD"])
    branch = probe_first_line(["git", "-C", str(repo_root), "branch", "--show-current"])
    status = probe_first_line(["git", "-C", str(repo_root), "status", "--short"])
    return {
        "git_commit": commit,
        "git_branch": branch,
        "git_dirty": bool(status),
    }


def file_metadata(path: Path) -> dict[str, object]:
    try:
        stat = path.stat()
    except OSError:
        return {}
    modified = dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc)
    return {
        "binary_mtime": modified.isoformat(timespec="seconds").replace("+00:00", "Z"),
    }


def total_memory_kb() -> int | None:
    if sys.platform == "darwin":
        raw = probe_first_line(["sysctl", "-n", "hw.memsize"])
        if raw and raw.isdigit():
            return max(1, int(raw) // 1024)
        return None

    if sys.platform.startswith("linux"):
        try:
            meminfo = Path("/proc/meminfo").read_text(encoding="utf-8")
        except OSError:
            return None
        match = re.search(r"^MemTotal:\s+(\d+)\s+kB$", meminfo, re.MULTILINE)
        if match:
            return int(match.group(1))
    return None


def host_metadata() -> dict[str, object]:
    host = {
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cpu_count": os.cpu_count(),
        "python_version": platform.python_version(),
    }
    cpu_name = (
        probe_first_line(["sysctl", "-n", "machdep.cpu.brand_string"])
        if sys.platform == "darwin"
        else None
    )
    if not cpu_name and sys.platform.startswith("linux"):
        try:
            cpuinfo = Path("/proc/cpuinfo").read_text(encoding="utf-8")
        except OSError:
            cpuinfo = ""
        match = re.search(r"^model name\s*:\s*(.+)$", cpuinfo, re.MULTILINE)
        if match:
            cpu_name = match.group(1).strip()
    if not cpu_name:
        cpu_name = platform.processor() or None
    if cpu_name:
        host["cpu_name"] = cpu_name
    total_mem = total_memory_kb()
    if total_mem is not None:
        host["total_memory_kb"] = total_mem
    return host


def snapshot_metadata(toolchain: Toolchain) -> dict[str, object]:
    prefix = peak_memory_command_prefix()
    target_policy = target_policy_metadata()
    pluto = {
        "bin": str(toolchain.pluto),
        "version": language_version("pluto", toolchain),
        "target_cpu": target_policy["pluto"]["env"]["PLUTO_TARGET_CPU"],
        "llvm": pluto_llvm_metadata(),
        "linker": resolved_command_metadata(
            "clang",
            ["--version"],
            env=command_env(pluto_compile_env()),
        ),
    }
    pluto.update(file_metadata(toolchain.pluto))
    pluto_repo = git_repo_metadata(toolchain.pluto)
    if pluto_repo is not None:
        pluto.update(pluto_repo)

    metadata: dict[str, object] = {
        "benchmark": {
            "generator": str(Path(__file__).resolve().relative_to(REPO_ROOT)),
            "process_model": "fresh-process",
            "warmup_runs_per_sample": 1,
            "time_unit": "ms",
        },
        "host": host_metadata(),
        "bench": git_repo_metadata(REPO_ROOT),
        "pluto": pluto,
        "c": {
            "bin": str(toolchain.cc),
            "version": language_version("c", toolchain),
        },
        "cpp": {
            "bin": str(toolchain.cxx),
            "version": language_version("cpp", toolchain),
        },
        "zig": {
            "bin": str(toolchain.zig),
            "version": language_version("zig", toolchain),
        },
        "luajit": {
            "bin": str(toolchain.luajit),
            "version": language_version("luajit", toolchain),
        },
        "memory_measurement": {
            "enabled": prefix is not None,
            "collector": " ".join(prefix) if prefix else None,
            "unit": "KiB",
        },
        "target_policy": target_policy,
    }
    return metadata


def short_commit(commit: str | None) -> str:
    if not commit:
        return "unknown"
    return commit[:12]


def branch_label(repo: dict[str, object] | None) -> str:
    if not repo:
        return "unknown"
    branch = repo.get("git_branch") or "detached"
    dirty = " dirty" if repo.get("git_dirty") else ""
    return f"{branch}{dirty}"


def format_total_memory_kb(value: int | None) -> str:
    if value is None:
        return "unknown RAM"
    gib = value / (1024.0 * 1024.0)
    if gib >= 100:
        return f"{gib:.0f} GiB RAM"
    return f"{gib:.1f} GiB RAM"


def metadata_summary_lines(metadata: dict[str, object]) -> list[str]:
    benchmark = metadata.get("benchmark", {})
    host = metadata.get("host", {})
    bench = metadata.get("bench", {})
    pluto = metadata.get("pluto", {})
    c_meta = metadata.get("c", {})
    cpp_meta = metadata.get("cpp", {})
    memory = metadata.get("memory_measurement", {})
    target_policy = metadata.get("target_policy", {})

    host_bits = [
        host.get("cpu_name") or host.get("machine") or "unknown host",
        host.get("platform") or "unknown platform",
    ]
    if host.get("cpu_count") is not None:
        host_bits.append(f"{host['cpu_count']} cores")
    host_bits.append(format_total_memory_kb(host.get("total_memory_kb")))
    if host.get("python_version"):
        host_bits.append(f"Python {host['python_version']}")

    lines = [
        "Benchmark metadata:",
        f"  Bench: {branch_label(bench)} @ {short_commit(bench.get('git_commit'))}",
        f"  Pluto: {pluto.get('version') or 'unknown'}",
        (
            f"  Pluto Binary: {pluto.get('bin') or 'unknown'}"
            + (f" | modified {pluto['binary_mtime']}" if pluto.get("binary_mtime") else "")
        ),
        f"  Pluto Repo: {branch_label(pluto)} @ {short_commit(pluto.get('git_commit'))}",
        f"  Host: {' | '.join(str(bit) for bit in host_bits if bit)}",
        (
            "  Mode: "
            f"{benchmark.get('process_model') or 'unknown'} | "
            f"warm-up x{benchmark.get('warmup_runs_per_sample') or '?'} | "
            f"units {benchmark.get('time_unit') or '?'}"
        ),
    ]
    if isinstance(pluto, dict) and isinstance(pluto.get("llvm"), dict):
        lines.append("  Pluto LLVM: " + format_pluto_llvm_metadata(pluto["llvm"]))
    if isinstance(pluto, dict) and isinstance(pluto.get("linker"), dict):
        lines.append("  Pluto Linker: " + format_tool_metadata(pluto["linker"]))
    if isinstance(c_meta, dict) and c_meta.get("bin"):
        lines.append(f"  C Compiler: {c_meta['bin']} | {c_meta.get('version') or 'unknown'}")
    if isinstance(cpp_meta, dict) and cpp_meta.get("bin"):
        lines.append(f"  C++ Compiler: {cpp_meta['bin']} | {cpp_meta.get('version') or 'unknown'}")
    if memory.get("enabled"):
        collector = memory.get("collector") or "unknown collector"
        lines.append(f"  Peak Memory: enabled via {collector}")
    else:
        lines.append("  Peak Memory: unavailable on this host")
    if target_policy:
        lines.append(
            "  Target Policy: "
            + str(target_policy.get("mode") or "unknown")
        )
    return lines


def print_metadata_summary(metadata: dict[str, object]) -> None:
    print("\n".join(metadata_summary_lines(metadata)))
    print()


def load_expected(case_dir: Path) -> str | None:
    expected_file = case_dir / "expected.txt"
    if not expected_file.exists():
        return None
    return expected_file.read_text(encoding="utf-8").strip()


def svg_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def format_ms(value: float) -> str:
    if value >= 100:
        return f"{value:.0f} ms"
    if value >= 10:
        return f"{value:.1f} ms"
    return f"{value:.2f} ms"


def format_memory_kb(value: float) -> str:
    mib = value / 1024.0
    if mib >= 100:
        return f"{mib:.0f} MiB"
    if mib >= 10:
        return f"{mib:.1f} MiB"
    return f"{mib:.2f} MiB"


def metric_value(result: Result, metric_name: str) -> float | None:
    if metric_name == "run":
        return result.run_ms
    if metric_name == "compile":
        return result.compile_ms
    if metric_name == "memory":
        return float(result.peak_memory_kb) if result.peak_memory_kb is not None else None
    raise ValueError(f"unsupported metric: {metric_name}")


def display_label(result: Result) -> str:
    if result.language == "python" and "NumPy" in result.version:
        return "Python (with NumPy)"
    return LANGUAGE_LABELS[result.language]


def format_metric(metric_name: str, value: float) -> str:
    if metric_name in {"run", "compile"}:
        return format_ms(value)
    if metric_name == "memory":
        return format_memory_kb(value)
    raise ValueError(f"unsupported metric: {metric_name}")


def nice_tick_step(max_val: float, *, max_ticks: int = 6) -> float:
    if max_val <= 0:
        return 1.0
    raw_step = max_val / max(1, max_ticks - 1)
    magnitude = 10 ** math.floor(math.log10(raw_step))
    residual = raw_step / magnitude
    if residual <= 1:
        nice = 1
    elif residual <= 2:
        nice = 2
    elif residual <= 5:
        nice = 5
    else:
        nice = 10
    return float(nice * magnitude)


def compile_tick_values(max_val: float) -> list[float]:
    step = nice_tick_step(max_val)
    limit = math.ceil(max_val / step) * step
    tick_count = int(round(limit / step))
    return [step * idx for idx in range(tick_count + 1)]


def memory_tick_values(max_val: float) -> list[float]:
    max_mib = max_val / 1024.0
    step_mib = nice_tick_step(max_mib)
    limit_mib = math.ceil(max_mib / step_mib) * step_mib
    tick_count = int(round(limit_mib / step_mib))
    return [step_mib * idx * 1024 for idx in range(tick_count + 1)]


def tick_values(metric_name: str, max_val: float) -> list[float]:
    if metric_name in {"run", "compile"}:
        return compile_tick_values(max_val)
    if metric_name == "memory":
        return memory_tick_values(max_val)
    raise ValueError(f"unsupported metric: {metric_name}")


def peak_memory_command_prefix() -> list[str] | None:
    time_bin = "/usr/bin/time"
    if not Path(time_bin).exists():
        return None
    if sys.platform == "darwin":
        return [time_bin, "-l"]
    if sys.platform.startswith("linux"):
        return [time_bin, "-v"]
    return None


def parse_peak_memory_kb(stderr_text: str) -> int | None:
    linux_match = re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)", stderr_text)
    if linux_match:
        return int(linux_match.group(1))

    darwin_match = re.search(r"^\s*(\d+)\s+maximum resident set size", stderr_text, re.MULTILINE)
    if darwin_match:
        # BSD time -l reports this field in bytes; normalize to KiB so Linux and
        # macOS snapshots use the same stored unit.
        return max(1, int(darwin_match.group(1)) // 1024)

    footprint_match = re.search(r"^\s*(\d+)\s+peak memory footprint", stderr_text, re.MULTILINE)
    if footprint_match:
        return max(1, int(footprint_match.group(1)) // 1024)
    return None


def probe_peak_memory_kb(spec: CommandSpec, cwd: Path) -> int | None:
    prefix = peak_memory_command_prefix()
    if prefix is None:
        return None
    env = None if spec.env is None else {**os.environ, **spec.env}
    proc = subprocess.run(
        prefix + spec.cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        details = []
        if proc.stdout.strip():
            details.append(proc.stdout.strip())
        if proc.stderr.strip():
            details.append(proc.stderr.strip())
        detail_text = "\n".join(details)
        raise RuntimeError(
            f"command failed: {' '.join(prefix + spec.cmd)}"
            + (f"\n{detail_text}" if detail_text else "")
        )
    return parse_peak_memory_kb(proc.stderr)


def render_bar_chart(
    path: Path,
    *,
    title: str,
    subtitle: str,
    cases: list[str],
    results_by_case: dict[str, list[Result]],
    metric_name: str,
    columns: int | None = None,
) -> None:
    font = (
        'font-family="ui-sans-serif, system-ui, -apple-system, '
        'BlinkMacSystemFont, sans-serif"'
    )

    # Collect per-case entries sorted by value (fastest first).
    case_data: list[tuple[str, list[tuple[Result, float]]]] = []
    all_values: list[float] = []
    for case in ordered_grid_cases(cases):
        entries: list[tuple[Result, float]] = []
        for result in results_by_case.get(case, []):
            value = metric_value(result, metric_name)
            if value is not None:
                entries.append((result, value))
                all_values.append(value)
        # Pin Pluto at the top, then sort the rest by value.
        pluto_entries = [e for e in entries if e[0].language == "pluto"]
        other_entries = sorted(
            (e for e in entries if e[0].language != "pluto"), key=lambda e: e[1],
        )
        case_data.append((case, pluto_entries + other_entries))

    if not all_values:
        return

    default_columns = 1 if len(case_data) == 1 else 2
    columns = max(1, min(columns or default_columns, len(case_data)))
    svg_width = 760 if columns == 1 else 1320
    outer_pad_x = 32
    gutter_x = 28
    gutter_y = 28
    header_h = 96
    footer_h = 36
    panel_w = int((svg_width - (outer_pad_x * 2) - (gutter_x * (columns - 1))) / columns)
    panel_pad_x = 18
    panel_pad_top = 18
    panel_pad_bottom = 18
    longest_label = max(
        len(display_label(result))
        for _, entries in case_data
        for result, _ in entries
    )
    label_w = max(68, longest_label * 7 + 12)
    value_pad = 86
    bar_max = panel_w - (panel_pad_x * 2) - label_w - value_pad
    bar_h = 20
    pluto_bar_h = 24
    bar_gap = 6
    pluto_gap = 10
    title_h = 30
    axis_h = 18

    panel_heights: list[int] = []
    for _, entries in case_data:
        bars_h = 0
        for lang, _ in entries:
            bars_h += (pluto_bar_h if lang == "pluto" else bar_h) + bar_gap
            if lang == "pluto":
                bars_h += pluto_gap
        panel_heights.append(panel_pad_top + title_h + axis_h + bars_h + panel_pad_bottom)

    row_heights: list[int] = []
    for row_idx in range(0, len(panel_heights), columns):
        row_heights.append(max(panel_heights[row_idx:row_idx + columns]))

    svg_height = header_h + footer_h + sum(row_heights)
    if row_heights:
        svg_height += gutter_y * (len(row_heights) - 1)

    lines: list[str] = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" '
        f'height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}" '
        f'role="img" aria-labelledby="chart-title chart-desc">'
    )
    lines.append(f'<title id="chart-title">{svg_escape(title)}</title>')
    lines.append(f'<desc id="chart-desc">{svg_escape(subtitle)}</desc>')
    lines.append(f'<rect width="{svg_width}" height="{svg_height}" fill="#f8fafc" />')
    lines.append(
        f'<text x="{label_w}" y="40" fill="#0f172a" font-size="24" '
        f'font-weight="700" {font}>{svg_escape(title)}</text>'
    )
    lines.append(
        f'<text x="{label_w}" y="64" fill="#475569" font-size="13" '
        f'{font}>{svg_escape(subtitle)}</text>'
    )

    row_y = header_h
    row_idx = 0
    for idx, (case, entries) in enumerate(case_data):
        if idx and idx % columns == 0:
            row_y += row_heights[row_idx] + gutter_y
            row_idx += 1

        col_idx = idx % columns
        panel_x = outer_pad_x + (col_idx * (panel_w + gutter_x))
        panel_y = row_y
        panel_h = panel_heights[idx]
        chart_left = panel_x + panel_pad_x + label_w
        chart_right = panel_x + panel_w - panel_pad_x
        label_x = chart_left - 10
        title_x = panel_x + panel_pad_x
        title_y = panel_y + panel_pad_top + 14
        grid_top = panel_y + panel_pad_top + title_h + axis_h

        lines.append(
            f'<rect x="{panel_x}" y="{panel_y}" width="{panel_w}" height="{panel_h}" '
            f'rx="16" fill="#ffffff" stroke="#e2e8f0" stroke-width="1.5" />'
        )

        # Per-case axis range (linear).
        case_max_val = max(v for _, v in entries)
        raw_max = case_max_val * 1.08 if case_max_val else 1.0
        case_ticks = tick_values(metric_name, raw_max)
        case_axis_max = max(case_ticks)

        case_label = CASE_LABELS.get(case, case.replace("_", " ").title())
        lines.append(
            f'<text x="{title_x}" y="{title_y}" fill="#0f172a" font-size="16" '
            f'font-weight="700" {font}>{svg_escape(case_label)}</text>'
        )

        case_bars_h = 0
        for result, _ in entries:
            case_bars_h += (pluto_bar_h if result.language == "pluto" else bar_h) + bar_gap
            if result.language == "pluto":
                case_bars_h += pluto_gap
        grid_bottom = grid_top + case_bars_h

        for tick in case_ticks:
            tx = chart_left + (tick / case_axis_max) * bar_max
            lines.append(
                f'<line x1="{tx:.1f}" y1="{grid_top}" x2="{tx:.1f}" '
                f'y2="{grid_bottom}" stroke="#e2e8f0" stroke-width="1" />'
            )
            lines.append(
                f'<text x="{tx:.1f}" y="{grid_top - 6}" text-anchor="middle" '
                f'fill="#94a3b8" font-size="10" {font}>'
                f'{svg_escape(format_metric(metric_name, tick))}</text>'
            )

        bar_y = grid_top
        for result, value in entries:
            is_pluto = result.language == "pluto"
            color = LANGUAGE_COLORS[result.language]
            bw = max((value / case_axis_max) * bar_max, 2)
            current_bar_h = pluto_bar_h if is_pluto else bar_h
            text_y = bar_y + current_bar_h / 2 + 4.5

            weight = "700" if is_pluto else "400"
            lines.append(
                f'<text x="{label_x}" y="{text_y:.1f}" text-anchor="end" '
                f'fill="#0f172a" font-size="13" font-weight="{weight}" '
                f'{font}>{svg_escape(display_label(result))}</text>'
            )

            opacity = "1.0" if is_pluto else "0.82"
            border = f' stroke="{color}" stroke-width="1.5"' if is_pluto else ""
            lines.append(
                f'<rect x="{chart_left}" y="{bar_y}" width="{bw:.1f}" '
                f'height="{current_bar_h}" rx="4" fill="{color}" '
                f'fill-opacity="{opacity}"{border} />'
            )

            value_text = format_metric(metric_name, value)
            value_x = chart_left + bw + 8
            value_anchor = "start"
            if value_x + (len(value_text) * 7) > chart_right:
                value_x = chart_right
                value_anchor = "end"
            lines.append(
                f'<text x="{value_x:.1f}" y="{text_y:.1f}" text-anchor="{value_anchor}" '
                f'fill="#334155" font-size="12" {font}>{value_text}</text>'
            )

            bar_y += current_bar_h + bar_gap
            if is_pluto:
                bar_y += pluto_gap

    # Footer.
    lines.append(
        f'<text x="{svg_width / 2:.1f}" y="{svg_height - 12}" '
        f'text-anchor="middle" fill="#94a3b8" font-size="12" {font}>'
        f'Lower is better</text>'
    )
    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_snapshot(
    snapshot_dir: Path,
    *,
    cases: list[str],
    results_by_case: dict[str, list[Result]],
    repeat: int,
    toolchain: Toolchain,
) -> None:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    generated_at = dt.datetime.now().astimezone().isoformat()
    snapshot = {
        "generated_at": generated_at,
        "repeat": repeat,
        "pluto_bin": str(toolchain.pluto),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "metadata": snapshot_metadata(toolchain),
        "cases": [
            {
                "name": case,
                "results": [
                    {
                        "language": result.language,
                        "version": result.version,
                        "compile_ms": result.compile_ms,
                        "run_ms": result.run_ms,
                        "peak_memory_kb": result.peak_memory_kb,
                        "output": result.output,
                    }
                    for result in results_by_case.get(case, [])
                ],
            }
            for case in cases
        ],
    }
    (snapshot_dir / "results.json").write_text(
        json.dumps(snapshot, indent=2) + "\n",
        encoding="utf-8",
    )

    render_bar_chart(
        snapshot_dir / "run-times.svg",
        title="Run Time Median by Benchmark",
        subtitle="Each benchmark uses its own linear scale. Pluto pinned first, rest sorted fastest-first.",
        cases=cases,
        results_by_case=results_by_case,
        metric_name="run",
        columns=2,
    )
    render_bar_chart(
        snapshot_dir / "run-times-mobile.svg",
        title="Run Time Median by Benchmark",
        subtitle="Each benchmark uses its own linear scale. Pluto pinned first, rest sorted fastest-first.",
        cases=cases,
        results_by_case=results_by_case,
        metric_name="run",
        columns=1,
    )
    render_bar_chart(
        snapshot_dir / "compile-times.svg",
        title="Compile Time Median by Benchmark",
        subtitle="Native languages only. Pluto includes frontend, in-process LLVM O3/object emission, and link.",
        cases=cases,
        results_by_case=results_by_case,
        metric_name="compile",
        columns=2,
    )
    render_bar_chart(
        snapshot_dir / "compile-times-mobile.svg",
        title="Compile Time Median by Benchmark",
        subtitle="Native languages only. Pluto includes frontend, in-process LLVM O3/object emission, and link.",
        cases=cases,
        results_by_case=results_by_case,
        metric_name="compile",
        columns=1,
    )
    if any(
        result.peak_memory_kb is not None
        for case_results in results_by_case.values()
        for result in case_results
    ):
        render_bar_chart(
            snapshot_dir / "peak-memory.svg",
            title="Peak Memory Use by Benchmark",
            subtitle="Approximate peak RAM used by each process, measured from the untimed warm-up run. Lower is better.",
            cases=cases,
            results_by_case=results_by_case,
            metric_name="memory",
            columns=2,
        )
        render_bar_chart(
            snapshot_dir / "peak-memory-mobile.svg",
            title="Peak Memory Use by Benchmark",
            subtitle="Approximate peak RAM used by each process, measured from the untimed warm-up run. Lower is better.",
            cases=cases,
            results_by_case=results_by_case,
            metric_name="memory",
            columns=1,
        )


def benchmark_source(
    source: CaseSource,
    repeat: int,
    toolchain: Toolchain,
    measure_memory: bool,
) -> Result:
    compile_samples = []
    run_samples = []
    memory_samples = []
    last_output = ""
    memory_enabled = measure_memory

    for idx in range(repeat):
        workdir = prepare_workdir(source.case, source.language, idx)
        try:
            copy_case_files(source.source_dir, workdir)
            compile_spec, run_spec = commands_for(source, workdir, toolchain)
            if compile_spec is not None:
                compile_ms, _ = timed_run(compile_spec, workdir)
                compile_samples.append(compile_ms)

            # Warm up one execution before timing to reduce one-off startup noise.
            if memory_enabled:
                try:
                    peak_memory_kb = probe_peak_memory_kb(run_spec, workdir)
                except RuntimeError as err:
                    # If the target command itself is healthy, keep the benchmark
                    # running and simply drop peak-memory sampling for this source. This avoids a
                    # flaky /usr/bin/time probe killing the whole suite.
                    timed_run(run_spec, workdir)
                    print(
                        f"warning: peak memory probe disabled for {source.case}/{source.language}: {err}",
                        file=sys.stderr,
                    )
                    memory_enabled = False
                else:
                    if peak_memory_kb is not None:
                        memory_samples.append(peak_memory_kb)
            else:
                timed_run(run_spec, workdir)
            run_ms, run_proc = timed_run(run_spec, workdir)
            run_samples.append(run_ms)
            last_output = run_proc.stdout.strip()
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    return Result(
        case=source.case,
        language=source.language,
        version=source_version(source, toolchain),
        compile_ms=statistics.median(compile_samples) if compile_samples else None,
        run_ms=statistics.median(run_samples),
        peak_memory_kb=int(statistics.median(memory_samples)) if memory_samples else None,
        output=last_output,
    )


def discover_cases(selected: list[str] | None) -> list[str]:
    if selected:
        return selected

    cases = {
        path.name
        for path in BENCHMARKS_DIR.iterdir()
        if path.is_dir()
    }
    return ordered_cases(cases)


def pluto_source_name(case: str, case_dir: Path) -> str | None:
    pluto_dir = case_dir / "pluto"
    candidates = [f"{case}.spt", "main.spt"]
    for candidate in candidates:
        if (pluto_dir / candidate).exists():
            return candidate
    return None


def sources_for_case(case: str) -> list[CaseSource]:
    case_dir = BENCHMARKS_DIR / case
    sources = []
    for language in LANGUAGE_ORDER:
        if language == "pluto":
            source_name = pluto_source_name(case, case_dir)
            if source_name is None:
                continue
        else:
            source_name = LANGUAGE_TO_SOURCE[language]
        source_dir = case_dir / language
        source_path = source_dir / source_name
        if source_path.exists():
            sources.append(
                CaseSource(
                    case=case,
                    case_dir=case_dir,
                    source_dir=source_dir,
                    language=language,
                    source_name=source_name,
                )
            )
    return sources


def benchmark_case(
    case: str,
    repeat: int,
    toolchain: Toolchain,
    measure_memory: bool,
) -> list[Result]:
    results = []
    for source in sources_for_case(case):
        if not source_available(source, toolchain):
            continue
        results.append(
            benchmark_source(
                source,
                repeat,
                toolchain,
                measure_memory,
            )
        )
    return sorted(results, key=lambda result: LANGUAGE_ORDER.index(result.language))


def print_case(results: list[Result]) -> None:
    if not results:
        return

    case = results[0].case
    show_peak_memory = any(result.peak_memory_kb is not None for result in results)
    language_width = max(len("Language"), *(len(display_label(result)) for result in results))
    version_width = max(len("Version"), *(len(result.version) for result in results))
    print(f"Case: {case}")
    header = (
        f"{'Language':<{language_width}} "
        f"{'Version':<{version_width}} "
        f"{'Compile ms':>12} {'Run ms':>12}"
    )
    if show_peak_memory:
        header += f" {'Peak Memory':>12}"
    print(header)
    for result in results:
        compile_text = "-" if result.compile_ms is None else f"{result.compile_ms:>.3f}"
        row = (
            f"{display_label(result):<{language_width}} "
            f"{result.version:<{version_width}} "
            f"{compile_text:>12} "
            f"{result.run_ms:>12.3f}"
        )
        if show_peak_memory:
            peak_text = "-" if result.peak_memory_kb is None else format_memory_kb(result.peak_memory_kb)
            row += f" {peak_text:>12}"
        print(row)

    outputs = {result.output for result in results}
    expected = load_expected(BENCHMARKS_DIR / case)
    if expected is not None and outputs != {expected}:
        print(f"Expected: {expected}")
        print("Output mismatch:")
        for result in results:
            print(f"  {LANGUAGE_LABELS[result.language]}: {result.output}")
    elif len(outputs) == 1:
        print(f"Output: {results[0].output}")
    else:
        print("Output mismatch:")
        for result in results:
            print(f"  {LANGUAGE_LABELS[result.language]}: {result.output}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Time compile and execution for Pluto, C, C++, Swift, Go, Rust, "
            "Zig, Julia, LuaJIT, Node, Bun, and Python sources."
        )
    )
    parser.add_argument(
        "cases",
        nargs="*",
        help="Case names to benchmark, for example: sum fib harmonic",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=10,
        help="Number of times to compile and run each source; results use the median.",
    )
    parser.add_argument(
        "--pluto",
        help="Path to the Pluto compiler binary. Defaults to ../pluto/pluto or $PLUTO_BIN.",
    )
    parser.add_argument(
        "--zig",
        help="Path to the Zig compiler binary. Defaults to .toolchains/zig-aarch64-macos-0.15.2/zig, `zig` on PATH, or $ZIG_BIN.",
    )
    parser.add_argument(
        "--cc",
        help="Path to the C compiler binary. Defaults to Homebrew LLVM clang, `cc` on PATH, or $CC_BIN. Use CC_BIN=/usr/bin/clang for the macOS platform toolchain.",
    )
    parser.add_argument(
        "--cxx",
        help="Path to the C++ compiler binary. Defaults to Homebrew LLVM clang++, `c++` on PATH, or $CXX_BIN. Use CXX_BIN=/usr/bin/clang++ for the macOS platform toolchain.",
    )
    parser.add_argument(
        "--luajit",
        help="Path to the LuaJIT binary. Defaults to `luajit` on PATH or $LUAJIT_BIN.",
    )
    parser.add_argument(
        "--snapshot-dir",
        help=(
            "Optional directory for writing a machine-readable results snapshot plus "
            "SVG charts."
        ),
    )
    args = parser.parse_args()

    if args.repeat < 1:
        raise SystemExit("--repeat must be at least 1")

    toolchain = Toolchain(
        pluto=resolve_pluto(args.pluto),
        zig=resolve_zig(args.zig),
        cc=resolve_cc(args.cc),
        cxx=resolve_cxx(args.cxx),
        luajit=resolve_luajit(args.luajit),
    )
    if not toolchain.pluto.exists():
        print(f"warning: Pluto compiler not found at {toolchain.pluto}", file=sys.stderr)
    if not toolchain.zig.exists():
        print(f"warning: Zig compiler not found at {toolchain.zig}", file=sys.stderr)
    if not toolchain.cc.exists():
        print(f"warning: C compiler not found at {toolchain.cc}", file=sys.stderr)
    if not toolchain.cxx.exists():
        print(f"warning: C++ compiler not found at {toolchain.cxx}", file=sys.stderr)
    if not toolchain.luajit.exists():
        print(f"warning: LuaJIT binary not found at {toolchain.luajit}", file=sys.stderr)

    cases = discover_cases(args.cases)
    if not cases:
        print("No benchmark sources found.", file=sys.stderr)
        return 1

    measure_memory = peak_memory_command_prefix() is not None
    metadata = snapshot_metadata(toolchain)
    print_metadata_summary(metadata)
    shutil.rmtree(WORK_ROOT, ignore_errors=True)
    try:
        results_by_case: dict[str, list[Result]] = {}
        for case in cases:
            results = benchmark_case(
                case,
                args.repeat,
                toolchain,
                measure_memory,
            )
            results_by_case[case] = results
            if not results:
                print(f"Case: {case}")
                print("No runnable sources found.\n")
                continue
            print_case(results)
        if args.snapshot_dir:
            snapshot_dir = Path(args.snapshot_dir).resolve()
            write_snapshot(
                snapshot_dir,
                cases=cases,
                results_by_case=results_by_case,
                repeat=args.repeat,
                toolchain=toolchain,
            )
            print(f"Snapshot written: {snapshot_dir / 'results.json'}")
    finally:
        shutil.rmtree(WORK_ROOT, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
