---
name: typst
description: Use when a task involves Typst authoring, layout rules, math, templates, references, or Typst CLI compilation and export to PDF, PNG, or SVG.
---

# Typst Authoring and Export

## Intent Router

Load sections based on the task:
- Syntax, layout, or math -> `references/language-and-layout.md`
- Show rules or reusable themes -> `references/templates-and-rules.md`
- CLI export or page rendering -> `references/export-and-cli.md`

## Overview

This skill covers Typst-native writing, layout control, and export workflows.
Use it when the task belongs in Typst itself rather than a conversion-first pipeline.

The guidance follows the official Typst documentation and reference.

## Quick Start

```bash
python typst/scripts/compile.py report.typ --format pdf --output report.pdf
```

```bash
python typst/scripts/compile.py slides.typ --format png --pages 1-3 --ppi 144
```

## Preferred Workflow

1. Decide whether the task is content authoring, layout policy, or export.
2. Keep document structure semantic before adding presentation rules.
3. Move repeated presentation logic into `set` and `show` rules.
4. Compile a narrow output first when iterating on visual layout.
5. Use `--root` explicitly when includes or external assets are involved.

## Authoring Guidance

Reach for this skill when the task involves:
- Typst-native page layout
- equations and math-heavy documents
- templates and reusable document shells
- figure, table, and reference formatting
- official CLI export to PDF, PNG, or SVG

```typst
#set page(margin: 1in)
= Heading
A concise Typst example.
```

## Export and Rendering

Use the official CLI for repeatable exports.

```bash
typst compile paper.typ paper.pdf
typst compile poster.typ poster.svg
```

The included wrapper covers common compile flags without exposing the entire CLI surface.

## Troubleshooting

Common issues include incorrect project roots, missing assets, over-specific show rules, and export assumptions about page ranges or raster density.
Reduce the document to one page or one include chain when isolating layout faults.

## Official References

Primary sources:
- Typst docs: <https://typst.app/docs/>
- Typst reference: <https://typst.app/docs/reference/>

Deep-dive references for this skill:
- `references/language-and-layout.md`
- `references/templates-and-rules.md`
- `references/export-and-cli.md`
