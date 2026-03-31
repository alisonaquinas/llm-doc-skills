---
name: obsidian-canvas
description: Use when a task involves Obsidian Canvas files, authoring or editing
  .canvas JSON, creating file nodes, text nodes, web link nodes, or group nodes,
  wiring edges between nodes, or using canvas as a visual knowledge map inside
  an Obsidian vault.
---

# Obsidian Canvas

## Intent Router

Load sections based on the task:

- `.canvas` file schema, node types, and edge structure → `references/canvas-json-format.md`
- Layout strategies, color coding, grouping, and navigation → `references/canvas-authoring-patterns.md`
- Linking canvas to vault notes, embedding, and MOC use → `references/canvas-and-vault-integration.md`

## Overview

This skill covers Obsidian Canvas — a visual workspace format stored as `.canvas` JSON files inside the vault.
Canvas files contain nodes (notes, text, links, or groups) and edges (connections between nodes), rendered as an infinite two-dimensional board.

Use it when authoring new canvas files, editing canvas JSON directly, designing visual knowledge maps, or integrating canvas boards with vault notes.

## Quick Start

```json
{
  "nodes": [
    {
      "id": "node1",
      "type": "text",
      "text": "Central idea",
      "x": 0, "y": 0,
      "width": 200, "height": 80
    },
    {
      "id": "node2",
      "type": "file",
      "file": "Notes/Research Overview.md",
      "x": 300, "y": 0,
      "width": 250, "height": 360
    }
  ],
  "edges": [
    {
      "id": "edge1",
      "fromNode": "node1",
      "toNode": "node2"
    }
  ]
}
```

```bash
# Validate a canvas file is well-formed JSON
python -c "import json; json.load(open('MyBoard.canvas')); print('valid')"
```

## Preferred Workflow

1. Create a new canvas from the command palette: `Canvas: Create new canvas`.
2. Use the Obsidian GUI to add nodes and edges interactively, then inspect or edit the resulting JSON for bulk changes.
3. When authoring JSON directly, start with one text node and one file node to verify the structure before adding more.
4. Assign unique, descriptive IDs to nodes when editing JSON manually — avoid numeric sequences that conflict on merge.
5. Validate JSON after every manual edit before opening in Obsidian to avoid a parse-failure that leaves the canvas blank.

## Authoring Guidance

This skill is the right fit for:

- creating visual maps of a topic or project by linking vault notes
- authoring canvas JSON in bulk (e.g., programmatically generating a board from a note index)
- debugging a corrupted or blank canvas file by inspecting the raw JSON
- designing a canvas as a visual MOC for a vault cluster
- adding group containers and color coding to organize a complex board

## Canvas Limits

Canvas files have no enforced node limit, but very large canvases (hundreds of nodes) slow rendering.
Prefer multiple focused canvas files linked to each other over one sprawling board.
Edges do not carry labels in the default schema; use text nodes adjacent to edges as annotation.

## Official References

Primary sources:

- Obsidian Canvas: <https://obsidian.md/canvas>
- Canvas file format spec: <https://jsoncanvas.org>

Deep-dive references for this skill:

- `references/canvas-json-format.md`
- `references/canvas-authoring-patterns.md`
- `references/canvas-and-vault-integration.md`
