# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.
The Python `sum` and `harmonic` cases use NumPy-backed implementations; the
recursive `fib` and `fib_tail` cases stay plain Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-04-19 09:26:34 UTC+05:30` with:

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
| **Pluto** | `pluto dev` | **126.486** | **8.274** | **1.3 MiB** | `160000000` |
| C | `Homebrew clang 22.1.3` | 117.682 | 8.228 | 1.3 MiB | `160000000` |
| C++ | `Homebrew clang 22.1.3` | 120.253 | 8.339 | 1.3 MiB | `160000000` |
| Swift | `Swift 6.3.1` | 209.303 | 19.761 | 1.8 MiB | `160000000` |
| Go | `go1.26.2` | 116.447 | 21.764 | 4.1 MiB | `160000000` |
| Rust | `rustc 1.94.1` | 92.345 | 23.744 | 1.5 MiB | `160000000` |
| Zig | `zig 0.15.2` | 209.288 | 14.569 | 1.4 MiB | `160000000` |
| Julia | `Julia 1.12.5` | - | 140.355 | 225.9 MiB | `160000000` |
| Node | `Node v25.9.0` | - | 84.255 | 48.8 MiB | `160000000` |
| Bun | `Bun 1.3.9` | - | 32.405 | 27.0 MiB | `160000000` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 126.487 | 35.8 MiB | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **125.821** | **8.704** | **1.3 MiB** | `2178309` |
| C | `Homebrew clang 22.1.3` | 115.235 | 9.527 | 1.3 MiB | `2178309` |
| C++ | `Homebrew clang 22.1.3` | 117.109 | 9.457 | 1.3 MiB | `2178309` |
| Swift | `Swift 6.3.1` | 195.381 | 12.506 | 1.8 MiB | `2178309` |
| Go | `go1.26.2` | 114.281 | 11.255 | 4.0 MiB | `2178309` |
| Rust | `rustc 1.94.1` | 89.322 | 9.829 | 1.5 MiB | `2178309` |
| Zig | `zig 0.15.2` | 206.332 | 9.831 | 1.4 MiB | `2178309` |
| Julia | `Julia 1.12.5` | - | 141.281 | 225.5 MiB | `2178309` |
| Node | `Node v25.9.0` | - | 86.059 | 48.7 MiB | `2178309` |
| Bun | `Bun 1.3.9` | - | 22.752 | 26.0 MiB | `2178309` |
| Python | `Python 3.14.4` | - | 263.437 | 14.5 MiB | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **126.922** | **13.952** | **1.3 MiB** | `2851443500000` |
| C | `Homebrew clang 22.1.3` | 116.196 | 13.952 | 1.3 MiB | `2851443500000` |
| C++ | `Homebrew clang 22.1.3` | 116.523 | 13.967 | 1.3 MiB | `2851443500000` |
| Swift | `Swift 6.3.1` | 216.717 | 11.596 | 1.8 MiB | `2851443500000` |
| Go | `go1.26.2` | 114.438 | 19.688 | 4.1 MiB | `2851443500000` |
| Rust | `rustc 1.94.1` | 94.062 | 15.389 | 1.5 MiB | `2851443500000` |
| Zig | `zig 0.15.2` | 202.174 | 14.175 | 1.4 MiB | `2851443500000` |
| Julia | `Julia 1.12.5` | - | 153.311 | 226.2 MiB | `2851443500000` |
| Node | `Node v25.9.0` | - | 206.327 | 49.1 MiB | `2851443500000` |
| Bun | `Bun 1.3.9` | - | 31.984 | 28.2 MiB | `2851443500000` |
| Python | `Python 3.14.4` | - | 1188.790 | 14.5 MiB | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **125.450** | **12.571** | **1.3 MiB** | `16.695311` |
| C | `Homebrew clang 22.1.3` | 117.286 | 12.579 | 1.3 MiB | `16.695311` |
| C++ | `Homebrew clang 22.1.3` | 117.860 | 12.584 | 1.3 MiB | `16.695311` |
| Swift | `Swift 6.3.1` | 310.408 | 14.139 | 5.6 MiB | `16.695311` |
| Go | `go1.26.2` | 114.752 | 13.754 | 4.1 MiB | `16.695311` |
| Rust | `rustc 1.94.1` | 92.396 | 12.878 | 1.5 MiB | `16.695311` |
| Zig | `zig 0.15.2` | 381.900 | 12.879 | 1.4 MiB | `16.695311` |
| Julia | `Julia 1.12.5` | - | 235.311 | 247.5 MiB | `16.695311` |
| Node | `Node v25.9.0` | - | 73.214 | 49.4 MiB | `16.695311` |
| Bun | `Bun 1.3.9` | - | 22.104 | 27.0 MiB | `16.695311` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 74.213 | 43.4 MiB | `16.695311` |

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
