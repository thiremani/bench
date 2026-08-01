#!/usr/bin/env python3
"""Guard the public benchmark snapshots.

results/*/results.json is committed to a public repo. It must not carry the
absolute paths of whichever machine produced it -- toolchain locations, the
memory collector, or the full $PATH. Run with:

    python3 scripts/test_snapshot.py
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from benchmark import assert_no_local_paths, scrub_local_paths  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_scrub_removes_paths() -> None:
    dirty = {
        "pluto_bin": "/Users/someone/pluto/pluto",
        "generated_at": "2026-07-23T14:59:58.162417+05:30",
        "metadata": {
            "pluto": {"version": "pluto dev", "bin": "/Users/someone/pluto/pluto"},
            "memory_measurement": {"enabled": True, "collector": "/usr/bin/time"},
            "target_policy": {"pluto": {"env": {"PATH": "/usr/local/bin:/usr/bin"}}},
        },
        "cases": [{"name": "sum", "results": [{"language": "c", "bin": "/usr/bin/cc"}]}],
    }
    clean = scrub_local_paths(dirty)
    assert_no_local_paths(clean)
    assert clean["generated_at"] == dirty["generated_at"], "scrub dropped real data"
    assert clean["metadata"]["pluto"]["version"] == "pluto dev", "scrub dropped versions"
    assert clean["cases"][0]["name"] == "sum", "scrub dropped case data"
    print("ok: scrub_local_paths removes paths and keeps everything else")


def test_assert_catches_a_leak() -> None:
    try:
        assert_no_local_paths({"metadata": {"pluto": {"bin": "/Users/someone/pluto"}}})
    except AssertionError:
        print("ok: assert_no_local_paths catches a leaked path")
        return
    raise AssertionError("assert_no_local_paths did not catch a leaked path")


def committed_snapshots() -> list[Path]:
    """Only git-tracked snapshots matter — those are the ones that go public.

    An untracked local run may legitimately contain the paths of the machine
    that produced it; failing on those would just train people to skip the test.
    """
    listed = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files", "results/*/results.json"],
        capture_output=True,
        text=True,
        check=True,
    )
    return [REPO_ROOT / line for line in listed.stdout.split() if line]


def test_committed_snapshots_are_clean() -> None:
    snapshots = committed_snapshots()
    assert snapshots, "no committed snapshots found"
    for path in snapshots:
        assert_no_local_paths(json.loads(path.read_text(encoding="utf-8")))
        print(f"ok: {path.relative_to(REPO_ROOT)} carries no local paths")


if __name__ == "__main__":
    test_scrub_removes_paths()
    test_assert_catches_a_leak()
    test_committed_snapshots_are_clean()
    print("all snapshot checks passed")
