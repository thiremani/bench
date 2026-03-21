# Pluto Bench

Small cross-language benchmarks for Pluto, C, C++, and Python.

This repo is separate from the main Pluto compiler repo. Its job is to keep a
small, reproducible benchmark suite that can be run against a local Pluto
binary and compared with equivalent C, C++, and Python programs.

The main script, `benchmark.py`, compiles and runs matching programs across the
languages, checks that they produce the same output, and reports timing results.

## What This Repo Does

- keeps benchmark cases in equivalent Pluto, C, C++, and Python forms
- measures native compile time for Pluto, C, and C++
- measures execution time for all languages
- treats Python as interpreted execution only, not as a native compile target
- checks output parity so timing comparisons are not based on different work

## Benchmarks

- `sum.*`
  Sums the natural numbers from `1` to `20,000,000`.
  This is a simple integer-reduction benchmark.
  Expected output: `200000010000000`

- `fib.*`
  Computes recursive Fibonacci at `fib(32)`.
  This is a branch-heavy recursive benchmark and is useful for comparing
  function-call and recursion cost.
  Expected output: `2178309`

- `t.*`
  Computes a harmonic sum using floating-point arithmetic.
  This is the current floating-point throughput benchmark.
  Expected output: `16.695311`

## Repo Layout

- `sum.*`, `fib.*`, `t.*`
  Matching benchmark programs across Pluto, C, C++, and Python
- `fib.pt`
  Pluto template definitions needed by the recursive Fibonacci benchmark
- `benchmark.py`
  Benchmark harness that builds, runs, times, and validates outputs
- `pt.mod`
  Pluto module file for the benchmark repo

## Notes on measurement

- Pluto, C, and C++ report native compile time and execution time separately.
- Python is reported as interpreted execution only. Its compile column is shown as `-` because `py_compile` bytecode generation is not comparable to native compilation.
- The benchmark uses repeated runs and reports the median.
- The harness performs a warm-up execution before timing each run.
- `sum`, `fib`, and `t` are the benchmark cases currently included.
- Very small programs are intentionally avoided as performance benchmarks because process startup noise dominates them.

## How The Harness Works

For each selected case:

1. `benchmark.py` creates an isolated temp work directory.
2. It copies the source file for the selected language into that directory.
3. For Pluto cases, it also copies any companion `.pt` file for that benchmark.
4. It measures compile time where that concept makes sense.
5. It runs the program once as a warm-up and then times the next execution.
6. It repeats that process and reports the median timing.
7. It verifies that all languages print the same output.

## Pluto compiler path

By default the script looks for Pluto at `../pluto/pluto`, which matches:

```text
/Users/tejas/Downloads/bench
/Users/tejas/Downloads/pluto/pluto
```

You can override that with either:

```sh
python3 benchmark.py --pluto /path/to/pluto sum fib t
```

or:

```sh
PLUTO_BIN=/path/to/pluto python3 benchmark.py sum fib t
```

## Usage

```sh
python3 benchmark.py sum
python3 benchmark.py fib
python3 benchmark.py t
python3 benchmark.py sum fib t --repeat 5
```

The script prints compile time and execution time separately where that makes sense, and checks that outputs match.
