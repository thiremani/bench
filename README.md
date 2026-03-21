# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Swift, Go, Rust, Zig, Julia, Node, Bun, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-03-21 11:26:48 IST` with:

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
| **Pluto (baseline)** | `pluto dev` | **96.947** | **2.662** | `200000010000000` |
| C | `Apple clang 17.0.0` | 63.688 | 2.414 | `200000010000000` |
| C++ | `Apple clang 17.0.0` | 322.931 | 2.451 | `200000010000000` |
| Swift | `Swift 6.2.4` | 196.662 | 13.315 | `200000010000000` |
| Go | `go1.26.1` | 118.283 | 14.002 | `200000010000000` |
| Rust | `rustc 1.94.0` | 104.388 | 17.532 | `200000010000000` |
| Zig | `zig 0.15.2` | 213.198 | 2.714 | `200000010000000` |
| Julia | `Julia 1.12.5` | - | 143.895 | `200000010000000` |
| Node | `Node v25.8.1` | - | 200.918 | `200000010000000` |
| Bun | `Bun 1.3.9` | - | 33.372 | `200000010000000` |
| Python | `Python 3.14.3` | - | 1369.513 | `200000010000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **95.055** | **30.067** | `2178309` |
| C | `Apple clang 17.0.0` | 65.561 | 11.620 | `2178309` |
| C++ | `Apple clang 17.0.0` | 344.915 | 11.686 | `2178309` |
| Swift | `Swift 6.2.4` | 197.456 | 15.001 | `2178309` |
| Go | `go1.26.1` | 126.435 | 14.020 | `2178309` |
| Rust | `rustc 1.94.0` | 102.376 | 11.967 | `2178309` |
| Zig | `zig 0.15.2` | 212.693 | 15.424 | `2178309` |
| Julia | `Julia 1.12.5` | - | 166.552 | `2178309` |
| Node | `Node v25.8.1` | - | 88.804 | `2178309` |
| Bun | `Bun 1.3.9` | - | 23.888 | `2178309` |
| Python | `Python 3.14.3` | - | 315.199 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **98.781** | **2.401** | `2178309` |
| C | `Apple clang 17.0.0` | 70.346 | 2.682 | `2178309` |
| C++ | `Apple clang 17.0.0` | 339.688 | 2.601 | `2178309` |
| Swift | `Swift 6.2.4` | 193.444 | 3.433 | `2178309` |
| Go | `go1.26.1` | 130.603 | 3.993 | `2178309` |
| Rust | `rustc 1.94.0` | 99.463 | 3.102 | `2178309` |
| Zig | `zig 0.15.2` | 205.666 | 2.879 | `2178309` |
| Julia | `Julia 1.12.5` | - | 152.422 | `2178309` |
| Node | `Node v25.8.1` | - | 74.550 | `2178309` |
| Bun | `Bun 1.3.9` | - | 13.110 | `2178309` |
| Python | `Python 3.14.3` | - | 23.241 | `2178309` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| **Pluto (baseline)** | `pluto dev` | **94.995** | **15.964** | `16.695311` |
| C | `Apple clang 17.0.0` | 61.426 | 15.278 | `16.695311` |
| C++ | `Apple clang 17.0.0` | 310.583 | 15.897 | `16.695311` |
| Swift | `Swift 6.2.4` | 297.806 | 19.086 | `16.695311` |
| Go | `go1.26.1` | 119.216 | 17.225 | `16.695311` |
| Rust | `rustc 1.94.0` | 103.064 | 17.531 | `16.695311` |
| Zig | `zig 0.15.2` | 383.632 | 18.156 | `16.695311` |
| Julia | `Julia 1.12.5` | - | 260.223 | `16.695311` |
| Node | `Node v25.8.1` | - | 77.018 | `16.695311` |
| Bun | `Bun 1.3.9` | - | 23.457 | `16.695311` |
| Python | `Python 3.14.3` | - | 776.498 | `16.695311` |

## Benchmarks

- `sum`
  Integer reduction benchmark.
  Sums the natural numbers from `1` to `20,000,000`.
  Expected output: `200000010000000`

- `fib`
  Naive recursive Fibonacci benchmark.
  Computes `fib(32)` with tree recursion to expose recursion, branching, and function-call cost.
  Expected output: `2178309`

- `fib_tail`
  Tail-recursive Fibonacci benchmark.
  Computes `fib(32)` using the helper/accumulator style from Pluto's own test suite.
  Expected output: `2178309`

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
