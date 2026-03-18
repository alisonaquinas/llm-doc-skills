# Creating Presentations with PptxGenJS

Use this guide when you are building a new deck from scratch or when the user
needs a generated presentation with repeatable layout rules.

## Starting point

```javascript
const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "llm-doc-skills";
pptx.subject = "Generated presentation";
pptx.title = "Project Update";

const slide = pptx.addSlide();
slide.background = { color: "1E2761" };
slide.addText("Project Update", {
  x: 0.5,
  y: 0.4,
  w: 8.5,
  h: 0.6,
  fontFace: "Georgia",
  fontSize: 26,
  bold: true,
  color: "FFFFFF",
});

slide.addText("Key outcomes and next steps", {
  x: 0.5,
  y: 1.2,
  w: 5.5,
  h: 0.5,
  fontFace: "Calibri",
  fontSize: 16,
  color: "CADCFC",
});

pptx.writeFile({ fileName: "project-update.pptx" });
```

## Layout guidance

- Use `LAYOUT_WIDE` unless the user explicitly asks for a 4:3 deck.
- Set a clear theme early: one dominant color, one support color, and one
  accent.
- Keep text boxes generous enough to survive font substitution on other
  systems.
- Prefer a few intentional layout motifs over repeating plain bullet slides.

## Useful building blocks

- `slide.addText(...)` for headings, callouts, and body copy
- `slide.addShape(...)` for cards, dividers, and color blocks
- `slide.addImage(...)` for screenshots, icons, and photography
- `slide.addTable(...)` for structured comparisons
- `slide.addNotes(...)` when speaker notes are part of the deliverable

## QA requirement

Always render the finished deck and inspect it visually:

```bash
python pptx-custom/scripts/thumbnail.py project-update.pptx
```

If the deck is client-facing, also convert it to PDF and inspect the full-size
pages before delivery.

## When to switch to XML editing

- The deck must preserve an existing master/theme exactly.
- The user supplied a `.pptx` template with non-trivial placeholders.
- Only a few slides need surgical edits and rebuilding the deck would be
  slower.

Use [`editing.md`](editing.md) for that workflow.
