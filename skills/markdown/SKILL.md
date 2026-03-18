---
name: markdown
description: Use when a task involves CommonMark, GitHub Flavored Markdown, README or docs authoring, frontmatter-aware Markdown workflows, rendering, or Markdown-native export and review patterns.
---

# Markdown Authoring and Rendering

## Intent Router

Load sections based on the task:
- Syntax and dialect boundaries -> `references/commonmark-vs-gfm.md`
- README or frontmatter-backed docs structure -> `references/frontmatter-and-docs-patterns.md`
- Rendering or lint strategy -> `references/rendering-and-linting.md`

## Overview

This skill covers Markdown authoring with CommonMark and GitHub Flavored Markdown as the default practical target.
Use it for semantic Markdown source work, repository docs, README editing, frontmatter-aware files, and straightforward rendering or export flows.

The guidance follows the CommonMark specification and the GitHub Flavored Markdown specification.

## Quick Start

```bash
python markdown/scripts/render.py README.md --to html --output README.html --gfm
```

```bash
python markdown/scripts/render.py guide.md --to docx --output guide.docx --toc
```

## Preferred Workflow

1. Decide whether the target is core CommonMark or CommonMark plus GFM extensions.
2. Keep the source semantic before worrying about renderer-specific cosmetics.
3. Treat frontmatter as a host-tool contract, not portable Markdown syntax.
4. Use `cmark-gfm` for fast HTML rendering when the task is purely Markdown.
5. Use `pandoc` when export leaves the Markdown ecosystem.

## Authoring Guidance

This skill is the right fit for:
- READMEs and contributor docs
- changelogs and release notes
- Markdown tables and task lists
- fenced command examples
- relative-link cleanup and heading structure

## Rendering and Export

HTML rendering should prefer `cmark-gfm` when available.
PDF and DOCX export should route through Pandoc.

```bash
cmark-gfm README.md > README.html
pandoc guide.md --to pdf --output guide.pdf
```

## Troubleshooting

Common issues include mixed Markdown dialect assumptions, frontmatter interpreted by the wrong tool, table rendering differences, and renderer-specific HTML output.
Reduce the document to a minimal example when parser behavior is unclear.

## Official References

Primary sources:
- CommonMark specification: <https://spec.commonmark.org/current/>
- GitHub Flavored Markdown specification: <https://github.github.com/gfm/>

Deep-dive references for this skill:
- `references/commonmark-vs-gfm.md`
- `references/frontmatter-and-docs-patterns.md`
- `references/rendering-and-linting.md`
