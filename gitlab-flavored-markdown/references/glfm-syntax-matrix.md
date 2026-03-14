# GLFM Syntax Matrix

GitLab Flavored Markdown builds on Markdown with GitLab-specific references and authoring affordances.
Use them when the target surface is GitLab and the extension supports review, navigation, or workflow clarity.

## Common GitLab-oriented patterns

- issue, merge request, and epic references
- quick mentions of users or groups where the surface supports them
- fenced code blocks with syntax hints
- tables, task lists, and autolinks
- admonition-style blocks documented by GitLab

## Host-dependent behavior

Some GitLab Markdown behavior depends on where the source renders:
- wiki pages and docs pages may support different conventions than issues
- references resolve against project or group context
- embeds and includes can be host-specific rather than portable Markdown

## Working guidance

Prefer plain Markdown structure where possible.
Use GitLab extensions to clarify workflow, not to hide essential content behind host magic.
When authoring portable material, isolate GitLab-only constructs so they are easy to revise for another host.

## Review checklist

- confirm references resolve in the intended project or group
- confirm admonitions match documented GitLab syntax
- confirm tables and code fences stay readable in diff views
- confirm any GitLab-only embeds are acceptable to drop in exported output
