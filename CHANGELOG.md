# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.3.2] - 2026-05-15

### Added

- Added `.codex-plugin/plugin.json` so the doc skills bundle can be published through a Codex plugin marketplace.
- Added `scripts/validate_plugin_manifests.py` and `make codex-bundle` to validate Codex/Claude manifest alignment and build `doc-skills-codex-plugin.zip`.
- Added back-link to the LLM Skills Marketplace from `README.md`.

## [1.3.1] - 2026-03-31

### Fixed

- Normalized file permissions on `hooks/run-hook.cmd` and `hooks/session-start` from executable (100755) to standard (100644) to match the rest of the repository and avoid spurious modified-file noise after pulls.

## [1.3.0] - 2026-03-31

### Added

- Added full Obsidian vault skill suite: six new skills covering local vault workflows — `obsidian-docs` (vault structure, Maps of Content, navigation, and knowledge-base patterns), `obsidian-config` (.obsidian/ settings, themes, CSS snippets, and sync), `obsidian-flavored-markdown` (wikilinks, embeds, callouts, block references, properties, and tags), `obsidian-plugins` (core and community plugin management and BRAT), `obsidian-templates` (Core Templates and Templater plugin authoring), and `obsidian-canvas` (.canvas JSON schema and visual knowledge maps).
- Added `agents/obsidian-maintainer.md` domain specialist agent scoped to the six Obsidian skills.
- Added `commands/obsidian-vault-health.md` health-check command covering broken wikilinks, orphan notes, canvas JSON validation, frontmatter audits, tag frequency, and plugin config validation.

### Fixed

- Replaced broken `SessionStart` prompt hook in `hooks/hooks.json` with a working `command`-type hook that invokes the session-start script via `run-hook.cmd`, eliminating "ToolUseContext is required for prompt hooks" errors. Also added `PostToolUse` hook that validates `.canvas` files as well-formed JSON after any Write operation.

## [1.2.4] - 2026-03-22

### Fixed

- Removed broken `SessionStart` prompt hook from `hooks/hooks.json`. The `type: "prompt"` hook requires a `ToolUseContext` that does not exist at session start, causing "ToolUseContext is required for prompt hooks" errors on every startup.

## [1.2.3] - 2026-03-16

### Added

- Added repository-wide skill agent manifest (agents/doc-workflow-maintainer.md), command entries (commands/deck-quality.md, commands/quality-gate.md), and hooks/hooks.json for consistent skill routing across Claude and Codex clients.
- Extended AGENTS.md with command + agent template section for focused doc-skill loops.

### Changed

- Hardened scripts/verify_built_zips.py with REQUIRED_FILES invariant checks ensuring each built ZIP contains SKILL.md, agents/claude.yaml, and agents/openai.yaml.
- Normalized line endings across repository files (CRLF → LF).

## [1.2.2] - 2026-03-18

### Fixed

- Fixed packaging invariants so each built skill ZIP is verified to include the required `SKILL.md`, `agents/claude.yaml`, and `agents/openai.yaml` members under the repo-rooted path (`llm-doc-skills/skills/<skill>/...`).
- Hardened `tests/test_ooxml_validate.py` temp workflow by using deterministic repo-local work directories and explicit cleanup to avoid Windows tempfile lifecycle and path-fragility failures.

## [1.2.1] - 2026-03-18

### Added

- Added repository-wide skill agent and command scaffolding for all skills, including per-skill `agents/` manifests and `commands/` entries, so skill invocations can be routed consistently by both Claude and Codex clients.
- Added `hooks/hooks.json` with preconfigured hooks for agent selection and command execution orchestration.

## [1.2.0] - 2026-03-16

### Added

- `Makefile`: added `bundle` target that packages all built `*-skill.zip` files into a single `doc-skills-plugin.zip` for one-click offline installation; `PLUGIN_NAME := doc-skills` variable drives the output filename

### Changed

- `Makefile`: extended `.PHONY` to include `bundle`; updated `help` text to document the new target
- `.github/workflows/release.yml`: added "Build plugin bundle ZIP" step (`make bundle`) so `doc-skills-plugin.zip` is uploaded alongside the individual skill ZIPs on every tag release

## [1.1.0] - 2026-03-16

### Added

- `skills/raw-document`: added XML validation reference, helper script, and tests for inspecting and repairing documents at the raw byte or XML level

### Changed

- moved all skill directories into a `skills/` subdirectory to align the repo layout with the rest of the skill workspace
- updated all internal script paths, test imports, and README links to match the new `skills/` prefix

### Fixed

- `tests/test_xlsx_recalc.py`: loader now catches `SystemExit` from `recalc.py` when openpyxl is not installed and converts it to `ImportError` so the test class is skipped cleanly instead of aborting discovery
- `VALIDATION_REPORT.md`: removed double blank line that triggered MD012
- README skill table and Quick Start command paths corrected to include `skills/` prefix

## [0.1.1] - 2026-03-14

### Fixed

- added release-time Node and lint/tool provisioning to `.github/workflows/release.yml` so tag releases run the same `make test` gate successfully on GitHub-hosted runners
- restored trailing newlines in the newly added skill agent manifests and wrapper scripts, and removed the unused import from `scripts/verify_built_zips.py`, so the CI YAML and Python lint jobs pass for the text-first publishing and diagram skills

## [0.1.0] - 2026-03-14

### Changed

- generalized the repo-owned skill lint and validation helpers so they can share the same baseline logic as the other plugin repos while still supporting `llm-doc-skills` top-level skill layout

### Added

- New packaged text-first publishing skills: `pandoc`, `latex`, `typst`, `markdown`, and `asciidoc`.
- New packaged platform-and-diagram skills: `github-flavored-markdown`, `gitlab-flavored-markdown`, `mermaid`, `plantuml`, and `graphviz`.
- Repo-owned wrapper CLIs for common conversion, build, render, and export flows under the text-first and diagram skill `scripts/` directories.
- Companion `references/` docs for the new skills so authoritative guidance stays deep without pushing `SKILL.md` over repo lint thresholds.
- Packaging and wrapper tests covering the new skills and their command-builder surfaces.
- `scripts/verify_built_zips.py` and `scripts/check_node_version.py` to make repo verification and lint prerequisites more explicit across environments.

### Fixed

- `Makefile`: route ZIP verification through a Python helper so `make verify` checks all built archives consistently on Windows-backed WSL paths.
- `Makefile`: fail early with a clear message when the active Node.js runtime is older than the version required by `markdownlint-cli2`.
- `.gitignore`: ignore repo-local scratch directories and transient `tmp*/` artifacts so failed local temp cleanup does not pollute git status.

## [0.0.5] - 2026-03-13

### Fixed

- `.markdownlint-cli2.jsonc`: disable MD024 for changelog-style repeated release headings so CHANGELOG.md passes the Markdown job.

## [0.0.4] - 2026-03-13

### Fixed

- `.github/workflows/release.yml`: move marketplace token handling into job env and gate the dispatch step on `env.MARKETPLACE_DISPATCH_TOKEN` so the workflow validates and skips cleanly when the secret is absent.

## [0.0.3] - 2026-03-13

### Fixed

- `.github/workflows/release.yml`: skip the marketplace dispatch when `MARKETPLACE_DISPATCH_TOKEN` is unset so a successful release is not marked failed by missing post-release credentials.

## [0.0.2] - 2026-03-13

### Fixed

- `office-custom/SKILL.md`: replaced bare space inside code span (MD038) with
  `&nbsp;` HTML entity to satisfy markdownlint `no-space-in-code` rule.
- `.github/workflows/ci.yml`: added `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`
  to silence Node.js 20 deprecation warnings from third-party actions.
- `.github/workflows/release.yml`: same Node.js 24 env var as ci.yml.

## [0.0.1] - 2026-03-13

### Added

- `office-custom`: shared OOXML utilities for unpacking, repacking, validating,
  and converting `.docx`, `.pptx`, and `.xlsx` packages via `unpack.py`,
  `pack.py`, `validate.py`, and `soffice.py`.
- `docx-custom`: Word document creation, XML editing, tracked changes, tables,
  and comments via python-docx and direct OOXML manipulation.
- `pdf-custom`: PDF merge, split, extraction, OCR, AcroForm filling, and
  generation via PyPDF, pypdfium2, and ReportLab; includes `FORMS.md` and
  `REFERENCE.md` companion guides.
- `pptx-custom`: Presentation generation and editing with visual QA; covers
  both PptxGenJS (generated) and python-pptx (edited) workflows with
  render-based thumbnail inspection via `thumbnail.py`.
- `xlsx-custom`: Spreadsheet modeling, formula preservation, and formatted
  output via openpyxl with mandatory post-edit recalculation via `recalc.py`.
- `scripts/lint_skills.py`: L01–L11 structural linter for skill directories.
- `scripts/validate_skills.py`: V01–V08 quality pre-flight validator.
- `tests/test_packaging.py`: packaging invariants — required files, non-empty
  manifests, and ZIP integrity checks.
- `tests/test_ooxml_validate.py`: unit tests for `office-custom/scripts/validate.py`.
- `Makefile`: `build`, `verify`, `lint`, `test`, `test-unit`, and `clean` targets.
- `.claude-plugin/plugin.json`: plugin metadata for marketplace registration.
- `.github/workflows/ci.yml`: CI gate running Markdown, YAML, Python linting,
  unit tests, and skill validation on every push and pull request.
- `.github/workflows/release.yml`: tag-driven release workflow that runs tests,
  builds ZIP artifacts, creates a GitHub Release with artifacts attached, and
  triggers the marketplace rebuild.
