# Rendering and Portability

GitHub Flavored Markdown is a host-targeted dialect, not a universal interchange format.
Plan rendering and export around that fact.

## Preview paths

- use `cmark-gfm` for quick HTML rendering close to the spec
- use Pandoc when exporting to PDF or DOCX
- use the live GitHub renderer when sanitization or repository references matter

## Portability boundaries

Some source features will not carry cleanly into every renderer:
- task list interactivity becomes static markup outside GitHub
- repository references may lose meaning in exported artifacts
- alerts and some HTML patterns may flatten into plain blockquotes or raw text
- heading anchors may differ across hosts

## Safe workflow

1. render a local preview
2. review any GitHub-only constructs
3. export through Pandoc only after the source is stable
4. spot-check the final artifact rather than assuming renderer parity

## Troubleshooting prompts

If output diverges, check:
- whether the parser is using `gfm` versus plain CommonMark
- whether HTML is being sanitized or stripped
- whether the export path preserved tables and fenced code blocks
- whether source links or references assume a GitHub repository context
