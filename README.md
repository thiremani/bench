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
| **Pluto (baseline)** | `pluto dev` | **150.622** | **9.696** | `160000000` |
| C | `Apple clang 21.0.0` | 67.565 | 9.679 | `160000000` |
| C++ | `Apple clang 21.0.0` | 397.564 | 9.665 | `160000000` |
| Swift | `Swift 6.3` | 243.694 | 23.008 | `160000000` |
| Go | `go1.26.1` | 131.106 | 25.318 | `160000000` |
| Rust | `rustc 1.94.1` | 106.982 | 27.803 | `160000000` |
| Zig | `zig 0.15.2` | 243.927 | 17.178 | `160000000` |
| Node | `Node v25.9.0` | - | 99.351 | `160000000` |
| Python | `Python 3.14.3` | - | 1779.109 | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **144.703** | **32.214** | `2178309` |
| C | `Apple clang 21.0.0` | 63.491 | 10.855 | `2178309` |
| C++ | `Apple clang 21.0.0` | 388.855 | 10.999 | `2178309` |
| Swift | `Swift 6.3` | 227.941 | 14.554 | `2178309` |
| Go | `go1.26.1` | 129.988 | 12.904 | `2178309` |
| Rust | `rustc 1.94.1` | 108.411 | 11.524 | `2178309` |
| Zig | `zig 0.15.2` | 236.333 | 11.231 | `2178309` |
| Node | `Node v25.9.0` | - | 99.245 | `2178309` |
| Python | `Python 3.14.3` | - | 362.125 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **148.121** | **134.821** | `2851443500000` |
| C | `Apple clang 21.0.0` | 66.129 | 16.115 | `2851443500000` |
| C++ | `Apple clang 21.0.0` | 387.113 | 16.206 | `2851443500000` |
| Swift | `Swift 6.3` | 251.316 | 13.417 | `2851443500000` |
| Go | `go1.26.1` | 131.325 | 22.712 | `2851443500000` |
| Rust | `rustc 1.94.1` | 108.285 | 16.624 | `2851443500000` |
| Zig | `zig 0.15.2` | 232.142 | 16.340 | `2851443500000` |
| Node | `Node v25.9.0` | - | 239.761 | `2851443500000` |
| Python | `Python 3.14.3` | - | 1903.829 | `2851443500000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **148.193** | **14.703** | `16.695311` |
| C | `Apple clang 21.0.0` | 65.312 | 14.551 | `16.695311` |
| C++ | `Apple clang 21.0.0` | 399.419 | 14.844 | `16.695311` |
| Swift | `Swift 6.3` | 367.894 | 16.485 | `16.695311` |
| Go | `go1.26.1` | 131.836 | 15.746 | `16.695311` |
| Rust | `rustc 1.94.1` | 108.209 | 15.071 | `16.695311` |
| Zig | `zig 0.15.2` | 415.433 | 14.834 | `16.695311` |
| Node | `Node v25.9.0` | - | 85.718 | `16.695311` |
| Python | `Python 3.14.3` | - | 910.486 | `16.695311` |

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
