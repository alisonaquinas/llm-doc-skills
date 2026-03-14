#!/usr/bin/env python3
"""Render Mermaid diagrams with the Mermaid CLI."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

MERMAID_DOCS = "https://mermaid.js.org/"


def find_mermaid() -> str:
    override = os.environ.get("MERMAID_CLI_PATH")
    if override and Path(override).exists():
        return override
    tool = shutil.which("mmdc")
    if tool:
        return tool
    raise FileNotFoundError(
        "Mermaid CLI not found. Install @mermaid-js/mermaid-cli and review the official docs at "
        f"{MERMAID_DOCS}"
    )


def build_command(mermaid: str, input_path: str, target_format: str, output_path: str, theme: str | None = None, background: str | None = None, config_file: str | None = None) -> list[str]:
    cmd = [mermaid, "--input", input_path, "--output", output_path]
    if theme:
        cmd.extend(["--theme", theme])
    if background:
        cmd.extend(["--backgroundColor", background])
    if config_file:
        cmd.extend(["--configFile", config_file])
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Mermaid diagrams with the Mermaid CLI.")
    parser.add_argument("input", help="Path to the .mmd file")
    parser.add_argument("--to", choices=["svg", "png", "pdf"], required=True, dest="target_format")
    parser.add_argument("--output", required=True, help="Output path")
    parser.add_argument("--theme", help="Theme name")
    parser.add_argument("--background", help="Background color")
    parser.add_argument("--config", dest="config_file", help="Path to a Mermaid config file")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    mermaid = find_mermaid()
    cmd = build_command(mermaid=mermaid, input_path=args.input, target_format=args.target_format, output_path=args.output, theme=args.theme, background=args.background, config_file=args.config_file)
    return subprocess.run(cmd).returncode


def main() -> None:
    try:
        raise SystemExit(run())
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
