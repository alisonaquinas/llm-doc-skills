---
name: github-flavored-markdown
description: Use when a task involves GitHub Flavored Markdown, README authoring, GitHub-rendered docs, issue or PR references, task lists, tables, alerts, or GitHub-specific Markdown review and export workflows.
---

# GitHub Flavored Markdown

## Intent Router

Load sections based on the task:
- Syntax and extension boundaries -> `references/gfm-syntax-matrix.md`
- README, repository docs, and sanitization rules -> `references/github-doc-patterns.md`
- Rendering, portability, and export tradeoffs -> `references/rendering-and-portability.md`

## Overview

This skill covers Markdown that must render well on GitHub surfaces.
Use it for README files, repository docs, issue and pull request content, release notes, and Markdown that depends on GitHub Flavored Markdown extensions.

The guidance follows the GitHub Flavored Markdown specification and GitHub's documented repository-writing behaviors.

## Quick Start

```bash
python github-flavored-markdown/scripts/render.py README.md --to html --output README.html
```

```bash
python github-flavored-markdown/scripts/render.py docs/guide.md --to pdf --output guide.pdf --toc
```

## Preferred Workflow

1. Start with portable Markdown structure, then add GitHub-specific extensions only where they improve review or navigation.
2. Keep links, headings, task lists, and tables readable in raw source before tuning rendered output.
3. Treat alerts, issue references, and autolinks as GitHub contracts rather than portable Markdown features.
4. Use `cmark-gfm` for fast HTML previews and Pandoc when the output leaves GitHub's renderer.
5. Re-check any exported output if the source relies on GitHub-only features.

## Authoring Guidance

This skill is the right fit for:
- README and landing-page structure
- task lists and table-heavy repository docs
- issue, pull request, and release-note Markdown
- GitHub alerts, autolinks, and repository references
- docs that must survive GitHub sanitization rules

## Rendering and Export

HTML preview should prefer `cmark-gfm`.
PDF and DOCX export should route through Pandoc, with a portability review if the source uses GitHub-only extensions.

```bash
cmark-gfm README.md > README.html
pandoc notes.md --from gfm --to docx --output notes.docx
```

## Portability and Troubleshooting

Common problems include assuming all GFM features are portable to GitLab or CommonMark renderers, relying on raw HTML that a host sanitizes, and expecting exported output to preserve GitHub-only affordances.
Reduce the document to a small example when extension behavior is unclear.

## Official References

Primary sources:
- GitHub Flavored Markdown specification: <https://github.github.com/gfm/>
- GitHub writing and formatting docs: <https://docs.github.com/en/get-started/writing-on-github>

Deep-dive references for this skill:
- `references/gfm-syntax-matrix.md`
- `references/github-doc-patterns.md`
- `references/rendering-and-portability.md`
