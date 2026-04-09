# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-04-09 16:51:58 UTC+05:30` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.4 (25E246)
- Command: `python3 scripts/benchmark.py --repeat 10 --snapshot-dir results/latest`
- Benchmark mode: median of 10 samples
- All languages are timed as fresh processes
- Compiled languages use host-native CPU tuning where the toolchain exposes it
- Pluto rows are bolded for quick comparison

## Visual Summary

Run time overview:

<picture>
  <source media="(max-width: 800px)" srcset="results/latest/run-times-mobile.svg" />
  <img src="results/latest/run-times.svg" alt="Run time chart" />
</picture>

Peak memory overview:

<picture>
  <source media="(max-width: 800px)" srcset="results/latest/peak-memory-mobile.svg" />
  <img src="results/latest/peak-memory.svg" alt="Peak memory chart" />
</picture>

Compile time overview:

<picture>
  <source media="(max-width: 800px)" srcset="results/latest/compile-times-mobile.svg" />
  <img src="results/latest/compile-times.svg" alt="Compile time chart" />
</picture>

## Pluto vs Python at a Glance

<picture>
  <source media="(max-width: 800px)" srcset="assets/pluto-vs-python-mobile.svg" />
  <img src="assets/pluto-vs-python.svg" alt="Pluto vs Python code comparison" />
</picture>

- `sum`: Pluto source is `benchmarks/sum/pluto/sum.spt`; Python source is `benchmarks/sum/python/main.py`.
- `fib`: Pluto uses `benchmarks/fib/pluto/fib.pt` plus `benchmarks/fib/pluto/fib.spt`; Python uses `benchmarks/fib/python/main.py`.

## Result Tables

### Sum

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **143.882** | **9.132** | **1.31 MiB** | `160000000` |
| C | `Apple clang 21.0.0` | 66.186 | 9.181 | 1.30 MiB | `160000000` |
| C++ | `Apple clang 21.0.0` | 386.829 | 9.217 | 1.31 MiB | `160000000` |
| Swift | `Swift 6.3` | 239.125 | 21.061 | 1.80 MiB | `160000000` |
| Go | `go1.26.2` | 132.544 | 23.084 | 3.88 MiB | `160000000` |
| Rust | `rustc 1.94.1` | 121.505 | 25.129 | 1.48 MiB | `160000000` |
| Zig | `zig 0.15.2` | 220.082 | 15.256 | 1.36 MiB | `160000000` |
| Julia | `Julia 1.12.5` | - | 151.990 | 226 MiB | `160000000` |
| Node | `Node v25.9.0` | - | 86.290 | 48.6 MiB | `160000000` |
| Bun | `Bun 1.3.9` | - | 35.264 | 27.1 MiB | `160000000` |
| Python | `Python 3.14.3` | - | 1578.405 | 14.6 MiB | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **135.600** | **9.140** | **1.31 MiB** | `2178309` |
| C | `Apple clang 21.0.0` | 58.355 | 9.670 | 1.30 MiB | `2178309` |
| C++ | `Apple clang 21.0.0` | 358.654 | 10.097 | 1.33 MiB | `2178309` |
| Swift | `Swift 6.3` | 223.884 | 13.896 | 1.83 MiB | `2178309` |
| Go | `go1.26.2` | 130.415 | 12.583 | 3.92 MiB | `2178309` |
| Rust | `rustc 1.94.1` | 102.196 | 10.654 | 1.48 MiB | `2178309` |
| Zig | `zig 0.15.2` | 214.475 | 10.273 | 1.34 MiB | `2178309` |
| Julia | `Julia 1.12.5` | - | 154.472 | 226 MiB | `2178309` |
| Node | `Node v25.9.0` | - | 91.286 | 48.5 MiB | `2178309` |
| Bun | `Bun 1.3.9` | - | 25.711 | 26.0 MiB | `2178309` |
| Python | `Python 3.14.3` | - | 314.329 | 14.6 MiB | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **145.592** | **14.826** | **1.33 MiB** | `2851443500000` |
| C | `Apple clang 21.0.0` | 59.907 | 14.456 | 1.31 MiB | `2851443500000` |
| C++ | `Apple clang 21.0.0` | 376.769 | 14.516 | 1.33 MiB | `2851443500000` |
| Swift | `Swift 6.3` | 235.531 | 12.072 | 1.80 MiB | `2851443500000` |
| Go | `go1.26.2` | 123.962 | 20.537 | 3.85 MiB | `2851443500000` |
| Rust | `rustc 1.94.1` | 106.577 | 14.921 | 1.50 MiB | `2851443500000` |
| Zig | `zig 0.15.2` | 208.918 | 14.311 | 1.36 MiB | `2851443500000` |
| Julia | `Julia 1.12.5` | - | 166.830 | 226 MiB | `2851443500000` |
| Node | `Node v25.9.0` | - | 210.587 | 48.8 MiB | `2851443500000` |
| Bun | `Bun 1.3.9` | - | 33.486 | 28.2 MiB | `2851443500000` |
| Python | `Python 3.14.3` | - | 1646.635 | 14.6 MiB | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **141.739** | **13.219** | **1.31 MiB** | `16.695311` |
| C | `Apple clang 21.0.0` | 63.864 | 13.394 | 1.31 MiB | `16.695311` |
| C++ | `Apple clang 21.0.0` | 378.235 | 13.238 | 1.33 MiB | `16.695311` |
| Swift | `Swift 6.3` | 333.373 | 14.573 | 5.55 MiB | `16.695311` |
| Go | `go1.26.2` | 122.549 | 14.132 | 3.94 MiB | `16.695311` |
| Rust | `rustc 1.94.1` | 110.511 | 13.716 | 1.50 MiB | `16.695311` |
| Zig | `zig 0.15.2` | 374.566 | 13.351 | 1.34 MiB | `16.695311` |
| Julia | `Julia 1.12.5` | - | 284.126 | 248 MiB | `16.695311` |
| Node | `Node v25.9.0` | - | 80.514 | 49.1 MiB | `16.695311` |
| Bun | `Bun 1.3.9` | - | 24.498 | 27.0 MiB | `16.695311` |
| Python | `Python 3.14.3` | - | 776.086 | 14.6 MiB | `16.695311` |

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
- Peak Memory is the median peak resident set size across the untimed warm-up runs.
- In plain terms, think of Peak Memory as the approximate RAM used by the benchmark process at its peak.
- Pluto currently uses its own LLVM pipeline with `opt -O3`.
- Pluto is compiled with `PLUTO_TARGET_CPU=native`.
- C and C++ are built with `-O3` plus host-native CPU tuning.
- Swift is built with `swiftc -O -target-cpu native`.
- Rust is built with `rustc -C opt-level=3 -C target-cpu=native`.
- Zig is built with `zig build-exe -O ReleaseFast -mcpu native`.
- Go uses the default optimized `go build` pipeline plus host-specific tuning when the
  toolchain exposes a native override, such as `GOAMD64` on `x86_64`.
- Julia runs with `julia --startup-file=no`.
- The harness creates isolated temp work directories and copies each benchmark into them before running.
- It copies the benchmark files into that directory, including Pluto support `.pt` files when present.
- Every timed sample launches a fresh process, so the published `run_ms` numbers are end-to-end wall-clock timings.
- One warm-up execution runs before each timed sample.
- Short runtime cases such as `sum` and `harmonic` still include non-trivial process-startup noise, so treat small differences there with caution.
- Output is checked against `expected.txt` for the benchmark.
