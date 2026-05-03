# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, LuaJIT, Node, Bun, and Python.
The Python `sum` and `harmonic` cases use NumPy-backed implementations; the
recursive `fib` and `fib_tail` cases stay plain Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-05-02 23:48:47 UTC+04:00` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.4.1 (25E253)
- Command: `python3 scripts/benchmark.py --repeat 10 --snapshot-dir results/latest`
- Benchmark mode: median of 10 samples
- All languages are timed as fresh processes
- Compiled languages use host-native CPU tuning where the toolchain exposes it
- Runtime values can drift with host load and thermal state; this snapshot's
  primary change is Pluto compile-time measurement after in-process LLVM codegen.
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
| **Pluto** | `pluto dev` | **67.435** | **8.687** | **1.3 MiB** | `160000000` |
| C | `Homebrew clang 22.1.4` | 129.164 | 9.267 | 1.3 MiB | `160000000` |
| C++ | `Homebrew clang 22.1.4` | 131.481 | 9.238 | 1.3 MiB | `160000000` |
| Swift | `Swift 6.3.1` | 237.748 | 22.693 | 1.8 MiB | `160000000` |
| Go | `go1.26.2` | 127.066 | 23.960 | 3.9 MiB | `160000000` |
| Rust | `rustc 1.95.0` | 103.618 | 25.976 | 1.5 MiB | `160000000` |
| Zig | `zig 0.15.2` | 227.387 | 15.870 | 1.4 MiB | `160000000` |
| Julia | `Julia 1.12.5` | - | 165.519 | 226.4 MiB | `160000000` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 43.052 | 1.8 MiB | `160000000` |
| Node | `Node v25.9.0` | - | 90.752 | 48.9 MiB | `160000000` |
| Bun | `Bun 1.3.9` | - | 37.642 | 27.0 MiB | `160000000` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 140.752 | 36.0 MiB | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **72.992** | **11.339** | **1.3 MiB** | `2178309` |
| C | `Homebrew clang 22.1.4` | 133.548 | 10.940 | 1.3 MiB | `2178309` |
| C++ | `Homebrew clang 22.1.4` | 134.449 | 10.723 | 1.3 MiB | `2178309` |
| Swift | `Swift 6.3.1` | 218.688 | 15.643 | 1.8 MiB | `2178309` |
| Go | `go1.26.2` | 129.333 | 12.316 | 3.9 MiB | `2178309` |
| Rust | `rustc 1.95.0` | 104.714 | 11.692 | 1.5 MiB | `2178309` |
| Zig | `zig 0.15.2` | 230.753 | 10.878 | 1.4 MiB | `2178309` |
| Julia | `Julia 1.12.5` | - | 165.920 | 226.0 MiB | `2178309` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 18.295 | 1.8 MiB | `2178309` |
| Node | `Node v25.9.0` | - | 93.270 | 48.8 MiB | `2178309` |
| Bun | `Bun 1.3.9` | - | 27.064 | 26.0 MiB | `2178309` |
| Python | `Python 3.14.4` | - | 276.011 | 14.6 MiB | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **71.895** | **15.557** | **1.3 MiB** | `2851443500000` |
| C | `Homebrew clang 22.1.4` | 132.664 | 15.196 | 1.3 MiB | `2851443500000` |
| C++ | `Homebrew clang 22.1.4` | 135.023 | 16.286 | 1.3 MiB | `2851443500000` |
| Swift | `Swift 6.3.1` | 245.149 | 13.068 | 1.8 MiB | `2851443500000` |
| Go | `go1.26.2` | 129.580 | 22.540 | 3.8 MiB | `2851443500000` |
| Rust | `rustc 1.95.0` | 104.775 | 15.641 | 1.5 MiB | `2851443500000` |
| Zig | `zig 0.15.2` | 230.550 | 15.642 | 1.4 MiB | `2851443500000` |
| Julia | `Julia 1.12.5` | - | 179.871 | 226.7 MiB | `2851443500000` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 25.284 | 1.8 MiB | `2851443500000` |
| Node | `Node v25.9.0` | - | 218.675 | 49.2 MiB | `2851443500000` |
| Bun | `Bun 1.3.9` | - | 36.418 | 28.3 MiB | `2851443500000` |
| Python | `Python 3.14.4` | - | 1245.533 | 14.6 MiB | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **71.939** | **13.782** | **1.3 MiB** | `16.695311` |
| C | `Homebrew clang 22.1.4` | 136.294 | 16.241 | 1.3 MiB | `16.695311` |
| C++ | `Homebrew clang 22.1.4` | 135.753 | 14.326 | 1.3 MiB | `16.695311` |
| Swift | `Swift 6.3.1` | 352.817 | 17.099 | 5.6 MiB | `16.695311` |
| Go | `go1.26.2` | 127.146 | 14.894 | 3.9 MiB | `16.695311` |
| Rust | `rustc 1.95.0` | 106.300 | 14.367 | 1.5 MiB | `16.695311` |
| Zig | `zig 0.15.2` | 433.362 | 15.370 | 1.3 MiB | `16.695311` |
| Julia | `Julia 1.12.5` | - | 276.296 | 248.0 MiB | `16.695311` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 14.543 | 1.8 MiB | `16.695311` |
| Node | `Node v25.9.0` | - | 81.383 | 49.3 MiB | `16.695311` |
| Bun | `Bun 1.3.9` | - | 26.345 | 27.0 MiB | `16.695311` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 84.176 | 43.6 MiB | `16.695311` |

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
`pluto`, builds it with Pluto's `build.py` on LLVM 22, runs the same harness,
and uploads a separate snapshot artifact under `results/linux-gha` semantics.
It does not overwrite the checked-in `results/latest` macOS snapshot.

Run a single benchmark:

```sh
python3 scripts/benchmark.py sum
python3 scripts/benchmark.py fib
python3 scripts/benchmark.py fib_tail
python3 scripts/benchmark.py harmonic
```

Override tool locations when needed with `--pluto`, `--zig`, `--cc`, `--cxx`,
and `--luajit` or the matching environment variables `PLUTO_BIN`, `ZIG_BIN`,
`CC_BIN`, `CXX_BIN`, and `LUAJIT_BIN`.

```sh
python3 scripts/benchmark.py \
  --pluto /path/to/pluto \
  --zig /path/to/zig \
  --cc /path/to/clang \
  --cxx /path/to/clang++ \
  --luajit /path/to/luajit
```

## Measurement Notes

- Pluto, C, C++, Swift, Go, Rust, and Zig report native compile time and execution time separately.
- Julia, LuaJIT, Node, Bun, and Python are reported as runtime or JIT execution only, so their compile column is `-`.
- Python uses NumPy-backed implementations for `sum` and `harmonic`, and plain Python for `fib` and `fib_tail`.
- Snapshot tables only include languages whose toolchains were available on the host where the snapshot was generated.
- Peak Memory is collected automatically when the host supports `/usr/bin/time`; it is the median peak resident set size from the warm-up runs.
- Pluto uses its in-process LLVM `default<O3>` pipeline and links executables through `clang`.
- Pluto is compiled with `PLUTO_TARGET_CPU=native`.
- For dev builds, rebuild the Pluto binary immediately before benchmarking; the metadata records
  the selected binary path and containing repo, but the dev binary does not embed its source commit.
- Compiled languages use their standard optimized modes plus host-native CPU tuning where supported.
- C and C++ use `-O3`, Swift uses `-O`, Rust uses `-C opt-level=3`, and Zig uses `-O ReleaseFast`.
- Julia runs with `julia --startup-file=no`.
- LuaJIT runs with `luajit`.
- The metadata's "Host LLVM Tools" line records tool availability on the benchmark host; it
  does not mean Pluto shells out to `opt` or `llc`.
- The harness creates isolated temp work directories, copies benchmark files into them, and launches a fresh process for every timed sample.
- One warm-up execution runs before each timed sample.
- Short runtime cases such as `sum` and `harmonic` still include non-trivial process-startup noise, so treat small differences there with caution.
- Output is checked against `expected.txt` for the benchmark.
