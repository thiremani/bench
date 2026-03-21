# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Go, Rust, Zig, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-03-21 10:48:45 IST` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.3.1 (25D2128)
- Command: `python3 scripts/benchmark.py sum fib fib_tail harmonic --repeat 3`
- Benchmark mode: median of 3 samples, with one warm-up execution before each timed run

### Sum

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 92.434 | 2.844 | `200000010000000` |
| C | `Apple clang 17.0.0` | 61.984 | 2.405 | `200000010000000` |
| C++ | `Apple clang 17.0.0` | 350.879 | 2.951 | `200000010000000` |
| Go | `go1.26.1` | 130.921 | 11.278 | `200000010000000` |
| Rust | `rustc 1.94.0` | 108.398 | 16.734 | `200000010000000` |
| Zig | `zig 0.15.2` | 216.619 | 2.878 | `200000010000000` |
| Python | `Python 3.14.3` | - | 1402.363 | `200000010000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 97.323 | 30.349 | `2178309` |
| C | `Apple clang 17.0.0` | 65.963 | 11.137 | `2178309` |
| C++ | `Apple clang 17.0.0` | 380.943 | 12.631 | `2178309` |
| Go | `go1.26.1` | 119.198 | 14.427 | `2178309` |
| Rust | `rustc 1.94.0` | 96.002 | 13.359 | `2178309` |
| Zig | `zig 0.15.2` | 257.850 | 10.866 | `2178309` |
| Python | `Python 3.14.3` | - | 311.287 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 102.379 | 2.309 | `2178309` |
| C | `Apple clang 17.0.0` | 63.117 | 2.561 | `2178309` |
| C++ | `Apple clang 17.0.0` | 299.517 | 2.249 | `2178309` |
| Go | `go1.26.1` | 116.772 | 3.475 | `2178309` |
| Rust | `rustc 1.94.0` | 95.773 | 2.511 | `2178309` |
| Zig | `zig 0.15.2` | 200.101 | 3.037 | `2178309` |
| Python | `Python 3.14.3` | - | 20.506 | `2178309` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 86.463 | 15.698 | `16.695311` |
| C | `Apple clang 17.0.0` | 61.034 | 14.911 | `16.695311` |
| C++ | `Apple clang 17.0.0` | 336.066 | 13.379 | `16.695311` |
| Go | `go1.26.1` | 127.401 | 17.205 | `16.695311` |
| Rust | `rustc 1.94.0` | 107.859 | 16.874 | `16.695311` |
| Zig | `zig 0.15.2` | 408.873 | 17.507 | `16.695311` |
| Python | `Python 3.14.3` | - | 771.609 | `16.695311` |

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

By default the harness looks for Pluto at `../pluto/pluto`, which matches:

```text
/Users/tejas/Downloads/bench
/Users/tejas/Downloads/pluto/pluto
```

Run a single benchmark:

```sh
python3 scripts/benchmark.py sum
python3 scripts/benchmark.py fib
python3 scripts/benchmark.py fib_tail
python3 scripts/benchmark.py harmonic
```

Run the full suite:

```sh
python3 scripts/benchmark.py sum fib fib_tail harmonic
```

Override the Pluto binary:

```sh
python3 scripts/benchmark.py --pluto /path/to/pluto sum fib fib_tail harmonic
```

or:

```sh
PLUTO_BIN=/path/to/pluto python3 scripts/benchmark.py sum fib fib_tail harmonic
```

## Measurement Notes

- Pluto, C, C++, Go, Rust, and Zig report native compile time and execution time separately.
- Python is reported as interpreted execution only, so its compile column is `-`.
- Pluto currently uses its own LLVM pipeline with `opt -O3`.
- C and C++ are built with `-O3` for consistency with the native comparison.
- Rust is built with `rustc -C opt-level=3`.
- Zig is built with `zig build-exe -O ReleaseFast`.
- Go uses the default optimized `go build` pipeline.
- The harness creates an isolated temp work directory for each sample.
- It copies the benchmark files into that directory, including Pluto support `.pt` files when present.
- It performs one warm-up execution before each timed run.
- Output is checked against `expected.txt` for the benchmark.
