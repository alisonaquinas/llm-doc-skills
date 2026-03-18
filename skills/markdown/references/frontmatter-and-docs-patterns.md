# Frontmatter and Docs Patterns

Credible references:
- CommonMark spec for core syntax: <https://spec.commonmark.org/current/>
- GFM spec for repository-hosted docs: <https://github.github.com/gfm/>

## Common document shapes

- README files for repository onboarding
- reference docs with stable heading hierarchies
- changelogs and release notes
- operational runbooks with fenced commands
- docs-site pages that begin with frontmatter

## Frontmatter guidance

Frontmatter is not part of CommonMark itself, so treat it as a tooling-layer contract.
Keep key ordering, quoting, and required fields aligned to the host system rather than assuming portability.

## Structural guidance

- Keep one H1 per document.
- Use fenced code blocks with language labels.
- Keep tables narrow enough to remain diffable.
- Prefer relative links for same-repo documentation.
- Prefer task lists only when progress semantics matter.
