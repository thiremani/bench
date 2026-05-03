# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, LuaJIT, Node, Bun, and Python.
The Python `sum` and `harmonic` cases use NumPy-backed implementations; the
recursive `fib` and `fib_tail` cases stay plain Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-05-03 07:11:26 UTC+04:00` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.4.1 (25E253)
- Command: `python3 scripts/benchmark.py --repeat 10 --snapshot-dir results/latest`
- Pluto LLVM: in-process LLVM 22.1.4
- Pluto linker: `/usr/bin/clang` (`Apple clang 21.0.0`)
- C/C++ compilers: `/usr/bin/clang`, `/usr/bin/clang++` (`Apple clang 21.0.0`)
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
| **Pluto** | `pluto dev` | **67.702** | **8.530** | **1.3 MiB** | `160000000` |
| C | `Apple clang 21.0.0` | 60.413 | 8.369 | 1.3 MiB | `160000000` |
| C++ | `Apple clang 21.0.0` | 61.870 | 8.392 | 1.3 MiB | `160000000` |
| Swift | `Swift 6.3.1` | 219.838 | 20.433 | 1.8 MiB | `160000000` |
| Go | `go1.26.2` | 122.470 | 22.620 | 4.1 MiB | `160000000` |
| Rust | `rustc 1.95.0` | 95.882 | 24.829 | 1.5 MiB | `160000000` |
| Zig | `zig 0.15.2` | 223.153 | 14.716 | 1.4 MiB | `160000000` |
| Julia | `Julia 1.12.5` | - | 157.133 | 226 MiB | `160000000` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 39.597 | 1.8 MiB | `160000000` |
| Node | `Node v25.9.0` | - | 89.943 | 48.9 MiB | `160000000` |
| Bun | `Bun 1.3.9` | - | 32.653 | 27.0 MiB | `160000000` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 133.188 | 35.9 MiB | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **64.976** | **9.082** | **1.3 MiB** | `2178309` |
| C | `Apple clang 21.0.0` | 58.981 | 9.524 | 1.3 MiB | `2178309` |
| C++ | `Apple clang 21.0.0` | 60.636 | 9.513 | 1.3 MiB | `2178309` |
| Swift | `Swift 6.3.1` | 206.373 | 12.768 | 1.8 MiB | `2178309` |
| Go | `go1.26.2` | 121.127 | 11.773 | 4.1 MiB | `2178309` |
| Rust | `rustc 1.95.0` | 93.214 | 10.041 | 1.5 MiB | `2178309` |
| Zig | `zig 0.15.2` | 218.176 | 10.193 | 1.4 MiB | `2178309` |
| Julia | `Julia 1.12.5` | - | 151.363 | 226 MiB | `2178309` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 16.339 | 1.8 MiB | `2178309` |
| Node | `Node v25.9.0` | - | 91.006 | 48.8 MiB | `2178309` |
| Bun | `Bun 1.3.9` | - | 25.442 | 26.0 MiB | `2178309` |
| Python | `Python 3.14.4` | - | 276.071 | 14.6 MiB | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **66.991** | **14.237** | **1.3 MiB** | `2851443500000` |
| C | `Apple clang 21.0.0` | 58.908 | 16.437 | 1.3 MiB | `2851443500000` |
| C++ | `Apple clang 21.0.0` | 61.002 | 14.201 | 1.3 MiB | `2851443500000` |
| Swift | `Swift 6.3.1` | 228.022 | 12.041 | 1.8 MiB | `2851443500000` |
| Go | `go1.26.2` | 123.161 | 20.487 | 4.1 MiB | `2851443500000` |
| Rust | `rustc 1.95.0` | 96.586 | 14.585 | 1.5 MiB | `2851443500000` |
| Zig | `zig 0.15.2` | 220.004 | 14.560 | 1.4 MiB | `2851443500000` |
| Julia | `Julia 1.12.5` | - | 170.722 | 226 MiB | `2851443500000` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 22.736 | 1.8 MiB | `2851443500000` |
| Node | `Node v25.9.0` | - | 217.518 | 49.1 MiB | `2851443500000` |
| Bun | `Bun 1.3.9` | - | 34.925 | 28.3 MiB | `2851443500000` |
| Python | `Python 3.14.4` | - | 1247.247 | 14.6 MiB | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Peak Memory | Output |
| --- | --- | ---: | ---: | ---: | --- |
| **Pluto** | `pluto dev` | **67.384** | **12.977** | **1.3 MiB** | `16.695311` |
| C | `Apple clang 21.0.0` | 60.851 | 13.036 | 1.3 MiB | `16.695311` |
| C++ | `Apple clang 21.0.0` | 61.900 | 13.149 | 1.4 MiB | `16.695311` |
| Swift | `Swift 6.3.1` | 325.947 | 14.485 | 5.6 MiB | `16.695311` |
| Go | `go1.26.2` | 123.531 | 13.946 | 4.1 MiB | `16.695311` |
| Rust | `rustc 1.95.0` | 92.419 | 13.008 | 1.5 MiB | `16.695311` |
| Zig | `zig 0.15.2` | 405.486 | 13.055 | 1.4 MiB | `16.695311` |
| Julia | `Julia 1.12.5` | - | 267.070 | 248 MiB | `16.695311` |
| LuaJIT | `LuaJIT 2.1.1774896198` | - | 14.073 | 1.8 MiB | `16.695311` |
| Node | `Node v25.9.0` | - | 78.361 | 49.3 MiB | `16.695311` |
| Bun | `Bun 1.3.9` | - | 24.434 | 27.0 MiB | `16.695311` |
| Python | `Python 3.14.4 + NumPy 2.4.4` | - | 77.930 | 43.5 MiB | `16.695311` |

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
- Pluto uses its in-process LLVM `default<O3>` pipeline to optimize IR and emit native objects, then
  links executables through `clang`; benchmark metadata records both separately.
- On macOS, the harness defaults to Apple clang for C/C++ and aligns Pluto's link-driver `PATH`
  to the selected C compiler directory.
- Pluto is compiled with `PLUTO_TARGET_CPU=native`.
- For dev builds, rebuild the Pluto binary immediately before benchmarking; the metadata records
  the selected binary path and containing repo, but the dev binary does not embed its source commit.
- Compiled languages use their standard optimized modes plus host-native CPU tuning where supported.
- C and C++ use `-O3`, Swift uses `-O`, Rust uses `-C opt-level=3`, and Zig uses `-O ReleaseFast`.
- Julia runs with `julia --startup-file=no`.
- LuaJIT runs with `luajit`.
- The harness creates isolated temp work directories, copies benchmark files into them, and launches a fresh process for every timed sample.
- One warm-up execution runs before each timed sample.
- Short runtime cases such as `sum` and `harmonic` still include non-trivial process-startup noise, so treat small differences there with caution.
- Output is checked against `expected.txt` for the benchmark.
