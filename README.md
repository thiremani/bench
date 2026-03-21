# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-03-21 14:22:10 IST` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.3.1 (25D2128)
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
| **Pluto (baseline)** | `pluto dev` | **123.532** | **21.762** | `160000000` |
| C | `Apple clang 17.0.0` | 59.387 | 16.776 | `160000000` |
| C++ | `Apple clang 17.0.0` | 302.941 | 19.088 | `160000000` |
| Swift | `Swift 6.2.4` | 194.483 | 22.049 | `160000000` |
| Go | `go1.26.1` | 114.885 | 24.969 | `160000000` |
| Rust | `rustc 1.94.0` | 95.287 | 26.470 | `160000000` |
| Zig | `zig 0.15.2` | 203.291 | 20.130 | `160000000` |
| Julia | `Julia 1.12.5` | - | 144.759 | `160000000` |
| Node | `Node v25.8.1` | - | 83.223 | `160000000` |
| Bun | `Bun 1.3.9` | - | 31.826 | `160000000` |
| Python | `Python 3.14.3` | - | 1550.331 | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **123.500** | **30.910** | `2178309` |
| C | `Apple clang 17.0.0` | 60.150 | 11.931 | `2178309` |
| C++ | `Apple clang 17.0.0` | 302.267 | 13.267 | `2178309` |
| Swift | `Swift 6.2.4` | 181.818 | 16.476 | `2178309` |
| Go | `go1.26.1` | 117.544 | 15.673 | `2178309` |
| Rust | `rustc 1.94.0` | 92.656 | 13.428 | `2178309` |
| Zig | `zig 0.15.2` | 205.363 | 15.407 | `2178309` |
| Julia | `Julia 1.12.5` | - | 146.098 | `2178309` |
| Node | `Node v25.8.1` | - | 82.787 | `2178309` |
| Bun | `Bun 1.3.9` | - | 22.119 | `2178309` |
| Python | `Python 3.14.3` | - | 317.006 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **138.264** | **18.441** | `285144350000` |
| C | `Apple clang 17.0.0` | 66.136 | 4.171 | `285144350000` |
| C++ | `Apple clang 17.0.0` | 350.655 | 4.123 | `285144350000` |
| Swift | `Swift 6.2.4` | 218.461 | 5.787 | `285144350000` |
| Go | `go1.26.1` | 123.378 | 5.318 | `285144350000` |
| Rust | `rustc 1.94.0` | 101.883 | 4.152 | `285144350000` |
| Zig | `zig 0.15.2` | 206.443 | 3.714 | `285144350000` |
| Julia | `Julia 1.12.5` | - | 142.712 | `285144350000` |
| Node | `Node v25.8.1` | - | 78.368 | `285144350000` |
| Bun | `Bun 1.3.9` | - | 15.128 | `285144350000` |
| Python | `Python 3.14.3` | - | 184.103 | `285144350000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
| --- | --- | ---: | ---: | --- |
| **Pluto (baseline)** | `pluto dev` | **125.842** | **12.056** | `16.695311` |
| C | `Apple clang 17.0.0` | 57.650 | 12.128 | `16.695311` |
| C++ | `Apple clang 17.0.0` | 314.106 | 13.837 | `16.695311` |
| Swift | `Swift 6.2.4` | 307.287 | 17.301 | `16.695311` |
| Go | `go1.26.1` | 119.034 | 16.622 | `16.695311` |
| Rust | `rustc 1.94.0` | 96.476 | 15.582 | `16.695311` |
| Zig | `zig 0.15.2` | 357.968 | 19.263 | `16.695311` |
| Julia | `Julia 1.12.5` | - | 246.576 | `16.695311` |
| Node | `Node v25.8.1` | - | 73.418 | `16.695311` |
| Bun | `Bun 1.3.9` | - | 21.123 | `16.695311` |
| Python | `Python 3.14.3` | - | 790.112 | `16.695311` |

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
  Accumulates `100,000` tail-recursive Fibonacci calls, alternating between `fib(32)` and `fib(33)`.
  This makes the runtime less sensitive to process-startup noise than a single `fib(32)` call.
  Expected output: `285144350000`

- `harmonic`
  Floating-point throughput benchmark.
  Computes the harmonic sum from `1` to `10,000,000`.
  Expected output: `16.695311`

Each benchmark directory contains equivalent `main.*` implementations for the
languages included in the suite, plus `expected.txt` and optional Pluto support
files such as `support.pt`.

## Running

Run the full suite:

```sh
python3 scripts/benchmark.py
```

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
- Zig is built with `zig build-exe -O ReleaseFast`.
- Go uses the default optimized `go build` pipeline.
- Julia runs with `julia --startup-file=no`.
- The harness creates isolated temp work directories and copies each benchmark into them before running.
- It copies the benchmark files into that directory, including Pluto support `.pt` files when present.
- Every timed sample launches a fresh process, so the published `run_ms` numbers are end-to-end wall-clock timings.
- One warm-up execution runs before each timed sample.
- Short runtime cases such as `sum`, `fib_tail`, and `harmonic` still include non-trivial process-startup noise, so treat small differences there with caution.
- Output is checked against `expected.txt` for the benchmark.
