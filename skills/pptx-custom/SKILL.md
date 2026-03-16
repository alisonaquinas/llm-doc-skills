---
name: pptx-custom
description: "Use this skill any time a .pptx file is involved in any way — as input, output, or both. This includes: creating slide decks, pitch decks, or presentations; reading, parsing, or extracting text from any .pptx file (even if the extracted content will be used elsewhere, like in an email or summary); editing, modifying, or updating existing presentations; combining or splitting slide files; working with templates, layouts, speaker notes, or comments. Trigger whenever the user mentions \"deck,\" \"slides,\" \"presentation,\" or references a .pptx filename, regardless of what they plan to do with the content afterward. If a .pptx file needs to be opened, created, or touched, use this skill."
---

# PPTX Skill

## Intent Router

Load sections based on the task:
- **Create from scratch** → Read [pptxgenjs.md](pptxgenjs.md) for color
  palettes, typography, and design principles; use the PptxGenJS library
- **Edit existing presentation** → Read [editing.md](editing.md) for the
  unpack/edit/pack workflow and slide manipulation patterns
- **Extract/analyze content** → Use markitdown or thumbnail.py from "Reading Content"
- **Design guidance** → "Design Ideas" section for color palettes, typography, spacing, and anti-patterns
- **Visual QA** → "QA (Required)" section for converting to images and inspection workflow
- **Converting to images** → "Converting to Images" section for pdftoppm workflow

## Quick Reference

| Task | Guide |
|------|-------|
| Read/analyze content | `python -m markitdown presentation.pptx` |
| Edit or create from template | Read [editing.md](editing.md) |
| Create from scratch | Read [pptxgenjs.md](pptxgenjs.md) |

---

## Reading Content

```bash
# Text extraction
python -m markitdown presentation.pptx

# Visual overview
python pptx-custom/scripts/thumbnail.py presentation.pptx

# Raw XML
python office-custom/scripts/unpack.py presentation.pptx unpacked/
```

---

## Editing Workflow

**Read [editing.md](editing.md) for full details.**

1. Analyze template with `thumbnail.py`
2. Unpack → manipulate slides → edit content → clean → pack

---

## Creating from Scratch

**Read [pptxgenjs.md](pptxgenjs.md) for full details.**

Use when no template or reference presentation is available.

---

## Design Ideas

**Don't create boring slides.** Plain bullets on a white background won't impress anyone. Consider ideas from this list for each slide.

### Before Starting

- **Pick a bold, content-informed color palette**: The palette should feel designed for THIS topic. If swapping your colors into a completely different presentation would still "work," you haven't made specific enough choices.
- **Dominance over equality**: One color should dominate (60-70% visual weight), with 1-2 supporting tones and one sharp accent. Never give all colors equal weight.
- **Dark/light contrast**: Dark backgrounds for title + conclusion slides, light for content ("sandwich" structure). Or commit to dark throughout for a premium feel.
- **Commit to a visual motif**: Pick ONE distinctive element and repeat it — rounded image frames, icons in colored circles, thick single-side borders. Carry it across every slide.

### Color Palettes

Choose colors that match your topic — don't default to generic blue. Use these palettes as inspiration:

| Theme | Primary | Secondary | Accent |
|-------|---------|-----------|--------|
| **Midnight Executive** | `1E2761` (navy) | `CADCFC` (ice blue) | `FFFFFF` (white) |
| **Forest & Moss** | `2C5F2D` (forest) | `97BC62` (moss) | `F5F5F5` (cream) |
| **Coral Energy** | `F96167` (coral) | `F9E795` (gold) | `2F3C7E` (navy) |
| **Warm Terracotta** | `B85042` (terracotta) | `E7E8D1` (sand) | `A7BEAE` (sage) |
| **Ocean Gradient** | `065A82` (deep blue) | `1C7293` (teal) | `21295C` (midnight) |
| **Charcoal Minimal** | `36454F` (charcoal) | `F2F2F2` (off-white) | `212121` (black) |
| **Teal Trust** | `028090` (teal) | `00A896` (seafoam) | `02C39A` (mint) |
| **Berry & Cream** | `6D2E46` (berry) | `A26769` (dusty rose) | `ECE2D0` (cream) |
| **Sage Calm** | `84B59F` (sage) | `69A297` (eucalyptus) | `50808E` (slate) |
| **Cherry Bold** | `990011` (cherry) | `FCF6F5` (off-white) | `2F3C7E` (navy) |

### For Each Slide

**Every slide needs a visual element** — image, chart, icon, or shape. Text-only slides are forgettable.

**Layout options:**
- Two-column (text left, illustration on right)
- Icon + text rows (icon in colored circle, bold header, description below)
- 2x2 or 2x3 grid (image on one side, grid of content blocks on other)
- Half-bleed image (full left or right side) with content overlay

**Data display:**
- Large stat callouts (big numbers 60-72pt with small labels below)
- Comparison columns (before/after, pros/cons, side-by-side options)
- Timeline or process flow (numbered steps, arrows)

**Visual polish:**
- Icons in small colored circles next to section headers
- Italic accent text for key stats or taglines

### Typography

**Choose an interesting font pairing** — don't default to Arial. Pick a header font with personality and pair it with a clean body font.

| Header Font | Body Font |
|-------------|-----------|
| Georgia | Calibri |
| Arial Black | Arial |
| Calibri | Calibri Light |
| Cambria | Calibri |
| Trebuchet MS | Calibri |
| Impact | Arial |
| Palatino | Garamond |
| Consolas | Calibri |

| Element | Size |
|---------|------|
| Slide title | 36-44pt bold |
| Section header | 20-24pt bold |
| Body text | 14-16pt |
| Captions | 10-12pt muted |

### Spacing

- 0.5" minimum margins
- 0.3-0.5" between content blocks
- Leave breathing room—don't fill every inch

### Avoid (Common Mistakes)

- **Don't repeat the same layout** — vary columns, cards, and callouts across slides
- **Don't center body text** — left-align paragraphs and lists; center only titles
- **Don't skimp on size contrast** — titles need 36pt+ to stand out from 14-16pt body
- **Don't default to blue** — pick colors that reflect the specific topic
- **Don't mix spacing randomly** — choose 0.3" or 0.5" gaps and use consistently
- **Don't style one slide and leave the rest plain** — commit fully or keep it simple throughout
- **Don't create text-only slides** — add images, icons, charts, or visual elements; avoid plain title + bullets
- **Don't forget text box padding** — when aligning lines or shapes with text edges, set `margin: 0` on the text box or offset the shape to account for padding
- **Don't use low-contrast elements** — icons AND text need strong contrast against the background; avoid light text on light backgrounds or dark text on dark backgrounds
- **NEVER use accent lines under titles** — these are a hallmark of AI-generated slides; use whitespace or background color instead

---

## QA (Required)

**Assume there are problems. Your job is to find them.**

Your first render is almost never correct. Approach QA as a bug hunt, not a confirmation step. If you found zero issues on first inspection, you weren't looking hard enough.

### Content QA

```bash
python -m markitdown output.pptx
```

Check for missing content, typos, wrong order.

**When using templates, check for leftover placeholder text:**

```bash
python -m markitdown output.pptx | grep -iE "\bx{3,}\b|lorem|ipsum|\bTODO|\[insert|this.*(page|slide).*layout"
```

If grep returns results, fix them before declaring success.

### Visual QA

**⚠️ USE SUBAGENTS** — even for 2-3 slides. You've been staring at the code and will see what you expect, not what's there. Subagents have fresh eyes.

Convert slides to images (see [Converting to Images](#converting-to-images)), then use this prompt:

```text
Visually inspect these slides. Assume there are issues — find them.

Look for:
- Overlapping elements (text through shapes, lines through words, stacked elements)
- Text overflow or cut off at edges/box boundaries
- Decorative lines positioned for single-line text but title wrapped to two lines
- Source citations or footers colliding with content above
- Elements too close (< 0.3" gaps) or cards/sections nearly touching
- Uneven gaps (large empty area in one place, cramped in another)
- Insufficient margin from slide edges (< 0.5")
- Columns or similar elements not aligned consistently
- Low-contrast text (e.g., light gray text on cream-colored background)
- Low-contrast icons (e.g., dark icons on dark backgrounds without a contrasting circle)
- Text boxes too narrow causing excessive wrapping
- Leftover placeholder content

For each slide, list issues or areas of concern, even if minor.

Read and analyze these images — run `ls -1 "$PWD"/slide-*.jpg` and use the exact absolute paths it prints:
1. <absolute-path>/slide-N.jpg — (Expected: [brief description])
2. <absolute-path>/slide-N.jpg — (Expected: [brief description])
...

Report ALL issues found, including minor ones.
```

### Verification Loop

1. Generate slides → Convert to images → Inspect
2. **List issues found** (if none found, look again more critically)
3. Fix issues
4. **Re-verify affected slides** — one fix often creates another problem
5. Repeat until a full pass reveals no new issues

**Do not declare success until you've completed at least one fix-and-verify cycle.**

---

## Converting to Images

Convert presentations to individual slide images for visual inspection:

```bash
python office-custom/scripts/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
ls -1 "$PWD"/slide-*.jpg
```

**Pass the absolute paths printed above directly to the view tool.** The `rm` clears stale images from prior runs. `pdftoppm` zero-pads based on page count: `slide-1.jpg` for decks under 10 pages, `slide-01.jpg` for 10-99, `slide-001.jpg` for 100+.

**After fixes, rerun all four commands above** — the PDF must be regenerated from the edited `.pptx` before `pdftoppm` can reflect your changes.

---

## Dependencies

- `pip install "markitdown[pptx]"` - text extraction
- `pip install Pillow` - thumbnail grids
- `npm install -g pptxgenjs` - creating from scratch
- LibreOffice (`soffice`) - PDF conversion (auto-configured for sandboxed environments via `office-custom/scripts/soffice.py`)
- Poppler (`pdftoppm`) - PDF to images

---

## API Reference

> Sources: [PptxGenJS docs](https://gitbrent.github.io/PptxGenJS/), [python-pptx docs](https://python-pptx.readthedocs.io/)

### PptxGenJS (creating .pptx from scratch)

Install: `npm install -g pptxgenjs`

#### Bootstrap

```javascript
const PptxGenJS = require("pptxgenjs");
const pptx = new PptxGenJS();

// Global presentation settings
pptx.layout = "LAYOUT_16x9";        // "LAYOUT_4x3", "LAYOUT_16x9", "LAYOUT_16x10", "LAYOUT_WIDE", custom
pptx.title  = "My Presentation";
pptx.subject = "Topic";
pptx.author  = "Name";
pptx.company = "Org";

const slide = pptx.addSlide();      // Blank slide
pptx.writeFile({ fileName: "output.pptx" });   // Save (returns Promise)
```

#### Slide master / layout

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

#### addText(text, options)

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

#### addImage(options)

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

#### addShape(shapeType, options)

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

#### addTable(rows, options)

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

#### addChart(type, data, options)

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

#### Coordinate system

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

### python-pptx (reading / editing existing .pptx)

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

prs = Presentation("existing.pptx")
slide = prs.slides[0]
prs.save("output.pptx")
```

#### Presentation

| Property | Type | Notes |
|----------|------|-------|
| `.slides` | `Slides` | Collection of slides |
| `.slide_width` / `.slide_height` | `Emu` | Overall dimensions |
| `.slide_layouts` | `SlideLayouts` | Available layouts |
| `.slide_masters` | `SlideMasters` | Master slides |
| `.core_properties` | `CoreProperties` | Title, author, etc. |

#### Slide

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

#### Shape

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

#### TextFrame and runs

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

#### OOXML unit conversions

| Unit | Emu | Python |
|------|-----|--------|
| 1 inch | 914,400 | `Inches(1)` |
| 1 cm | 360,000 | `Cm(1)` |
| 1 pt | 12,700 | `Pt(1)` |
| Slide 16:9 width | 9,144,000 | `Inches(10)` |
| Slide 16:9 height | 6,858,000 | `Inches(7.5)` |

---

## See Also

- **`$raw-document`** — specification-level reference (OOXML/ODF schemas, namespace tables,
  package structure deep-dives, cross-format mapping). Use when this skill's content is
  insufficient or when schema validation, format recovery, or deep PresentationML element
  research is required.
