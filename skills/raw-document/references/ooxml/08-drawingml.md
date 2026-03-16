# OOXML DrawingML

> **Cross-references:** [Namespaces](./04-xml-namespaces.md) | [WordprocessingML](./05-wordprocessingml.md) | [SpreadsheetML](./06-spreadsheetml.md) | [PresentationML](./07-presentationml.md) | [ODF Drawing](../odf/08-drawing-graphics.md)

---

## 1. Overview

DrawingML is OOXML's unified XML vocabulary for all graphical content. It is **not a standalone document format** — it always appears embedded within WordprocessingML, SpreadsheetML, or PresentationML documents.

DrawingML handles:

- Shapes and drawing objects
- Pictures and images
- Charts
- SmartArt/Diagrams
- Tables in presentations/drawings
- Themes, colors, fonts
- Effects (shadows, reflections, glows, gradients)

Main namespace: `xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"`

---

## 2. DrawingML Architecture

```text
DrawingML Main (a:)
├── Shapes (a:sp, a:grpSp)
│   ├── Shape Properties (a:spPr)
│   ├── Non-Visual Properties (nvSpPr)
│   └── Text Body (a:txBody)
├── Pictures (pic:pic)
├── Group Shapes (a:grpSp)
├── Connections (a:cxnSp)
├── Graphic Frames (a:graphicFrame → charts, diagrams)
└── Tables (a:tbl)

Context-specific wrappers:
├── Word: wp:inline / wp:anchor
├── Excel: xdr:oneCellAnchor / xdr:twoCellAnchor
└── PowerPoint: p:sp / p:pic / p:graphicFrame (direct)
```

---

## 3. Shapes

### Preset Geometries (`a:prstGeom`)

All shapes reference a preset geometry name. Key presets:

```xml
<a:prstGeom prst="rect">         <!-- rectangle -->
<a:prstGeom prst="roundRect">    <!-- rounded rectangle -->
<a:prstGeom prst="ellipse">      <!-- ellipse/circle -->
<a:prstGeom prst="triangle">     <!-- triangle -->
<a:prstGeom prst="rightTriangle"> <!-- right triangle -->
<a:prstGeom prst="parallelogram">
<a:prstGeom prst="trapezoid">
<a:prstGeom prst="diamond">
<a:prstGeom prst="pentagon">
<a:prstGeom prst="hexagon">
<a:prstGeom prst="heptagon">
<a:prstGeom prst="octagon">
<a:prstGeom prst="decagon">
<a:prstGeom prst="donut">
<a:prstGeom prst="star4">        <!-- 4-pointed star -->
<a:prstGeom prst="star5">        <!-- 5-pointed star -->
<a:prstGeom prst="star6">
<a:prstGeom prst="star8">
<a:prstGeom prst="star12">
<a:prstGeom prst="star24">
<a:prstGeom prst="star32">
<a:prstGeom prst="ribbon2">
<a:prstGeom prst="ribbon">
<a:prstGeom prst="arrow">        <!-- process: rightArrow, leftArrow, upArrow, downArrow -->
<a:prstGeom prst="callout1">     <!-- various callout shapes -->
<a:prstGeom prst="wedgeRectCallout">
<a:prstGeom prst="cloudCallout">
<a:prstGeom prst="lineCallout1">
<a:prstGeom prst="heart">
<a:prstGeom prst="cloud">
<a:prstGeom prst="line">         <!-- straight connector line -->
<a:prstGeom prst="straightConnector1">
<a:prstGeom prst="bentConnector2">
<a:prstGeom prst="curvedConnector2">
```

### Custom Geometry

```xml
<a:custGeom>
  <a:pathLst>
    <a:path w="10000" h="10000">
      <a:moveTo><a:pt x="0" y="5000"/></a:moveTo>
      <a:lnTo><a:pt x="5000" y="0"/></a:lnTo>
      <a:lnTo><a:pt x="10000" y="5000"/></a:lnTo>
      <a:lnTo><a:pt x="5000" y="10000"/></a:lnTo>
      <a:close/>
    </a:path>
  </a:pathLst>
</a:custGeom>
```

---

## 4. Shape Properties (`a:spPr`)

```xml
<a:spPr>

  <!-- Position and size (EMU) -->
  <a:xfrm>
    <a:off x="1000000" y="1000000"/>        <!-- offset from top-left of slide/page -->
    <a:ext cx="3000000" cy="2000000"/>      <!-- width and height -->
    <!-- Optional rotation: rot="5400000" = 90° (60000 units = 1°) -->
  </a:xfrm>

  <!-- Geometry -->
  <a:prstGeom prst="roundRect">
    <a:avLst>
      <!-- Adjust values for shape parameters -->
      <a:gd name="adj" fmla="val 16667"/>   <!-- corner radius ~17% -->
    </a:avLst>
  </a:prstGeom>

  <!-- Fill -->
  <a:solidFill>
    <a:srgbClr val="4472C4"/>              <!-- solid hex color (no #) -->
  </a:solidFill>

  <!-- Alternative fills: -->
  <!-- <a:noFill/> -->
  <!-- <a:gradFill> ... </a:gradFill> -->
  <!-- <a:blipFill> ... </a:blipFill> -->
  <!-- <a:pattFill> ... </a:pattFill> -->

  <!-- Outline/stroke -->
  <a:ln w="12700">                          <!-- w in EMU (12700 = 1pt) -->
    <a:solidFill>
      <a:srgbClr val="2E4E8F"/>
    </a:solidFill>
    <a:prstDash val="solid"/>              <!-- solid | dot | dash | dashDot | lgDash | lgDashDot | lgDashDotDot | sysDash | sysDot | sysDashDot | sysDashDotDot -->
    <a:round/>                              <!-- line join: round | bevel | miter -->
  </a:ln>

  <!-- Effects -->
  <a:effectLst>
    <a:outerShdw blurRad="40000" dist="23000" dir="5400000" rotWithShape="0">
      <a:srgbClr val="000000">
        <a:alpha val="35000"/>             <!-- 35% opacity -->
      </a:srgbClr>
    </a:outerShdw>
  </a:effectLst>

  <!-- 3D effects -->
  <a:sp3d>
    <a:bevelT w="63500" h="25400" prst="circle"/>
    <a:bevelB w="63500" h="25400" prst="circle"/>
    <a:extrusionClr><a:srgbClr val="C0C0C0"/></a:extrusionClr>
  </a:sp3d>

</a:spPr>
```

---

## 5. Color Models

DrawingML provides multiple ways to specify colors:

```xml
<!-- Hex RGB -->
<a:srgbClr val="FF0000"/>

<!-- Theme color -->
<a:schemeClr val="accent1">
  <a:lumMod val="75000"/>    <!-- 75% luminance -->
  <a:lumOff val="15000"/>    <!-- +15% luminance offset -->
</a:schemeClr>

<!-- System color -->
<a:sysClr lastClr="FFFFFF" val="window"/>

<!-- Preset color -->
<a:prstClr val="red"/>

<!-- HSL color -->
<a:hslClr hue="0" sat="100000" lum="50000"/>

<!-- Percentage RGB -->
<a:prstClr val="red">
  <a:alpha val="50000"/>     <!-- 50% opacity -->
</a:prstClr>
```

### Color Modifications

| Modifier | Effect |
| --- | --- |
| `<a:alpha val="N"/>` | Opacity (0–100000) |
| `<a:lumMod val="N"/>` | Luminance multiply (0–100000) |
| `<a:lumOff val="N"/>` | Luminance offset (0–100000) |
| `<a:shade val="N"/>` | Darken by N% |
| `<a:tint val="N"/>` | Lighten by N% |
| `<a:hueMod val="N"/>` | Hue rotation |
| `<a:satMod val="N"/>` | Saturation multiply |
| `<a:gray/>` | Convert to grayscale |
| `<a:comp/>` | Complement color |
| `<a:inv/>` | Invert color |

---

## 6. Text in Shapes (`a:txBody`)

```xml
<a:txBody>

  <!-- Body properties -->
  <a:bodyPr
      rot="0"
      spcFirstLastPara="0"
      vertOverflow="overflow"       <!-- overflow | ellipsis | clip -->
      horzOverflow="overflow"
      vert="horz"                   <!-- horz | vert | vert270 | wordArtVert | eaVert | mongolianVert | wordArtVertRtl -->
      wrap="square"                 <!-- square | none -->
      lIns="91440" tIns="45720" rIns="91440" bIns="45720"  <!-- internal margins (EMU) -->
      numCol="1"
      spcCol="0"
      rtlCol="0"
      anchor="ctr"                  <!-- t | ctr | b | just | dist -->
      anchorCtr="0"
      compatLnSpc="1">
    <a:normAutofit/>                <!-- auto-fit: normAutofit | noAutofit | spAutoFit -->
  </a:bodyPr>

  <!-- List style -->
  <a:lstStyle/>

  <!-- Paragraphs -->
  <a:p>
    <a:pPr
        marL="0"                    <!-- left margin in EMU -->
        indent="0"
        algn="ctr"                  <!-- l | ctr | r | just | justLow | dist | thDist -->
        lvl="0"                     <!-- indent level 0–8 (in presentations) -->
        rtl="0"
        eaLnBrk="1"
        latinLnBrk="0"
        hangingPunct="1">
      <a:spcBef>
        <a:spcPts val="0"/>         <!-- space before in hundredths of a point (0 = 0pt) -->
      </a:spcBef>
      <a:spcAft>
        <a:spcPts val="0"/>
      </a:spcAft>
      <a:buNone/>                   <!-- no bullet on this paragraph -->
      <!-- Alternatively: <a:buChar char="•"/> or <a:buAutoNum type="arabicPeriod"/> -->
    </a:pPr>

    <!-- Run -->
    <a:r>
      <a:rPr
          lang="en-US"
          sz="2800"                 <!-- font size in hundredths of a point (2800 = 28pt) -->
          b="1"                     <!-- bold -->
          i="0"                     <!-- italic -->
          u="sng"                   <!-- underline: none | sng | dbl | heavy | dotted | dottedHvy | dash | dashHvy | dashLong | dashLongHvy | dotDash | dotDashHvy | dotDotDash | dotDotDashHvy | wavy | wavyHvy | wavyDbl -->
          strike="noStrike"
          kern="1200"
          baseline="0"              <!-- superscript/subscript: 30000 | -25000 | 0 -->
          dirty="0"
          smtClean="0">
        <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
        <a:latin typeface="Calibri" panose="020F0502020204030204" pitchFamily="34" charset="0"/>
        <a:ea typeface=""/>
        <a:cs typeface=""/>
      </a:rPr>
      <a:t>Text content here</a:t>
    </a:r>

    <!-- Line break within paragraph -->
    <a:br>
      <a:rPr lang="en-US" dirty="0"/>
    </a:br>

    <!-- Field (dynamic value) -->
    <a:fld id="{GUID}" type="slidenum">
      <a:rPr lang="en-US"/>
      <a:t>‹#›</a:t>
    </a:fld>

  </a:p>
</a:txBody>
```

---

## 7. Pictures (`pic:pic`)

```xml
<pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">

  <pic:nvPicPr>
    <pic:cNvPr id="1" name="Image 1" descr="Alt text for accessibility"/>
    <pic:cNvPicPr>
      <a:picLocks noChangeAspect="1"/>
    </pic:cNvPicPr>
  </pic:nvPicPr>

  <pic:blipFill>
    <a:blip r:embed="rId6"          <!-- relationship ID pointing to image file -->
            cstate="print"/>         <!-- print | email | hqprint | screen -->
      <!-- Optional: image corrections -->
      <a:extLst>
        <a:ext uri="{28A0092B-C50C-407E-A947-70E740481C1C}">
          <!-- useLocalDpi: 0 = use document DPI -->
        </a:ext>
      </a:extLst>
    </a:blip>
    <a:stretch>
      <a:fillRect/>                  <!-- stretch to fill the frame -->
    </a:stretch>
    <!-- Alternative: <a:tile/> for tiling -->
  </pic:blipFill>

  <pic:spPr>
    <a:xfrm>
      <a:off x="0" y="0"/>
      <a:ext cx="3000000" cy="2000000"/>
    </a:xfrm>
    <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
  </pic:spPr>

</pic:pic>
```

---

## 8. Charts (`c:chart`)

Charts are referenced via `a:graphicData`:

```xml
<a:graphic>
  <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">
    <c:chart r:id="rId1"
        xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"/>
  </a:graphicData>
</a:graphic>
```

The chart XML file (`xl/charts/chart1.xml` or `ppt/charts/chart1.xml`):

```xml
<c:chartSpace xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart">

  <c:chart>
    <c:title>
      <c:tx><c:rich><a:bodyPr/><a:lstStyle/>
        <a:p><a:r><a:t>Chart Title</a:t></a:r></a:p>
      </c:rich></c:tx>
    </c:title>

    <c:plotArea>

      <!-- Bar chart -->
      <c:barChart>
        <c:barDir val="col"/>          <!-- col = vertical bars, bar = horizontal -->
        <c:grouping val="clustered"/>  <!-- clustered | stacked | percentStacked -->

        <c:ser>                        <!-- Data series -->
          <c:idx val="0"/>
          <c:order val="0"/>
          <c:tx>                       <!-- Series name -->
            <c:strRef>
              <c:f>Sheet1!$B$1</c:f>
            </c:strRef>
          </c:tx>
          <c:cat>                      <!-- Category (X) axis data -->
            <c:strRef>
              <c:f>Sheet1!$A$2:$A$5</c:f>
            </c:strRef>
          </c:cat>
          <c:val>                      <!-- Values (Y) data -->
            <c:numRef>
              <c:f>Sheet1!$B$2:$B$5</c:f>
              <c:numCache>
                <c:formatCode>General</c:formatCode>
                <c:ptCount val="4"/>
                <c:pt idx="0"><c:v>42</c:v></c:pt>
                <c:pt idx="1"><c:v>85</c:v></c:pt>
                <c:pt idx="2"><c:v>63</c:v></c:pt>
                <c:pt idx="3"><c:v>97</c:v></c:pt>
              </c:numCache>
            </c:numRef>
          </c:val>
        </c:ser>

      </c:barChart>

      <!-- Axes -->
      <c:catAx><c:axId val="1"/><c:scaling><c:orientation val="minMax"/></c:scaling>
               <c:crossAx val="2"/></c:catAx>
      <c:valAx><c:axId val="2"/><c:scaling><c:orientation val="minMax"/></c:scaling>
               <c:crossAx val="1"/></c:valAx>

    </c:plotArea>

    <c:legend>
      <c:legendPos val="b"/>           <!-- b | t | l | r | tr -->
    </c:legend>

  </c:chart>

</c:chartSpace>
```

### Chart Types

| Element | Chart Type |
| --- | --- |
| `c:barChart` | Bar/column chart |
| `c:lineChart` | Line chart |
| `c:pieChart` | Pie chart |
| `c:doughnutChart` | Doughnut chart |
| `c:areaChart` | Area chart |
| `c:scatterChart` | Scatter/XY chart |
| `c:bubbleChart` | Bubble chart |
| `c:radarChart` | Radar/spider chart |
| `c:stockChart` | Stock chart (OHLC) |
| `c:surfaceChart` | 3D surface chart |
| `c:bar3DChart` | 3D bar chart |
| `c:line3DChart` | 3D line chart |
| `c:pie3DChart` | 3D pie chart |
| `c:area3DChart` | 3D area chart |
| `c:ofPieChart` | Bar of pie / pie of pie |

---

## 9. SmartArt / Diagrams

SmartArt diagrams reference three parts:

1. **Layout** (`ppt/diagrams/layout1.xml`) — structure
2. **Data** (`ppt/diagrams/data1.xml`) — content
3. **Style** (`ppt/diagrams/quickStyle1.xml`) — colors/fonts

Referenced via:

```xml
<a:graphic>
  <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/diagram">
    <dgm:relIds r:dm="rId1" r:lo="rId2" r:qs="rId3" r:cs="rId4"
        xmlns:dgm="http://schemas.openxmlformats.org/drawingml/2006/diagram"/>
  </a:graphicData>
</a:graphic>
```

---

## 10. Placing DrawingML in Different Document Types

### In Word Documents (Inline)

```xml
<w:r>
  <w:drawing>
    <wp:inline distT="0" distB="0" distL="114300" distR="114300">
      <wp:extent cx="3000000" cy="2000000"/>
      <wp:effectExtent l="0" t="0" r="0" b="0"/>
      <wp:docPr id="1" name="Image 1" descr="Alt text"/>
      <wp:cNvGraphicFramePr>
        <a:graphicFrameLocks noChangeAspect="1"/>
      </wp:cNvGraphicFramePr>
      <a:graphic>
        <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
          <pic:pic>...</pic:pic>
        </a:graphicData>
      </a:graphic>
    </wp:inline>
  </w:drawing>
</w:r>
```

### In Word Documents (Floating/Anchored)

```xml
<w:drawing>
  <wp:anchor distT="114300" distB="114300" distL="114300" distR="114300"
             simplePos="0" relativeHeight="251659264"
             behindDoc="0" locked="0"
             layoutInCell="1" allowOverlap="1">
    <wp:simplePos x="0" y="0"/>
    <wp:positionH relativeFrom="margin">
      <wp:posOffset>1000000</wp:posOffset>  <!-- from margin in EMU -->
    </wp:positionH>
    <wp:positionV relativeFrom="paragraph">
      <wp:posOffset>0</wp:posOffset>
    </wp:positionV>
    <wp:extent cx="3000000" cy="2000000"/>
    <wp:wrapSquare wrapText="both"/>
    <!-- Other wrap options: wrapNone | wrapThrough | wrapTight | wrapTopAndBottom -->
    <wp:docPr id="2" name="Floating Image"/>
    <a:graphic>...</a:graphic>
  </wp:anchor>
</w:drawing>
```

---

*Previous: [PresentationML ←](./07-presentationml.md) | Next: [Styles & Themes →](./09-styles-themes.md)*
