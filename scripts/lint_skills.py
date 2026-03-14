#!/usr/bin/env python3
"""Lint all skill directories in the current plugin repository.

Implements the 11 automatable rules from the skill-linting standard
(L01–L11; L12 is handled by markdownlint-cli2 separately):

  L01  SKILL.md frontmatter has exactly the fields: name, description
  L02  name value is kebab-case, ≤64 chars, and matches the folder name
  L03  Required files present: SKILL.md, agents/claude.yaml, agents/openai.yaml
  L04  Agent YAMLs have display_name, short_description, default_prompt
  L05  short_description is 25–64 characters
  L06  SKILL.md body line count: WARN ≥450, FAIL ≥500
  L07  No dangling references (all mentioned references/*.md actually exist)
  L08  All scripts/*.sh pass `bash -n` (syntax check)
  L09  No platform-specific agent names in prose
  L10  No forbidden files present (README.md, CHANGELOG.md, etc.)
  L11  No second-person language in SKILL.md

Exit codes:
  0  No FAILs (WARNs may still be present)
  1  One or more FAILs

Usage:
  python3 scripts/lint_skills.py                # all skill dirs
  python3 scripts/lint_skills.py git bash
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def skills_root() -> Path:
    candidate = REPO_ROOT / "skills"
    return candidate if candidate.exists() else REPO_ROOT

# ---------------------------------------------------------------------------
# Policy constants
# ---------------------------------------------------------------------------

REQUIRED_FILES = [
    "SKILL.md",
    "agents/claude.yaml",
    "agents/openai.yaml",
]

AGENT_REQUIRED_FIELDS = ["display_name", "short_description", "default_prompt"]

FORBIDDEN_FILES = [
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "LICENSE.md",
    ".DS_Store",
]

# Platform-specific names that must not appear in prose
PLATFORM_NAMES = [
    r"\bClaude Code\b",
    r"\bClaude\.ai\b",
    r"\bChatGPT\b",
    r"\bOpenAI\b",
    r"\bCodex\b",
    r"\bCopilot\b",
    r"\bGemini\b",
]

# Second-person patterns
SECOND_PERSON_RE = re.compile(
    r"\bYou (should|can|need|must|will|are|have|may|might|could|want)\b",
    re.IGNORECASE,
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
REFERENCES_LINK_RE = re.compile(r"`(references/[^`]+\.md)`")
KEBAB_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

LINE_WARN = 450
LINE_FAIL = 500

# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------

FAIL = "FAIL"
WARN = "WARN"
PASS = "PASS"


def _result(level: str, rule: str, message: str) -> dict:
    return {"level": level, "rule": rule, "message": message}


# ---------------------------------------------------------------------------
# Individual rule implementations
# ---------------------------------------------------------------------------

def _parse_frontmatter(skill_md: Path) -> dict[str, str] | None:
    """Return the parsed YAML frontmatter as a dict, or None if absent/malformed."""
    content = skill_md.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(content)
    if not m:
        return None
    fields: dict[str, str] = {}
    current_key: str | None = None
    for line in m.group(1).splitlines():
        if line.startswith(("  ", "\t")) and current_key:
            fields[current_key] = f"{fields[current_key]} {line.strip()}".strip()
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            current_key = key.strip()
            value = val.strip()
            if value in {">", "|"}:
                fields[current_key] = ""
            else:
                fields[current_key] = value
    return fields


def check_l01(skill_dir: Path) -> list[dict]:
    """L01: Frontmatter has exactly name + description."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []  # L03 will report this
    fm = _parse_frontmatter(skill_md)
    if fm is None:
        return [_result(FAIL, "L01", "SKILL.md has no YAML frontmatter block (--- ... ---)")]
    expected = {"name", "description"}
    extra = set(fm.keys()) - expected
    missing = expected - set(fm.keys())
    results = []
    if missing:
        results.append(_result(FAIL, "L01", f"Frontmatter missing fields: {sorted(missing)}"))
    if extra:
        results.append(_result(FAIL, "L01", f"Frontmatter has extra fields: {sorted(extra)}"))
    return results


def check_l02(skill_dir: Path) -> list[dict]:
    """L02: name is kebab-case, ≤64 chars, matches folder."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []
    fm = _parse_frontmatter(skill_md)
    if fm is None or "name" not in fm:
        return []
    name = fm["name"].strip('"').strip("'")
    results = []
    if not KEBAB_RE.match(name):
        results.append(_result(FAIL, "L02", f"name {name!r} is not kebab-case"))
    if len(name) > 64:
        results.append(_result(FAIL, "L02", f"name {name!r} exceeds 64 characters ({len(name)})"))
    if name != skill_dir.name:
        results.append(
            _result(FAIL, "L02", f"name {name!r} does not match folder {skill_dir.name!r}")
        )
    return results


def check_l03(skill_dir: Path) -> list[dict]:
    """L03: Required files are present."""
    results = []
    for rel in REQUIRED_FILES:
        if not (skill_dir / rel).exists():
            results.append(_result(FAIL, "L03", f"Missing required file: {rel}"))
    return results


def _load_agent_yaml_text(skill_dir: Path, filename: str) -> str | None:
    p = skill_dir / "agents" / filename
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_l04(skill_dir: Path) -> list[dict]:
    """L04: Both agent YAMLs have display_name, short_description, default_prompt."""
    results = []
    for yaml_file in ("claude.yaml", "openai.yaml"):
        text = _load_agent_yaml_text(skill_dir, yaml_file)
        if text is None:
            continue  # L03 reports the missing file
        for field in AGENT_REQUIRED_FIELDS:
            if field not in text:
                results.append(
                    _result(FAIL, "L04", f"agents/{yaml_file}: missing field {field!r}")
                )
    return results


def check_l05(skill_dir: Path) -> list[dict]:
    """L05: short_description is 25–64 characters."""
    results = []
    for yaml_file in ("claude.yaml", "openai.yaml"):
        text = _load_agent_yaml_text(skill_dir, yaml_file)
        if text is None:
            continue
        for line in text.splitlines():
            if "short_description" in line:
                # Extract the value
                _, _, val = line.partition(":")
                val = val.strip().strip('"').strip("'")
                length = len(val)
                if length > 64:
                    results.append(
                        _result(
                            FAIL, "L05",
                            f"agents/{yaml_file}: short_description is {length} chars (max 64): {val!r}",
                        )
                    )
                elif length < 25:
                    results.append(
                        _result(
                            WARN, "L05",
                            f"agents/{yaml_file}: short_description is only {length} chars (min 25): {val!r}",
                        )
                    )
    return results


def check_l06(skill_dir: Path) -> list[dict]:
    """L06: SKILL.md body line count < 500 (warn at 450)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    # Exclude frontmatter (lines between first two ---)
    body_lines = lines
    if lines and lines[0].strip() == "---":
        try:
            end = lines.index("---", 1)
            body_lines = lines[end + 1:]
        except ValueError:
            pass
    count = len(body_lines)
    if count >= LINE_FAIL:
        return [_result(FAIL, "L06", f"SKILL.md body is {count} lines (limit: {LINE_FAIL})")]
    if count >= LINE_WARN:
        return [_result(WARN, "L06", f"SKILL.md body is {count} lines (warn at {LINE_WARN}); consider moving details to references/")]
    return []


def check_l07(skill_dir: Path) -> list[dict]:
    """L07: No dangling references (all mentioned references/*.md exist)."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []
    content = skill_md.read_text(encoding="utf-8")
    results = []
    for match in REFERENCES_LINK_RE.finditer(content):
        ref_rel = match.group(1)
        if "*" in ref_rel:
            continue
        ref_path = skill_dir / ref_rel
        if not ref_path.exists():
            results.append(
                _result(FAIL, "L07", f"Dangling reference: {ref_rel!r} does not exist")
            )
    return results


def check_l08(skill_dir: Path) -> list[dict]:
    """L08: All scripts/*.sh pass `bash -n`."""
    results = []
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.exists():
        return []
    for sh in scripts_dir.glob("*.sh"):
        r = subprocess.run(
            ["bash", "-n", sh.name],
            capture_output=True,
            text=True,
            cwd=scripts_dir,
        )
        if r.returncode != 0:
            detail = (r.stderr or r.stdout).replace("\x00", "").strip()
            if "Bash/Service" in detail or "Access is denied" in detail:
                results.append(
                    _result(
                        WARN,
                        "L08",
                        f"scripts/{sh.name}: bash syntax check skipped because bash is unavailable in this environment",
                    )
                )
                continue
            results.append(
                _result(
                    FAIL,
                    "L08",
                    f"scripts/{sh.name}: bash syntax error: {detail}",
                )
            )
    return results


def check_l09(skill_dir: Path) -> list[dict]:
    """L09: No platform-specific agent names in prose."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []
    content = skill_md.read_text(encoding="utf-8")
    results = []
    for pattern in PLATFORM_NAMES:
        m = re.search(pattern, content)
        if m:
            results.append(
                _result(WARN, "L09", f"Platform-specific language found: {m.group()!r}")
            )
    return results


def _git_tracked(path: Path) -> bool:
    """Return True if *path* is tracked by git."""
    r = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path)],
        capture_output=True,
        cwd=REPO_ROOT,
    )
    return r.returncode == 0


def check_l10(skill_dir: Path) -> list[dict]:
    """L10: No forbidden files present (tracked by git)."""
    results = []
    for name in FORBIDDEN_FILES:
        p = skill_dir / name
        if p.exists() and _git_tracked(p):
            results.append(_result(FAIL, "L10", f"Forbidden file tracked in git: {name}"))
    return results


def check_l11(skill_dir: Path) -> list[dict]:
    """L11: No second-person language in SKILL.md."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return []
    results = []
    for i, line in enumerate(skill_md.read_text(encoding="utf-8").splitlines(), 1):
        m = SECOND_PERSON_RE.search(line)
        if m:
            results.append(
                _result(WARN, "L11", f"Line {i}: second-person language: {line.strip()!r}")
            )
    return results


ALL_CHECKS = [
    check_l01, check_l02, check_l03, check_l04, check_l05,
    check_l06, check_l07, check_l08, check_l09, check_l10, check_l11,
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def _load_lintignore(skill_dir: Path) -> set[str]:
    """Return the set of rule IDs suppressed by a .lintignore file, if present."""
    p = skill_dir / ".lintignore"
    if not p.exists():
        return set()
    suppressed: set[str] = set()
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            suppressed.add(line.upper())
    return suppressed


def lint_skill(skill_dir: Path) -> list[dict]:
    """Run all checks for *skill_dir* and return a flat list of results."""
    suppressed = _load_lintignore(skill_dir)
    results = []
    for check in ALL_CHECKS:
        for item in check(skill_dir):
            if item["rule"] in suppressed:
                continue
            results.append(item)
    return results


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    args = argv if argv is not None else sys.argv[1:]

    if args:
        root = skills_root()
        skill_dirs = [root / a for a in args]
    else:
        root = skills_root()
        skill_dirs = sorted(p.parent for p in root.glob("*/SKILL.md"))

    total_fails = 0
    total_warns = 0

    for skill_dir in skill_dirs:
        results = lint_skill(skill_dir)
        fails = [r for r in results if r["level"] == FAIL]
        warns = [r for r in results if r["level"] == WARN]
        total_fails += len(fails)
        total_warns += len(warns)

        if fails or warns:
            status = "FAIL" if fails else "WARN"
            print(f"{status}  {skill_dir.name}")
            for r in results:
                if r["level"] in (FAIL, WARN):
                    print(f"       [{r['rule']}] {r['level']}: {r['message']}")
        else:
            print(f"OK    {skill_dir.name}")

    print()
    if total_fails:
        print(f"Skill lint: {total_fails} FAIL(s), {total_warns} WARN(s) across {len(skill_dirs)} skill(s)")
        return 1
    if total_warns:
        print(f"Skill lint: 0 FAILs, {total_warns} WARN(s) across {len(skill_dirs)} skill(s)")
    else:
        print(f"Skill lint: all {len(skill_dirs)} skill(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
