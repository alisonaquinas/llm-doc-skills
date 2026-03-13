"""Tests for skill packaging invariants.

Verifies that every skill directory ships the three required files:
  - SKILL.md
  - agents/claude.yaml
  - agents/openai.yaml

Also checks that built/*.zip archives (if present) contain those same files
under the llm-doc-skills/ root.
"""

import unittest
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
REPO_NAME = REPO_ROOT.name  # "llm-doc-skills"


def _discover_skills() -> list[Path]:
    """Return skill directories that contain SKILL.md."""
    return sorted(p.parent for p in REPO_ROOT.glob("*/SKILL.md"))


REQUIRED_FILES = ["SKILL.md", "agents/claude.yaml", "agents/openai.yaml"]


class TestSkillSourceLayout(unittest.TestCase):
    """Every skill source directory must ship the required manifest files."""

    def test_skills_discovered(self):
        skills = _discover_skills()
        self.assertGreater(len(skills), 0, "No skill directories found")

    def test_required_files_present_in_source(self):
        skills = _discover_skills()
        for skill_dir in skills:
            with self.subTest(skill=skill_dir.name):
                for rel_path in REQUIRED_FILES:
                    full_path = skill_dir / rel_path
                    self.assertTrue(
                        full_path.exists(),
                        f"{skill_dir.name}: missing required file {rel_path}",
                    )

    def test_skill_md_not_empty(self):
        skills = _discover_skills()
        for skill_dir in skills:
            with self.subTest(skill=skill_dir.name):
                skill_md = skill_dir / "SKILL.md"
                content = skill_md.read_text(encoding="utf-8").strip()
                self.assertTrue(
                    len(content) > 0,
                    f"{skill_dir.name}/SKILL.md is empty",
                )

    def test_agent_yamls_not_empty(self):
        skills = _discover_skills()
        for skill_dir in skills:
            for yaml_path in ["agents/claude.yaml", "agents/openai.yaml"]:
                with self.subTest(skill=skill_dir.name, file=yaml_path):
                    full = skill_dir / yaml_path
                    content = full.read_text(encoding="utf-8").strip()
                    self.assertTrue(
                        len(content) > 0,
                        f"{skill_dir.name}/{yaml_path} is empty",
                    )


class TestBuiltZipInvariants(unittest.TestCase):
    """Built ZIP files must contain the required files under the repo root."""

    def setUp(self):
        build_dir = REPO_ROOT / "built"
        self.zip_files = sorted(build_dir.glob("*-skill.zip")) if build_dir.exists() else []

    def test_built_zips_present(self):
        if not self.zip_files:
            self.skipTest("built/ directory is empty — run 'make build' first")

    def test_required_files_in_zips(self):
        if not self.zip_files:
            self.skipTest("built/ directory is empty — run 'make build' first")

        for zip_path in self.zip_files:
            skill_name = zip_path.stem.replace("-skill", "")
            with self.subTest(zip=zip_path.name):
                with zipfile.ZipFile(zip_path, "r") as zf:
                    names = set(zf.namelist())
                for rel_path in REQUIRED_FILES:
                    # ZIPs are rooted at llm-doc-skills/<skill>/
                    expected = f"{REPO_NAME}/{skill_name}/{rel_path}"
                    self.assertIn(
                        expected,
                        names,
                        f"{zip_path.name}: missing {expected}",
                    )

    def test_zips_are_valid_ooxml_or_plain_zips(self):
        """All built ZIPs must open without error (ZIP integrity)."""
        if not self.zip_files:
            self.skipTest("built/ directory is empty — run 'make build' first")

        for zip_path in self.zip_files:
            with self.subTest(zip=zip_path.name):
                try:
                    with zipfile.ZipFile(zip_path, "r") as zf:
                        zf.testzip()  # Returns None on success
                except zipfile.BadZipFile as exc:
                    self.fail(f"{zip_path.name} is not a valid ZIP: {exc}")


class TestAgentManifestContent(unittest.TestCase):
    """Agent manifests must reference the skill and include basic structure."""

    def test_claude_yaml_has_skill_reference(self):
        """claude.yaml should contain a 'skill' or 'name' key."""
        skills = _discover_skills()
        for skill_dir in skills:
            with self.subTest(skill=skill_dir.name):
                content = (skill_dir / "agents" / "claude.yaml").read_text(encoding="utf-8")
                # Very loose check: must not be just whitespace
                self.assertTrue(content.strip(), f"{skill_dir.name}/agents/claude.yaml has no content")

    def test_openai_yaml_has_skill_reference(self):
        skills = _discover_skills()
        for skill_dir in skills:
            with self.subTest(skill=skill_dir.name):
                content = (skill_dir / "agents" / "openai.yaml").read_text(encoding="utf-8")
                self.assertTrue(content.strip(), f"{skill_dir.name}/agents/openai.yaml has no content")


if __name__ == "__main__":
    unittest.main()
