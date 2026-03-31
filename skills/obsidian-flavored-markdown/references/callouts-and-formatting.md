# Callouts and Formatting

Obsidian callouts extend the blockquote syntax with typed, optionally collapsible highlighted blocks.

## Callout syntax

```markdown
> [!TYPE] Optional Title
> Body content here.
> Multiple lines are fine.
```

The TYPE is case-insensitive. If no title is given, the type name is used as the title.

## Callout types

| Type | Aliases | Typical use |
| --- | --- | --- |
| `note` | — | General annotations |
| `info` | — | Informational asides |
| `tip` | `hint`, `important` | Helpful suggestions |
| `warning` | `caution`, `attention` | Cautionary notes |
| `danger` | `error` | Errors or critical warnings |
| `success` | `check`, `done` | Confirmations |
| `question` | `help`, `faq` | Open questions |
| `example` | — | Examples and samples |
| `quote` | `cite` | Quoted material |
| `abstract` | `summary`, `tldr` | Summaries |
| `bug` | — | Known issues |
| `todo` | — | Action items |

## Collapsible callouts

Add `-` after the type to collapse by default; add `+` to expand by default:

```markdown
> [!NOTE]- Collapsed by default
> Body only visible after clicking.

> [!TIP]+ Expanded by default
> Body visible immediately, but can be collapsed.
```

## Nested callouts

Callouts can be nested by increasing the blockquote depth:

```markdown
> [!INFO] Outer callout
> Outer content.
>> [!WARNING] Inner callout
>> Inner content.
```

## OFM comment blocks

Obsidian supports inline comment syntax that hides content from the rendered preview:

```markdown
%% This text is hidden in preview mode. %%

%%
Multi-line comments are also supported.
They are not exported or rendered.
%%
```

Comments are visible in source mode and useful for authoring notes, TODOs, or metadata not intended for readers.

## Strikethrough and highlights

```markdown
~~strikethrough text~~
==highlighted text==
```

Highlights (`==`) are an OFM extension and do not render in standard Markdown tools.
