# LaTeX Engines and Toolchain Operations

Authoritative sources:
- learnlatex: <https://www.learnlatex.org/en/>
- LaTeX Project documentation: <https://latex-project.org/help/documentation/>
- TeX FAQ: <https://texfaq.org/>
- CTAN latexmk package page: <https://ctan.org/pkg/latexmk>

## Engine choices

- `pdflatex`: stable default for classic PDF workflows
- `xelatex`: strong Unicode and system-font support
- `lualatex`: modern Unicode engine with programmable extensions

## Build orchestration

`latexmk` is the preferred orchestrator because it manages repeated passes and bibliography/index reruns.

```bash
latexmk -pdf report.tex
latexmk -xelatex thesis.tex
latexmk -lualatex article.tex
```

## Bibliography guidance

- Prefer `biblatex` plus `biber` for modern projects.
- Use BibTeX when a publisher class or legacy template requires it.
- Keep bibliography tool choice explicit in automation when reproducibility matters.

## Operational notes

- Separate output with `-outdir` in CI or scripted builds.
- Clean intermediates after a successful build when artifact directories must stay tidy.
- Capture the full `.log` file for diagnostics; console output alone is rarely sufficient.
