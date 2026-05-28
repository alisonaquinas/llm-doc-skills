# Creating Presentations with PptxGenJS

Use this guide when you are building a new deck from scratch or when the user
needs a generated presentation with repeatable layout rules.

## Setup check

Prefer a project-local install when writing a Node script that imports
PptxGenJS:

```bash
npm install pptxgenjs
node -e "require('pptxgenjs'); console.log('pptxgenjs ok')"
```

If PptxGenJS was installed globally, make sure Node can resolve global modules
before running `require("pptxgenjs")`:

```powershell
$env:NODE_PATH = npm root -g
node -e "require('pptxgenjs'); console.log('pptxgenjs ok')"
```

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
- Read [`effective-maintainable-decks.md`](effective-maintainable-decks.md)
  before generating a deck that must be edited, reused, co-authored, or opened
  reliably in Microsoft Office.

## Maintainability defaults

- Treat the generated `.pptx` as the editable source. Keep PDF, video, and image
  exports downstream from that source.
- Use familiar system fonts unless a supplied template or brand requirement says
  otherwise.
- Prefer native text, shapes, icons, charts, and tables over flattened images
  when content may be updated later.
- Give every slide one clear takeaway and a unique, useful title.
- Put presenter detail in notes with `slide.addNotes(...)` instead of crowding
  the visible slide.
- Keep components simple enough for PowerPoint desktop, PowerPoint for the web,
  and common import targets to preserve editability.
- Switch to template/XML editing when true slide masters, placeholder reuse, or
  exact brand-template preservation matters more than scratch generation speed.

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
