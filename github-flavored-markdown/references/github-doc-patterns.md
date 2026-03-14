# GitHub Doc Patterns

Use GitHub-oriented Markdown intentionally.
The best repository docs read clearly in raw form, render cleanly on GitHub, and degrade gracefully in alternate renderers.

## README patterns

A strong README usually includes:
- one-sentence project summary near the top
- installation or quick-start commands in fenced blocks
- a compact feature or capability list
- contribution or development pointers
- links to deeper docs instead of overloading the landing page

## Repository doc patterns

For `/docs` content and contributor guides:
- keep heading hierarchy shallow and predictable
- use relative links for repo-local navigation
- prefer fenced code blocks with info strings
- keep tables compact enough to review in pull requests
- use alerts only where emphasis improves scanning

## Sanitization expectations

GitHub sanitizes HTML in many Markdown contexts.
That means inline HTML can help with layout, but it should not be the only way critical content is conveyed.
If a table, image, or note depends on raw HTML, verify the rendered result on the actual target surface.

## Export caution

When the same source must be published outside GitHub, audit:
- issue and pull request references
- alerts or callouts
- raw HTML blocks
- anchor assumptions tied to GitHub heading generation
