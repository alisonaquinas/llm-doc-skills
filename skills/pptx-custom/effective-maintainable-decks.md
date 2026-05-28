# Effective, Maintainable, Office-Compatible Decks

Use this reference when a deck must remain persuasive, editable, reusable, and
compatible after handoff. It distills the imported PowerPoint deck research into
operational guidance for creating and modifying `.pptx` files.

## Core Model

Treat a PowerPoint deck as a small document system, not as a stack of isolated
artboards.

- Message: one clear point per slide, expressed in an action title whenever
  possible.
- Structure: sections, slide titles, layouts, and placeholders define the
  content architecture.
- Style: slide masters, layouts, theme colors, theme fonts, and backgrounds carry
  recurring design decisions so colors, backgrounds, and layout geometry do not
  need to be set manually on each slide.
- Objects: text, shapes, icons, charts, tables, media, notes, and comments stay
  native and semantically meaningful when future editing is expected.
- Operations: collaboration, review, export, and archive practices preserve one
  canonical source deck.

When these layers are mixed together through manual formatting, screenshots, and
ad hoc text boxes, the deck becomes harder to revise, restyle, search, reuse, and
export.

## Message And Audience

- Start from the audience, decision, and desired action before choosing layouts.
- Give each slide one dominant takeaway; split slides that carry multiple
  independent arguments.
- Prefer sentence-like action titles over topic labels. A title such as
  "Retention risk is concentrated in two roles" is more useful than "Attrition".
- Keep explanatory detail in speaker notes when the audience should listen
  rather than read.
- Use visuals to reduce effort: direct chart labels, clear grouping, generous
  whitespace, and visible hierarchy.
- Treat appendix slides as reference material. Keep them structured and
  searchable, but do not let appendix density leak into the main narrative.

## PowerPoint Architecture

- Use `.pptx` as the editable working master. Use `.potx` for reusable
  templates and PDF, video, or images as downstream exports only.
- When a template exists, preserve its slide master, theme, layouts, and
  placeholders. Reapply or reset layouts before resorting to local overrides.
- Use slide masters and themes as the repeatability layer. Define backgrounds,
  colors, font roles, logos, page furniture, and common layouts there instead of
  hand-formatting each slide.
- Prefer one primary slide master and a limited set of useful layouts: title,
  section divider, title-plus-content, comparison, picture-with-caption,
  dashboard, timeline/process, summary, and appendix.
- Put recurring logos, backgrounds, page furniture, and fixed brand elements on
  masters or layouts instead of duplicating them on every slide.
- Use placeholders for standard titles, body regions, pictures, charts, tables,
  and captions. Reserve free text boxes for intentional exceptions.
- Keep title placeholders present and unique, even when the visual title is
  hidden, so navigation and accessibility remain intact.

## Native Editable Objects

- Prefer PowerPoint text, shapes, icons, charts, and simple tables over
  screenshots or flattened artwork for content that may change.
- Use screenshots only for evidence of an external interface or fixed visual
  state. Do not screenshot a chart, table, or diagram that editors will need to
  update.
- Build portable diagrams from grouped shapes and icons. SmartArt is acceptable
  for PowerPoint-only drafting, but grouped native shapes are usually safer for
  cross-tool editing.
- Group within meaningful components, not across entire slides. Componentize
  first, animate later.
- Keep tables simple: header row, no nested tables, minimal merged or split
  cells, and enough cell padding to survive font substitution.
- Keep charts editable when the underlying numbers may change. Use direct labels
  and an action title so the chart's interpretation remains clear.

## Compatibility Defaults

- Use familiar system fonts when broad compatibility matters. If a custom font is
  required, embed all characters for editable handoff where PowerPoint supports
  it; subset embedding is smaller but weakens later editing.
- Leave text boxes and placeholders wider than the exact local rendering needs.
  Font substitution, localization, and web rendering often expand text.
- Use theme colors and a small style vocabulary. Avoid manual one-off colors that
  are hard to normalize later.
- Avoid macros, OLE/ActiveX objects, complex SmartArt, unusual effects, and
  elaborate animation trees unless the target environment is explicitly
  PowerPoint desktop.
- Embed small critical images and media. Link large or frequently updated assets
  only when the source file path and handoff folder are managed.
- Package linked files before external handoff. Keep linked media beside the deck
  when packaging is not possible.
- Preserve an uncompressed source copy when media accessibility tracks matter;
  PowerPoint media compression can remove embedded subtitles or alternate audio.
- Test the actual target environment for high-stakes decks: PowerPoint desktop,
  PowerPoint for the web, Teams/PowerPoint Live, Google Slides, Keynote, PDF, or
  projected display.

## Collaboration And Governance

- Maintain one canonical working `.pptx` in OneDrive or SharePoint when
  Microsoft 365 co-authoring is expected.
- Use comments, tasks, version history, and shared permissions for review.
  Compare/Merge is an offline-copy fallback, not the primary review model.
- Keep exports in a separate folder from editable source decks.
- Use compact, sortable filenames such as
  `2026-05-28-project-audience-working-v03.pptx`.
- Preserve a milestone copy at approval points even when cloud version history is
  available.
- Keep source data, image originals, and linked media in a predictable sibling
  folder so future editors can rebuild or audit the deck.

## Accessibility And Maintainability

- Every non-blank slide needs a unique title.
- Reading order must match the intended visual and narrative order.
- Meaningful visuals need concise alt text; decorative visuals should be marked
  decorative where the target tool supports it.
- Text and meaningful non-text elements need sufficient contrast. Do not rely on
  color alone to encode categories, status, or sequence.
- Use large, readable type. Keep all visible text at 12 pt or larger as an
  absolute floor, and use 18 pt or larger for normal body text in presentation
  slides. Dense reference material belongs in appendix or notes.
- Use simple, readable sans-serif fonts for broad accessibility and compatibility.
- Re-run accessibility and visual checks after localization, template changes, or
  major object movement.

## Review Contact Sheets

Generate contact sheets of the slide deck during review, iteration, and
improvement. A contact sheet makes the whole sequence visible at once, which is
especially useful for judging whether slides are effective as a narrative rather
than merely valid as individual pages.

```bash
python pptx-custom/scripts/thumbnail.py deck.pptx deck-contact-sheet.jpg --cols 4 --dpi 120
```

- Generate a contact sheet after the first complete draft and after meaningful
  revisions.
- Use the contact sheet to evaluate slide order, visual rhythm, repeated layout
  patterns, title clarity, density, contrast, and whether each slide's main point
  is legible at a glance.
- Pair contact-sheet review with full-size slide rendering. Contact sheets catch
  story, consistency, and pacing problems; full-size renders catch overflow,
  small type, crop problems, and fine alignment issues.
- Iterate visibly: mark weak slides, revise them, regenerate the contact sheet,
  and compare before/after.

## Agent Checklist

Before creating or handing off a deck:

- Does each slide have one clear takeaway and a useful title?
- Are recurring structures built from layouts, placeholders, theme colors, and
  native objects rather than manual formatting?
- Are slide masters and themes carrying repeatable colors, backgrounds, and
  layouts instead of per-slide manual styling?
- Are charts, tables, diagrams, and text editable where future maintenance is
  likely?
- Are screenshots limited to fixed external evidence?
- Is every visible text element at least 12 pt, with normal presentation body
  text usually 18 pt or larger?
- Is the working file a `.pptx`, with `.potx` reserved for templates and PDF or
  video reserved for exports?
- Are fonts, media, linked assets, and target-client limitations accounted for?
- Have visual QA, text extraction, accessibility checks, and target-environment
  checks been run where practical?
- Has a contact sheet been generated and used to review slide effectiveness,
  sequence, density, and visual consistency?
