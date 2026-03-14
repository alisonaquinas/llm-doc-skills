---
name: mermaid
description: Use when a task involves Mermaid diagram source, Mermaid CLI rendering, flowcharts, sequence diagrams, state or class diagrams, Markdown-embedded diagrams, or Mermaid theme and export workflows.
---

# Mermaid Diagrams

## Intent Router

Load sections based on the task:
- Diagram syntax and type selection -> `references/diagram-types.md`
- Configuration, themes, and directives -> `references/config-and-theming.md`
- Embedding, export, and troubleshooting -> `references/embedding-and-troubleshooting.md`

## Overview

This skill covers Mermaid diagram authoring and rendering.
Use it for text-first diagrams embedded in Markdown, lightweight documentation visuals, and CLI-based export to common image formats.

The guidance follows the official Mermaid documentation and Mermaid CLI patterns.

## Quick Start

```bash
python mermaid/scripts/render.py architecture.mmd --to svg --output architecture.svg
```

```bash
python mermaid/scripts/render.py sequence.mmd --to png --output sequence.png --theme neutral
```

## Preferred Workflow

1. Pick the smallest Mermaid diagram type that communicates the structure clearly.
2. Keep labels short so diagrams survive both embedded and exported contexts.
3. Use config or theme flags instead of editing raw SVG after rendering.
4. Render locally with the Mermaid CLI before embedding into docs.
5. Re-check diagram readability after scaling or exporting.

## Authoring Guidance

This skill is the right fit for:
- flowcharts and process maps
- sequence and interaction diagrams
- class, state, entity, and timeline diagrams where Mermaid supports them
- Markdown-embedded diagrams for docs portals and READMEs
- diagrams that benefit from text review in version control

## Rendering and Export

Mermaid CLI is the preferred execution path.
Output format is usually inferred from the destination file extension, with SVG and PNG as the most common stable targets.

```bash
mmdc -i architecture.mmd -o architecture.svg
mmdc -i sequence.mmd -o sequence.png -t neutral
```

## Portability and Troubleshooting

Common issues include unsupported syntax for a chosen diagram type, theme or config drift between environments, and embedding assumptions that do not hold across Markdown hosts.
Reduce the source to a minimal diagram when parser errors are unclear.

## Official References

Primary sources:
- Mermaid documentation: <https://mermaid.js.org/>
- Mermaid configuration docs: <https://mermaid.js.org/config/configuration.html>

Deep-dive references for this skill:
- `references/diagram-types.md`
- `references/config-and-theming.md`
- `references/embedding-and-troubleshooting.md`
