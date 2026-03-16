#!/usr/bin/env python3
"""Thin Pandoc wrapper for common conversion workflows.

This module keeps command construction deterministic and easy to unit test while
leaving actual conversion to the official Pandoc CLI.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

OFFICIAL_DOCS = "https://pandoc.org/getting-started.html"


def find_pandoc() -> str:
    """Return the Pandoc executable path or raise with an install hint."""
    override = os.environ.get("PANDOC_PATH")
    if override and Path(override).exists():
        return override

    path = shutil.which("pandoc")
    if path:
        return path

    raise FileNotFoundError(
        "Pandoc not found. Install the official CLI and review "
        f"{OFFICIAL_DOCS}"
    )


def build_command(
    pandoc: str,
    input_path: str,
    to_format: str,
    output_path: str | None = None,
    from_format: str | None = None,
    standalone: bool = False,
    toc: bool = False,
    citeproc: bool = False,
    pdf_engine: str | None = None,
    metadata: list[str] | None = None,
) -> list[str]:
    """Build a Pandoc command for a stable subset of common options."""
    cmd = [pandoc, input_path, "--to", to_format]
    if from_format:
        cmd.extend(["--from", from_format])
    if output_path:
        cmd.extend(["--output", output_path])
    if standalone:
        cmd.append("--standalone")
    if toc:
        cmd.append("--toc")
    if citeproc:
        cmd.append("--citeproc")
    if pdf_engine:
        cmd.extend(["--pdf-engine", pdf_engine])
    for item in metadata or []:
        cmd.extend(["--metadata", item])
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the conversion wrapper."""
    parser = argparse.ArgumentParser(description="Run Pandoc with common document-conversion flags.")
    parser.add_argument("input", help="Path to the source document")
    parser.add_argument("--to", required=True, dest="to_format", help="Target format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--from", dest="from_format", help="Explicit input format")
    parser.add_argument("--standalone", action="store_true", help="Emit a standalone document")
    parser.add_argument("--toc", action="store_true", help="Include a table of contents")
    parser.add_argument("--citeproc", action="store_true", help="Run citeproc during conversion")
    parser.add_argument("--pdf-engine", help="PDF engine to use for PDF output")
    parser.add_argument(
        "--metadata",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Repeatable metadata field",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    """Resolve the tool, build the command, and run the conversion."""
    args = parse_args(argv)
    pandoc = find_pandoc()
    cmd = build_command(
        pandoc=pandoc,
        input_path=args.input,
        to_format=args.to_format,
        output_path=args.output,
        from_format=args.from_format,
        standalone=args.standalone,
        toc=args.toc,
        citeproc=args.citeproc,
        pdf_engine=args.pdf_engine,
        metadata=args.metadata,
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
