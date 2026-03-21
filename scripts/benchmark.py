#!/usr/bin/env python3

import argparse
import datetime as dt
import json
import math
import os
import platform
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
CASE_ORDER = ("sum", "fib", "fib_tail", "harmonic")
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
LANGUAGE_COLORS = {
    "pluto": "#c2410c",
    "c": "#2563eb",
    "cpp": "#16a34a",
    "swift": "#dc2626",
    "go": "#0891b2",
    "rust": "#6d28d9",
    "zig": "#ca8a04",
    "julia": "#7c3aed",
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
    output: str


@dataclass(frozen=True)
class CaseSource:
    case: str
    case_dir: Path
    language: str
    source_name: str


def ordered_cases(cases: list[str] | set[str]) -> list[str]:
    seen = set(cases)
    ordered = [case for case in CASE_ORDER if case in seen]
    ordered.extend(sorted(case for case in seen if case not in set(CASE_ORDER)))
    return ordered


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


def runtime_tick_values(min_val: float, max_val: float) -> list[float]:
    ticks = []
    start = max(0, int(math.floor(math.log10(min_val))))
    end = int(math.ceil(math.log10(max_val)))
    for exponent in range(start, end + 1):
        for base in (1, 2, 5):
            tick = base * (10 ** exponent)
            if min_val <= tick <= max_val:
                ticks.append(float(tick))
    if not ticks:
        ticks = [min_val, max_val]
    return ticks


def compile_tick_values(max_val: float) -> list[float]:
    if max_val <= 100:
        step = 20
    elif max_val <= 250:
        step = 50
    else:
        step = 100
    limit = int(math.ceil(max_val / step) * step)
    return [float(tick) for tick in range(0, limit + step, step)]


def plot_y(value: float, min_val: float, max_val: float, top: float, height: float, log_scale: bool) -> float:
    if log_scale:
        min_log = math.log10(min_val)
        max_log = math.log10(max_val)
        ratio = (math.log10(value) - min_log) / (max_log - min_log)
    else:
        ratio = (value - min_val) / (max_val - min_val)
    return top + height - (ratio * height)


def render_metric_chart(
    path: Path,
    *,
    title: str,
    subtitle: str,
    cases: list[str],
    results_by_case: dict[str, list[Result]],
    metric_name: str,
    log_scale: bool,
) -> None:
    languages = []
    for language in LANGUAGE_ORDER:
        points = []
        for case in cases:
            for result in results_by_case.get(case, []):
                if result.language != language:
                    continue
                value = result.run_ms if metric_name == "run" else result.compile_ms
                if value is not None:
                    points.append((case, value))
                break
        if points:
            languages.append((language, points))

    if not languages:
        return

    all_values = [value for _, points in languages for _, value in points]
    min_val = min(all_values)
    max_val = max(all_values)

    if log_scale:
        min_val = 10 ** math.floor(math.log10(min_val))
        max_val = 10 ** math.ceil(math.log10(max_val))
        ticks = runtime_tick_values(min_val, max_val)
    else:
        min_val = 0.0
        max_val = max_val * 1.08 if max_val else 1.0
        ticks = compile_tick_values(max_val)
        max_val = max(ticks)

    width = 1280
    height = 760
    left = 110
    top = 110
    right = 260
    bottom = 95
    plot_width = width - left - right
    plot_height = height - top - bottom

    x_positions = {}
    if len(cases) == 1:
        x_positions[cases[0]] = left + (plot_width / 2)
    else:
        step = plot_width / (len(cases) - 1)
        for index, case in enumerate(cases):
            x_positions[case] = left + (index * step)

    lines: list[str] = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">'
    )
    lines.append("<defs>")
    lines.append('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">')
    lines.append('<stop offset="0%" stop-color="#f8fafc" />')
    lines.append('<stop offset="100%" stop-color="#eef2ff" />')
    lines.append("</linearGradient>")
    lines.append("</defs>")
    lines.append(f"<title>{svg_escape(title)}</title>")
    lines.append(f"<desc>{svg_escape(subtitle)}</desc>")
    lines.append(f'<rect width="{width}" height="{height}" fill="url(#bg)" />')
    lines.append(
        f'<text x="{left}" y="52" fill="#0f172a" font-size="28" font-weight="700" '
        'font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif">'
        f"{svg_escape(title)}</text>"
    )
    lines.append(
        f'<text x="{left}" y="80" fill="#475569" font-size="15" '
        'font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif">'
        f"{svg_escape(subtitle)}</text>"
    )
    lines.append(
        f'<rect x="{left}" y="{top}" width="{plot_width}" height="{plot_height}" '
        'rx="18" fill="#ffffff" fill-opacity="0.82" stroke="#cbd5e1" />'
    )

    for tick in ticks:
        y = plot_y(tick, min_val, max_val, top, plot_height, log_scale)
        lines.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{left + plot_width}" y2="{y:.2f}" '
            'stroke="#e2e8f0" stroke-width="1" />'
        )
        lines.append(
            f'<text x="{left - 16}" y="{y + 5:.2f}" text-anchor="end" fill="#475569" font-size="13" '
            'font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif">'
            f"{svg_escape(format_ms(tick))}</text>"
        )

    for case, x in x_positions.items():
        label = CASE_LABELS.get(case, case.replace("_", " ").title())
        lines.append(
            f'<line x1="{x:.2f}" y1="{top}" x2="{x:.2f}" y2="{top + plot_height}" '
            'stroke="#f1f5f9" stroke-width="1" />'
        )
        lines.append(
            f'<text x="{x:.2f}" y="{top + plot_height + 34}" text-anchor="middle" fill="#0f172a" font-size="14" '
            'font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif">'
            f"{svg_escape(label)}</text>"
        )
    lines.append(
        f'<text x="{left + plot_width / 2:.2f}" y="{height - 28}" text-anchor="middle" fill="#64748b" font-size="13" '
        'font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif">'
        'Lower is better</text>'
    )

    for language, points in languages:
        color = LANGUAGE_COLORS[language]
        stroke_width = 4.0 if language == "pluto" else 2.2
        opacity = 1.0 if language == "pluto" else 0.88
        commands = []
        for idx, (case, value) in enumerate(points):
            x = x_positions[case]
            y = plot_y(value, min_val, max_val, top, plot_height, log_scale)
            commands.append(f'{"M" if idx == 0 else "L"} {x:.2f} {y:.2f}')
        lines.append(
            f'<path d="{" ".join(commands)}" fill="none" stroke="{color}" '
            f'stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" '
            f'opacity="{opacity}" />'
        )
        for case, value in points:
            x = x_positions[case]
            y = plot_y(value, min_val, max_val, top, plot_height, log_scale)
            radius = 5 if language == "pluto" else 3.5
            lines.append(
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{radius}" fill="{color}" '
                'stroke="#ffffff" stroke-width="1.5" />'
            )

    legend_x = left + plot_width + 26
    legend_y = top + 18
    lines.append(
        f'<text x="{legend_x}" y="{legend_y}" fill="#0f172a" font-size="16" font-weight="700" '
        'font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif">'
        'Languages</text>'
    )
    for index, (language, _) in enumerate(languages):
        y = legend_y + 30 + (index * 28)
        color = LANGUAGE_COLORS[language]
        label = LANGUAGE_LABELS[language] + (" (baseline)" if language == "pluto" else "")
        weight = "700" if language == "pluto" else "500"
        lines.append(
            f'<line x1="{legend_x}" y1="{y}" x2="{legend_x + 26}" y2="{y}" '
            f'stroke="{color}" stroke-width="4" stroke-linecap="round" />'
        )
        lines.append(
            f'<text x="{legend_x + 36}" y="{y + 4}" fill="#0f172a" font-size="14" font-weight="{weight}" '
            'font-family="ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, sans-serif">'
            f"{svg_escape(label)}</text>"
        )

    lines.append("</svg>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_snapshot(
    snapshot_dir: Path,
    *,
    cases: list[str],
    results_by_case: dict[str, list[Result]],
    repeat: int,
    pluto_bin: Path,
) -> None:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    generated_at = dt.datetime.now().astimezone().isoformat()
    snapshot = {
        "generated_at": generated_at,
        "repeat": repeat,
        "pluto_bin": str(pluto_bin),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "cases": [
            {
                "name": case,
                "results": [
                    {
                        "language": result.language,
                        "version": result.version,
                        "compile_ms": result.compile_ms,
                        "run_ms": result.run_ms,
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

    render_metric_chart(
        snapshot_dir / "run-times.svg",
        title="Run Time Median by Benchmark",
        subtitle="Log scale. All languages are timed as fresh processes. Lower is better.",
        cases=cases,
        results_by_case=results_by_case,
        metric_name="run",
        log_scale=True,
    )
    render_metric_chart(
        snapshot_dir / "compile-times.svg",
        title="Compile Time Median by Benchmark",
        subtitle="Native languages only. Pluto includes frontend plus LLVM opt, llc, and link.",
        cases=cases,
        results_by_case=results_by_case,
        metric_name="compile",
        log_scale=False,
    )


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
    return ordered_cases(cases)


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

    pluto_bin = resolve_pluto(args.pluto)
    if not pluto_bin.exists():
        print(f"warning: Pluto compiler not found at {pluto_bin}", file=sys.stderr)

    cases = discover_cases(args.cases)
    if not cases:
        print("No benchmark sources found.", file=sys.stderr)
        return 1

    shutil.rmtree(WORK_ROOT, ignore_errors=True)
    try:
        results_by_case: dict[str, list[Result]] = {}
        for case in cases:
            results = benchmark_case(case, args.repeat, pluto_bin)
            results_by_case[case] = results
            if not results:
                print(f"Case: {case}")
                print("No runnable sources found.\n")
                continue
            print_case(results)
        if args.snapshot_dir:
            write_snapshot(
                Path(args.snapshot_dir).resolve(),
                cases=cases,
                results_by_case=results_by_case,
                repeat=args.repeat,
                pluto_bin=pluto_bin,
            )
    finally:
        shutil.rmtree(WORK_ROOT, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
