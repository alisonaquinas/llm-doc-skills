# AGENTS.md

Guidance for agent runtimes working with `llm-doc-skills` content. The repo is
packaged for both Claude and OpenAI agents, so this file stays platform-neutral
and focuses on when to use direct tools versus delegated agents.

## Use Direct Tools First

Prefer direct search and file reads for small tasks.

| Task | Preferred tool |
| --- | --- |
| Find a file | `Glob` or `rg --files` |
| Search text | `Grep` or `rg` |
| Read one file | `Read` |
| Compare two files | `diff` |

Do not delegate a trivial search that can be answered immediately.

```text
Wrong: "Use Explore to find references to recalc.py"
Right: Grep pattern="recalc\.py" path="/Users/allisonaquinas/llm-doc-skills"
```

## Good Uses for Delegated Agents

### Explore agent

Use for unfamiliar or cross-skill investigation:

- how `office-custom/scripts/` supports both `docx-custom` and `pptx-custom`
- where LibreOffice wrappers are reused
- how a pattern varies across multiple skill directories

### Plan agent

Use for multi-file or strategic changes:

- consolidating repeated workflows
- changing archive layout or packaging rules
- deciding between rebuild versus XML-edit workflows

### Review-oriented agents

Use a review or failure-hunting agent after substantial edits to:

- catch missing tests or regressions
- check error handling around conversion scripts
- validate large documentation changes for clarity and consistency

## Visual QA for Presentations

Presentation QA benefits from fresh eyes. When the repo generates or edits a
deck, use a separate agent for visual inspection after rendering slides to
images.

```text
1. Build or edit the deck
2. Render with `python pptx-custom/scripts/thumbnail.py file.pptx`
3. Ask another agent to inspect the rendered slides for overflow, overlap,
   spacing, contrast, or placeholder artifacts
4. Fix and repeat until the QA pass is clean
```

## Research Workflow

Read the skill docs before delegating broader exploration.

```text
1. Read `docx-custom/SKILL.md`
2. Read `office-custom/SKILL.md` if the task touches OOXML internals
3. Delegate only what remains unclear
```

Good follow-up prompt:

```text
"I've read `docx-custom/SKILL.md`. Explore whether `pptx-custom` uses the same
unpack/edit/repack pattern and summarize the differences."
```

## Delegation Checklist

Only delegate when all of these are true:

- the task is not trivial
- the goal is specific and bounded
- you have already done the obvious local reading
- the delegated work is independent or meaningfully parallel
- the selected agent type matches the task

Default behavior: use direct tools first, then delegate only when another pass
will add real value.
