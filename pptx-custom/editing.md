# Editing Existing Presentations

Use this guide when the source of truth is an existing `.pptx` file or a
template deck that must keep its current theme, layouts, and slide masters.

## Preferred workflow

1. Generate a quick visual overview.
2. Unpack the presentation XML.
3. Edit slide content or relationships.
4. Repack the file.
5. Convert it to images and visually QA every slide.

```bash
python pptx-custom/scripts/thumbnail.py presentation.pptx
python office-custom/scripts/unpack.py presentation.pptx unpacked/
# edit files inside unpacked/ppt/
python office-custom/scripts/pack.py unpacked/ output.pptx --original presentation.pptx
python pptx-custom/scripts/thumbnail.py output.pptx output-thumbnails.jpg
```

## Where to edit

| Path | Purpose |
| --- | --- |
| `ppt/presentation.xml` | Slide order and presentation metadata |
| `ppt/slides/slideN.xml` | Slide content |
| `ppt/slides/_rels/slideN.xml.rels` | Slide-level media and hyperlink relationships |
| `ppt/slideLayouts/` | Layout definitions shared by slides |
| `ppt/slideMasters/` | Theme and master placeholders |
| `ppt/theme/` | Theme colors and fonts |

## Common edit patterns

- Replace text directly in `slideN.xml` when the layout is already correct.
- Add or swap media by updating both the file in `ppt/media/` and the matching
  relationship entry.
- Preserve relationship IDs unless you are intentionally creating a new target.
- Be cautious with placeholder geometry. Theme and layout files affect many
  slides at once.

## Slide QA loop

After every meaningful edit:

```bash
python office-custom/scripts/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Check for:

- overflow or clipped text
- shifted images
- placeholder artifacts
- low-contrast text
- accidental theme/layout regressions

## When not to use XML editing

- Use [`pptxgenjs.md`](pptxgenjs.md) when you are building a new deck from
  scratch.
- Use the existing slide masters when the user requires brand fidelity.
- If most slides are being rebuilt anyway, a fresh `pptxgenjs` deck may be
  faster than hand-editing XML.
