#!/usr/bin/env python3
"""Automated pre-flight validation for all skill directories.

Implements the automated (non-qualitative) portion of the skill-validation
standard.  Each criterion is scored PASS / WARN / FAIL based on measurable
signals.  Qualitative criteria (V07 LLM usability, V08 public docs alignment)
require human/LLM review and are reported as INFO items with prompts.

Criteria:
  V01  Description effectiveness — frontmatter description has triggers/scenarios
  V02  Intent Router completeness — section present and links load conditions
  V03  Quick reference coverage — inline code examples ≥ 2
  V04  Safety coverage — destructive-op mentions have guardrail language nearby
  V05  Example quality — concrete fenced code blocks present (≥ 2)
  V06  Reference file depth — referenced files exist and are non-trivial (> 10 lines)
  V07  LLM usability — Quick Start section present (proxy only)
  V08  Public docs alignment — INFO: manual review required

Exit codes:
  0  No FAILs
  1  One or more FAILs

Usage:
  python3 scripts/validate_skills.py                # all skills
  python3 scripts/validate_skills.py git
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def skills_root() -> Path:
    candidate = REPO_ROOT / "skills"
    return candidate if candidate.exists() else REPO_ROOT

# ---------------------------------------------------------------------------
# Signals and thresholds
# ---------------------------------------------------------------------------

TRIGGER_WORDS = re.compile(
    r"\b(use when|trigger|use for|triggers include|call when|invoke when)\b",
    re.IGNORECASE,
)
INTENT_ROUTER_RE = re.compile(r"^## Intent Router", re.MULTILINE)
INTENT_ROUTER_LINK_RE = re.compile(r"`[^`]+\.md`")
QUICK_START_RE = re.compile(r"^## Quick[- ]?Start", re.MULTILINE | re.IGNORECASE)
CODE_FENCE_RE = re.compile(r"^```", re.MULTILINE)
DESTRUCTIVE_OPS_RE = re.compile(
    r"\b(rm\s+-rf?|git\s+reset\s+--hard|git\s+push\s+--force|DROP\s+TABLE"
    r"|delete\s+all|wipe|overwrite|truncate)\b",
    re.IGNORECASE,
)
GUARDRAIL_RE = re.compile(
    r"\b(warning|caution|danger|irreversible|backup|cannot\s+be\s+undone"
    r"|make\s+sure|verify|confirm|double.check|safe\s+alternative)\b",
    re.IGNORECASE,
)
REFERENCES_LINK_RE = re.compile(r"`(references/[^`]+\.md)`")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)

MIN_CODE_FENCES = 2
MIN_REFERENCE_LINES = 10

FAIL = "FAIL"
WARN = "WARN"
PASS = "PASS"
INFO = "INFO"


def _result(level: str, criterion: str, message: str) -> dict:
    return {"level": level, "criterion": criterion, "message": message}


# ---------------------------------------------------------------------------
# Individual criterion checks
# ---------------------------------------------------------------------------

def check_v01(content: str, skill_dir: Path) -> dict:
    """V01: frontmatter description mentions triggers or scenarios."""
    m = FRONTMATTER_RE.match(content)
    if not m:
        return _result(FAIL, "V01", "No frontmatter found; description effectiveness cannot be assessed")
    fm_text = m.group(1)
    if not TRIGGER_WORDS.search(fm_text):
        return _result(
            WARN, "V01",
            "Frontmatter description does not mention triggers or use-when scenarios; "
            "add 'Use when …' or 'Triggers include …' to help agents route correctly"
        )
    return _result(PASS, "V01", "Frontmatter description includes trigger/scenario language")


def check_v02(content: str, skill_dir: Path) -> dict:
    """V02: Intent Router section is present and has reference links with load conditions."""
    if not INTENT_ROUTER_RE.search(content):
        return _result(WARN, "V02", "No '## Intent Router' section found")
    # Check section has at least one reference link
    m = INTENT_ROUTER_RE.search(content)
    section_start = m.end()
    # Take content up to next ## heading
    rest = content[section_start:]
    next_section = re.search(r"\n## ", rest)
    section_body = rest[: next_section.start()] if next_section else rest
    if not INTENT_ROUTER_LINK_RE.search(section_body):
        return _result(
            WARN, "V02",
            "Intent Router section has no reference file links (e.g. `references/foo.md`)"
        )
    return _result(PASS, "V02", "Intent Router section present with reference links")


def check_v03(content: str, skill_dir: Path) -> dict:
    """V03: Inline code fences ≥ 2 (quick reference coverage proxy)."""
    count = len(CODE_FENCE_RE.findall(content)) // 2  # each block uses opening + closing
    if count < MIN_CODE_FENCES:
        return _result(
            WARN, "V03",
            f"Only {count} fenced code block(s) found; add at least {MIN_CODE_FENCES} "
            "inline examples so ~80% of requests are answerable without loading references"
        )
    return _result(PASS, "V03", f"{count} fenced code block(s) found")


def check_v04(content: str, skill_dir: Path) -> dict:
    """V04: Destructive-op mentions have nearby guardrail language."""
    issues = []
    lines = content.splitlines()
    for i, line in enumerate(lines):
        if DESTRUCTIVE_OPS_RE.search(line):
            window = "\n".join(lines[max(0, i - 3): i + 4])
            if not GUARDRAIL_RE.search(window):
                issues.append(f"Line {i + 1}: {line.strip()!r}")
    if issues:
        return _result(
            WARN, "V04",
            "Potentially destructive op(s) without nearby guardrail language:\n  "
            + "\n  ".join(issues)
        )
    return _result(PASS, "V04", "No unguarded destructive operations found")


def check_v05(content: str, skill_dir: Path) -> dict:
    """V05: ≥ 2 fenced code examples (example quality proxy — same signal as V03)."""
    count = len(CODE_FENCE_RE.findall(content)) // 2
    if count < MIN_CODE_FENCES:
        return _result(
            WARN, "V05",
            f"Fewer than {MIN_CODE_FENCES} fenced code examples; add concrete, runnable examples"
        )
    return _result(PASS, "V05", f"{count} fenced example block(s) found")


def check_v06(content: str, skill_dir: Path) -> dict:
    """V06: Referenced files exist and are non-trivial."""
    issues = []
    for m in REFERENCES_LINK_RE.finditer(content):
        ref_rel = m.group(1)
        if "*" in ref_rel:
            continue
        ref_path = skill_dir / ref_rel
        if not ref_path.exists():
            issues.append(f"{ref_rel!r} does not exist")
        elif len(ref_path.read_text(encoding="utf-8").splitlines()) < MIN_REFERENCE_LINES:
            issues.append(f"{ref_rel!r} is very short (<{MIN_REFERENCE_LINES} lines)")
    if issues:
        return _result(WARN, "V06", "Reference file issues:\n  " + "\n  ".join(issues))
    return _result(PASS, "V06", "All referenced files exist and are non-trivial")


def check_v07(content: str, skill_dir: Path) -> dict:
    """V07: Quick Start section present (LLM usability proxy)."""
    if not QUICK_START_RE.search(content):
        return _result(
            WARN, "V07",
            "No '## Quick Start' section found; agents benefit from a clear "
            "entry point that answers the most common request directly"
        )
    return _result(PASS, "V07", "Quick Start section present")


def check_v08(content: str, skill_dir: Path) -> dict:
    """V08: Public docs alignment — requires manual review."""
    return _result(
        INFO, "V08",
        "Manual review required: verify the skill reflects current Anthropic/OpenAI "
        "prompt engineering standards (see skill-validation/validation/public-references.md)"
    )


ALL_CRITERIA = [
    check_v01, check_v02, check_v03, check_v04,
    check_v05, check_v06, check_v07, check_v08,
]

THRESHOLD_APPROVE = 7   # ≥7 PASS, ≤1 FAIL → APPROVE
THRESHOLD_REJECT_FAIL = 3   # ≥3 FAILs → REJECT


def validate_skill(skill_dir: Path) -> list[dict]:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [_result(FAIL, "pre-flight", "SKILL.md not found")]
    content = skill_md.read_text(encoding="utf-8")
    return [check(content, skill_dir) for check in ALL_CRITERIA]


def _overall(results: list[dict]) -> str:
    fails = sum(1 for r in results if r["level"] == FAIL)
    passes = sum(1 for r in results if r["level"] == PASS)
    if fails >= THRESHOLD_REJECT_FAIL:
        return "REJECT"
    if passes >= THRESHOLD_APPROVE and fails <= 1:
        return "APPROVE"
    return "REVISE"


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

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

    any_fail = False

    for skill_dir in skill_dirs:
        results = validate_skill(skill_dir)
        fails = [r for r in results if r["level"] == FAIL]
        warns = [r for r in results if r["level"] == WARN]
        passes = [r for r in results if r["level"] == PASS]
        verdict = _overall(results)

        if fails:
            any_fail = True

        header_level = FAIL if fails else (WARN if warns else PASS)
        print(f"{header_level}  {skill_dir.name}  [{verdict}]  "
              f"{len(passes)} PASS / {len(warns)} WARN / {len(fails)} FAIL")
        for r in results:
            if r["level"] != PASS:
                print(f"       [{r['criterion']}] {r['level']}: {r['message']}")

    print()
    if any_fail:
        print(f"Skill validation: FAILs found across {len(skill_dirs)} skill(s)")
        return 1
    print(f"Skill validation: {len(skill_dirs)} skill(s) checked, no FAILs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
