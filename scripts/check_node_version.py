#!/usr/bin/env python3
"""Require a modern Node.js runtime for markdownlint-cli2."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys

VERSION_RE = re.compile(r'^v?(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')


def parse_version(raw: str) -> tuple[int, int, int] | None:
    match = VERSION_RE.match(raw.strip())
    if not match:
        return None
    return tuple(int(match.group(name)) for name in ('major', 'minor', 'patch'))


def run(min_major: int) -> int:
    try:
        completed = subprocess.run(['node', '--version'], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        print('Node.js not found. Install Node.js 20 or newer so markdownlint-cli2 can run.', file=sys.stderr)
        return 1
    except subprocess.CalledProcessError as exc:
        output = exc.stderr.strip() or exc.stdout.strip() or 'unknown error'
        print(f'Unable to determine Node.js version: {output}', file=sys.stderr)
        return 1

    version = parse_version(completed.stdout)
    if version is None:
        print(f'Could not parse Node.js version from: {completed.stdout.strip()}', file=sys.stderr)
        return 1
    if version[0] < min_major:
        print(
            f'Node.js {completed.stdout.strip()} is too old for markdownlint-cli2 in this repo. '
            f'Install Node.js {min_major}+ and rerun make test.',
            file=sys.stderr,
        )
        return 1
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Check the minimum supported Node.js version.')
    parser.add_argument('--min-major', type=int, default=20, help='Minimum supported Node.js major version')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    return run(args.min_major)


if __name__ == '__main__':
    raise SystemExit(main())
