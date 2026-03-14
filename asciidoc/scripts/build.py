#!/usr/bin/env python3
"""Asciidoctor wrapper for HTML, PDF, and DocBook exports."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

OFFICIAL_DOCS = "https://docs.asciidoctor.org/"


def choose_tool(target_format: str) -> str:
    """Return the appropriate Asciidoctor executable for the backend."""
    env_var = "ASCIIDOCTOR_PDF_PATH" if target_format == "pdf" else "ASCIIDOCTOR_PATH"
    override = os.environ.get(env_var)
    if override and Path(override).exists():
        return override

    tool_name = "asciidoctor-pdf" if target_format == "pdf" else "asciidoctor"
    path = shutil.which(tool_name)
    if path:
        return path

    raise FileNotFoundError(
        f"{tool_name} not found. Install Asciidoctor tooling and review {OFFICIAL_DOCS}"
    )


def build_command(
    tool: str,
    input_path: str,
    target_format: str,
    output_path: str | None = None,
    safe_mode: str = "safe",
    attributes: list[str] | None = None,
) -> list[str]:
    """Build an Asciidoctor command for common publishing backends."""
    cmd = [tool, input_path, "--safe-mode", safe_mode]
    if Path(tool).name.lower() == "asciidoctor" and target_format in {"html", "docbook"}:
        backend = "html5" if target_format == "html" else "docbook"
        cmd.extend(["--backend", backend])
    for item in attributes or []:
        cmd.extend(["--attribute", item])
    if output_path:
        cmd.extend(["--out-file", output_path])
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI options for AsciiDoc builds."""
    parser = argparse.ArgumentParser(description="Build AsciiDoc files with Asciidoctor.")
    parser.add_argument("input", help="Path to the .adoc file")
    parser.add_argument("--to", choices=["html", "pdf", "docbook"], required=True, dest="target_format")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--safe-mode", choices=["unsafe", "safe", "server", "secure"], default="safe")
    parser.add_argument(
        "--attribute",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Repeatable document attribute",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    """Resolve the tool, build the command, and execute it."""
    args = parse_args(argv)
    tool = choose_tool(args.target_format)
    cmd = build_command(
        tool=tool,
        input_path=args.input,
        target_format=args.target_format,
        output_path=args.output,
        safe_mode=args.safe_mode,
        attributes=args.attribute,
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
