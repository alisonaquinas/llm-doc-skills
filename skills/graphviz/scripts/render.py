#!/usr/bin/env python3
"""Render Graphviz DOT diagrams with the selected layout engine."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

GRAPHVIZ_DOCS = "https://graphviz.org/documentation/"


def find_layout_tool(layout: str) -> str:
    env_var = f"GRAPHVIZ_{layout.upper()}_PATH"
    override = os.environ.get(env_var)
    if override and Path(override).exists():
        return override
    tool = shutil.which(layout)
    if tool:
        return tool
    raise FileNotFoundError(
        f"Graphviz layout tool '{layout}' not found. Install Graphviz and review {GRAPHVIZ_DOCS}"
    )


def build_command(layout_tool: str, input_path: str, target_format: str, output_path: str) -> list[str]:
    return [layout_tool, f"-T{target_format}", input_path, "-o", output_path]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Graphviz DOT diagrams.")
    parser.add_argument("input", help="Path to the .dot file")
    parser.add_argument("--to", choices=["svg", "png", "pdf"], required=True, dest="target_format")
    parser.add_argument("--output", required=True, help="Output path")
    parser.add_argument("--layout", choices=["dot", "neato", "fdp", "sfdp", "twopi", "circo"], default="dot")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    layout_tool = find_layout_tool(args.layout)
    cmd = build_command(layout_tool=layout_tool, input_path=args.input, target_format=args.target_format, output_path=args.output)
    return subprocess.run(cmd).returncode


def main() -> None:
    try:
        raise SystemExit(run())
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
