# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
