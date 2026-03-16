# LaTeX Packages and Authoring Patterns

Authoritative sources:
- learnlatex lessons: <https://www.learnlatex.org/en/>
- LaTeX Project documentation hub: <https://latex-project.org/help/documentation/>

## Core document structure

Prefer a stable preamble, then keep content in semantic environments.
Typical building blocks:
- `\documentclass`
- package declarations
- title, author, date metadata
- section structure
- tables, figures, math, bibliography

## Common package families

- page geometry and headers: `geometry`, `fancyhdr`
- graphics and color: `graphicx`, `xcolor`
- math: `amsmath`, `amssymb`, `mathtools`
- tables: `array`, `booktabs`, `longtable`, `tabularx`
- bibliography: `biblatex`
- hyperlinks and cross references: `hyperref`, `cleveref`

## Pattern guidance

- Prefer semantic macros for repeated inline styling.
- Prefer `booktabs` for publication-style tables.
- Prefer `biblatex` for modern bibliography workflows unless a legacy style requires BibTeX.
- Keep package order intentional when `hyperref` or bibliography packages are involved.

```tex
\usepackage{amsmath, amssymb, mathtools}
\usepackage{graphicx}
\usepackage{booktabs, tabularx}
\usepackage{hyperref}
```
