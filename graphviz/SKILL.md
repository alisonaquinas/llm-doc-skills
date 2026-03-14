---
name: graphviz
description: Use when a task involves Graphviz, DOT source, directed or undirected graph diagrams, layout engine selection, node or edge styling, or Graphviz rendering and export workflows.
---

# Graphviz and DOT

## Intent Router

Load sections based on the task:
- DOT syntax and graph structure -> `references/dot-syntax-and-attributes.md`
- Layout engine selection -> `references/layout-engines.md`
- Rendering and troubleshooting -> `references/render-and-debug.md`

## Overview

This skill covers Graphviz and the DOT language.
Use it for graph-structured diagrams, dependency maps, cluster-based architecture views, and CLI-driven export to SVG, PNG, or PDF.

The guidance follows the official Graphviz documentation and DOT language references.

## Quick Start

```bash
python graphviz/scripts/render.py system.dot --to svg --output system.svg
```

```bash
python graphviz/scripts/render.py topology.dot --to png --output topology.png --layout neato
```

## Preferred Workflow

1. Choose the layout engine before tuning individual node and edge attributes.
2. Keep graph structure clear in source before styling for presentation.
3. Use subgraphs and clusters intentionally rather than as decorative grouping only.
4. Render SVG first when diffable output and label clarity matter.
5. Simplify the graph when layout behavior becomes hard to reason about.

## Authoring Guidance

This skill is the right fit for:
- dependency and relationship graphs
- architecture maps with clusters or subgraphs
- directed and undirected graph visualizations
- DOT-driven diagrams generated from text or code
- layout problems where engine choice matters as much as styling

## Rendering and Export

Graphviz uses different executables for different layout engines.
`dot` is the usual default for hierarchical graphs, while force-directed layouts may fit `neato`, `fdp`, or `sfdp` better.

```bash
dot -Tsvg system.dot -o system.svg
neato -Tpng topology.dot -o topology.png
```

## Portability and Troubleshooting

Common issues include choosing the wrong layout engine, over-constraining the graph with style attributes, and expecting one engine's layout behavior to translate directly to another.
Reduce the graph until the structural cause of the layout problem is obvious.

## Official References

Primary sources:
- Graphviz documentation: <https://graphviz.org/documentation/>
- DOT language reference: <https://graphviz.org/doc/info/lang.html>

Deep-dive references for this skill:
- `references/dot-syntax-and-attributes.md`
- `references/layout-engines.md`
- `references/render-and-debug.md`
