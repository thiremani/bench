# Pluto Bench

Small cross-language benchmarks for Pluto, C, C++, and Python.

## Files

- `sum.*`: integer sum of natural numbers
- `fib.*`: recursive fibonacci
- `t.*`: harmonic-sum floating-point workload for comparing execution time
- `benchmark.py`: times compile and run phases separately and checks output parity

## Notes on measurement

- Pluto, C, and C++ report native compile time and execution time separately.
- Python is reported as interpreted execution only. Its compile column is shown as `-` because `py_compile` bytecode generation is not comparable to native compilation.
- The benchmark uses repeated runs and reports the median.
- `sum`, `fib`, and `t` are the benchmark cases currently included.

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
