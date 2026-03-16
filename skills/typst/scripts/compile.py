#!/usr/bin/env python3
"""Thin Typst CLI wrapper for compile and export workflows."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

OFFICIAL_DOCS = "https://typst.app/docs/reference/"


def find_typst() -> str:
    """Return the Typst executable path or raise with an install hint."""
    override = os.environ.get("TYPST_PATH")
    if override and Path(override).exists():
        return override

    path = shutil.which("typst")
    if path:
        return path

    raise FileNotFoundError(
        "Typst CLI not found. Install the official CLI and review "
        f"{OFFICIAL_DOCS}"
    )


def derive_output_path(input_path: str, output_path: str | None, target_format: str) -> str:
    """Return the requested output path or one derived from the source stem."""
    if output_path:
        return output_path
    source = Path(input_path)
    return str(source.with_suffix(f".{target_format}"))


def build_command(
    typst: str,
    input_path: str,
    target_format: str = "pdf",
    output_path: str | None = None,
    root: str | None = None,
    ppi: int | None = None,
    pages: str | None = None,
) -> list[str]:
    """Build a Typst compile command for common output formats."""
    cmd = [typst, "compile"]
    if root:
        cmd.extend(["--root", root])
    if pages:
        cmd.extend(["--pages", pages])
    if ppi is not None:
        cmd.extend(["--ppi", str(ppi)])
    cmd.extend([input_path, derive_output_path(input_path, output_path, target_format)])
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI options for Typst compilation."""
    parser = argparse.ArgumentParser(description="Compile a Typst document with the official CLI.")
    parser.add_argument("input", help="Path to the .typ file")
    parser.add_argument("--format", choices=["pdf", "png", "svg"], default="pdf")
    parser.add_argument("--output", help="Output path; defaults to the source stem with the requested suffix")
    parser.add_argument("--root", help="Project root for include and asset resolution")
    parser.add_argument("--ppi", type=int, help="Pixels per inch for raster exports")
    parser.add_argument("--pages", help="Page selection expression for multi-page export")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    """Resolve the Typst CLI, build the command, and execute it."""
    args = parse_args(argv)
    typst = find_typst()
    cmd = build_command(
        typst=typst,
        input_path=args.input,
        target_format=args.format,
        output_path=args.output,
        root=args.root,
        ppi=args.ppi,
        pages=args.pages,
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
