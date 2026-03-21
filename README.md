# Pluto Bench

Cross-language benchmarks for Pluto, C, C++, Go, Rust, Zig, and Python.

This repo is separate from the main Pluto compiler repo. It keeps a small set
of equivalent benchmark programs and a single harness that compiles and runs
them in each language, checks output parity, and reports timings.

## Latest Results

Tested on `2026-03-21 09:48:34 IST` with:

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.3.1 (25D2128)
- Command: `python3 scripts/benchmark.py sum fib harmonic --repeat 3`
- Benchmark mode: median of 3 samples, with one warm-up execution before each timed run

### Sum

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 100.238 | 2.905 | `200000010000000` |
| C | `Apple clang 17.0.0` | 68.706 | 2.751 | `200000010000000` |
| C++ | `Apple clang 17.0.0` | 351.578 | 3.153 | `200000010000000` |
| Go | `go1.26.1` | 131.640 | 12.332 | `200000010000000` |
| Rust | `rustc 1.94.0` | 118.006 | 18.494 | `200000010000000` |
| Zig | `zig 0.15.2` | 209.010 | 2.699 | `200000010000000` |
| Python | `Python 3.14.3` | - | 1284.106 | `200000010000000` |

### Fib

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 96.137 | 30.828 | `2178309` |
| C | `Apple clang 17.0.0` | 69.066 | 11.356 | `2178309` |
| C++ | `Apple clang 17.0.0` | 341.197 | 11.272 | `2178309` |
| Go | `go1.26.1` | 126.682 | 15.599 | `2178309` |
| Rust | `rustc 1.94.0` | 107.823 | 12.119 | `2178309` |
| Zig | `zig 0.15.2` | 207.098 | 12.843 | `2178309` |
| Python | `Python 3.14.3` | - | 313.633 | `2178309` |

### Harmonic

| Language | Version | Compile ms | Run ms | Output |
|---|---|---:|---:|---|
| Pluto | `pluto dev` | 103.731 | 15.957 | `16.695311` |
| C | `Apple clang 17.0.0` | 67.253 | 14.501 | `16.695311` |
| C++ | `Apple clang 17.0.0` | 345.384 | 15.563 | `16.695311` |
| Go | `go1.26.1` | 126.631 | 18.443 | `16.695311` |
| Rust | `rustc 1.94.0` | 108.609 | 15.438 | `16.695311` |
| Zig | `zig 0.15.2` | 397.805 | 18.831 | `16.695311` |
| Python | `Python 3.14.3` | - | 792.908 | `16.695311` |

## Benchmarks

- `sum`
  Integer reduction benchmark.
  Sums the natural numbers from `1` to `20,000,000`.
  Expected output: `200000010000000`

- `fib`
  Recursive Fibonacci benchmark.
  Computes `fib(32)` to expose recursion, branching, and function-call cost.
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
python3 scripts/benchmark.py harmonic
```

Run the full suite:

```sh
python3 scripts/benchmark.py sum fib harmonic
```

Override the Pluto binary:

```sh
python3 scripts/benchmark.py --pluto /path/to/pluto sum fib harmonic
```

or:

```sh
PLUTO_BIN=/path/to/pluto python3 scripts/benchmark.py sum fib harmonic
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
