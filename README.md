# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-03-21 12:25:18 IST` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.3.1 (25D2128)
- Command: `python3 scripts/benchmark.py --repeat 10`
- Benchmark mode: median of 10 samples
- Native languages use one warm-up execution before each timed run
- Runtime languages use one warm-up call inside a persistent worker process
- Pluto rows are marked as `Pluto (baseline)` for quick comparison

### Sum

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **96.602** | **19.913** | `160000000` |
| C | `Apple clang 17.0.0` | 65.583 | 15.842 | `160000000` |
| C++ | `Apple clang 17.0.0` | 338.244 | 17.140 | `160000000` |
| Swift | `Swift 6.2.4` | 195.456 | 21.740 | `160000000` |
| Go | `go1.26.1` | 125.666 | 24.807 | `160000000` |
| Rust | `rustc 1.94.0` | 103.681 | 27.049 | `160000000` |
| Zig | `zig 0.15.2` | 207.721 | 19.575 | `160000000` |
| Julia | `Julia 1.12.5` | - | 11.863 | `160000000` |
| Node | `Node v25.8.1` | - | 20.005 | `160000000` |
| Bun | `Bun 1.3.9` | - | 15.722 | `160000000` |
| Python | `Python 3.14.3` | - | 826.621 | `160000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **94.679** | **30.120** | `2178309` |
| C | `Apple clang 17.0.0` | 64.558 | 11.699 | `2178309` |
| C++ | `Apple clang 17.0.0` | 336.508 | 11.743 | `2178309` |
| Swift | `Swift 6.2.4` | 198.327 | 15.211 | `2178309` |
| Go | `go1.26.1` | 125.929 | 13.723 | `2178309` |
| Rust | `rustc 1.94.0` | 102.098 | 12.357 | `2178309` |
| Zig | `zig 0.15.2` | 200.150 | 11.565 | `2178309` |
| Julia | `Julia 1.12.5` | - | 8.608 | `2178309` |
| Node | `Node v25.8.1` | - | 21.000 | `2178309` |
| Bun | `Bun 1.3.9` | - | 11.511 | `2178309` |
| Python | `Python 3.14.3` | - | 283.440 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **97.944** | **14.527** | `285144350000` |
| C | `Apple clang 17.0.0` | 65.703 | 3.936 | `285144350000` |
| C++ | `Apple clang 17.0.0` | 375.595 | 4.414 | `285144350000` |
| Swift | `Swift 6.2.4` | 218.121 | 5.723 | `285144350000` |
| Go | `go1.26.1` | 126.314 | 5.943 | `285144350000` |
| Rust | `rustc 1.94.0` | 105.262 | 4.362 | `285144350000` |
| Zig | `zig 0.15.2` | 209.938 | 4.134 | `285144350000` |
| Julia | `Julia 1.12.5` | - | 3.101 | `285144350000` |
| Node | `Node v25.8.1` | - | 14.216 | `285144350000` |
| Bun | `Bun 1.3.9` | - | 6.944 | `285144350000` |
| Python | `Python 3.14.3` | - | 156.252 | `285144350000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **92.423** | **14.395** | `16.695311` |
| C | `Apple clang 17.0.0` | 60.813 | 13.876 | `16.695311` |
| C++ | `Apple clang 17.0.0` | 341.386 | 13.801 | `16.695311` |
| Swift | `Swift 6.2.4` | 326.089 | 14.881 | `16.695311` |
| Go | `go1.26.1` | 126.149 | 14.772 | `16.695311` |
| Rust | `rustc 1.94.0` | 106.040 | 13.720 | `16.695311` |
| Zig | `zig 0.15.2` | 376.238 | 13.747 | `16.695311` |
| Julia | `Julia 1.12.5` | - | 9.977 | `16.695311` |
| Node | `Node v25.8.1` | - | 9.855 | `16.695311` |
| Bun | `Bun 1.3.9` | - | 9.851 | `16.695311` |
| Python | `Python 3.14.3` | - | 442.333 | `16.695311` |

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
- Native languages perform one warm-up execution before each timed run.
- Julia, Node, Bun, and Python run inside a persistent worker process for each benchmark/language, with one warm-up call before the timed samples.
- Native run time still includes process launch for the produced executable. Runtime-language run time is closer to steady-state execution inside the already-started interpreter or VM.
- Output is checked against `expected.txt` for the benchmark.
