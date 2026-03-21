# Pluto Bench

Small cross-language benchmarks for Pluto, C, C++, and Python.

## Files

- `hello.*`: minimal smoke test that should compile and print `Hello world`
- `t.*`: simple integer workload for comparing execution time
- `benchmark.py`: times compile and run phases separately and checks output parity

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

The script prints compile time and execution time separately for each language and also checks that outputs match.
