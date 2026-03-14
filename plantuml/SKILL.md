---
name: plantuml
description: Use when a task involves PlantUML source, UML-style diagrams, sequence or component diagrams, includes, themes, stdlib usage, or PlantUML rendering and export workflows.
---

# PlantUML Diagrams

## Intent Router

Load sections based on the task:
- Diagram families and syntax patterns -> `references/diagram-families.md`
- Includes, themes, and stdlib usage -> `references/includes-themes-and-stdlib.md`
- Rendering, layout, and troubleshooting -> `references/render-and-debug.md`

## Overview

This skill covers PlantUML authoring and rendering.
Use it for UML-oriented diagrams, architecture views, text-first diagram maintenance, and export workflows driven by the PlantUML toolchain.

The guidance follows the official PlantUML documentation and standard rendering patterns.

## Quick Start

```bash
python plantuml/scripts/render.py system.puml --to svg --output out
```

```bash
python plantuml/scripts/render.py sequence.puml --to png --output out --theme plain
```

## Preferred Workflow

1. Choose the PlantUML diagram family that best matches the model instead of forcing everything into a sequence diagram.
2. Keep includes and themes explicit so output is reproducible.
3. Prefer text-level layout hints before manual image editing.
4. Render locally before embedding diagrams in docs or slide material.
5. Narrow the source to a small failing example when debugging parser or layout issues.

## Authoring Guidance

This skill is the right fit for:
- UML class, sequence, activity, component, and deployment diagrams
- C4-style diagrams where PlantUML support is already part of the workflow
- reusable diagram includes and stdlib-backed notation
- architecture diagrams that benefit from text review and diffability
- export pipelines based on the PlantUML CLI or JAR path

## Rendering and Export

PlantUML can run through its native launcher or a Java plus JAR workflow.
SVG and PNG are the most common output targets, with text-based exports useful for lightweight review paths.

```bash
plantuml -tsvg diagram.puml
plantuml -tpng diagram.puml
```

## Portability and Troubleshooting

Common problems include missing Java runtime support, unresolved includes, theme drift, and layout directives that make output less predictable instead of more readable.
Shrink the source until the failing construct is obvious.

## Official References

Primary sources:
- PlantUML documentation: <https://plantuml.com/>
- PlantUML guide pages: <https://plantuml.com/guide>

Deep-dive references for this skill:
- `references/diagram-families.md`
- `references/includes-themes-and-stdlib.md`
- `references/render-and-debug.md`
