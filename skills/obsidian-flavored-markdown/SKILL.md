---
name: obsidian-flavored-markdown
description: Use when a task involves Obsidian Flavored Markdown syntax including
  wikilinks, embedded files, callouts, inline tags, YAML frontmatter properties,
  block references, aliases, or Obsidian comment blocks.
---

# Obsidian Flavored Markdown

## Intent Router

Load sections based on the task:

- Wikilinks, embeds, block references, and link aliases → `references/wikilinks-and-embeds.md`
- Callout syntax, collapsible blocks, and OFM-specific formatting → `references/callouts-and-formatting.md`
- YAML frontmatter properties, inline tags, aliases, and tag hierarchies → `references/properties-and-tags.md`

## Overview

This skill covers the Markdown dialect used inside Obsidian vaults.
Obsidian Flavored Markdown extends CommonMark with wikilinks, file embeds, block references, callouts, frontmatter properties, and comment syntax.

Use it when authoring notes that rely on OFM-specific features, auditing notes for portability outside Obsidian, or converting between OFM and standard Markdown formats.

## Quick Start

```markdown
# Wikilink examples
[[Note Title]]                    links to a note by title
[[Note Title|Display Text]]       link with custom display text
[[Note Title#Section Heading]]    link to a specific heading
[[Note Title#^block-id]]          link to a named block

# Embed examples
![[Note Title]]                   embed entire note inline
![[image.png]]                    embed an image
![[Note Title#Section Heading]]   embed a specific section
```

```markdown
# Callout examples
> [!NOTE] Optional title
> Callout body text here.

> [!WARNING]- Collapsible warning
> This callout is collapsed by default.

> [!TIP]+ Expanded tip
> This callout starts expanded.
```

## Preferred Workflow

1. Use wikilinks (`[[...]]`) for all internal note references rather than standard Markdown links, since Obsidian tracks and updates wikilinks on rename.
2. Prefer embed syntax (`![[...]]`) to inline repeated content — it stays in sync with the source note.
3. Define block IDs (`^block-id`) at the end of a paragraph when a specific block needs to be linked or embedded from other notes.
4. Use callouts for highlighted information rather than raw blockquotes; callout types carry semantic meaning that appears visually in the rendered view.
5. Keep frontmatter properties minimal and typed consistently — mixed types for the same property across notes break Dataview queries.

## Authoring Guidance

This skill is the right fit for:

- authoring notes that use wikilinks, embeds, and block references
- writing or converting callout blocks for notes, documentation, or MOCs
- defining frontmatter property schemas for a vault
- auditing OFM-specific syntax before exporting notes to a non-Obsidian system
- using inline tags and nested tag hierarchies for note classification

## Portability Notes

OFM-specific features do not render in standard Markdown tools.
Wikilinks become broken text in GitHub, VS Code preview, and most static site generators unless a preprocessor converts them.
Callouts render as plain blockquotes outside Obsidian.
When exporting OFM notes for external publishing, run a conversion pass to replace wikilinks with relative Markdown links and callouts with equivalent markup.

## Official References

Primary sources:

- Obsidian Flavored Markdown: <https://help.obsidian.md/obsidian-flavored-markdown>
- Obsidian callouts: <https://help.obsidian.md/Editing+and+formatting/Callouts>
- Obsidian properties: <https://help.obsidian.md/Editing+and+formatting/Properties>

Deep-dive references for this skill:

- `references/wikilinks-and-embeds.md`
- `references/callouts-and-formatting.md`
- `references/properties-and-tags.md`
