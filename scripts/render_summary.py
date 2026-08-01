#!/usr/bin/env python3
"""Render a benchmark snapshot as a GitHub Actions job summary.

Extracted from .github/workflows/linux-bench.yml so it can be tested against
the sanitized snapshot schema rather than only discovered in CI. Reads the
snapshot named on the command line (default results/linux-gha/results.json)
and appends markdown to $GITHUB_STEP_SUMMARY, or stdout when that is unset.

Snapshots carry no filesystem paths (see scrub_local_paths in benchmark.py),
so nothing here may depend on one.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import sys
from pathlib import Path


def render(data: dict, out) -> None:
    metadata = data.get("metadata", {})

    def compile_text(value):
        return "-" if value is None else f"{value:.3f}"

    def short_commit(value):
        return "unknown" if not value else value[:12]

    def branch_label(repo):
        if not repo:
            return "unknown"
        branch = repo.get("git_branch") or "detached"
        return f"{branch}{' dirty' if repo.get('git_dirty') else ''}"

    def memory_text(value):
        if value is None:
            return "unknown RAM"
        gib = value / (1024.0 * 1024.0)
        return f"{gib:.1f} GiB RAM"

    with contextlib.nullcontext(out):
        host = metadata.get("host", {})
        bench = metadata.get("bench", {})
        pluto = metadata.get("pluto", {})
        c_meta = metadata.get("c", {})
        cpp_meta = metadata.get("cpp", {})
        memory = metadata.get("memory_measurement", {})
        target_policy = metadata.get("target_policy", {})

        out.write("## Linux benchmark snapshot\n\n")
        out.write(f"- Platform: `{data['platform']}`\n")
        out.write(f"- Machine: `{data['machine']}`\n")
        out.write(f"- Repeat: `{data['repeat']}`\n")
        out.write(f"- Warm-up runs per sample: `{data.get('warmup_runs', metadata.get('benchmark', {}).get('warmup_runs_per_sample', 'unknown'))}`\n")
        # Snapshots carry no binary path by design; the mtime is the half
        # that is useful here and safe to publish.
        pluto_mtime = pluto.get("binary_mtime")
        if pluto_mtime:
            out.write(f"- Pluto binary modified: `{pluto_mtime}`\n\n")
        else:
            out.write("\n")

        out.write("### Provenance\n\n")
        out.write(
            f"- Bench: `{branch_label(bench)}` @ `{short_commit(bench.get('git_commit'))}`\n"
        )
        out.write(
            f"- Pluto: `{pluto.get('version', 'unknown')}`\n"
        )
        out.write(
            f"- Pluto Repo: `{branch_label(pluto)}` @ "
            f"`{short_commit(pluto.get('git_commit'))}`\n"
        )
        pluto_llvm = pluto.get("llvm", {})
        if pluto_llvm:
            llvm_mode = pluto_llvm.get("mode", "in-process")
            llvm_version = pluto_llvm.get("version", "unknown LLVM")
            llvm_source = pluto_llvm.get("source")
            llvm_bin = pluto_llvm.get("bin")
            if llvm_source and llvm_bin:
                out.write(
                    f"- Pluto LLVM: `{llvm_mode} {llvm_version}` | "
                    f"`{llvm_source} {llvm_bin}`\n"
                )
            else:
                out.write(f"- Pluto LLVM: `{llvm_mode} {llvm_version}`\n")
        linker = pluto.get("linker", {})
        if linker:
            linker_bin = linker.get("bin") or linker.get("command") or "clang"
            linker_version = linker.get("version") or "unavailable"
            out.write(f"- Pluto Linker: `{linker_bin}` | `{linker_version}`\n")
        if c_meta.get("bin"):
            out.write(
                f"- C Compiler: `{c_meta.get('bin')}` | "
                f"`{c_meta.get('version', 'unknown')}`\n"
            )
        if cpp_meta.get("bin"):
            out.write(
                f"- C++ Compiler: `{cpp_meta.get('bin')}` | "
                f"`{cpp_meta.get('version', 'unknown')}`\n"
            )
        out.write(
            f"- Host: `{host.get('cpu_name', host.get('machine', 'unknown host'))}` | "
            f"`{host.get('platform', data['platform'])}` | "
            f"`{host.get('cpu_count', '?')} cores` | "
            f"`{memory_text(host.get('total_memory_kb'))}` | "
            f"`Python {host.get('python_version', '?')}`\n"
        )
        if memory.get("enabled"):
            out.write(f"- Peak Memory: `{memory.get('collector', 'enabled')}`\n")
        else:
            out.write("- Peak Memory: unavailable on this host\n")
        if target_policy:
            out.write(
                f"- Target Policy: `{target_policy.get('mode', 'unknown')}`\n"
            )
        out.write("\n")

        for case in data["cases"]:
            out.write(f"### {case['name'].replace('_', ' ').title()}\n\n")
            out.write("| Language | Version | Compile ms | Run ms | Output |\n")
            out.write("| --- | --- | ---: | ---: | --- |\n")
            for result in case["results"]:
                out.write(
                    f"| {result['language']} | `{result['version']}` | "
                    f"{compile_text(result['compile_ms'])} | "
                    f"{result['run_ms']:.3f} | `{result['output']}` |\n"
                )
            out.write("\n")

def main(argv: list[str]) -> int:
    snapshot = Path(argv[1] if len(argv) > 1 else "results/linux-gha/results.json")
    data = json.loads(snapshot.read_text(encoding="utf-8"))
    target = os.environ.get("GITHUB_STEP_SUMMARY")
    if target:
        with Path(target).open("a", encoding="utf-8") as out:
            render(data, out)
    else:
        buffer = io.StringIO()
        render(data, buffer)
        sys.stdout.write(buffer.getvalue())
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
