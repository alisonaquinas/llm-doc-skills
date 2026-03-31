# Canvas JSON Format

Obsidian Canvas files (`.canvas`) are JSON documents containing a `nodes` array and an `edges` array.
The format is also published as an open spec at jsoncanvas.org.

## Top-level structure

```json
{
  "nodes": [ ...node objects... ],
  "edges": [ ...edge objects... ]
}
```

Both arrays default to `[]` for an empty canvas.

## Node types

### Text node

```json
{
  "id": "abc123",
  "type": "text",
  "text": "Markdown content here",
  "x": 0,
  "y": 0,
  "width": 250,
  "height": 100,
  "color": "1"
}
```

### File node (links to a vault note)

```json
{
  "id": "def456",
  "type": "file",
  "file": "Notes/My Note.md",
  "x": 300,
  "y": 0,
  "width": 250,
  "height": 360,
  "subpath": "#Section Heading"
}
```

The `subpath` field optionally restricts the embedded view to a heading or block.

### Link node (web URL)

```json
{
  "id": "ghi789",
  "type": "link",
  "url": "https://example.com",
  "x": 600,
  "y": 0,
  "width": 400,
  "height": 300
}
```

### Group node (container)

```json
{
  "id": "grp001",
  "type": "group",
  "label": "Research Cluster",
  "x": -50,
  "y": -50,
  "width": 700,
  "height": 500,
  "color": "4"
}
```

Groups do not automatically contain other nodes — positioning nodes inside a group's bounding box creates the visual grouping.

## Edge object

```json
{
  "id": "edge1",
  "fromNode": "abc123",
  "toNode": "def456",
  "fromSide": "right",
  "toSide": "left",
  "label": "relates to",
  "color": "2",
  "toEnd": "arrow"
}
```

Optional edge fields: `fromSide`, `toSide` (`top`, `right`, `bottom`, `left`), `label`, `color`, `fromEnd`, `toEnd` (`none` or `arrow`).

## Color values

| Value | Color |
| --- | --- |
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |
| CSS hex | e.g., `"#ff6600"` |
