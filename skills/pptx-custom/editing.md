# Editing Existing Presentations

Use this guide when the source of truth is an existing `.pptx` file or a
template deck that must keep its current theme, layouts, and slide masters.

> **STOP — read this before any unpack/pack or python-pptx call.** Decks
> produced by third-party exporters (Walnut Exporter and friends) parse
> cleanly in tolerant readers (LibreOffice, python-pptx, even PowerPoint
> Desktop with silent repair) but a normalizing re-save can break the file
> in **both PowerPoint Online and PowerPoint Desktop**. The workflow below
> only applies to decks that pass the provenance check in Step 0.

## Step 0 — Provenance check (required)

```bash
python pptx-custom/scripts/check_fragility.py presentation.pptx
```

The script exits 0 when no signals are found and 1 when any signal is
found. The `--json` form (`--json | jq '.[0].worst'`) reports `info`,
`warn`, or `fail` so the triage below can be automated.

### Triage by worst severity

| Worst severity | What this means | What to do |
| --- | --- | --- |
| (none / exit 0) | No fragility signals — package looks like real Office output. | Continue with the **Preferred workflow** below. `python-pptx` full-save and `pack.py` ElementTree round-trips are safe. |
| `warn` only | Producer is unrecognized OR there are mild structural smells (random-hex rel IDs, misplaced theme, empty `<a:xfrm/>`, dc:creator-only signature, slide/notes mismatch), but the file is still well-formed enough for tolerant tooling. | Surgical byte-level edits via `patch_slide_xml.py` are safe. **Do not** run `python-pptx`'s save or `pack.py`'s ElementTree round-trip — both will normalize the XML declaration and can push the file across the validator threshold. Read [`recovering-fragile-decks.md`](recovering-fragile-decks.md) §Path B. |
| `fail` (any) | Hard signals of a fragile producer (Walnut Exporter / Aspose / Syncfusion / Spire / GemBox / OpenXML-SDK pipeline) or a structural bug PowerPoint Online's validator will reject (`Default Extension="xml"` core-properties, image-dup ratio >5×, inline-xmlns spam >150 per slide). | Canonicalize **first** via [`recovering-fragile-decks.md`](recovering-fragile-decks.md) §Path A (PowerPoint Desktop Save As, or LibreOffice `--convert-to pptx`). Edit the canonical copy with the Preferred workflow below. Do not edit the fragile original through any normalizing tool. |

When in doubt, treat the file as fragile. The fragile-deck recovery flow is
also safe on healthy decks; the inverse is not true.

## Preferred workflow (non-fragile decks)

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

`pack.py` runs an ElementTree round-trip during `condense_xml`. That is
canonical OOXML, but it is not byte-preserving — which is exactly why Step 0
exists: a Walnut-style deck does not survive the round-trip even though the
script reports no errors.

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

## Tool-choice rules

| Operation | Safe on healthy decks? | Safe on fragile decks? |
| --- | --- | --- |
| `markitdown` text extraction | ✅ | ✅ (read-only) |
| `thumbnail.py` rendering | ✅ | ✅ (read-only) |
| `unpack.py` + manual edits + `pack.py` | ✅ | ❌ — pack.py runs an ET round-trip |
| `python-pptx` full save | ✅ | ❌ — rewrites XML declaration |
| `patch_slide_xml.py` (byte-level) | ✅ | ✅ — see [`recovering-fragile-decks.md`](recovering-fragile-decks.md) |

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
- a `… - Repaired.pptx` companion appearing when the deck is opened in
  PowerPoint Desktop — that is PowerPoint flagging structural problems that
  `validate.py` may not catch. Re-run `check_fragility.py` if it appears.

## When not to use XML editing

- Use [`pptxgenjs.md`](pptxgenjs.md) when you are building a new deck from
  scratch.
- Use the existing slide masters when the user requires brand fidelity.
- If most slides are being rebuilt anyway, a fresh `pptxgenjs` deck may be
  faster than hand-editing XML.
- Use [`recovering-fragile-decks.md`](recovering-fragile-decks.md) when the
  Step 0 provenance check flags the deck as fragile.
