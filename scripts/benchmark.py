#!/usr/bin/env python3

import argparse
import os
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
PT_MOD = REPO_ROOT / "pt.mod"
WORK_ROOT = Path(tempfile.gettempdir()) / "pluto-bench"

LANGUAGE_ORDER = (
    "pluto",
    "c",
    "cpp",
    "swift",
    "go",
    "rust",
    "zig",
    "julia",
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
    "node": "Node",
    "bun": "Bun",
    "python": "Python",
}
LANGUAGE_TO_SOURCE = {
    "pluto": "main.spt",
    "c": "main.c",
    "cpp": "main.cpp",
    "swift": "main.swift",
    "go": "main.go",
    "rust": "main.rs",
    "zig": "main.zig",
    "julia": "main.jl",
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
    "node": ["node", "--version"],
    "bun": ["bun", "--version"],
    "python": [sys.executable, "--version"],
}


@dataclass
class Result:
    case: str
    language: str
    version: str
    compile_ms: float | None
    run_ms: float
    output: str


@dataclass(frozen=True)
class CaseSource:
    case: str
    case_dir: Path
    language: str
    source_name: str


def first_line(text: str) -> str:
    return text.strip().splitlines()[0] if text.strip() else ""


def normalize_version(language: str, raw: str) -> str:
    if not raw:
        return "unknown"
    if language == "pluto":
        return raw.split(" (", 1)[0]
    if language in {"c", "cpp"} and raw.startswith("Apple clang version "):
        parts = raw.split()
        if len(parts) >= 4:
            return f"Apple clang {parts[3]}"
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
    if language == "node" and raw.startswith("v"):
        return f"Node {raw}"
    if language == "bun":
        return f"Bun {raw}"
    return raw


def timed_run(cmd: list[str], cwd: Path) -> tuple[float, subprocess.CompletedProcess[str]]:
    start = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=cwd,
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
            f"command failed: {' '.join(cmd)}"
            + (f"\n{detail_text}" if detail_text else "")
        )
    return elapsed_ms, proc


def prepare_workdir(base: str, language: str, repeat: int) -> Path:
    WORK_ROOT.mkdir(parents=True, exist_ok=True)
    workdir = WORK_ROOT / f"{base}_{language}_{repeat}"
    if workdir.exists():
        shutil.rmtree(workdir)
    workdir.mkdir(parents=True)
    if PT_MOD.exists():
        shutil.copy2(PT_MOD, workdir / PT_MOD.name)
    return workdir


def copy_case_files(case_dir: Path, workdir: Path) -> None:
    for path in case_dir.iterdir():
        if not path.is_file():
            continue
        if path.name == "expected.txt":
            continue
        shutil.copy2(path, workdir / path.name)


def commands_for(
    source: CaseSource, workdir: Path, pluto_bin: Path
) -> tuple[list[str] | None, list[str]]:
    stem = "main"
    if source.language == "pluto":
        compile_cmd = [str(pluto_bin), source.source_name]
        run_cmd = [str(workdir / stem)]
    elif source.language == "c":
        compile_cmd = ["cc", "-O3", source.source_name, "-o", stem]
        run_cmd = [str(workdir / stem)]
    elif source.language == "cpp":
        compile_cmd = ["c++", "-O3", source.source_name, "-o", stem]
        run_cmd = [str(workdir / stem)]
    elif source.language == "swift":
        compile_cmd = ["swiftc", "-O", source.source_name, "-o", stem]
        run_cmd = [str(workdir / stem)]
    elif source.language == "go":
        compile_cmd = ["go", "build", "-trimpath", "-o", stem, source.source_name]
        run_cmd = [str(workdir / stem)]
    elif source.language == "rust":
        compile_cmd = ["rustc", "-C", "opt-level=3", source.source_name, "-o", stem]
        run_cmd = [str(workdir / stem)]
    elif source.language == "zig":
        compile_cmd = [
            "zig",
            "build-exe",
            "-O",
            "ReleaseFast",
            f"-femit-bin={workdir / stem}",
            source.source_name,
        ]
        run_cmd = [str(workdir / stem)]
    elif source.language == "julia":
        compile_cmd = None
        run_cmd = ["julia", "--startup-file=no", source.source_name]
    elif source.language == "node":
        compile_cmd = None
        run_cmd = ["node", source.source_name]
    elif source.language == "bun":
        compile_cmd = None
        run_cmd = ["bun", source.source_name]
    elif source.language == "python":
        compile_cmd = None
        run_cmd = [sys.executable, source.source_name]
    else:
        raise ValueError(f"unsupported language: {source.language}")
    return compile_cmd, run_cmd


def resolve_pluto(path_arg: str | None) -> Path:
    raw_path = path_arg or os.environ.get("PLUTO_BIN")
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    return DEFAULT_PLUTO


def language_available(language: str, pluto_bin: Path) -> bool:
    if language == "pluto":
        return pluto_bin.exists()
    if language == "python":
        return True
    tool = LANGUAGE_TO_TOOL.get(language)
    if tool is None:
        return False
    return shutil.which(tool) is not None


def language_version(language: str, pluto_bin: Path) -> str:
    if language == "pluto":
        if not pluto_bin.exists():
            return "not found"
        proc = subprocess.run(
            [str(pluto_bin), "--version"],
            capture_output=True,
            text=True,
            check=False,
        )
        text = proc.stdout if proc.stdout.strip() else proc.stderr
        return normalize_version(language, first_line(text))

    cmd = LANGUAGE_TO_VERSION_CMD.get(language)
    if cmd is None:
        return "unknown"
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    text = proc.stdout if proc.stdout.strip() else proc.stderr
    return normalize_version(language, first_line(text))


def load_expected(case_dir: Path) -> str | None:
    expected_file = case_dir / "expected.txt"
    if not expected_file.exists():
        return None
    return expected_file.read_text(encoding="utf-8").strip()


def benchmark_source(source: CaseSource, repeat: int, pluto_bin: Path) -> Result:
    compile_samples = []
    run_samples = []
    last_output = ""

    for idx in range(repeat):
        workdir = prepare_workdir(source.case, source.language, idx)
        try:
            copy_case_files(source.case_dir, workdir)
            compile_cmd, run_cmd = commands_for(source, workdir, pluto_bin)
            if compile_cmd is not None:
                compile_ms, _ = timed_run(compile_cmd, workdir)
                compile_samples.append(compile_ms)

            # Warm up one execution before timing to reduce one-off startup noise.
            timed_run(run_cmd, workdir)
            run_ms, run_proc = timed_run(run_cmd, workdir)
            run_samples.append(run_ms)
            last_output = run_proc.stdout.strip()
        finally:
            shutil.rmtree(workdir, ignore_errors=True)

    return Result(
        case=source.case,
        language=source.language,
        version=language_version(source.language, pluto_bin),
        compile_ms=statistics.median(compile_samples) if compile_samples else None,
        run_ms=statistics.median(run_samples),
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
    return sorted(cases)


def sources_for_case(case: str) -> list[CaseSource]:
    case_dir = BENCHMARKS_DIR / case
    sources = []
    for language in LANGUAGE_ORDER:
        source_name = LANGUAGE_TO_SOURCE[language]
        source_path = case_dir / source_name
        if source_path.exists():
            sources.append(
                CaseSource(
                    case=case,
                    case_dir=case_dir,
                    language=language,
                    source_name=source_name,
                )
            )
    return sources


def benchmark_case(case: str, repeat: int, pluto_bin: Path) -> list[Result]:
    results = []
    for source in sources_for_case(case):
        if not language_available(source.language, pluto_bin):
            continue
        results.append(benchmark_source(source, repeat, pluto_bin))
    return sorted(results, key=lambda result: LANGUAGE_ORDER.index(result.language))


def print_case(results: list[Result]) -> None:
    if not results:
        return

    case = results[0].case
    print(f"Case: {case}")
    print(f"{'Language':<8} {'Version':<18} {'Compile ms':>12} {'Run ms':>12}")
    for result in results:
        compile_text = "-" if result.compile_ms is None else f"{result.compile_ms:>.3f}"
        print(
            f"{LANGUAGE_LABELS[result.language]:<8} "
            f"{result.version[:18]:<18} "
            f"{compile_text:>12} "
            f"{result.run_ms:>12.3f}"
        )

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
            "Zig, Julia, Node, Bun, and Python sources."
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
    args = parser.parse_args()

    if args.repeat < 1:
        raise SystemExit("--repeat must be at least 1")

    pluto_bin = resolve_pluto(args.pluto)
    if not pluto_bin.exists():
        print(f"warning: Pluto compiler not found at {pluto_bin}", file=sys.stderr)

    cases = discover_cases(args.cases)
    if not cases:
        print("No benchmark sources found.", file=sys.stderr)
        return 1

    shutil.rmtree(WORK_ROOT, ignore_errors=True)
    try:
        for case in cases:
            results = benchmark_case(case, args.repeat, pluto_bin)
            if not results:
                print(f"Case: {case}")
                print("No runnable sources found.\n")
                continue
            print_case(results)
    finally:
        shutil.rmtree(WORK_ROOT, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
