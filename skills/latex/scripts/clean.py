#!/usr/bin/env python3
"""Remove common LaTeX intermediate files for one document stem."""

from __future__ import annotations

import argparse
from pathlib import Path

INTERMEDIATE_SUFFIXES = [
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".log",
    ".out",
    ".run.xml",
    ".synctex.gz",
    ".toc",
]


def collect_cleanup_targets(input_path: str, outdir: str | None = None) -> list[Path]:
    """Return intermediate files that would be removed for the given source."""
    source = Path(input_path)
    base = source.stem
    directory = Path(outdir) if outdir else source.parent
    return [directory / f"{base}{suffix}" for suffix in INTERMEDIATE_SUFFIXES]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for the cleanup wrapper."""
    parser = argparse.ArgumentParser(description="Clean common LaTeX intermediates for one source file.")
    parser.add_argument("input", help="Path to the .tex file")
    parser.add_argument("--outdir", help="Directory that contains generated files")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    """Delete known intermediate files if they exist."""
    args = parse_args(argv)
    for path in collect_cleanup_targets(args.input, args.outdir):
        if path.exists():
            path.unlink()
    return 0


def main() -> None:
    """CLI entry point."""
    raise SystemExit(run())


if __name__ == "__main__":
    main()
