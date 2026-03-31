# Properties and Tags

## Frontmatter properties

YAML frontmatter at the top of a note defines properties (also called metadata).
Obsidian parses frontmatter and displays it in the Properties panel.

```yaml
---
title: My Note Title
date: 2025-01-15
tags:
  - project
  - reference
aliases:
  - My Note
  - Alt Title
cssclass: wide-table
status: active
priority: 2
---
```

## Property types

Obsidian infers property types from values and allows manual type assignment in the Properties view:

| Type | Example value | Notes |
| --- | --- | --- |
| Text | `"My text"` | Default for unrecognized values |
| List | `[item1, item2]` | Array of text values |
| Number | `42` | Integer or float |
| Checkbox | `true` / `false` | Boolean |
| Date | `2025-01-15` | ISO 8601 format |
| Date & time | `2025-01-15T10:30` | ISO 8601 with time |

Keep property types consistent across all notes in a vault. Mixed types for the same key break Dataview queries and the Properties panel.

## Built-in properties

| Property | Purpose |
| --- | --- |
| `tags` | Note tags; also accepts `tag:` singular form |
| `aliases` | Alternative names for wikilink resolution |
| `cssclass` | CSS class(es) applied to the note view |

## Inline tags

Tags can appear anywhere in the note body with a `#` prefix:

```markdown
This note covers #machine-learning and #python topics.
```

Tags must not contain spaces. Use hyphens or underscores for multi-word tags.

## Tag hierarchies

Use forward slashes to create nested tags:

```markdown
#project/active
#project/archived
#lang/python
#lang/go
```

Tag hierarchies appear as trees in the Tags panel and support parent-level filtering.
Searching `tag:#project` matches both `#project/active` and `#project/archived`.

## Aliases

The `aliases` property lists alternative names for a note that wikilinks can resolve to:

```yaml
---
aliases:
  - ML
  - Machine Learning Basics
---
```

After setting aliases, `[[ML]]` links to this note even though the filename differs.
