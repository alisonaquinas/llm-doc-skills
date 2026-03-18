# GitLab Doc Patterns

GitLab-targeted Markdown should match the surface where it will live.
The strongest pages are readable in raw form, render clearly in GitLab, and make host-specific assumptions obvious.

## Docs and handbook pages

For long-form GitLab documentation:
- keep heading depth predictable
- prefer explicit relative links for project-local docs
- use admonitions only when emphasis changes reader action
- keep command examples fenced and runnable
- favor concise tables over wide comparison matrices

## Wiki and collaboration pages

For wiki pages, issues, and merge requests:
- use references that point to durable project artifacts
- avoid overloading the page with inline status decorations
- keep checklists actionable rather than descriptive only
- separate discussion context from evergreen documentation

## Portability caution

GitLab references, mentions, and embeds can lose meaning outside GitLab.
If the same Markdown must be published elsewhere, review:
- issue and merge request references
- mentions and cross-project links
- admonitions or embeds tied to GitLab rendering
- anchor assumptions that depend on host behavior
