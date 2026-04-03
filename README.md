# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-04-03 22:06:21 UTC+05:30` with:

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
| **Pluto (baseline)** | `pluto dev` | **137.685** | **8.642** | `160000000` |
| C | `Apple clang 21.0.0` | 61.789 | 9.312 | `160000000` |
| C++ | `Apple clang 21.0.0` | 373.204 | 9.376 | `160000000` |
| Swift | `Swift 6.3` | 240.218 | 21.724 | `160000000` |
| Go | `go1.26.1` | 122.145 | 22.033 | `160000000` |
| Rust | `rustc 1.94.1` | 97.162 | 23.779 | `160000000` |
| Zig | `zig 0.15.2` | 220.998 | 15.294 | `160000000` |
| Node | `Node v25.9.0` | - | 90.158 | `160000000` |
| Python | `Python 3.14.3` | - | 1537.175 | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **133.545** | **9.063** | `2178309` |
| C | `Apple clang 21.0.0` | 60.357 | 10.379 | `2178309` |
| C++ | `Apple clang 21.0.0` | 395.378 | 10.456 | `2178309` |
| Swift | `Swift 6.3` | 213.733 | 13.275 | `2178309` |
| Go | `go1.26.1` | 120.117 | 11.868 | `2178309` |
| Rust | `rustc 1.94.1` | 98.871 | 10.414 | `2178309` |
| Zig | `zig 0.15.2` | 201.663 | 10.002 | `2178309` |
| Node | `Node v25.9.0` | - | 87.114 | `2178309` |
| Python | `Python 3.14.3` | - | 311.650 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **134.416** | **14.259** | `2851443500000` |
| C | `Apple clang 21.0.0` | 59.167 | 14.323 | `2851443500000` |
| C++ | `Apple clang 21.0.0` | 355.177 | 14.265 | `2851443500000` |
| Swift | `Swift 6.3` | 225.752 | 12.072 | `2851443500000` |
| Go | `go1.26.1` | 119.498 | 20.584 | `2851443500000` |
| Rust | `rustc 1.94.1` | 103.079 | 15.017 | `2851443500000` |
| Zig | `zig 0.15.2` | 208.513 | 14.726 | `2851443500000` |
| Node | `Node v25.9.0` | - | 207.062 | `2851443500000` |
| Python | `Python 3.14.3` | - | 1641.072 | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **134.394** | **13.079** | `16.695311` |
| C | `Apple clang 21.0.0` | 60.468 | 13.150 | `16.695311` |
| C++ | `Apple clang 21.0.0` | 359.312 | 13.046 | `16.695311` |
| Swift | `Swift 6.3` | 333.620 | 14.711 | `16.695311` |
| Go | `go1.26.1` | 119.853 | 13.980 | `16.695311` |
| Rust | `rustc 1.94.1` | 102.826 | 13.209 | `16.695311` |
| Zig | `zig 0.15.2` | 380.829 | 13.292 | `16.695311` |
| Node | `Node v25.9.0` | - | 81.360 | `16.695311` |
| Python | `Python 3.14.3` | - | 754.507 | `16.695311` |

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
