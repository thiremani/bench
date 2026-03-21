# Pluto Bench

Small cross-language benchmarks for Pluto, C, C++, and Python.

## Files

- `hello.*`: minimal smoke test that should compile and print `Hello world`
- `t.*`: harmonic-sum floating-point workload for comparing execution time
- `benchmark.py`: times compile and run phases separately and checks output parity

## Notes on measurement

- Pluto, C, and C++ report native compile time and execution time separately.
- Python is reported as interpreted execution only. Its compile column is shown as `-` because `py_compile` bytecode generation is not comparable to native compilation.
- The benchmark uses repeated runs and reports the median.
- `hello` is mainly a smoke test. Its run time is dominated by process startup, so use `t` for runtime comparisons.

## Pluto compiler path

By default the script looks for Pluto at `../pluto/pluto`, which matches:

```text
/Users/tejas/Downloads/bench
/Users/tejas/Downloads/pluto/pluto
```

You can override that with either:

```sh
python3 benchmark.py --pluto /path/to/pluto hello t
```

or:

```sh
PLUTO_BIN=/path/to/pluto python3 benchmark.py hello t
```

## Usage

```sh
python3 benchmark.py hello
python3 benchmark.py t
python3 benchmark.py hello t --repeat 5
```

The script prints compile time and execution time separately where that makes sense, and checks that outputs match.
