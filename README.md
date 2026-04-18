# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.
The Python `sum` and `harmonic` cases use NumPy-backed implementations; the
recursive `fib` and `fib_tail` cases stay plain Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-04-18 20:34:58 UTC+05:30` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.4.1 (25E253)
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

- `sum`: Pluto source is `benchmarks/sum/pluto/sum.spt`; Python source is `benchmarks/sum/python/main.py` and uses NumPy.
- `fib`: Pluto uses `benchmarks/fib/pluto/fib.pt` plus `benchmarks/fib/pluto/fib.spt`; Python uses `benchmarks/fib/python/main.py`.

## Result Tables

### Sum

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **134.081** | **8.704** | **1.3 MiB** | `160000000` |
| C | `Homebrew clang 22.1.3` | 122.058 | 8.647 | 1.3 MiB | `160000000` |
| C++ | `Homebrew clang 22.1.3` | 397.399 | 8.663 | 1.3 MiB | `160000000` |
| Swift | `Swift 6.3.1` | 218.749 | 20.729 | 1.8 MiB | `160000000` |
| Go | `go1.26.2` | 119.988 | 22.630 | 4.1 MiB | `160000000` |
| Rust | `rustc 1.94.1` | 99.552 | 24.848 | 1.5 MiB | `160000000` |
| Zig | `zig 0.15.2` | 217.519 | 15.172 | 1.4 MiB | `160000000` |
| Julia | `Julia 1.12.5` | - | 152.062 | 226 MiB | `160000000` |
| Node | `Node v25.9.0` | - | 90.222 | 48.8 MiB | `160000000` |
| Bun | `Bun 1.3.9` | - | 35.960 | 27.0 MiB | `160000000` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 133.402 | 35.9 MiB | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **133.455** | **9.178** | **1.3 MiB** | `2178309` |
| C | `Homebrew clang 22.1.3` | 122.820 | 9.856 | 1.3 MiB | `2178309` |
| C++ | `Homebrew clang 22.1.3` | 402.476 | 9.840 | 1.3 MiB | `2178309` |
| Swift | `Swift 6.3.1` | 206.342 | 13.150 | 1.8 MiB | `2178309` |
| Go | `go1.26.2` | 120.557 | 11.734 | 4.0 MiB | `2178309` |
| Rust | `rustc 1.94.1` | 96.233 | 10.355 | 1.5 MiB | `2178309` |
| Zig | `zig 0.15.2` | 216.305 | 10.203 | 1.4 MiB | `2178309` |
| Julia | `Julia 1.12.5` | - | 152.127 | 225.7 MiB | `2178309` |
| Node | `Node v25.9.0` | - | 89.985 | 48.7 MiB | `2178309` |
| Bun | `Bun 1.3.9` | - | 25.106 | 26.0 MiB | `2178309` |
| Python | `Python 3.14.4` | - | 276.876 | 14.5 MiB | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **134.005** | **14.566** | **1.3 MiB** | `2851443500000` |
| C | `Homebrew clang 22.1.3` | 123.520 | 14.621 | 1.3 MiB | `2851443500000` |
| C++ | `Homebrew clang 22.1.3` | 400.846 | 14.579 | 1.3 MiB | `2851443500000` |
| Swift | `Swift 6.3.1` | 232.074 | 12.297 | 1.8 MiB | `2851443500000` |
| Go | `go1.26.2` | 120.285 | 20.409 | 4.1 MiB | `2851443500000` |
| Rust | `rustc 1.94.1` | 100.284 | 14.929 | 1.5 MiB | `2851443500000` |
| Zig | `zig 0.15.2` | 218.507 | 14.764 | 1.4 MiB | `2851443500000` |
| Julia | `Julia 1.12.5` | - | 168.108 | 226.2 MiB | `2851443500000` |
| Node | `Node v25.9.0` | - | 213.686 | 49.2 MiB | `2851443500000` |
| Bun | `Bun 1.3.9` | - | 34.076 | 28.3 MiB | `2851443500000` |
| Python | `Python 3.14.4` | - | 1254.375 | 14.5 MiB | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **135.609** | **13.280** | **1.3 MiB** | `16.695311` |
| C | `Homebrew clang 22.1.3` | 123.973 | 13.182 | 1.3 MiB | `16.695311` |
| C++ | `Homebrew clang 22.1.3` | 405.680 | 13.250 | 1.3 MiB | `16.695311` |
| Swift | `Swift 6.3.1` | 332.214 | 14.664 | 5.6 MiB | `16.695311` |
| Go | `go1.26.2` | 120.379 | 14.182 | 4.1 MiB | `16.695311` |
| Rust | `rustc 1.94.1` | 98.877 | 13.346 | 1.5 MiB | `16.695311` |
| Zig | `zig 0.15.2` | 403.113 | 13.412 | 1.4 MiB | `16.695311` |
| Julia | `Julia 1.12.5` | - | 261.034 | 247.9 MiB | `16.695311` |
| Node | `Node v25.9.0` | - | 78.154 | 49.3 MiB | `16.695311` |
| Bun | `Bun 1.3.9` | - | 24.340 | 27.0 MiB | `16.695311` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 79.724 | 43.4 MiB | `16.695311` |

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

Regenerate the checked-in charts and snapshot:

```sh
python3 scripts/benchmark.py --repeat 10 --snapshot-dir results/latest
```

The harness is compatible with Python 3.9+.

GitHub Actions also runs the suite on `ubuntu-24.04`. That workflow checks out
`pluto`, builds it with LLVM 21, runs the same harness, and uploads a separate
snapshot artifact under `results/linux-gha` semantics. It does not overwrite the
checked-in `results/latest` macOS snapshot.

Run a single benchmark:

```sh
python3 scripts/benchmark.py sum
python3 scripts/benchmark.py fib
python3 scripts/benchmark.py fib_tail
python3 scripts/benchmark.py harmonic
```

Override tool locations when needed with `--pluto`, `--zig`, `--cc`, and `--cxx`
or the matching environment variables `PLUTO_BIN`, `ZIG_BIN`, `CC_BIN`, and
`CXX_BIN`.

```sh
python3 scripts/benchmark.py \
  --pluto /path/to/pluto \
  --zig /path/to/zig \
  --cc /path/to/clang \
  --cxx /path/to/clang++
```

## Measurement Notes

- Pluto, C, C++, Swift, Go, Rust, and Zig report native compile time and execution time separately.
- Julia, Node, Bun, and Python are reported as runtime or JIT execution only, so their compile column is `-`.
- Python uses NumPy-backed implementations for `sum` and `harmonic`, and plain Python for `fib` and `fib_tail`.
- Snapshot tables only include languages whose toolchains were available on the host where the snapshot was generated.
- Peak Memory is collected automatically when the host supports `/usr/bin/time`; it is the median peak resident set size from the warm-up runs.
- Pluto currently uses its own LLVM pipeline with `opt -O3`.
- Pluto is compiled with `PLUTO_TARGET_CPU=native`.
- Compiled languages use their standard optimized modes plus host-native CPU tuning where supported.
- C and C++ use `-O3`, Swift uses `-O`, Rust uses `-C opt-level=3`, and Zig uses `-O ReleaseFast`.
- Julia runs with `julia --startup-file=no`.
- The harness creates isolated temp work directories, copies benchmark files into them, and launches a fresh process for every timed sample.
- One warm-up execution runs before each timed sample.
- Short runtime cases such as `sum` and `harmonic` still include non-trivial process-startup noise, so treat small differences there with caution.
- Output is checked against `expected.txt` for the benchmark.
