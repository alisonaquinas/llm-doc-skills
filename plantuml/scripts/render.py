#!/usr/bin/env python3
"""Render PlantUML diagrams with a native executable or Java plus JAR."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

PLANTUML_DOCS = "https://plantuml.com/"
JAVA_DOCS = "https://plantuml.com/starting"


def find_plantuml_command() -> list[str]:
    override = os.environ.get("PLANTUML_PATH")
    if override and Path(override).exists():
        return [override]
    native = shutil.which("plantuml")
    if native:
        return [native]
    jar_path = os.environ.get("PLANTUML_JAR_PATH")
    java = shutil.which("java")
    if jar_path and Path(jar_path).exists() and java:
        return [java, "-jar", jar_path]
    raise FileNotFoundError(
        "PlantUML not found. Install PlantUML or provide PLANTUML_JAR_PATH with Java available. "
        f"Review {PLANTUML_DOCS} and {JAVA_DOCS}."
    )


def build_command(plantuml_cmd: list[str], input_path: str, target_format: str, output_dir: str | None = None, theme: str | None = None, config_file: str | None = None) -> list[str]:
    cmd = list(plantuml_cmd)
    cmd.append(f"-t{target_format}")
    if output_dir:
        cmd.extend(["-o", output_dir])
    if config_file:
        cmd.extend(["-config", config_file])
    if theme:
        cmd.extend(["-theme", theme])
    cmd.append(input_path)
    return cmd


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render PlantUML diagrams.")
    parser.add_argument("input", help="Path to the .puml or .plantuml file")
    parser.add_argument("--to", choices=["svg", "png", "pdf", "txt"], required=True, dest="target_format")
    parser.add_argument("--output", dest="output_dir", help="Output directory")
    parser.add_argument("--theme", help="PlantUML theme name")
    parser.add_argument("--config", dest="config_file", help="Path to a PlantUML config file")
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    plantuml_cmd = find_plantuml_command()
    cmd = build_command(plantuml_cmd=plantuml_cmd, input_path=args.input, target_format=args.target_format, output_dir=args.output_dir, theme=args.theme, config_file=args.config_file)
    return subprocess.run(cmd).returncode


def main() -> None:
    try:
        raise SystemExit(run())
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
