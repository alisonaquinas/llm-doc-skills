# ODF Drawing and Graphics

> **Cross-references:** [Text Documents](./05-text-documents.md) | [Presentations](./07-presentations.md) | [Namespaces](./04-xml-namespaces.md) | [OOXML DrawingML](../ooxml/08-drawingml.md)

---

## 1. Overview

ODF uses the `draw:` namespace to define all vector drawing, shape, image, and frame elements. Drawing shapes appear in:

- Text documents (`.odt`) — inline or anchored
- Spreadsheets (`.ods`) — overlaid on cells
- Presentations (`.odp`) — as slide content
- Drawing documents (`.odg`) — primary content

---

## 2. Shape Categories

| Category | Elements |
| --- | --- |
| Basic geometry | `draw:rect`, `draw:circle`, `draw:ellipse`, `draw:line` |
| Polygons | `draw:polyline`, `draw:polygon`, `draw:path` |
| Connectors | `draw:connector` |
| Media/containers | `draw:frame`, `draw:image`, `draw:text-box`, `draw:object` |
| Groups | `draw:g` |
| 3D | `draw:scene`, `dr3d:cube`, `dr3d:sphere` |
| Captions | `draw:caption` |
| Measures | `draw:measure` |

---

## 3. Frames and Images

### `draw:frame`

The primary container for images, text boxes, and embedded objects:

```xml
<draw:frame
    draw:name="Image1"
    draw:style-name="fr1"
    text:anchor-type="paragraph"
    svg:x="2cm" svg:y="3cm"
    svg:width="10cm" svg:height="7.5cm"
    draw:z-index="1">

  <!-- Content (one of these): -->
  <draw:image xlink:href="Pictures/photo.jpg"
              xlink:type="simple"
              xlink:show="embed"
              xlink:actuate="onLoad"/>

  <!-- Optional: alt text for accessibility -->
  <svg:title>Photo of the team</svg:title>
  <svg:desc>Group photograph of the project team at the 2024 conference</svg:desc>
</draw:frame>
```

### Image Anchor Types

| `text:anchor-type` | Behavior |
| --- | --- |
| `page` | Fixed to a page position |
| `paragraph` | Moves with its anchor paragraph |
| `char` | Moves with its anchor character |
| `as-char` | Inline, like a large character |
| `frame` | Anchored within an enclosing frame |

### Text Wrapping

Controlled via `style:wrap` in the frame's graphic properties:

```xml
<style:graphic-properties style:wrap="parallel"
                           style:wrap-contour="false"
                           style:number-wrapped-paragraphs="no-limit"
                           style:wrap-left="0.3cm"
                           style:wrap-right="0.3cm"
                           style:wrap-top="0.3cm"
                           style:wrap-bottom="0.3cm"/>
```

Wrap values: `none`, `left`, `right`, `parallel`, `dynamic`, `run-through`, `biggest`

---

## 4. Basic Geometric Shapes

### Rectangle

```xml
<draw:rect
    draw:style-name="sh1"
    draw:layer="layout"
    svg:x="3cm" svg:y="4cm"
    svg:width="6cm" svg:height="4cm"
    draw:corner-radius="0.5cm">  <!-- rounded corners -->
  <text:p>Optional text inside</text:p>
</draw:rect>
```

### Circle / Ellipse

```xml
<!-- Full circle -->
<draw:circle
    draw:style-name="sh2"
    svg:cx="8cm" svg:cy="5cm"
    svg:r="3cm"/>

<!-- Ellipse -->
<draw:ellipse
    draw:style-name="sh3"
    svg:x="2cm" svg:y="3cm"
    svg:width="8cm" svg:height="5cm"
    draw:kind="full"/>              <!-- full | arc | section | cut -->
```

### Line

```xml
<draw:line
    draw:style-name="sh4"
    draw:layer="layout"
    svg:x1="2cm" svg:y1="2cm"
    svg:x2="12cm" svg:y2="8cm">
  <text:p/>
</draw:line>
```

---

## 5. Path Shapes (SVG-like)

```xml
<draw:path
    draw:style-name="sh5"
    svg:x="0cm" svg:y="0cm"
    svg:width="10cm" svg:height="8cm"
    svg:viewBox="0 0 10000 8000"
    svg:d="M 1000 0 L 9000 0 L 9000 8000 L 1000 8000 Z"/>
```

SVG path commands supported:

- `M` / `m` — Move to
- `L` / `l` — Line to
- `H` / `h` — Horizontal line
- `V` / `v` — Vertical line
- `C` / `c` — Cubic bezier curve
- `Q` / `q` — Quadratic bezier
- `A` / `a` — Arc
- `Z` / `z` — Close path

---

## 6. Polygon and Polyline

```xml
<!-- Polygon (closed) -->
<draw:polygon
    draw:style-name="sh6"
    svg:x="0cm" svg:y="0cm"
    svg:width="8cm" svg:height="6cm"
    svg:viewBox="0 0 8000 6000"
    svg:points="4000,0 8000,6000 0,6000"/>

<!-- Polyline (open) -->
<draw:polyline
    draw:style-name="sh7"
    svg:x="0cm" svg:y="0cm"
    svg:width="10cm" svg:height="5cm"
    svg:viewBox="0 0 10000 5000"
    svg:points="0,5000 2000,0 5000,3000 8000,0 10000,5000"/>
```

---

## 7. Connectors

```xml
<draw:connector
    draw:style-name="sh8"
    draw:type="standard"              <!-- straight | curve | lines | standard -->
    draw:start-shape="shape-id-1"
    draw:start-glue-point="1"         <!-- 0=top,1=right,2=bottom,3=left -->
    draw:end-shape="shape-id-2"
    draw:end-glue-point="3"
    svg:x1="3cm" svg:y1="5cm"
    svg:x2="12cm" svg:y2="5cm"/>
```

---

## 8. Groups

```xml
<draw:g draw:style-name="gr1">
  <draw:rect draw:style-name="sh1" svg:x="1cm" svg:y="1cm"
             svg:width="4cm" svg:height="3cm"/>
  <draw:circle draw:style-name="sh2" svg:x="2cm" svg:y="1.5cm"
               svg:width="2cm" svg:height="2cm"/>
</draw:g>
```

---

## 9. Shape Fill and Stroke (Style Properties)

Fill and stroke are defined in `<style:graphic-properties>`:

```xml
<style:style style:name="sh1" style:family="graphic">
  <style:graphic-properties
      draw:fill="solid"                  <!-- none | solid | bitmap | gradient | hatch -->
      draw:fill-color="#4472C4"
      draw:opacity="100%"
      draw:stroke="solid"               <!-- none | solid | dash -->
      svg:stroke-color="#2E4E8F"
      svg:stroke-width="0.05cm"
      draw:shadow="hidden"              <!-- visible | hidden -->
      draw:shadow-color="#808080"
      draw:shadow-offset-x="0.2cm"
      draw:shadow-offset-y="0.2cm"
      fo:max-height="0cm"
      fo:max-width="0cm"
      style:wrap="none"
      style:run-through="foreground"
      style:overflow-behavior="clip"/>
</style:style>
```

### Gradient Fill

```xml
<draw:gradient draw:name="LinearBlue"
               draw:display-name="Blue Linear"
               draw:style="linear"
               draw:start-color="#FFFFFF"
               draw:end-color="#4472C4"
               draw:start-intensity="100%"
               draw:end-intensity="100%"
               draw:angle="0"
               draw:border="0%"/>

<!-- Reference in style: -->
<style:graphic-properties draw:fill="gradient"
                           draw:fill-gradient-name="LinearBlue"/>
```

---

## 10. Text Inside Shapes

Any shape can contain text:

```xml
<draw:rect draw:style-name="sh1"
           svg:x="3cm" svg:y="4cm"
           svg:width="6cm" svg:height="3cm">
  <text:p text:style-name="ShapeText">Text inside rectangle</text:p>
  <text:p text:style-name="ShapeText">Second line</text:p>
</draw:rect>
```

Text alignment inside shapes:

```xml
<style:graphic-properties
    draw:textarea-horizontal-align="center"  <!-- left | center | right | justify -->
    draw:textarea-vertical-align="middle"    <!-- top | middle | bottom | justify -->
    draw:auto-grow-height="true"
    draw:auto-grow-width="false"
    fo:padding-left="0.3cm"
    fo:padding-right="0.3cm"
    fo:padding-top="0.15cm"
    fo:padding-bottom="0.15cm"/>
```

---

## 11. Layers (Drawing Documents)

Drawing documents (`.odg`) and presentations support layers:

```xml
<draw:layer-set>
  <draw:layer draw:name="layout" draw:display="always"/>
  <draw:layer draw:name="background" draw:display="always"/>
  <draw:layer draw:name="backgroundobjects" draw:display="always"/>
  <draw:layer draw:name="controls" draw:display="always"/>
  <draw:layer draw:name="measurelines" draw:display="never"/>
</draw:layer-set>
```

Shapes reference layers with `draw:layer="layout"`.

---

## 12. Chart Embedding

Charts are embedded as ODF objects within draw frames:

```xml
<draw:frame draw:name="Chart1"
            svg:x="3cm" svg:y="6cm"
            svg:width="14cm" svg:height="9cm">
  <draw:object xlink:href="./Object1"
               xlink:type="simple"
               xlink:show="embed"
               xlink:actuate="onLoad"/>
  <draw:image xlink:href="./Object1/thumbnail.png"
              xlink:type="simple"
              xlink:show="embed"
              xlink:actuate="onLoad"/>
</draw:frame>
```

The chart data lives in `Object1/content.xml` using the `chart:` namespace.

---

*Previous: [Presentations ←](./07-presentations.md) | Next: [Styles & Formatting →](./09-styles-formatting.md)*
