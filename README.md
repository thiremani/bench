# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-03-21 11:57:34 IST` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.3.1 (25D2128)
- Command: `python3 scripts/benchmark.py --repeat 10`
- Benchmark mode: median of 10 samples, with one warm-up execution before each timed run
- Pluto rows are marked as `Pluto (baseline)` for quick comparison

### Sum

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **94.082** | **2.324** | `5000000050000000` |
| C | `Apple clang 17.0.0` | 62.264 | 2.356 | `5000000050000000` |
| C++ | `Apple clang 17.0.0` | 345.001 | 2.746 | `5000000050000000` |
| Swift | `Swift 6.2.4` | 213.228 | 38.086 | `5000000050000000` |
| Go | `go1.26.1` | 122.646 | 37.666 | `5000000050000000` |
| Rust | `rustc 1.94.0` | 104.104 | 68.859 | `5000000050000000` |
| Zig | `zig 0.15.2` | 213.171 | 2.992 | `5000000050000000` |
| Julia | `Julia 1.12.5` | - | 150.692 | `5000000050000000` |
| Node | `Node v25.8.1` | - | 725.256 | `5000000050000000` |
| Bun | `Bun 1.3.9` | - | 110.074 | `5000000050000000` |
| Python | `Python 3.14.3` | - | 6474.846 | `5000000050000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **86.080** | **30.799** | `2178309` |
| C | `Apple clang 17.0.0` | 61.698 | 13.202 | `2178309` |
| C++ | `Apple clang 17.0.0` | 316.187 | 13.023 | `2178309` |
| Swift | `Swift 6.2.4` | 208.918 | 14.356 | `2178309` |
| Go | `go1.26.1` | 126.885 | 13.926 | `2178309` |
| Rust | `rustc 1.94.0` | 102.353 | 12.159 | `2178309` |
| Zig | `zig 0.15.2` | 212.021 | 14.783 | `2178309` |
| Julia | `Julia 1.12.5` | - | 165.159 | `2178309` |
| Node | `Node v25.8.1` | - | 85.864 | `2178309` |
| Bun | `Bun 1.3.9` | - | 22.015 | `2178309` |
| Python | `Python 3.14.3` | - | 304.807 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **90.036** | **16.993** | `285144350000` |
| C | `Apple clang 17.0.0` | 67.669 | 3.961 | `285144350000` |
| C++ | `Apple clang 17.0.0` | 337.795 | 3.916 | `285144350000` |
| Swift | `Swift 6.2.4` | 224.364 | 5.960 | `285144350000` |
| Go | `go1.26.1` | 124.700 | 6.550 | `285144350000` |
| Rust | `rustc 1.94.0` | 110.434 | 4.256 | `285144350000` |
| Zig | `zig 0.15.2` | 218.143 | 4.263 | `285144350000` |
| Julia | `Julia 1.12.5` | - | 147.668 | `285144350000` |
| Node | `Node v25.8.1` | - | 74.486 | `285144350000` |
| Bun | `Bun 1.3.9` | - | 14.587 | `285144350000` |
| Python | `Python 3.14.3` | - | 177.037 | `285144350000` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **86.748** | **15.422** | `16.695311` |
| C | `Apple clang 17.0.0` | 58.008 | 15.558 | `16.695311` |
| C++ | `Apple clang 17.0.0` | 304.393 | 16.468 | `16.695311` |
| Swift | `Swift 6.2.4` | 304.638 | 18.536 | `16.695311` |
| Go | `go1.26.1` | 125.177 | 17.076 | `16.695311` |
| Rust | `rustc 1.94.0` | 105.685 | 15.012 | `16.695311` |
| Zig | `zig 0.15.2` | 374.575 | 18.509 | `16.695311` |
| Julia | `Julia 1.12.5` | - | 280.125 | `16.695311` |
| Node | `Node v25.8.1` | - | 77.162 | `16.695311` |
| Bun | `Bun 1.3.9` | - | 24.300 | `16.695311` |
| Python | `Python 3.14.3` | - | 766.900 | `16.695311` |

## Benchmarks

- `sum`
  Integer reduction benchmark.
  Sums the natural numbers from `1` to `100,000,000`.
  This stays within JavaScript's exact integer range without switching Node or Bun to `BigInt`.
  Expected output: `5000000050000000`

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
- The harness creates an isolated temp work directory for each sample.
- It copies the benchmark files into that directory, including Pluto support `.pt` files when present.
- It performs one warm-up execution before each timed run.
- Each timed run launches a fresh process, so runtime and JIT languages still include per-process startup work in the measured run time.
- Output is checked against `expected.txt` for the benchmark.
