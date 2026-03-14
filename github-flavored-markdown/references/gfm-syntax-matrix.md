# GFM Syntax Matrix

GitHub Flavored Markdown extends CommonMark with a practical set of repository-focused features.
Use these extensions when the target surface is GitHub and the added structure improves readability or workflow.

## Core extensions

- tables for tabular docs and comparison grids
- task list items for checklists and release work
- autolink literals for bare URLs
- strikethrough for change tracking in prose
- tagfilter behavior for raw HTML safety

## GitHub-native patterns

GitHub also supports platform conventions that live beside the spec:
- issue and pull request references such as `#123`
- commit SHA references where context makes them useful
- repository references such as `owner/repo#123`
- alerts in supported docs contexts using blockquote markers

## Working guidance

Prefer headings, lists, and code fences that remain understandable outside GitHub.
Reach for GFM tables only when columnar structure matters.
Treat task lists as workflow state, not decorative bullets.
Keep raw HTML limited because host sanitization may trim unsupported tags or attributes.

## Review checklist

- confirm tables remain legible on narrow screens
- confirm task lists are intentional and not copied from plain bullets
- confirm references are meaningful outside the current repository when exported
- confirm alerts or HTML blocks degrade acceptably in non-GitHub renderers
