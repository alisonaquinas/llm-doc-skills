# Rendering and Portability

GitLab Flavored Markdown is shaped by GitLab's product surfaces.
Local rendering is useful for structure checks, but it is not a perfect substitute for the live host.

## Preview paths

- use `cmark-gfm` for a quick structural preview when the source mostly uses GFM-compatible syntax
- use Pandoc for HTML, PDF, or DOCX export
- review on GitLab before finalizing content that depends on references, mentions, or embeds

## Portability boundaries

Expect differences when moving the same source elsewhere:
- references may stop resolving outside GitLab
- admonitions can flatten or change appearance
- embeds and host shortcuts can disappear entirely
- anchors and sanitization rules may differ

## Safe workflow

1. draft the source with standard Markdown structure
2. add GitLab-specific constructs where they serve a real docs or workflow need
3. preview locally for basic structure
4. confirm the final rendering on GitLab before exporting or copying elsewhere

## Troubleshooting prompts

If output diverges, check:
- whether the document relies on GitLab-only references
- whether the export path used `gfm` parsing for Markdown input
- whether admonitions or embeds were flattened in export
- whether the target surface has stricter sanitization or link behavior
