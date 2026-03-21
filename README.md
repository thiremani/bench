# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Go, Rust, Zig, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-03-21 10:54:47 IST` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.3.1 (25D2128)
- Command: `python3 scripts/benchmark.py sum fib fib_tail harmonic --repeat 10`
- Benchmark mode: median of 10 samples, with one warm-up execution before each timed run

### Sum

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 92.730 | 2.383 | `200000010000000` |
| C | `Apple clang 17.0.0` | 62.663 | 2.397 | `200000010000000` |
| C++ | `Apple clang 17.0.0` | 302.589 | 2.526 | `200000010000000` |
| Go | `go1.26.1` | 116.699 | 13.500 | `200000010000000` |
| Rust | `rustc 1.94.0` | 93.472 | 19.221 | `200000010000000` |
| Zig | `zig 0.15.2` | 193.207 | 2.998 | `200000010000000` |
| Python | `Python 3.14.3` | - | 1253.118 | `200000010000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 98.446 | 30.606 | `2178309` |
| C | `Apple clang 17.0.0` | 66.964 | 10.073 | `2178309` |
| C++ | `Apple clang 17.0.0` | 362.147 | 9.862 | `2178309` |
| Go | `go1.26.1` | 125.090 | 13.337 | `2178309` |
| Rust | `rustc 1.94.0` | 102.671 | 12.850 | `2178309` |
| Zig | `zig 0.15.2` | 207.064 | 14.191 | `2178309` |
| Python | `Python 3.14.3` | - | 306.886 | `2178309` |

### Fib Tail

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 101.958 | 2.608 | `2178309` |
| C | `Apple clang 17.0.0` | 68.100 | 2.608 | `2178309` |
| C++ | `Apple clang 17.0.0` | 322.300 | 2.497 | `2178309` |
| Go | `go1.26.1` | 127.517 | 3.251 | `2178309` |
| Rust | `rustc 1.94.0` | 100.230 | 2.915 | `2178309` |
| Zig | `zig 0.15.2` | 206.296 | 2.831 | `2178309` |
| Python | `Python 3.14.3` | - | 20.128 | `2178309` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 93.380 | 14.618 | `16.695311` |
| C | `Apple clang 17.0.0` | 61.262 | 17.262 | `16.695311` |
| C++ | `Apple clang 17.0.0` | 319.618 | 17.371 | `16.695311` |
| Go | `go1.26.1` | 124.915 | 18.034 | `16.695311` |
| Rust | `rustc 1.94.0` | 97.323 | 17.676 | `16.695311` |
| Zig | `zig 0.15.2` | 378.977 | 17.738 | `16.695311` |
| Python | `Python 3.14.3` | - | 763.578 | `16.695311` |

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
