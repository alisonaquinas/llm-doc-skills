# OOXML PresentationML (PPTX)

> **Cross-references:** [Namespaces](./04-xml-namespaces.md) | [DrawingML](./08-drawingml.md) | [Styles & Themes](./09-styles-themes.md) | [ODF Presentations](../odf/07-presentations.md)

---

## 1. Overview

PresentationML (PML) is the XML vocabulary for presentation documents in OOXML. It is defined in `pml.xsd` and uses the namespace:

```text
http://schemas.openxmlformats.org/presentationml/2006/main
```

Prefix: `p:`

---

## 2. Presentation Root (`ppt/presentation.xml`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation
    xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
    xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    saveSubsetFonts="1">

  <!-- Slide size -->
  <p:sldSz cx="9144000" cy="5143500" type="custom"/>
  <!-- cx/cy in EMU (English Metric Units): 1 inch = 914400 EMU -->
  <!-- 9144000 = 10 inches (widescreen width), 5143500 = 5.625 inches (widescreen height) -->

  <!-- Common slide sizes in EMU: -->
  <!-- Widescreen 16:9: cx=9144000 cy=5143500 type="custom" -->
  <!-- Standard 4:3: cx=9144000 cy=6858000 type="screen4x3" -->
  <!-- A4: cx=9144000 cy=6480000 type="A4" -->

  <!-- Notes size -->
  <p:notesSz cx="6858000" cy="9144000"/>

  <!-- Default text style -->
  <p:defaultTextStyle>
    <a:defPPr>
      <a:defRPr lang="en-US" dirty="0"/>
    </a:defPPr>
  </p:defaultTextStyle>

  <!-- Slide master list -->
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rId1"/>
  </p:sldMasterIdLst>

  <!-- Notes master -->
  <p:notesMasterIdLst>
    <p:notesMasterId r:id="rId4"/>
  </p:notesMasterIdLst>

  <!-- Slide list (order determines slide order) -->
  <p:sldIdLst>
    <p:sldId id="256" r:id="rId2"/>
    <p:sldId id="257" r:id="rId3"/>
  </p:sldIdLst>

</p:presentation>
```

---

## 3. Slide Structure (`ppt/slides/slide1.xml`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld
    xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
    xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
    xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <p:cSld>                            <!-- Common Slide Data -->
    <p:spTree>                        <!-- Shape Tree -->

      <!-- Group properties (required but invisible) -->
      <p:nvGrpSpPr>
        <p:cNvPr id="1" name=""/>
        <p:cNvGrpSpPr/>
        <p:nvPr/>
      </p:nvGrpSpPr>
      <p:grpSpPr>
        <a:xfrm>
          <a:off x="0" y="0"/>
          <a:ext cx="0" cy="0"/>
          <a:chOff x="0" y="0"/>
          <a:chExt cx="0" cy="0"/>
        </a:xfrm>
      </p:grpSpPr>

      <!-- Title shape -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="Title 1"/>
          <p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
          <p:nvPr>
            <p:ph type="title"/>      <!-- title | body | subTitle | dt | sldNum | ftr | hdr | obj | pic | tbl | chart | clipArt | dgm | media | sldImg | txBox -->
          </p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" dirty="0"/>
              <a:t>Slide Title Here</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Content shape (body) -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="3" name="Content Placeholder 2"/>
          <p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
          <p:nvPr>
            <p:ph idx="1"/>          <!-- idx 1 = first content placeholder -->
          </p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <!-- Bullet points -->
          <a:p>
            <a:pPr lvl="0"/>          <!-- indent level 0 = first level -->
            <a:r><a:rPr lang="en-US" dirty="0"/><a:t>First bullet</a:t></a:r>
          </a:p>
          <a:p>
            <a:pPr lvl="1"/>          <!-- indent level 1 = second level -->
            <a:r><a:rPr lang="en-US" dirty="0"/><a:t>Nested bullet</a:t></a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Picture shape -->
      <p:pic>
        <p:nvPicPr>
          <p:cNvPr id="4" name="Picture 3"/>
          <p:cNvPicPr/>
          <p:nvPr/>
        </p:nvPicPr>
        <p:blipFill>
          <a:blip r:embed="rId2"/>
          <a:stretch><a:fillRect/></a:stretch>
        </p:blipFill>
        <p:spPr>
          <a:xfrm>
            <a:off x="5000000" y="1000000"/>
            <a:ext cx="3000000" cy="2000000"/>
          </a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
      </p:pic>

    </p:spTree>
  </p:cSld>

  <!-- Slide layout reference -->
  <p:clrMapOvr>
    <a:masterClrMapping/>
  </p:clrMapOvr>

  <!-- Slide transitions -->
  <p:transition speed="med">
    <p:fade/>
  </p:transition>

  <!-- Slide timing (animations) -->
  <p:timing>
    <p:tnLst>
      <p:par>
        <p:cTn id="1" dur="indefinite" restart="whenNotActive" nodeType="tmRoot">
          <!-- Animation timeline -->
        </p:cTn>
      </p:par>
    </p:tnLst>
  </p:timing>

</p:sld>
```

---

## 4. Placeholder Types

| `p:ph type` | Description |
| --- | --- |
| `title` | Slide title |
| `body` | Main content body |
| `subTitle` | Subtitle (title slide) |
| `obj` | Generic object placeholder |
| `chart` | Chart placeholder |
| `tbl` | Table placeholder |
| `clipArt` | Clip art placeholder |
| `dgm` | Diagram/SmartArt placeholder |
| `media` | Media placeholder |
| `sldNum` | Slide number |
| `dt` | Date and time |
| `ftr` | Footer |
| `hdr` | Header |
| `pic` | Picture placeholder |
| `txBox` | Text box (no inherited placeholder style) |

---

## 5. Slide Master (`ppt/slideMasters/slideMaster1.xml`)

The slide master defines the overall visual theme for slides:

```xml
<p:sldMaster xmlns:p="..." xmlns:a="..." xmlns:r="...">

  <p:cSld>
    <p:bg>
      <p:bgRef idx="1001">
        <a:schemeClr val="bg1"/>
      </p:bgRef>
    </p:bg>

    <p:spTree>
      <!-- Define default placeholder positions and styles -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="Title Placeholder"/>
          <p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
          <p:nvPr><p:ph type="title"/></p:nvPr>
        </p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="457200" y="274638"/>
                  <a:ext cx="8229600" cy="1143000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
        </p:spPr>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" smtClean="0"/>
              <a:t>Click to edit Master title style</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>

  <!-- Color scheme mapping for this master -->
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2"
            accent1="accent1" accent2="accent2"
            accent3="accent3" accent4="accent4"
            accent5="accent5" accent6="accent6"
            hlink="hlink" folHlink="folHlink"/>

  <!-- List of layouts that use this master -->
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rId1"/>
    <p:sldLayoutId id="2147483650" r:id="rId2"/>
    <!-- ... more layouts ... -->
  </p:sldLayoutIdLst>

  <!-- Theme reference -->
  <p:txStyles>
    <!-- Master text styles for title, body, other -->
  </p:txStyles>

</p:sldMaster>
```

---

## 6. Slide Layouts (`ppt/slideLayouts/slideLayout1.xml`)

Layouts define template-specific positioning between a master and individual slides:

```xml
<p:sldLayout
    xmlns:p="..." xmlns:a="..."
    type="title"          <!-- Predefined layout type -->
    preserve="1">         <!-- Preserve placeholders from master -->

  <p:cSld name="Title Slide">
    <p:spTree>
      <!-- Override/add placeholders for this layout -->
    </p:spTree>
  </p:cSld>

</p:sldLayout>
```

Built-in layout types:

- `title` — Title slide
- `titleObj` — Title, content
- `twoObj` — Two content
- `objTx` — Content, caption
- `txObj` — Text, content
- `blank` — Blank
- `obj` — Content only
- `tx` — Title and text
- `twoTx` — Two text
- `picTx` — Picture with caption

---

## 7. Slide Transitions

```xml
<p:transition speed="med" advClk="0" advTm="3000">
  <!-- speed: slow | med | fast -->
  <!-- advClk: advance on click -->
  <!-- advTm: advance after milliseconds -->

  <!-- Transition effects (one of these): -->
  <p:fade/>
  <p:blinds dir="horz"/>          <!-- dir: horz | vert -->
  <p:checker dir="horz"/>
  <p:circle/>
  <p:dissolve/>
  <p:strips dir="lt-rb"/>         <!-- lt-rb | lt-rt | rb-lt | rt-lb -->
  <p:pull dir="l"/>               <!-- dir: d | l | r | u | lu | ru | ld | rd -->
  <p:wipe dir="l"/>
  <p:wedge/>
  <p:wheel spokes="4"/>           <!-- spokes: 1 | 2 | 3 | 4 | 8 -->
  <p:zoom dir="in"/>              <!-- dir: in | out -->
  <p:cut/>
  <p:push dir="l"/>
  <p:split dir="horz-in"/>        <!-- horz-in | horz-out | vert-in | vert-out -->
  <p:cover dir="l"/>
  <p:fly dir="b" hasBounce="1"/>
  <p:glitter dir="l" pattern="hexagon"/>
  <p:prism dir="l" isInverted="1"/>
  <p:vortex dir="l"/>
  <p:ripple clr="#FFFFFF"/>
  <p:honeycomb dir="l"/>
  <p:flash/>
  <p:shred pattern="strip" dir="in"/>
  <p:switch dir="l"/>
  <p:flip dir="l"/>
  <p:cube dir="l"/>
  <p:box dir="l"/>
  <p:doors dir="horz"/>
  <p:window dir="horz"/>
  <p:ferris dir="l"/>
  <p:gallery dir="l"/>
  <p:conveyor dir="l"/>
  <p:pan dir="l"/>
  <p:newsflash/>
  <p:rotate/>
  <p:orbit dir="l"/>
  <p:reveal dir="l"/>
  <p:flythrough dir="in" hasBounce="1"/>
  <p:wind dir="l"/>

</p:transition>
```

---

## 8. Animations

PresentationML uses a SMIL-like timing model:

```xml
<p:timing>
  <p:tnLst>
    <p:par>                           <!-- Parallel timing container -->
      <p:cTn id="1" dur="indefinite" restart="whenNotActive" nodeType="tmRoot">
        <p:childTnLst>

          <!-- Sequence of animations triggered on click -->
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>

                <!-- Animation group for a shape -->
                <p:par>
                  <p:cTn id="3" fill="hold">
                    <p:stCondLst>
                      <p:cond delay="indefinite"/>  <!-- Triggered on click -->
                    </p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="4" fill="hold">
                          <p:stCondLst>
                            <p:cond delay="0"/>
                          </p:stCondLst>
                          <p:childTnLst>

                            <!-- Fly-in animation -->
                            <p:animEffect transition="in" filter="fly(dir=from-bottom)">
                              <p:cBhvr>
                                <p:cTn id="5" dur="500" fill="hold"/>
                                <p:tgtEl>
                                  <p:spTgt spid="3"/>  <!-- Shape ID -->
                                </p:tgtEl>
                              </p:cBhvr>
                            </p:animEffect>

                          </p:childTnLst>
                        </p:cTn>
                      </p:par>
                    </p:childTnLst>
                  </p:cTn>
                </p:par>

              </p:childTnLst>
            </p:cTn>
          </p:seq>

        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>
```

---

## 9. Speaker Notes (`ppt/slides/slide1.xml` with notes reference)

Notes are in a separate part linked by relationship:

```xml
<!-- ppt/notesSlides/notesSlide1.xml -->
<p:notes xmlns:p="..." xmlns:a="...">
  <p:cSld>
    <p:spTree>
      <!-- Slide image placeholder -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="2" name="Slide Image Placeholder"/>
          <p:nvPr><p:ph type="sldImg"/></p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
      </p:sp>

      <!-- Notes text placeholder -->
      <p:sp>
        <p:nvSpPr>
          <p:cNvPr id="3" name="Notes Placeholder"/>
          <p:nvPr><p:ph type="body" idx="1"/></p:nvPr>
        </p:nvSpPr>
        <p:spPr/>
        <p:txBody>
          <a:bodyPr/>
          <a:lstStyle/>
          <a:p><a:r><a:rPr lang="en-US"/><a:t>Speaker notes here.</a:t></a:r></a:p>
        </p:txBody>
      </p:sp>

    </p:spTree>
  </p:cSld>
</p:notes>
```

---

*Previous: [SpreadsheetML ←](./06-spreadsheetml.md) | Next: [DrawingML →](./08-drawingml.md)*
