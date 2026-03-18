#!/usr/bin/env python3
"""Render GitLab-targeted Markdown for preview or export."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

CMARK_DOCS = "https://github.github.com/gfm/"
PANDOC_DOCS = "https://pandoc.org/getting-started.html"
GITLAB_DOCS = "https://docs.gitlab.com/user/markdown/"


def find_tool(name: str, env_var: str) -> str | None:
    override = os.environ.get(env_var)
    if override and Path(override).exists():
        return override
    return shutil.which(name)


def choose_renderer(target_format: str) -> str:
    if target_format == "html":
        cmark = find_tool("cmark-gfm", "CMARK_GFM_PATH")
        if cmark:
            return cmark
    pandoc = find_tool("pandoc", "PANDOC_PATH")
    if pandoc:
        return pandoc
    raise FileNotFoundError(
        "No suitable renderer found. Install Pandoc for export workflows "
        f"({PANDOC_DOCS}); cmark-gfm can assist with structural HTML previews ({CMARK_DOCS}). "
        f"Review GitLab behavior at {GITLAB_DOCS}."
    )


def build_command(renderer: str, input_path: str, target_format: str, output_path: str | None = None, toc: bool = False) -> list[str]:
    tool_name = Path(renderer).name.lower()
    if "cmark-gfm" in tool_name:
        return [renderer, input_path]
    cmd = [renderer, input_path, "--from", "gfm", "--to", target_format]
    if output_path:
        cmd.extend(["--output", output_path])
    if toc:
        cmd.append("--toc")
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render GitLab-targeted Markdown.")
    parser.add_argument("input", help="Path to the .md file")
    parser.add_argument("--to", choices=["html", "pdf", "docx"], required=True, dest="target_format")
    parser.add_argument("--output", help="Output path")
    parser.add_argument("--toc", action="store_true", help="Include a table of contents where supported")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    renderer = choose_renderer(args.target_format)
    cmd = build_command(renderer=renderer, input_path=args.input, target_format=args.target_format, output_path=args.output, toc=args.toc)
    if Path(renderer).name.lower().startswith("cmark-gfm"):
        if args.output:
            with open(args.output, "w", encoding="utf-8") as handle:
                completed = subprocess.run(cmd, stdout=handle)
                return completed.returncode
        return subprocess.run(cmd).returncode
    return subprocess.run(cmd).returncode


def main() -> None:
    try:
        raise SystemExit(run())
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
