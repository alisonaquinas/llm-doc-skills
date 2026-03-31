# Core Templates Reference

The Core Templates plugin is built into Obsidian and provides basic variable substitution when inserting a template file into a note.

## Enabling and configuring

1. Settings → Core Plugins → Templates → toggle on.
2. Settings → Templates → set **Template folder location** (e.g., `Templates`).
3. Optionally set a date format and time format using Moment.js tokens.

## Available variables

| Variable | Output |
| --- | --- |
| `{{title}}` | Title of the note the template is inserted into |
| `{{date}}` | Current date using the configured date format |
| `{{time}}` | Current time using the configured time format |
| `{{date:FORMAT}}` | Date with an inline Moment.js format override |
| `{{time:FORMAT}}` | Time with an inline Moment.js format override |

## Common Moment.js format tokens

| Token | Output example |
| --- | --- |
| `YYYY` | 2025 |
| `MM` | 01 |
| `DD` | 15 |
| `ddd` | Wed |
| `HH` | 14 |
| `mm` | 30 |
| `W` | Week number (1–52) |

Example usage:

```markdown
---
date: {{date:YYYY-MM-DD}}
week: {{date:W}}
---
```

## Inserting a template

- Command palette: `Templates: Insert template` → select template file.
- Assign a hotkey in Settings → Hotkeys → search "Insert template".

## Limitations

Core Templates only substitutes variables at insert time.
It does not support scripting, conditional logic, user input prompts, or file system operations.
For those capabilities, use the Templater community plugin instead.
