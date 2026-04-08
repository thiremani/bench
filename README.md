# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-04-08 22:15:03 UTC+05:30` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.4 (25E246)
- Command: `python3 scripts/benchmark.py --repeat 10 --snapshot-dir results/latest`
- Benchmark mode: median of 10 samples
- All languages are timed as fresh processes
- Pluto rows are marked as `Pluto (baseline)` for quick comparison

## Visual Summary

Run time overview:

<picture>
  <source media="(max-width: 800px)" srcset="results/latest/run-times-mobile.svg" />
  <img src="results/latest/run-times.svg" alt="Run time chart" />
</picture>

Peak memory overview:

<picture>
  <source media="(max-width: 800px)" srcset="results/latest/peak-rss-mobile.svg" />
  <img src="results/latest/peak-rss.svg" alt="Peak memory chart" />
</picture>

Compile time overview:

<picture>
  <source media="(max-width: 800px)" srcset="results/latest/compile-times-mobile.svg" />
  <img src="results/latest/compile-times.svg" alt="Compile time chart" />
</picture>

The charts are the quick view. Each benchmark uses its own linear scale, so bar lengths are comparable within a benchmark but not across benchmarks. The tables below are the exact reference.

## Pluto vs Python at a Glance

<picture>
  <source media="(max-width: 800px)" srcset="assets/pluto-vs-python-mobile.svg" />
  <img src="assets/pluto-vs-python.svg" alt="Pluto vs Python code comparison" />
</picture>

- `sum`: Pluto source is `benchmarks/sum/pluto/main.spt`; Python source is `benchmarks/sum/python/main.py`.
- `fib`: Pluto uses `benchmarks/fib/pluto/fib.pt` plus `benchmarks/fib/pluto/fib.spt`; Python uses `benchmarks/fib/python/main.py`.

## Result Tables

### Sum

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **145.278** | **9.127** | **1.31 MiB** | `160000000` |
| C | `Apple clang 21.0.0` | 66.825 | 8.778 | 1.30 MiB | `160000000` |
| C++ | `Apple clang 21.0.0` | 392.645 | 9.226 | 1.32 MiB | `160000000` |
| Swift | `Swift 6.3` | 267.067 | 21.587 | 1.80 MiB | `160000000` |
| Go | `go1.26.2` | 150.710 | 23.138 | 3.88 MiB | `160000000` |
| Rust | `rustc 1.94.1` | 103.331 | 24.883 | 1.48 MiB | `160000000` |
| Zig | `zig 0.15.2` | 211.719 | 14.769 | 1.35 MiB | `160000000` |
| Node | `Node v25.9.0` | - | 84.313 | 48.50 MiB | `160000000` |
| Python | `Python 3.14.3` | - | 1517.709 | 14.50 MiB | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **128.347** | **8.828** | **1.31 MiB** | `2178309` |
| C | `Apple clang 21.0.0` | 60.828 | 9.954 | 1.30 MiB | `2178309` |
| C++ | `Apple clang 21.0.0` | 377.569 | 10.084 | 1.33 MiB | `2178309` |
| Swift | `Swift 6.3` | 218.304 | 13.692 | 1.81 MiB | `2178309` |
| Go | `go1.26.2` | 120.962 | 11.537 | 3.86 MiB | `2178309` |
| Rust | `rustc 1.94.1` | 103.958 | 10.705 | 1.48 MiB | `2178309` |
| Zig | `zig 0.15.2` | 204.244 | 10.062 | 1.36 MiB | `2178309` |
| Node | `Node v25.9.0` | - | 98.578 | 48.46 MiB | `2178309` |
| Python | `Python 3.14.3` | - | 320.027 | 14.57 MiB | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **140.822** | **14.638** | **1.32 MiB** | `2851443500000` |
| C | `Apple clang 21.0.0` | 62.030 | 14.727 | 1.31 MiB | `2851443500000` |
| C++ | `Apple clang 21.0.0` | 386.897 | 14.804 | 1.33 MiB | `2851443500000` |
| Swift | `Swift 6.3` | 239.314 | 13.054 | 1.80 MiB | `2851443500000` |
| Go | `go1.26.2` | 142.322 | 20.932 | 3.88 MiB | `2851443500000` |
| Rust | `rustc 1.94.1` | 113.780 | 15.426 | 1.50 MiB | `2851443500000` |
| Zig | `zig 0.15.2` | 224.125 | 15.278 | 1.35 MiB | `2851443500000` |
| Node | `Node v25.9.0` | - | 222.548 | 48.97 MiB | `2851443500000` |
| Python | `Python 3.14.3` | - | 1672.322 | 14.57 MiB | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **166.582** | **13.995** | **1.32 MiB** | `16.695311` |
| C | `Apple clang 21.0.0` | 66.759 | 13.568 | 1.31 MiB | `16.695311` |
| C++ | `Apple clang 21.0.0` | 435.809 | 13.485 | 1.33 MiB | `16.695311` |
| Swift | `Swift 6.3` | 434.773 | 16.097 | 5.53 MiB | `16.695311` |
| Go | `go1.26.2` | 132.793 | 14.682 | 3.95 MiB | `16.695311` |
| Rust | `rustc 1.94.1` | 107.887 | 13.418 | 1.50 MiB | `16.695311` |
| Zig | `zig 0.15.2` | 379.322 | 13.360 | 1.36 MiB | `16.695311` |
| Node | `Node v25.9.0` | - | 75.509 | 49.04 MiB | `16.695311` |
| Python | `Python 3.14.3` | - | 783.068 | 14.55 MiB | `16.695311` |

## Benchmarks

- `sum`
  Integer reduction benchmark.
  Sums `(i * 3) % 17` for `i` from `1` to `20,000,000`.
  This avoids closed-form constant folding in native compilers while staying within JavaScript's exact integer range.
  Expected output: `160000000`

- `fib`
  Naive recursive Fibonacci benchmark.
  Computes `fib(32)` with tree recursion to expose recursion, branching, and function-call cost.
  Expected output: `2178309`

- `fib_tail`
  Tail-recursive Fibonacci benchmark.
  Accumulates `1,000,000` tail-recursive Fibonacci calls, alternating between `fib(32)` and `fib(33)`.
  This makes the runtime less sensitive to process-startup noise than a single `fib(32)` call.
  Expected output: `2851443500000`

- `harmonic`
  Floating-point throughput benchmark.
  Computes the harmonic sum from `1` to `10,000,000`.
  Expected output: `16.695311`

Each benchmark directory keeps `expected.txt` at the case root and places each
language implementation under its own subdirectory, for example
`benchmarks/sum/go/main.go` or `benchmarks/fib/pluto/fib.spt`. Pluto-specific
template files such as `fib.pt` live alongside the Pluto script in that
benchmark's `pluto/` subdirectory.

## Running

Run the full suite:

```sh
python3 scripts/benchmark.py
```

The harness is compatible with Python 3.9+.

GitHub Actions also runs the suite on `ubuntu-24.04`. That workflow checks out
`pluto`, builds it with LLVM 21, runs the same harness, and uploads a separate
snapshot artifact under `results/linux-gha` semantics. It does not overwrite the
checked-in `results/latest` macOS snapshot.

Regenerate the checked-in charts and snapshot:

```sh
python3 scripts/benchmark.py --repeat 10 --snapshot-dir results/latest
```

Run a single benchmark:

```sh
python3 scripts/benchmark.py sum
python3 scripts/benchmark.py fib
python3 scripts/benchmark.py fib_tail
python3 scripts/benchmark.py harmonic
```

By default the harness looks for Pluto at `../pluto/pluto`, which matches:

```text
/Users/tejas/Downloads/bench
/Users/tejas/Downloads/pluto/pluto
```

If your Pluto binary is elsewhere, override it with:

```sh
python3 scripts/benchmark.py --pluto /path/to/pluto
```

or:

```sh
PLUTO_BIN=/path/to/pluto python3 scripts/benchmark.py
```

## Measurement Notes

- Pluto, C, C++, Swift, Go, Rust, and Zig report native compile time and execution time separately.
- Julia, Node, Bun, and Python are reported as runtime or JIT execution only, so their compile column is `-`.
- Snapshot tables only include languages whose toolchains were available on the host where the snapshot was generated.
- Peak Memory is collected automatically when the host supports `/usr/bin/time`.
- Peak Memory is the median peak resident set size (RSS) across the untimed warm-up runs.
- In plain terms, think of Peak Memory as the approximate RAM used by the benchmark process at its peak.
- Pluto currently uses its own LLVM pipeline with `opt -O3`.
- C and C++ are built with `-O3` for consistency with the native comparison.
- Swift is built with `swiftc -O`.
- Rust is built with `rustc -C opt-level=3`.
- Zig is built with `zig build-exe -O ReleaseFast` and a baseline CPU target
  for fairer comparison with the other native compilers.
- Go uses the default optimized `go build` pipeline.
- Julia runs with `julia --startup-file=no`.
- The harness creates isolated temp work directories and copies each benchmark into them before running.
- It copies the benchmark files into that directory, including Pluto support `.pt` files when present.
- Every timed sample launches a fresh process, so the published `run_ms` numbers are end-to-end wall-clock timings.
- One warm-up execution runs before each timed sample.
- Short runtime cases such as `sum` and `harmonic` still include non-trivial process-startup noise, so treat small differences there with caution.
- Output is checked against `expected.txt` for the benchmark.
