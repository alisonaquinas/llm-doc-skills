# Wikilinks and Embeds

Obsidian uses double-bracket syntax for internal links and embeds.
These are called wikilinks and are the primary navigation primitive in Obsidian vaults.

## Wikilink syntax

| Syntax | Meaning |
| --- | --- |
| `[[Note Title]]` | Link to a note by title |
| `[[Note Title\|Display Text]]` | Link with custom visible text |
| `[[Note Title#Heading]]` | Link to a specific heading within a note |
| `[[Note Title#^block-id]]` | Link to a named block within a note |
| `[[folder/Note Title]]` | Disambiguate when multiple notes share a title |

Obsidian resolves wikilinks by title match across the entire vault, regardless of folder location.
When a link target is ambiguous, the shortest unique path wins.
On note rename, Obsidian updates all wikilinks automatically.

## Embed syntax

Prefix any wikilink with `!` to embed its content inline:

| Syntax | Meaning |
| --- | --- |
| `![[Note Title]]` | Embed the full note |
| `![[Note Title#Heading]]` | Embed from a heading to the next heading |
| `![[Note Title#^block-id]]` | Embed a single named block |
| `![[image.png]]` | Embed an image file |
| `![[file.pdf#page=3]]` | Embed a specific page of a PDF |
| `![[audio.mp3]]` | Embed an audio player |

## Block references

A block ID is a unique identifier appended to any paragraph or list item:

```markdown
This is the paragraph to reference. ^my-block-id
```

Block IDs must consist of only letters, numbers, and hyphens.
After adding a block ID, other notes can link directly to that block: `[[Note#^my-block-id]]`.

## Unresolved links

Wikilinks to notes that do not yet exist are shown in a distinct color in the rendered view.
Clicking an unresolved link creates the target note immediately.
Unresolved links appear in the graph view as disconnected nodes.
