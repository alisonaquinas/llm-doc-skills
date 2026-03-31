# Canvas Authoring Patterns

## Layout strategies

**Hub and spoke**: place a central text or file node at the origin, then radiate related nodes outward.
Works well for topic overviews and MOC-style boards.

**Sequential flow**: arrange nodes left to right or top to bottom in a linear chain connected by edges.
Works well for process maps, workflows, and decision trees.

**Cluster layout**: group thematically related nodes inside group containers with distinct colors.
Works well for multi-domain research boards.

**Timeline**: arrange file nodes left to right by date, with group containers per year or quarter.

## Coordinate system

Canvas uses a flat integer coordinate space.
The origin (0, 0) is the initial viewport center.
Positive X is right; positive Y is down.
Nodes do not overlap — plan spacing carefully when authoring JSON directly.

A reasonable starting grid:

- Node width: 250–400px
- Node height: 80px (text) to 400px (file)
- Horizontal gap: 50–100px
- Vertical gap: 50px

## Color coding conventions

Assign consistent color semantics across a canvas:

- Red (1): blockers, urgent items
- Orange (2): in-progress or attention-needed
- Yellow (3): references or secondary material
- Green (4): completed or validated
- Cyan (5): external links or resources
- Purple (6): meta-notes, MOCs, or indexes

## Group containers

Groups visually cluster nodes but have no JSON-level membership — any node positioned inside a group's bounding box appears grouped.
Give groups descriptive labels and a distinct background color.
Resize groups to tightly fit their members after finalizing layout.

## Canvas-to-canvas navigation

Create a file node pointing to another `.canvas` file to link boards:

```json
{
  "id": "nav1",
  "type": "file",
  "file": "Boards/Research Overview.canvas",
  "x": 1000,
  "y": 0,
  "width": 200,
  "height": 80
}
```

Keep individual canvases focused on one domain or project; use navigation nodes to move between them.

## Zoom and pan

Obsidian Canvas supports standard scroll-to-zoom and drag-to-pan.
Press `Shift+1` to fit all nodes into view.
Press `Ctrl+Shift+F` (Cmd+Shift+F) to zoom to a selected node.
