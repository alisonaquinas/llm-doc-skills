# CommonMark and GFM

Authoritative sources:
- CommonMark specification: <https://spec.commonmark.org/current/>
- GitHub Flavored Markdown specification: <https://github.github.com/gfm/>

## Default target for this repo

This skill treats CommonMark plus GitHub Flavored Markdown as the default practical target.
That means core CommonMark parsing plus GFM extensions such as:
- tables
- task lists
- autolinks
- strikethrough

## Routing guidance

Prefer this skill when the task is about Markdown source semantics, README structure, fenced examples, links, tables, or docs writing conventions.
Prefer `pandoc` when the task becomes a cross-format publishing pipeline.

## Example contrast

```md
| Column | Value |
| --- | --- |
| Task | Done |
```

```md
- [x] Draft
- [ ] Review
```
