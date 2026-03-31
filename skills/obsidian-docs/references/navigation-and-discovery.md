# Navigation and Discovery

Obsidian provides several overlapping navigation tools.
Combine them rather than relying on folder browsing alone.

## Graph view

Open with Ctrl+G (Cmd+G on macOS).
The global graph shows every note and link as a force-directed diagram.
Local graph (accessible from the note menu) shows only the current note and its immediate neighbors.

Useful graph settings:

- **Depth**: increase to see second- and third-degree connections.
- **Filters**: restrict to a folder, tag, or file name pattern.
- **Groups**: color-code notes by path or tag for visual clustering.

Orphan nodes (no links) often signal notes that need to be integrated or deleted.

## Backlinks and outgoing links

The backlinks panel lists every note that links to the current file.
Outgoing links panel lists every wikilink in the current note, including unresolved ones.
Both panels are in the right sidebar and update as notes are edited.

## Search operators

| Operator | Example | Matches |
| --- | --- | --- |
| `tag:` | `tag:#project` | notes tagged #project |
| `path:` | `path:Projects/` | notes inside Projects/ folder |
| `file:` | `file:meeting` | file names containing "meeting" |
| `line:` | `line:TODO` | lines containing "TODO" |
| `block:` | `block:summary` | block content containing "summary" |

Combine operators: `tag:#active path:Projects` finds active notes inside Projects.

## Quick switcher

Open with Ctrl+O (Cmd+O).
Type any part of a note title to navigate directly.
The switcher also creates new notes when no match exists.

## Command palette

Open with Ctrl+P (Cmd+P).
Searches all available commands including plugin commands.
Assign hotkeys to frequently used commands from Settings → Hotkeys.
