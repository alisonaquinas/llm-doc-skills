# ODF Presentations (ODP)

> **Cross-references:** [Namespaces](./04-xml-namespaces.md) | [Styles & Formatting](./09-styles-formatting.md) | [Drawing & Graphics](./08-drawing-graphics.md) | [OOXML PresentationML](../ooxml/07-presentationml.md)

---

## 1. Overview

OpenDocument Presentation (`.odp`) is the ODF format for presentations. Presentations are structured as a sequence of **drawing pages** (slides), each containing **shapes** (text boxes, images, lines, etc.).

Key structures:

- **Drawing pages** (`draw:page`) correspond to slides
- **Shapes** (`draw:frame`, `draw:rect`, etc.) contain content
- **Master pages** (`style:master-page`) define slide masters
- **Presentation styles** control animations and transitions

---

## 2. Document Structure

```xml
<office:document-content ...>
  <office:automatic-styles>
    <!-- Auto-generated drawing page styles, shape styles, etc. -->
  </office:automatic-styles>

  <office:body>
    <office:presentation>

      <!-- Slide 1 -->
      <draw:page draw:name="Slide1"
                 draw:style-name="dp1"
                 draw:master-page-name="Default"
                 presentation:presentation-page-layout-name="AL1T0">

        <!-- Title placeholder -->
        <draw:frame presentation:class="title"
                    draw:style-name="pr1"
                    draw:text-style-name="P1"
                    draw:layer="layout"
                    svg:width="20cm" svg:height="3cm"
                    svg:x="2cm" svg:y="1cm">
          <draw:text-box>
            <text:p text:style-name="P-Title">Slide Title Here</text:p>
          </draw:text-box>
        </draw:frame>

        <!-- Content placeholder -->
        <draw:frame presentation:class="body"
                    draw:style-name="pr2"
                    draw:layer="layout"
                    svg:width="20cm" svg:height="12cm"
                    svg:x="2cm" svg:y="5cm">
          <draw:text-box>
            <text:list>
              <text:list-item>
                <text:p text:style-name="P-Body">First bullet point</text:p>
              </text:list-item>
              <text:list-item>
                <text:p text:style-name="P-Body">Second bullet point</text:p>
              </text:list-item>
            </text:list>
          </draw:text-box>
        </draw:frame>

      </draw:page>

    </office:presentation>
  </office:body>
</office:document-content>
```

---

## 3. Slide (Drawing Page) Attributes

```xml
<draw:page
    draw:name="Slide2"
    draw:style-name="dp2"                     <!-- drawing page style (background, etc.) -->
    draw:master-page-name="Title Slide"        <!-- master page reference -->
    presentation:presentation-page-layout-name="AL2T1"  <!-- layout name -->
    presentation:use-header-name="hf1"        <!-- header/footer reference -->
    presentation:use-footer-name="hf1"
    presentation:use-page-number="true">
```

### Presentation Layout Names

Predefined layout names in ODP (similar to OOXML slide layouts):

| Layout | Description |
| --- | --- |
| `AL0T0` | Blank |
| `AL1T0` | Title, Content |
| `AL2T0` | Title, 2 Content |
| `AL3T0` | Title Only |
| `AL4T0` | Centered Text |
| `AL5T0` | Title, 4 Content |

---

## 4. Presentation Classes (Placeholders)

ODP distinguishes different placeholder types via `presentation:class`:

| Class | Description |
| --- | --- |
| `title` | Slide title |
| `subtitle` | Subtitle (on title slides) |
| `body` | Main content area |
| `outline` | Outline/bullet content |
| `notes` | Speaker notes |
| `header` | Header area |
| `footer` | Footer area |
| `page-number` | Page number placeholder |
| `date-time` | Date/time placeholder |
| `graphic` | Image placeholder |
| `object` | Embedded object placeholder |
| `chart` | Chart placeholder |
| `table` | Table placeholder |

---

## 5. Master Pages (Slide Masters)

Master pages are defined in `styles.xml` and referenced by slides:

```xml
<!-- In styles.xml -->
<office:master-styles>

  <style:master-page style:name="Default"
                     style:page-layout-name="PM1"
                     draw:style-name="Default-master">

    <!-- Background image or color (via style reference) -->

    <!-- Fixed elements on all slides using this master -->
    <draw:frame presentation:class="footer"
                svg:x="1cm" svg:y="26cm"
                svg:width="8cm" svg:height="1cm">
      <draw:text-box>
        <text:p><presentation:footer/></text:p>
      </draw:text-box>
    </draw:frame>

    <draw:frame presentation:class="page-number"
                svg:x="20cm" svg:y="26cm"
                svg:width="3cm" svg:height="1cm">
      <draw:text-box>
        <text:p><presentation:page-number/></text:p>
      </draw:text-box>
    </draw:frame>

  </style:master-page>

  <style:master-page style:name="Title Slide"
                     style:page-layout-name="PM2">
    <!-- Title slide master -->
  </style:master-page>

</office:master-styles>
```

---

## 6. Page Layout (Slide Size)

```xml
<!-- In styles.xml -->
<office:automatic-styles>
  <style:page-layout style:name="PM1">
    <style:page-layout-properties
        fo:margin-top="0cm"
        fo:margin-bottom="0cm"
        fo:margin-left="0cm"
        fo:margin-right="0cm"
        fo:page-width="25.4cm"
        fo:page-height="19.05cm"
        style:print-orientation="landscape"
        presentation:background-visible="true"
        presentation:background-objects-visible="true"/>
  </style:page-layout>
</office:automatic-styles>
```

Common slide dimensions:

| Format | Width × Height |
| --- | --- |
| Widescreen (16:9) | 33.87cm × 19.05cm |
| Standard (4:3) | 25.4cm × 19.05cm |
| A4 | 29.7cm × 21.0cm |

---

## 7. Slide Transitions

Transitions are defined on drawing pages using the `presentation:transition` element or via `presentation:` attributes:

```xml
<draw:page draw:name="Slide3" ...>

  <!-- Transition defined as child element -->
  <presentation:transition presentation:type="automatic"
                            presentation:speed="medium"
                            smil:type="fade"
                            smil:subtype="crossfade"
                            presentation:show-updated-presentation="false"/>

  <!-- ... shapes ... -->
</draw:page>
```

Common transition types (SMIL):

- `smil:type="fade"` (crossfade, fadeToColor)
- `smil:type="slide"` (fromLeft, fromRight, fromTop, fromBottom)
- `smil:type="wipe"` (left, right, up, down)
- `smil:type="push"` (fromLeft, fromRight)
- `smil:type="zoom"` (in, out)

---

## 8. Animations

ODF animations use the SMIL-based animation model:

```xml
<draw:page draw:name="Slide4" ...>
  <!-- Shapes -->
  <draw:frame draw:id="shape1" ...>
    <draw:text-box>
      <text:p>Animated Text</text:p>
    </draw:text-box>
  </draw:frame>

  <!-- Animations -->
  <anim:par>
    <anim:par smil:begin="0s">
      <anim:seq smil:begin="next">
        <anim:par smil:begin="0s">
          <anim:animateMotion
              smil:targetElement="shape1"
              smil:begin="0s"
              smil:dur="1s"
              smil:fill="hold"
              svg:path="M0,0L0,-1"/>
        </anim:par>
      </anim:seq>
    </anim:par>
  </anim:par>
</draw:page>
```

---

## 9. Speaker Notes

```xml
<draw:page draw:name="Slide1" ...>
  <!-- Slide shapes -->
  ...

  <!-- Speaker notes -->
  <presentation:notes draw:style-name="dp-notes">
    <draw:frame presentation:class="notes"
                svg:x="1cm" svg:y="6cm"
                svg:width="22cm" svg:height="14cm">
      <draw:text-box>
        <text:p text:style-name="P-Notes">Speaker notes text here.</text:p>
        <text:p text:style-name="P-Notes">Second paragraph of notes.</text:p>
      </draw:text-box>
    </draw:frame>
  </presentation:notes>
</draw:page>
```

---

## 10. Slide Show Settings

```xml
<!-- In settings.xml -->
<presentation:show-views presentation:current-view="page"/>
<presentation:shows>
  <presentation:show presentation:name="AllSlides"
                      presentation:pages="Slide1 Slide2 Slide3"
                      presentation:show-background="true"
                      presentation:show-background-objects="true"/>
</presentation:shows>
```

---

## 11. Presentation Settings (document-level)

```xml
<!-- In styles.xml automatic-styles or content.xml -->
<presentation:settings
    presentation:show="AllSlides"
    presentation:full-screen="true"
    presentation:endless="false"
    presentation:pause="PT0S"
    presentation:show-logo="false"
    presentation:force-manual="false"
    presentation:start-page="Slide1"
    presentation:mouse-visible="true"
    presentation:mouse-as-pen="false"
    presentation:show-end-of-presentation-slide="true"/>
```

---

*Previous: [Spreadsheets ←](./06-spreadsheets.md) | Next: [Drawing & Graphics →](./08-drawing-graphics.md)*
