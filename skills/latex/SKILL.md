---
name: latex
description: Use when a task involves LaTeX authoring, package selection, bibliography setup, compile loops, engine choice, PDF production, or TeX toolchain troubleshooting across full document workflows.
---

# LaTeX Authoring and Toolchain Operations

## Intent Router

Load sections based on the task:
- Package choice or source structure -> `references/packages-and-patterns.md`
- Engine selection or build orchestration -> `references/engines-and-toolchain.md`
- Compile failures and log triage -> `references/error-triage.md`

## Overview

This skill covers LaTeX as both a writing system and a build toolchain.
Use it for document structure, mathematics, tables, bibliographies, engine selection, compile automation, and error diagnosis.

The guidance follows learnlatex, the LaTeX Project documentation, TeX FAQ material, and the CTAN latexmk documentation.

## Quick Start

```bash
python latex/scripts/build.py report.tex --engine pdflatex
```

```bash
python latex/scripts/build.py thesis.tex --engine xelatex --outdir build
```

## Preferred Workflow

1. Choose the document class and packages based on document type.
2. Keep the preamble stable and move repeated presentation choices into macros.
3. Select an engine explicitly when fonts, Unicode, or package compatibility matter.
4. Run `latexmk` as the primary orchestrator instead of manual repeated engine calls.
5. Read the first meaningful compile error from the log before changing package sets.

## Authoring Guidance

Reach for this skill when the task involves:
- article, report, or book structure
- mathematical notation and theorem environments
- bibliography and citation setup
- figures, floats, and tables
- page layout and PDF output quality

```tex
\documentclass{article}
\usepackage{amsmath, amssymb, mathtools}
\usepackage{graphicx}
\usepackage{hyperref}
```

## Build and Export

LaTeX output depends on engine and package compatibility.
Prefer `latexmk` with an explicit engine flag.

```bash
latexmk -pdf paper.tex
latexmk -xelatex slides.tex
```

Use the included wrappers to standardize common tasks:
- `latex/scripts/build.py`
- `latex/scripts/clean.py`

## Troubleshooting

Frequent issues include missing packages, stale auxiliary files, bibliography mismatches, and font-engine conflicts.
When a compile fails, inspect the first real error and reduce the document if needed.

## Official References

Primary sources:
- learnlatex: <https://www.learnlatex.org/en/>
- LaTeX Project documentation: <https://latex-project.org/help/documentation/>
- TeX FAQ: <https://texfaq.org/>
- CTAN latexmk: <https://ctan.org/pkg/latexmk>

Deep-dive references for this skill:
- `references/packages-and-patterns.md`
- `references/engines-and-toolchain.md`
- `references/error-triage.md`
