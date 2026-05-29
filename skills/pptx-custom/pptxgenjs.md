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

## Brand/theme inputs

When the user supplies branding, colors, typography, footer rules, or reusable
layout direction, encode those decisions before adding slides. A branded deck
should not be a set of individually styled slides.

Use `pptx.theme` for the deck's heading and body fonts, and use
`pptx.defineSlideMaster(...)` for repeated backgrounds, color bars, logos,
footer text, page furniture, slide numbers, and common layout geometry.

```javascript
const brand = {
  primary: "0F766E",
  accent: "F59E0B",
  dark: "0F172A",
  light: "F8FAFC",
  headingFont: "Aptos Display",
  bodyFont: "Aptos",
};

pptx.theme = {
  headFontFace: brand.headingFont,
  bodyFontFace: brand.bodyFont,
};

pptx.defineSlideMaster({
  title: "BRAND_TITLE",
  background: { color: brand.dark },
  objects: [
    {
      rect: {
        x: 0,
        y: 0,
        w: "100%",
        h: 0.18,
        fill: { color: brand.accent },
        line: { color: brand.accent },
      },
    },
    {
      text: {
        text: "ACME STRATEGY",
        options: {
          x: 0.5,
          y: 6.95,
          w: 4,
          h: 0.25,
          fontFace: brand.bodyFont,
          fontSize: 10,
          bold: true,
          color: "CBD5E1",
          margin: 0,
        },
      },
    },
  ],
  slideNumber: { x: 12.2, y: 6.95, color: "CBD5E1", fontSize: 9 },
});

pptx.defineSlideMaster({
  title: "BRAND_CONTENT",
  background: { color: brand.light },
  objects: [
    {
      rect: {
        x: 0,
        y: 0,
        w: "100%",
        h: 0.16,
        fill: { color: brand.primary },
        line: { color: brand.primary },
      },
    },
    {
      text: {
        text: "ACME",
        options: {
          x: 0.5,
          y: 6.95,
          w: 1,
          h: 0.25,
          fontFace: brand.bodyFont,
          fontSize: 10,
          bold: true,
          color: brand.primary,
          margin: 0,
        },
      },
    },
  ],
  slideNumber: { x: 12.25, y: 6.95, color: brand.primary, fontSize: 9 },
});

const titleSlide = pptx.addSlide({ masterName: "BRAND_TITLE" });
titleSlide.addText("Brand inputs become deck infrastructure", {
  x: 0.65,
  y: 1,
  w: 11.5,
  h: 0.8,
  fontFace: brand.headingFont,
  fontSize: 34,
  bold: true,
  color: brand.light,
});

const contentSlide = pptx.addSlide({ masterName: "BRAND_CONTENT" });
contentSlide.addText("Use masters for repeated brand furniture", {
  x: 0.6,
  y: 0.6,
  w: 10,
  h: 0.5,
  fontFace: brand.headingFont,
  fontSize: 28,
  bold: true,
  color: "111827",
});
```

Rules for branded scratch decks:

- Define all masters before adding slides, then create slides with
  `pptx.addSlide({ masterName: "..." })`.
- Create a small set of useful masters: title, section divider, content,
  comparison, dashboard, and appendix only when needed.
- Put repeated brand furniture on masters. Keep individual slides limited to
  unique content and intentional one-off exceptions.
- Use `pptx.theme` for heading/body fonts. PptxGenJS exposes theme-color tokens
  for object styling, but its scratch theme API is strongest for fonts; if an
  exact corporate theme color palette must be preserved, start from a `.pptx` or
  `.potx` template and use the XML editing workflow.
- Do not set `slide.background` or duplicate logos/footer shapes on every slide
  when a master can carry that work.

## Brand/theme verification

Visual review is necessary but not sufficient for branded decks. After
generation, unpack the file and verify that theme and master/layout parts carry
the reusable decisions:

```bash
python office-custom/scripts/unpack.py branded.pptx unpacked/ --merge-runs false
rg -n "BRAND_|Aptos|0F766E|F59E0B" unpacked/ppt/theme unpacked/ppt/slideLayouts unpacked/ppt/slideMasters
rg -n "slideLayout" unpacked/ppt/slides/_rels
python pptx-custom/scripts/thumbnail.py branded.pptx branded-contact-sheet.jpg --cols 4 --dpi 120
```

Confirm these signals:

- `ppt/theme/theme1.xml` contains the requested heading and body fonts.
- PptxGenJS `defineSlideMaster(...)` output appears in
  `ppt/slideLayouts/slideLayout*.xml`, with relationships back to
  `ppt/slideMasters/slideMaster*.xml`.
- Each branded slide's relationship file points at the intended slide layout.
- Recurring backgrounds, bars, logos, footers, and slide numbers are not copied
  as ordinary shapes onto every slide.

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
- Use `defineSlideMaster(...)` when brand or theme inputs imply repeated
  backgrounds, furniture, or layout rules.
- Switch to template/XML editing when placeholder reuse, exact brand-template
  preservation, or exact custom theme color palettes matter more than scratch
  generation speed.

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
