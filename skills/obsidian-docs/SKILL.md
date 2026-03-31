---
name: obsidian-docs
description: Use when a task involves Obsidian vault documentation, note organization,
  Maps of Content (MOC), index notes, inter-note navigation, graph view strategy,
  vault-wide search, or building and maintaining a local knowledge base in Obsidian.
---

# Obsidian Docs

## Intent Router

Load sections based on the task:

- Folder layout, MOC design, and index notes → `references/vault-structure-and-moc.md`
- Graph view, backlinks, search operators, and quick switcher → `references/navigation-and-discovery.md`
- Zettelkasten, PARA, evergreen notes, and daily note patterns → `references/knowledge-base-patterns.md`

## Overview

This skill covers documentation strategy and note organization inside a local Obsidian vault.
Use it for designing vault folder hierarchies, authoring Maps of Content, wiring inter-note navigation, and applying knowledge-base patterns such as Zettelkasten or PARA to an existing collection.

The guidance targets local vault workflows and assumes Obsidian desktop or mobile with the default file-system storage backend.

## Quick Start

```bash
# Open the Obsidian command palette and create a new MOC note
# Title: "000 Home" or "MOC - <Topic>"
# Add wikilinks to major topic clusters
```

```bash
# Search vault-wide for a term using Obsidian search (Ctrl+Shift+F / Cmd+Shift+F)
# Use path: and tag: operators to narrow results
# Example query: tag:#project path:Projects
```

## Preferred Workflow

1. Decide on a top-level folder structure before adding many notes — flat, PARA, or topic-based hierarchies each suit different workflows.
2. Create one index or MOC note per major topic cluster and link it from the vault home note.
3. Use wikilinks generously; unresolved links create new notes on click, which supports incremental growth.
4. Enable backlinks and outgoing-links panels to review connection density before reorganizing.
5. Audit orphan notes (no links in or out) periodically using the graph view local mode or a Dataview query.

## Authoring Guidance

This skill is the right fit for:

- designing or refactoring a vault folder hierarchy
- authoring MOC and index notes that act as navigation hubs
- linking daily notes into a larger topic graph
- deciding between flat versus nested folder strategies
- writing vault documentation conventions for a team or shared vault

## Navigation and Discovery

The graph view (Ctrl+G / Cmd+G) visualizes note relationships.
Use local graph on a single note to see its immediate neighbors.
Backlinks panel shows all notes that link to the current file.
Search operators include `path:`, `tag:`, `file:`, `line:`, and `block:` for precise queries.

## Official References

Primary sources:

- Obsidian help: <https://help.obsidian.md>
- Obsidian forum: <https://forum.obsidian.md>

Deep-dive references for this skill:

- `references/vault-structure-and-moc.md`
- `references/navigation-and-discovery.md`
- `references/knowledge-base-patterns.md`
