# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-04-03 18:32:54 UTC+05:30` with:

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

![Run time chart](results/latest/run-times.svg)

Compile time overview:

![Compile time chart](results/latest/compile-times.svg)

The charts are the quick view. Each benchmark uses its own linear scale, so bar lengths are comparable within a benchmark but not across benchmarks. The tables below are the exact reference.

### Sum

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **136.651** | **9.562** | `160000000` |
| C | `Apple clang 21.0.0` | 62.303 | 8.873 | `160000000` |
| C++ | `Apple clang 21.0.0` | 387.051 | 9.128 | `160000000` |
| Swift | `Swift 6.3` | 230.465 | 21.288 | `160000000` |
| Go | `go1.26.1` | 125.593 | 23.050 | `160000000` |
| Rust | `rustc 1.94.1` | 104.258 | 24.590 | `160000000` |
| Zig | `zig 0.15.2` | 214.723 | 15.275 | `160000000` |
| Node | `Node v25.9.0` | - | 90.766 | `160000000` |
| Python | `Python 3.14.3` | - | 1522.752 | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **138.054** | **29.709** | `2178309` |
| C | `Apple clang 21.0.0` | 62.930 | 10.305 | `2178309` |
| C++ | `Apple clang 21.0.0` | 378.665 | 10.252 | `2178309` |
| Swift | `Swift 6.3` | 216.882 | 13.956 | `2178309` |
| Go | `go1.26.1` | 124.498 | 12.290 | `2178309` |
| Rust | `rustc 1.94.1` | 100.825 | 10.603 | `2178309` |
| Zig | `zig 0.15.2` | 212.273 | 10.373 | `2178309` |
| Node | `Node v25.9.0` | - | 91.349 | `2178309` |
| Python | `Python 3.14.3` | - | 313.174 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **141.439** | **115.651** | `2851443500000` |
| C | `Apple clang 21.0.0` | 62.287 | 14.666 | `2851443500000` |
| C++ | `Apple clang 21.0.0` | 381.448 | 14.858 | `2851443500000` |
| Swift | `Swift 6.3` | 238.624 | 12.643 | `2851443500000` |
| Go | `go1.26.1` | 126.129 | 21.047 | `2851443500000` |
| Rust | `rustc 1.94.1` | 105.499 | 15.025 | `2851443500000` |
| Zig | `zig 0.15.2` | 207.048 | 14.910 | `2851443500000` |
| Node | `Node v25.9.0` | - | 216.159 | `2851443500000` |
| Python | `Python 3.14.3` | - | 1649.912 | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **140.187** | **13.296** | `16.695311` |
| C | `Apple clang 21.0.0` | 66.058 | 13.730 | `16.695311` |
| C++ | `Apple clang 21.0.0` | 406.795 | 13.546 | `16.695311` |
| Swift | `Swift 6.3` | 340.710 | 14.969 | `16.695311` |
| Go | `go1.26.1` | 129.997 | 14.342 | `16.695311` |
| Rust | `rustc 1.94.1` | 105.219 | 13.858 | `16.695311` |
| Zig | `zig 0.15.2` | 383.617 | 13.449 | `16.695311` |
| Node | `Node v25.9.0` | - | 78.439 | `16.695311` |
| Python | `Python 3.14.3` | - | 764.565 | `16.695311` |

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
`benchmarks/sum/go/main.go` or `benchmarks/fib/pluto/main.spt`. Pluto-specific
support files such as `support.pt` live alongside the Pluto source in that
benchmark's `pluto/` subdirectory.

## Running

Run the full suite:

```sh
python3 scripts/benchmark.py
```

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
