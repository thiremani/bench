#!/usr/bin/env python3
"""Guard the public benchmark snapshots.

results/*/results.json is committed to a public repo, and CI publishes a job
summary built from a fresh one. Neither may carry the absolute paths of the
machine that produced it -- toolchain locations, the memory collector, or the
full $PATH.

    python3 scripts/test_snapshot.py                 # check tracked snapshots
    python3 scripts/test_snapshot.py path/to.json    # check specific ones
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import benchmark  # noqa: E402
from render_summary import render as render_summary  # noqa: E402
from benchmark import (  # noqa: E402
    Result,
    Toolchain,
    assert_no_local_paths,
    looks_like_absolute_path,
    scrub_local_paths,
    write_snapshot,
)

REPO_ROOT = Path(__file__).resolve().parent.parent

DIRTY_METADATA = {
    "pluto": {"version": "pluto dev", "bin": "/Users/someone/pluto/pluto"},
    "memory_measurement": {"enabled": True, "collector": "/usr/bin/time"},
    "target_policy": {"pluto": {"env": {"PATH": "/usr/local/bin:/usr/bin"}}},
}


def test_scrub_removes_paths() -> None:
    dirty = {
        "pluto_bin": "/Users/someone/pluto/pluto",
        "generated_at": "2026-07-23T14:59:58.162417+05:30",
        "metadata": DIRTY_METADATA,
        "cases": [{"name": "sum", "results": [{"language": "c", "bin": "/usr/bin/cc"}]}],
    }
    clean = scrub_local_paths(dirty)
    assert_no_local_paths(clean)
    assert clean["generated_at"] == dirty["generated_at"], "scrub dropped real data"
    assert clean["metadata"]["pluto"]["version"] == "pluto dev", "scrub dropped versions"
    assert clean["cases"][0]["name"] == "sum", "scrub dropped case data"
    print("ok: scrub_local_paths removes paths and keeps everything else")


def test_assert_catches_leaks() -> None:
    for leak in (
        {"metadata": {"pluto": {"bin": "/Users/someone/pluto"}}},
        {"version": "clang installed at /Users/someone/toolchain/bin/clang"},
        {"version": "clang --sysroot=/opt/sdk"},
        {"flags": "-I/usr/include -L/opt/toolchain/lib"},
        {"source": "file:///Users/someone/toolchain/manifest.json"},
        {"metadata": {"pluto": {"bin": "C:\\Users\\someone\\pluto.exe"}}},
        {"version": "compiler=C:\\Users\\someone\\pluto.exe"},
        {"flags": r"-IC:\Users\someone\sdk -LC:\toolchain\lib"},
        {"metadata": {"pluto": {"bin": "\\\\fileserver\\share\\pluto.exe"}}},
        {"version": "compiler at \\\\fileserver\\share\\pluto.exe"},
        {"flags": r"-I\\fileserver\share\sdk"},
    ):
        try:
            assert_no_local_paths(leak)
        except AssertionError:
            continue
        raise AssertionError(f"assert_no_local_paths missed a leak: {leak}")
    for benign in (
        "pluto dev",
        "go1.26.5",
        "in-process LLVM 22.1.8",
        "arm64",
        "x86_64-linux/gnu",
        "ratio 1/2",
        "LLVM 22.1.8 / API 3",
        "https://example.com/releases/22.1.8/toolchain.tar.xz",
        "source https://github.com/llvm/llvm-project.git at llvmorg-22.1.8",
    ):
        assert not looks_like_absolute_path(benign), f"false positive on {benign!r}"
    print("ok: assert_no_local_paths catches standalone and embedded local paths")


def test_write_snapshot_scrubs() -> None:
    """The integration point: whatever metadata the harness collects, the
    results.json write_snapshot produces must be clean."""
    original = benchmark.snapshot_metadata
    benchmark.snapshot_metadata = lambda toolchain, warmup_runs: dict(DIRTY_METADATA)
    try:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            write_snapshot(
                out,
                cases=["sum"],
                results_by_case={
                    "sum": [
                        Result(
                            case="sum",
                            language="pluto",
                            version="pluto dev",
                            compile_ms=1.0,
                            run_ms=2.0,
                            peak_memory_kb=1024,
                            output="42",
                        )
                    ]
                },
                repeat=1,
                warmup_runs=1,
                toolchain=Toolchain(
                    pluto=Path("/Users/someone/pluto/pluto"),
                    zig=Path("/usr/local/bin/zig"),
                    cc=Path("/usr/bin/cc"),
                    cxx=Path("/usr/bin/c++"),
                    luajit=Path("/usr/local/bin/luajit"),
                ),
            )
            written = json.loads((out / "results.json").read_text(encoding="utf-8"))
            assert_no_local_paths(written)
            assert written["cases"][0]["results"][0]["run_ms"] == 2.0, "lost results"
    finally:
        benchmark.snapshot_metadata = original
    print("ok: write_snapshot writes a scrubbed results.json")


def committed_snapshots() -> list[Path]:
    """Only git-tracked snapshots matter by default -- those go public.

    An untracked local run may legitimately contain the paths of the machine
    that produced it; failing on those would just train people to skip the test.
    CI passes the freshly generated snapshot explicitly instead.
    """
    listed = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "results/*/results.json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / line for line in listed.stdout.split() if line]


def test_snapshots_are_clean(paths: list[Path]) -> None:
    assert paths, "no snapshots to check"
    for path in paths:
        assert_no_local_paths(json.loads(path.read_text(encoding="utf-8")))
        rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
        print(f"ok: {rel} carries no local paths")


def test_summary_renderer(paths: list[Path]) -> None:
    """Keep the public summary coupled to the sanitized snapshot schema."""
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        out = io.StringIO()
        render_summary(data, out)
        rendered = out.getvalue()
        assert rendered.startswith("## Linux benchmark snapshot\n")
        assert f"- Platform: `{data['platform']}`" in rendered
        assert_no_local_paths(rendered, "/job-summary")
        rel = path.relative_to(REPO_ROOT) if path.is_absolute() else path
        print(f"ok: {rel} renders with the sanitized snapshot schema")


if __name__ == "__main__":
    explicit = [Path(arg) for arg in sys.argv[1:]]
    snapshots = explicit or committed_snapshots()
    test_scrub_removes_paths()
    test_assert_catches_leaks()
    test_write_snapshot_scrubs()
    test_snapshots_are_clean(snapshots)
    test_summary_renderer(snapshots)
    print("all snapshot checks passed")
