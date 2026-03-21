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


ROOT = Path(__file__).resolve().parent
DEFAULT_PLUTO = (ROOT / "../pluto/pluto").resolve()
PT_MOD = ROOT / "pt.mod"
WORK_ROOT = Path(tempfile.gettempdir()) / "pluto-bench"

LANGUAGE_ORDER = ("pluto", "c", "cpp", "python")
LANGUAGE_LABELS = {
    "pluto": "Pluto",
    "c": "C",
    "cpp": "C++",
    "python": "Python",
}
SUFFIX_TO_LANGUAGE = {
    ".spt": "pluto",
    ".c": "c",
    ".cpp": "cpp",
    ".py": "python",
}


@dataclass
class Result:
    case: str
    language: str
    compile_ms: float | None
    run_ms: float
    output: str


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


def copy_source(src: Path, workdir: Path) -> Path:
    dst = workdir / src.name
    shutil.copy2(src, dst)
    return dst


def copy_support_files(src: Path, workdir: Path) -> None:
    # Pluto code templates live in companion .pt files. Copy the case-specific
    # one when present so each benchmark stays isolated.
    companion_pt = ROOT / f"{src.stem}.pt"
    if src.suffix == ".spt" and companion_pt.exists():
        shutil.copy2(companion_pt, workdir / companion_pt.name)


def commands_for(
    src: Path, copied_src: Path, pluto_bin: Path
) -> tuple[list[str] | None, list[str]]:
    stem = copied_src.stem
    if src.suffix == ".spt":
        compile_cmd = [str(pluto_bin), copied_src.name]
        run_cmd = [str(copied_src.parent / stem)]
    elif src.suffix == ".c":
        compile_cmd = ["cc", "-O2", copied_src.name, "-o", stem]
        run_cmd = [str(copied_src.parent / stem)]
    elif src.suffix == ".cpp":
        compile_cmd = ["c++", "-O2", copied_src.name, "-o", stem]
        run_cmd = [str(copied_src.parent / stem)]
    elif src.suffix == ".py":
        compile_cmd = None
        run_cmd = [sys.executable, copied_src.name]
    else:
        raise ValueError(f"unsupported file type: {src}")
    return compile_cmd, run_cmd


def resolve_pluto(path_arg: str | None) -> Path:
    raw_path = path_arg or os.environ.get("PLUTO_BIN")
    if raw_path:
        return Path(raw_path).expanduser().resolve()
    return DEFAULT_PLUTO


def benchmark_source(src: Path, repeat: int, pluto_bin: Path) -> Result:
    language = SUFFIX_TO_LANGUAGE[src.suffix]
    compile_samples = []
    run_samples = []
    last_output = ""

    for idx in range(repeat):
        workdir = prepare_workdir(src.stem, language, idx)
        copied_src = copy_source(src, workdir)
        copy_support_files(src, workdir)
        compile_cmd, run_cmd = commands_for(src, copied_src, pluto_bin)
        if compile_cmd is not None:
            compile_ms, _ = timed_run(compile_cmd, workdir)
            compile_samples.append(compile_ms)

        # Warm up one execution before timing to reduce one-off startup noise.
        timed_run(run_cmd, workdir)
        run_ms, run_proc = timed_run(run_cmd, workdir)
        run_samples.append(run_ms)
        last_output = run_proc.stdout.strip()

    return Result(
        case=src.stem,
        language=language,
        compile_ms=statistics.median(compile_samples) if compile_samples else None,
        run_ms=statistics.median(run_samples),
        output=last_output,
    )


def discover_cases(selected: list[str] | None) -> list[str]:
    if selected:
        return selected

    cases = {
        path.stem
        for path in ROOT.iterdir()
        if path.is_file() and path.suffix in SUFFIX_TO_LANGUAGE
    }
    return sorted(cases)


def benchmark_case(case: str, repeat: int, pluto_bin: Path) -> list[Result]:
    results = []
    for suffix, language in SUFFIX_TO_LANGUAGE.items():
        src = ROOT / f"{case}{suffix}"
        if not src.exists():
            continue
        if language == "pluto" and not pluto_bin.exists():
            continue
        results.append(benchmark_source(src, repeat, pluto_bin))
    return sorted(results, key=lambda result: LANGUAGE_ORDER.index(result.language))


def print_case(results: list[Result]) -> None:
    if not results:
        return

    case = results[0].case
    print(f"Case: {case}")
    print(f"{'Language':<8} {'Compile ms':>12} {'Run ms':>12}")
    for result in results:
        compile_text = "-" if result.compile_ms is None else f"{result.compile_ms:>.3f}"
        print(
            f"{LANGUAGE_LABELS[result.language]:<8} "
            f"{compile_text:>12} "
            f"{result.run_ms:>12.3f}"
        )

    outputs = {result.output for result in results}
    if len(outputs) == 1:
        print(f"Output: {results[0].output}")
    else:
        print("Output mismatch:")
        for result in results:
            print(f"  {LANGUAGE_LABELS[result.language]}: {result.output}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Time compile and execution for Pluto, C, C++, and Python sources."
    )
    parser.add_argument(
        "cases",
        nargs="*",
        help="Case basenames to benchmark, for example: sum fib t",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=5,
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

    for case in cases:
        results = benchmark_case(case, args.repeat, pluto_bin)
        if not results:
            print(f"Case: {case}")
            print("No runnable sources found.\n")
            continue
        print_case(results)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
