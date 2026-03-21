# Pluto Bench

Small cross-language benchmarks for Pluto, C, C++, and Python.

This repo is separate from the main Pluto compiler repo. Its purpose is to keep
a small benchmark suite with equivalent implementations across languages, run
them against a local Pluto binary, and make the results easy to compare.

## What This Repo Does

- keeps each benchmark self-contained under `benchmarks/<case>/`
- compares Pluto against equivalent C, C++, and Python programs
- measures native compile time for Pluto, C, and C++
- measures execution time for all languages
- treats Python as interpreted execution only, not as a native compile target
- checks output parity against the benchmark's expected result

## Repo Layout

```text
bench/
  README.md
  pt.mod
  scripts/
    benchmark.py
  benchmarks/
    sum/
      main.spt
      main.c
      main.cpp
      main.py
      expected.txt
    fib/
      main.spt
      support.pt
      main.c
      main.cpp
      main.py
      expected.txt
    harmonic/
      main.spt
      main.c
      main.cpp
      main.py
      expected.txt
```

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

## Measurement Method

- Pluto, C, and C++ report native compile time and execution time separately.
- Python is reported as interpreted execution only, so its compile column is `-`.
- The harness creates an isolated temp work directory for each sample.
- It copies the benchmark files into that directory, including Pluto support `.pt` files when present.
- It performs one warm-up execution before each timed run.
- Results are reported as medians.
- Output is checked against `expected.txt` for the benchmark.

## Latest Results

Tested on `2026-03-21 09:31:16 IST`.

- Machine: Apple M1 Pro
- CPU cores: 10
- Memory: 16 GiB
- OS: macOS 26.3.1 (25D2128)
- Pluto commit: `1760d26`
- C/C++ compiler: `Apple clang version 17.0.0 (clang-1700.6.4.2)`
- Python: `Python 3.14.3`
- Command: `python3 scripts/benchmark.py sum fib harmonic`
- Benchmark mode: median of 5 samples, with one warm-up execution before each timed run

### Sum

| Language | Compile ms | Run ms | Output |
|---|---:|---:|---|
| Pluto | 98.363 | 3.062 | `200000010000000` |
| C | 65.188 | 2.983 | `200000010000000` |
| C++ | 378.571 | 3.220 | `200000010000000` |
| Python | - | 1310.196 | `200000010000000` |

### Fib

| Language | Compile ms | Run ms | Output |
|---|---:|---:|---|
| Pluto | 102.700 | 29.703 | `2178309` |
| C | 65.163 | 10.686 | `2178309` |
| C++ | 366.108 | 10.381 | `2178309` |
| Python | - | 314.876 | `2178309` |

### Harmonic

| Language | Compile ms | Run ms | Output |
|---|---:|---:|---|
| Pluto | 94.727 | 12.741 | `16.695311` |
| C | 65.692 | 13.662 | `16.695311` |
| C++ | 358.161 | 13.288 | `16.695311` |
| Python | - | 740.072 | `16.695311` |
