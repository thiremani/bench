#!/usr/bin/env python3

import importlib.util
import pathlib
import sys
import traceback


def load_module(path: pathlib.Path):
    spec = importlib.util.spec_from_file_location("bench_module", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if len(sys.argv) != 2:
        print("ERR expected source path", flush=True)
        return 1

    source_path = pathlib.Path(sys.argv[1]).resolve()
    try:
        module = load_module(source_path)
        bench_output = getattr(module, "bench_output")
    except Exception:
        print(f"ERR {traceback.format_exc().strip().splitlines()[-1]}", flush=True)
        return 1

    for raw in sys.stdin:
        cmd = raw.strip()
        if cmd == "run":
            try:
                print(f"OK {bench_output()}", flush=True)
            except Exception:
                print(f"ERR {traceback.format_exc().strip().splitlines()[-1]}", flush=True)
                return 1
        elif cmd == "exit":
            return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
