# API Reference

> Sources: [PptxGenJS docs](https://gitbrent.github.io/PptxGenJS/), [python-pptx docs](https://python-pptx.readthedocs.io/)

This is a quick lookup for the two libraries the skill recommends. Use
[`pptxgenjs.md`](pptxgenjs.md) for end-to-end guidance on building a deck
from scratch and [`editing.md`](editing.md) for the unpack/edit/pack flow
that uses python-pptx (or raw XML edits) on an existing deck.

## PptxGenJS (creating .pptx from scratch)

Install: `npm install -g pptxgenjs`

### Bootstrap

```javascript
const PptxGenJS = require("pptxgenjs");
const pptx = new PptxGenJS();

// Global presentation settings
pptx.layout = "LAYOUT_16x9";        // "LAYOUT_4x3", "LAYOUT_16x9", "LAYOUT_16x10", "LAYOUT_WIDE", custom
pptx.title  = "My Presentation";
pptx.subject = "Topic";
pptx.author  = "Name";
pptx.company = "Org";
pptx.theme = {
  headFontFace: "Aptos Display",
  bodyFontFace: "Aptos",
};

const slide = pptx.addSlide();      // Blank slide
pptx.writeFile({ fileName: "output.pptx" });   // Save (returns Promise)
```

### Slide master / layout

```text
pptx.defineSlideMaster({
  title: "MASTER_SLIDE",
  background: { color: "1E2761" },
  objects: [
    { rect: { x: 0, y: 6.9, w: "100%", h: 0.6, fill: { color: "003366" } } },
    { text: { text: "Confidential", options: { x: 0, y: 6.9, w: "100%", h: 0.6, align: "right", color: "FFFFFF", fontSize: 10 } } },
  ],
  slideNumber: { x: 0.5, y: 7.0, color: "FFFFFF", fontSize: 10 },
});

const slide = pptx.addSlide({ masterName: "MASTER_SLIDE" });
```

### addText(text, options)

```text
slide.addText("Hello", {
  x: 0.5, y: 0.5, w: 9, h: 1.5,   // inches (default unit)
  fontSize: 36,                     // pt
  fontFace: "Arial",
  bold: true,
  italic: true,
  underline: { style: "sng" },      // "sng", "dbl", "dotted", "dash", "wavy"
  color: "FFFFFF",                  // Hex, no "#"
  align: "center",                  // "left", "center", "right", "justify"
  valign: "middle",                 // "top", "middle", "bottom"
  fill: { color: "1E2761" },
  transparency: 0,                  // 0–100
  margin: 0,                        // pts, or [top, right, bottom, left]
  lineSpacingMultiple: 1.5,
  paraSpaceBefore: 6,               // pts
  paraSpaceAfter: 6,
  charSpacing: 2,                   // pts
  hyperlink: { url: "https://example.com", tooltip: "Link" },
  rotate: 45,                       // degrees
  wrap: true,
  autoFit: false,
  shrinkText: false,
  inset: 0,                         // pts
  lang: "en-US",
  isTextBox: false,
  line: { color: "888888", width: 1, dashType: "solid" },  // Text box border
  shadow: { type: "outer", angle: 45, blur: 3, offset: 2, color: "000000", opacity: 0.5 },
  // Rich text: pass array of objects
  // [{ text: "Bold ", options: { bold: true } }, { text: "Normal" }]
});
```

### addImage(options)

```text
slide.addImage({
  path: "image.png",                // File path (Node.js)
  // OR: data: "base64string",      // Base64-encoded image
  x: 1, y: 1, w: 4, h: 3,         // inches
  sizing: {                         // Optional: control fit
    type: "contain",                // "contain", "cover", "crop"
    x: 0, y: 0, w: 4, h: 3,
  },
  transparency: 0,                  // 0–100
  rotate: 0,
  rounding: false,                  // Rounded image (circle/oval)
  hyperlink: { url: "https://example.com" },
  altText: "Description",
  shadow: { type: "outer", angle: 45, blur: 3, offset: 2, color: "000000", opacity: 0.5 },
});
```

### addShape(shapeType, options)

```javascript
const { ShapeType } = require("pptxgenjs");

slide.addShape(pptx.ShapeType.rect, {
  x: 1, y: 1, w: 3, h: 2,
  fill: { color: "003366" },
  line: { color: "FFFFFF", width: 2, dashType: "solid" },
  transparency: 0,
  rotate: 0,
  shadow: { type: "outer", angle: 45, blur: 3, offset: 2, color: "000000", opacity: 0.5 },
});

// Common shapes: rect, roundRect, ellipse, triangle, rightArrow, leftArrow,
//                upArrow, downArrow, star5, star6, hexagon, cloud,
//                callout1, wedgeRectCallout, plus, cross, ribbon, bevel
```

### addTable(rows, options)

```text
slide.addTable(
  [
    [{ text: "Header", options: { bold: true, fill: { color: "003366" }, color: "FFFFFF" } }, "Col 2"],
    ["Row 1", "Data"],
    ["Row 2", "Data"],
  ],
  {
    x: 0.5, y: 1.5, w: 9, h: 4,
    colW: [4.5, 4.5],              // Per-column widths in inches (or single number)
    rowH: 0.5,                     // Uniform row height, or array per row
    border: { type: "solid", pt: 1, color: "CCCCCC" },
    fill: { color: "F5F5F5" },
    align: "left",
    valign: "middle",
    fontSize: 12,
    fontFace: "Arial",
    color: "000000",
    margin: 5,                     // pts, or [top, right, bottom, left]
    autoPage: false,               // Auto-paginate on overflow
    autoPageRepeatHeader: true,
    autoPageHeaderRows: 1,
    verbose: false,
  }
);
```

### addChart(type, data, options)

```text
slide.addChart(pptx.ChartType.bar, [
  { name: "Series 1", labels: ["Q1","Q2","Q3","Q4"], values: [10,20,30,40] },
  { name: "Series 2", labels: ["Q1","Q2","Q3","Q4"], values: [15,25,35,45] },
], {
  x: 1, y: 1, w: 8, h: 4,
  chartColors: ["003366","FF6600"],
  showLegend: true,
  legendPos: "b",                  // "t", "b", "l", "r", "tr"
  showTitle: true,
  title: "Revenue",
  titleFontSize: 16,
  showValue: false,
  dataLabelFontSize: 10,
  catAxisTitle: "Quarter",
  valAxisTitle: "USD ($mm)",
  valAxisMinVal: 0,
  valAxisMaxVal: 50,
  barGrouping: "clustered",        // "clustered", "stacked", "percentStacked"
  barDir: "col",                   // "col" (vertical), "bar" (horizontal)
  lineDataSymbol: "none",          // For line charts: "none", "circle", "square", "diamond"
});

// Chart types: pptx.ChartType.bar, line, pie, doughnut, area, scatter, bubble,
//              radar, stock, surface
```

### Coordinate system

| Unit | Notes |
|------|-------|
| Default | Inches |
| `"50%"` | Percentage of slide dimension |
| `{ unit: "emu", value: 914400 }` | EMU (914,400 = 1 inch) |

**Standard slide dimensions:**

- 16:9 → 10" × 7.5"
- 4:3 → 10" × 7.5" (same total, different aspect)
- Widescreen → 13.33" × 7.5"

---

## python-pptx (reading / editing existing .pptx)

> **Read [`editing.md`](editing.md) first.** python-pptx's full-presentation
> save normalizes the XML declaration and can break decks flagged by
> `check_fragility.py` — including in PowerPoint Desktop, not just Online.
> If the deck is fragile, use the byte-level surgical patch path in
> [`recovering-fragile-decks.md`](recovering-fragile-decks.md) instead.

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation("existing.pptx")
slide = prs.slides[0]
prs.save("output.pptx")
```

### Presentation

| Property | Type | Notes |
|----------|------|-------|
| `.slides` | `Slides` | Collection of slides |
| `.slide_width` / `.slide_height` | `Emu` | Overall dimensions |
| `.slide_layouts` | `SlideLayouts` | Available layouts |
| `.slide_masters` | `SlideMasters` | Master slides |
| `.core_properties` | `CoreProperties` | Title, author, etc. |

### Slide

```text
layout = prs.slide_layouts[1]          # Title and Content layout
slide = prs.slides.add_slide(layout)
```

| Property | Type |
|----------|------|
| `.shapes` | `ShapeCollection` |
| `.placeholders` | `PlaceholderCollection` |
| `.notes_slide` | `NotesSlide` |
| `.slide_layout` | `SlideLayout` |
| `.background` | `Background` |

### Shape

```text
shape = slide.shapes.add_textbox(Inches(1), Inches(1), Inches(4), Inches(2))
shape = slide.shapes.add_picture("img.png", Inches(1), Inches(1), Inches(3), Inches(2))
shape = slide.shapes.add_shape(MSO_SHAPE_TYPE.RECTANGLE, Inches(1), Inches(1), Inches(2), Inches(1))
shape = slide.shapes.add_table(3, 4, Inches(1), Inches(1), Inches(6), Inches(3)).table
```

| Property | Type | Notes |
|----------|------|-------|
| `.left`, `.top`, `.width`, `.height` | `Emu` | Position & size |
| `.name` | `str` | Shape name |
| `.shape_type` | `MSO_SHAPE_TYPE` | |
| `.text_frame` | `TextFrame` | For text shapes |
| `.fill` | `FillFormat` | |
| `.line` | `LineFormat` | |
| `.has_text_frame` | `bool` | |

### TextFrame and runs

```text
tf = shape.text_frame
tf.word_wrap = True
tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE

para = tf.paragraphs[0]
para.alignment = PP_ALIGN.CENTER
run = para.add_run()
run.text = "Hello"
run.font.bold = True
run.font.size = Pt(24)
run.font.color.rgb = RGBColor(0xFF, 0x00, 0x00)
```

### OOXML unit conversions

| Unit | Emu | Python |
|------|-----|--------|
| 1 inch | 914,400 | `Inches(1)` |
| 1 cm | 360,000 | `Cm(1)` |
| 1 pt | 12,700 | `Pt(1)` |
| Slide 16:9 width | 9,144,000 | `Inches(10)` |
| Slide 16:9 height | 6,858,000 | `Inches(7.5)` |
