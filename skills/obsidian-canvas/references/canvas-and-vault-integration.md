# Canvas and Vault Integration

Canvas boards live inside the vault as `.canvas` files and integrate with notes through wikilinks and file nodes.

## Embedding notes in canvas

Use a file node to embed any vault note into a canvas board:

```json
{
  "id": "note1",
  "type": "file",
  "file": "Projects/Active/Sprint 12.md",
  "x": 0, "y": 0,
  "width": 300, "height": 400
}
```

The file node renders the note content inline on the board.
Clicking the node opens the note in an editor pane.

To embed only a section of a note, add a `subpath`:

```json
{
  "subpath": "#Summary"
}
```

## Using canvas as a MOC

A canvas board can serve as a visual MOC for a topic cluster:

1. Create a text node describing the topic.
2. Add file nodes for each note in the cluster.
3. Connect them with edges to show relationships.
4. Link the canvas from the topic MOC note using a wikilink.

In the topic MOC note:

```markdown
## Visual Map

See the [[Boards/Machine Learning Overview.canvas]] for the full relationship diagram.
```

## Linking from notes to canvas

Reference a canvas board from a note using a standard wikilink:

```markdown
[[Research Canvas.canvas]]
```

Obsidian resolves `.canvas` wikilinks and opens the board in Canvas view.

## Canvas in search and graph

Canvas files appear in the file explorer and search results.
They do not appear as nodes in the note graph view by default.
To include canvas boards in search: canvas content (text nodes and file node paths) is indexed by Obsidian search.

## Exporting canvas

Obsidian Canvas does not have a built-in export to image or PDF.
Third-party options:
- Take a screenshot with canvas fit-to-view (Shift+1) active.
- Use the Export Canvas community plugin for PNG export.
- Parse the `.canvas` JSON and render with a custom script using the jsoncanvas.org spec.

## Backup and version control

Canvas files are plain JSON and version-control cleanly.
Commit `.canvas` files to Git alongside vault notes.
JSON diffs are readable and merge conflicts can be resolved manually by inspecting node and edge IDs.
