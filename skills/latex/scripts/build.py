#!/usr/bin/env python3
"""LaTeX build wrapper that uses latexmk as the primary orchestrator."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

OFFICIAL_DOCS = "https://www.learnlatex.org/en/"
ENGINE_FLAGS = {
    "pdflatex": "-pdf",
    "xelatex": "-xelatex",
    "lualatex": "-lualatex",
}


def find_latexmk() -> str:
    """Return the latexmk executable path or raise with an install hint."""
    override = os.environ.get("LATEXMK_PATH")
    if override and Path(override).exists():
        return override

    path = shutil.which("latexmk")
    if path:
        return path

    raise FileNotFoundError(
        "latexmk not found. Install a TeX distribution with latexmk and review "
        f"{OFFICIAL_DOCS}"
    )


def build_command(
    latexmk: str,
    input_path: str,
    engine: str = "pdflatex",
    bib_tool: str = "biber",
    outdir: str | None = None,
    clean_intermediates: bool = False,
) -> list[str]:
    """Build a latexmk command for a stable compile loop."""
    cmd = [latexmk, ENGINE_FLAGS[engine], "-interaction=nonstopmode", "-file-line-error"]
    if bib_tool == "bibtex":
        cmd.append("-bibtex")
    if outdir:
        cmd.append(f"-outdir={outdir}")
    if clean_intermediates:
        cmd.append("-c")
    cmd.append(input_path)
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI options for the LaTeX build wrapper."""
    parser = argparse.ArgumentParser(description="Build a LaTeX document with latexmk.")
    parser.add_argument("input", help="Path to the .tex file")
    parser.add_argument("--engine", choices=sorted(ENGINE_FLAGS), default="pdflatex")
    parser.add_argument("--bib-tool", choices=["bibtex", "biber"], default="biber")
    parser.add_argument("--outdir", help="Output directory for generated files")
    parser.add_argument("--clean-intermediates", action="store_true", help="Clean intermediates after the build pass")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    """Resolve latexmk, build the command, and execute it."""
    args = parse_args(argv)
    latexmk = find_latexmk()
    cmd = build_command(
        latexmk=latexmk,
        input_path=args.input,
        engine=args.engine,
        bib_tool=args.bib_tool,
        outdir=args.outdir,
        clean_intermediates=args.clean_intermediates,
    )
    return subprocess.run(cmd).returncode


def main() -> None:
    """CLI entry point."""
    try:
        raise SystemExit(run())
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
