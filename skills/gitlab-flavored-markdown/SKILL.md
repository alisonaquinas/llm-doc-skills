---
name: gitlab-flavored-markdown
description: Use when a task involves GitLab Flavored Markdown, GitLab docs or wiki pages, merge request or issue formatting, GitLab references, admonitions, or GitLab-specific Markdown review and export workflows.
---

# GitLab Flavored Markdown

## Intent Router

Load sections based on the task:
- Syntax and GitLab extension coverage -> `references/glfm-syntax-matrix.md`
- Wiki, docs, issues, and merge request patterns -> `references/gitlab-doc-patterns.md`
- Rendering, portability, and export caveats -> `references/rendering-and-portability.md`

## Overview

This skill covers Markdown that must behave well on GitLab surfaces.
Use it for GitLab docs pages, wikis, issues, merge requests, snippets, and Markdown that depends on GitLab-specific extensions or rendering expectations.

The guidance follows GitLab's official Markdown documentation and platform-specific authoring behaviors.

## Quick Start

```bash
python gitlab-flavored-markdown/scripts/render.py handbook.md --to html --output handbook.html
```

```bash
python gitlab-flavored-markdown/scripts/render.py proposal.md --to docx --output proposal.docx --toc
```

## Preferred Workflow

1. Write clear Markdown first, then layer in GitLab-specific constructs only where the target surface benefits.
2. Keep issue references, admonitions, and embeds purposeful rather than decorative.
3. Treat GitLab rendering behavior as a host contract, especially for docs and wiki features.
4. Use local preview for structure checks and final GitLab review for host-specific rendering.
5. Audit portability before exporting to formats that do not share GitLab semantics.

## Authoring Guidance

This skill is the right fit for:
- GitLab documentation and handbook pages
- wiki content and long-form project notes
- issue and merge request descriptions
- GitLab references, admonitions, and embeds
- Markdown that must survive GitLab rendering rules

## Rendering and Export

HTML preview can use `cmark-gfm` for fast local structure checks or Pandoc when a fuller export path is needed.
DOCX and PDF export should route through Pandoc, with a review for GitLab-specific constructs.

```bash
pandoc handbook.md --from gfm --to html --output handbook.html
pandoc proposal.md --from gfm --to pdf --output proposal.pdf
```

## Portability and Troubleshooting

Common issues include assuming GitLab-specific references or admonitions will carry cleanly to GitHub, expecting exported output to preserve platform behavior, and relying on embeds that do not exist outside GitLab.
Reduce the source to a small sample when renderer differences are unclear.

## Official References

Primary sources:
- GitLab Markdown documentation: <https://docs.gitlab.com/user/markdown/>
- GitLab docs site guidance: <https://docs.gitlab.com/development/documentation/styleguide/>

Deep-dive references for this skill:
- `references/glfm-syntax-matrix.md`
- `references/gitlab-doc-patterns.md`
- `references/rendering-and-portability.md`
