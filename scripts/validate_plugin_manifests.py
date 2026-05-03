#!/usr/bin/env python3
"""Validate Claude and Codex plugin manifests stay in sync."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_MANIFEST = REPO_ROOT / ".claude-plugin" / "plugin.json"
CODEX_MANIFEST = REPO_ROOT / ".codex-plugin" / "plugin.json"
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def read_plugin_name() -> str | None:
    makefile = REPO_ROOT / "Makefile"
    if not makefile.exists():
        return None
    for line in makefile.read_text(encoding="utf-8").splitlines():
        if line.startswith("PLUGIN_NAME"):
            _, _, value = line.partition(":=")
            return value.strip()
    return None


def fail(message: str) -> int:
    print(f"FAIL: {message}")
    return 1


def main() -> int:
    if not CLAUDE_MANIFEST.exists():
        return fail(f"missing {CLAUDE_MANIFEST.relative_to(REPO_ROOT)}")
    if not CODEX_MANIFEST.exists():
        return fail(f"missing {CODEX_MANIFEST.relative_to(REPO_ROOT)}")

    claude = load_json(CLAUDE_MANIFEST)
    codex = load_json(CODEX_MANIFEST)
    expected_name = read_plugin_name()

    if expected_name and codex.get("name") != expected_name:
        return fail(f".codex-plugin/plugin.json name must be {expected_name!r}")
    if not isinstance(codex.get("name"), str) or not KEBAB_RE.match(codex["name"]):
        return fail(".codex-plugin/plugin.json name must be kebab-case")
    if codex.get("version") != claude.get("version"):
        return fail("Codex plugin version must match Claude plugin version")
    if codex.get("description") != claude.get("description"):
        return fail("Codex plugin description must match Claude plugin description")
    if codex.get("author") != claude.get("author"):
        return fail("Codex plugin author must match Claude plugin author")

    skills_path = codex.get("skills")
    if not isinstance(skills_path, str) or not skills_path.startswith("./"):
        return fail("Codex plugin skills path must start with ./")
    if not (REPO_ROOT / skills_path[2:]).is_dir():
        return fail(f"Codex plugin skills path does not exist: {skills_path}")

    interface = codex.get("interface")
    if not isinstance(interface, dict):
        return fail("Codex plugin manifest must include interface metadata")
    for field in ["displayName", "shortDescription", "longDescription", "developerName", "category"]:
        if not isinstance(interface.get(field), str) or not interface[field].strip():
            return fail(f"Codex plugin interface.{field} is required")

    print("OK: plugin manifests are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
