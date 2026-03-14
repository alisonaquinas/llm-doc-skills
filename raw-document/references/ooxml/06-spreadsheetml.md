# OOXML SpreadsheetML (XLSX)

> **Cross-references:** [Namespaces](./04-xml-namespaces.md) | [Styles & Themes](./09-styles-themes.md) | [DrawingML](./08-drawingml.md) | [ODF Spreadsheets](../odf/06-spreadsheets.md)

---

## 1. Overview

SpreadsheetML (SML) is the XML vocabulary for spreadsheet documents in OOXML. It is defined in `sml.xsd` and uses the namespace:

```text
http://schemas.openxmlformats.org/spreadsheetml/2006/main
```

Default prefix: (no prefix, default namespace) or `x:`

---

## 2. Workbook Structure (`xl/workbook.xml`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <fileVersion appName="xl" lastEdited="7" lowestEdited="7" rupBuild="23801"/>

  <workbookPr defaultThemeVersion="166925" codeName="ThisWorkbook"/>

  <!-- Workbook view settings -->
  <bookViews>
    <workbookView xWindow="0" yWindow="0" windowWidth="28800" windowHeight="12645"
                  activeTab="0"/>
  </bookViews>

  <!-- Sheet list -->
  <sheets>
    <sheet name="Sheet1" sheetId="1" r:id="rId1"/>
    <sheet name="Sheet2" sheetId="2" r:id="rId2"/>
    <sheet name="HiddenSheet" sheetId="3" state="hidden" r:id="rId3"/>
    <!-- state values: visible | hidden | veryHidden -->
  </sheets>

  <!-- Named ranges and expressions -->
  <definedNames>
    <definedName name="SalesData">Sheet1!$A$1:$E$100</definedName>
    <definedName name="PrintArea" localSheetId="0">Sheet1!$A$1:$G$50</definedName>
    <definedName name="_xlnm.Print_Titles" localSheetId="0">Sheet1!$1:$1</definedName>
  </definedNames>

  <calcPr calcId="181029" fullCalcOnLoad="1"/>

</workbook>
```

---

## 3. Worksheet Structure (`xl/worksheets/sheet1.xml`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
           xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">

  <!-- Sheet dimensions -->
  <dimension ref="A1:G50"/>

  <!-- Sheet view settings -->
  <sheetViews>
    <sheetView tabSelected="1" workbookViewId="0">
      <pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/>
      <!-- Freeze row 1: ySplit=1 means freeze after row 1 -->
      <selection pane="bottomLeft" activeCell="A2" sqref="A2"/>
    </sheetView>
  </sheetViews>

  <!-- Sheet formatting -->
  <sheetFormatPr defaultRowHeight="15" x14ac:dyDescent="0.25"
                 xmlns:x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"/>

  <!-- Column widths -->
  <cols>
    <col min="1" max="1" width="20" bestFit="1" customWidth="1"/>
    <col min="2" max="5" width="12" customWidth="1"/>
    <col min="6" max="1024" width="8.43"/>
  </cols>

  <!-- Sheet data -->
  <sheetData>
    <!-- Row 1 (header, height 20) -->
    <row r="1" ht="20" customHeight="1">
      <c r="A1" t="s">                  <!-- t="s" = shared string -->
        <v>0</v>                         <!-- index into sharedStrings.xml -->
      </c>
      <c r="B1" t="s"><v>1</v></c>
      <c r="C1" s="2" t="s"><v>2</v></c>   <!-- s="2" = style index -->
    </row>

    <!-- Row 2 (data) -->
    <row r="2">
      <c r="A2" t="s"><v>3</v></c>        <!-- string reference -->
      <c r="B2">                          <!-- number (no t attribute) -->
        <v>42.5</v>
      </c>
      <c r="C2" t="b">                    <!-- t="b" = boolean -->
        <v>1</v>
      </c>
      <c r="D2" t="d">                    <!-- t="d" = date (ISO 8601) -->
        <v>2024-03-15T00:00:00</v>
      </c>
      <c r="E2" s="3">                    <!-- formula cell -->
        <f>SUM(B2:B100)</f>
        <v>450</v>                        <!-- cached value -->
      </c>
      <c r="F2" t="e">                    <!-- t="e" = error -->
        <v>#DIV/0!</v>
      </c>
    </row>
  </sheetData>

  <!-- Merged cells -->
  <mergeCells count="1">
    <mergeCell ref="A10:C10"/>
  </mergeCells>

  <!-- Hyperlinks -->
  <hyperlinks>
    <hyperlink ref="A5" r:id="rId1" tooltip="Visit Example"/>
  </hyperlinks>

  <!-- Print setup -->
  <printOptions headings="0" gridLines="0"/>
  <pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75"
               header="0.3" footer="0.3"/>
  <pageSetup paperSize="9" orientation="portrait" r:id="rId2"/>

  <!-- Conditional formatting -->
  <conditionalFormatting sqref="B2:B100">
    <cfRule type="cellIs" dxfId="0" priority="1" operator="greaterThan">
      <formula>50</formula>
    </cfRule>
  </conditionalFormatting>

  <!-- Data validation -->
  <dataValidations count="1">
    <dataValidation type="whole" operator="between"
                    allowBlank="1" showInputMessage="1" showErrorAlert="1"
                    errorTitle="Invalid" error="Must be 1-100"
                    promptTitle="Enter Number" prompt="Enter a number 1-100"
                    sqref="C2:C100">
      <formula1>1</formula1>
      <formula2>100</formula2>
    </dataValidation>
  </dataValidations>

  <!-- Auto-filter -->
  <autoFilter ref="A1:G1"/>

  <!-- Table references -->
  <tableParts count="1">
    <tablePart r:id="rId3"/>
  </tableParts>

</worksheet>
```

---

## 4. Cell Value Types (`t` attribute)

| `t` value | Type | `v` Content |
| --- | --- | --- |
| *(absent)* | Number | Numeric value |
| `s` | Shared String | Index into `sharedStrings.xml` |
| `str` | Formula string | Inline string (for formula result strings) |
| `inlineStr` | Inline String | Contains `<is><t>text</t></is>` instead of `<v>` |
| `b` | Boolean | `1` = true, `0` = false |
| `e` | Error | Error string: `#VALUE!`, `#REF!`, `#DIV/0!`, `#NAME?`, `#NULL!`, `#NUM!`, `#N/A` |
| `d` | Date | ISO 8601 datetime string |

---

## 5. Shared Strings (`xl/sharedStrings.xml`)

Repeated strings are stored once in a shared string table, referenced by index:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
     count="15" uniqueCount="10">

  <!-- Index 0 -->
  <si>
    <t>Product Name</t>
  </si>

  <!-- Index 1 (rich text with formatting) -->
  <si>
    <r>
      <rPr>
        <b/>
        <sz val="11"/>
        <color rgb="FF000000"/>
        <rFont val="Calibri"/>
      </rPr>
      <t>Bold Header</t>
    </r>
  </si>

  <!-- Index 2 (with phonetic hints for East Asian text) -->
  <si>
    <t>Regular String</t>
    <phoneticPr fontId="1" type="fullwidthKatakana"/>
  </si>

</sst>
```

---

## 6. Styles (`xl/styles.xml`)

The styles file defines number formats, fonts, fills, borders, and cell formats:

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">

  <!-- Custom number formats (built-in formats use IDs 0–49) -->
  <numFmts count="2">
    <numFmt numFmtId="164" formatCode="#,##0.00"/>
    <numFmt numFmtId="165" formatCode="MM/DD/YYYY"/>
  </numFmts>

  <!-- Fonts -->
  <fonts count="3">
    <font>  <!-- Index 0: default -->
      <sz val="11"/>
      <color theme="1"/>
      <name val="Calibri"/>
      <family val="2"/>
      <scheme val="minor"/>
    </font>
    <font>  <!-- Index 1: bold -->
      <b/>
      <sz val="11"/>
      <color rgb="FF000000"/>
      <name val="Calibri"/>
    </font>
  </fonts>

  <!-- Fills -->
  <fills count="4">
    <fill><patternFill patternType="none"/></fill>         <!-- Index 0 -->
    <fill><patternFill patternType="gray125"/></fill>      <!-- Index 1 -->
    <fill>                                                  <!-- Index 2: solid fill -->
      <patternFill patternType="solid">
        <fgColor rgb="FF4472C4"/>
        <bgColor indexed="64"/>
      </patternFill>
    </fill>
  </fills>

  <!-- Borders -->
  <borders count="2">
    <border>  <!-- Index 0: no border -->
      <left/><right/><top/><bottom/><diagonal/>
    </border>
    <border>  <!-- Index 1: thin all around -->
      <left style="thin"><color indexed="64"/></left>
      <right style="thin"><color indexed="64"/></right>
      <top style="thin"><color indexed="64"/></top>
      <bottom style="thin"><color indexed="64"/></bottom>
    </border>
  </borders>

  <!-- Cell style formats (xf) -->
  <cellStyleXfs count="1">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0"/>
  </cellStyleXfs>

  <!-- Cell formats (xf) — referenced by cells via s attribute -->
  <cellXfs count="4">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>  <!-- s=0: default -->
    <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0"    <!-- s=1: bold+fill+border -->
        applyFont="1" applyFill="1" applyBorder="1">
      <alignment horizontal="center" vertical="center" wrapText="1"/>
    </xf>
    <xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0"  <!-- s=2: currency -->
        applyNumberFormat="1"/>
    <xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0"  <!-- s=3: date -->
        applyNumberFormat="1"/>
  </cellXfs>

  <!-- Named cell styles -->
  <cellStyles count="1">
    <cellStyle name="Normal" xfId="0" builtinId="0"/>
  </cellStyles>

  <!-- Differential formatting (for conditional formatting) -->
  <dxfs count="1">
    <dxf>
      <fill>
        <patternFill>
          <bgColor rgb="FF92D050"/>  <!-- green -->
        </patternFill>
      </fill>
    </dxf>
  </dxfs>

</styleSheet>
```

---

## 7. Formulas

Formulas use standard Excel formula syntax (not the `of:` prefix of ODF):

```xml
<!-- SUM formula with absolute reference -->
<c r="B10" s="2">
  <f>SUM(B2:B9)</f>
  <v>450</v>
</c>

<!-- Array formula (Ctrl+Shift+Enter) -->
<c r="F2">
  <f t="array" ref="F2">SUM(B2:B10*C2:C10)</f>
  <v>1250</v>
</c>

<!-- Shared formula (efficient repetition) -->
<c r="D2">
  <f t="shared" ref="D2:D100" si="0">B2*C2</f>
  <v>84</v>
</c>
<c r="D3">
  <f t="shared" si="0"/>  <!-- references shared formula si=0 -->
  <v>90</v>
</c>

<!-- Table formula -->
<c r="E2">
  <f>Table1[[#This Row],[Qty]]*Table1[[#This Row],[Price]]</f>
  <v>42</v>
</c>
```

---

## 8. Tables (`xl/tables/table1.xml`)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<table xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
       id="1" name="SalesTable" displayName="SalesTable"
       ref="A1:E100" totalsRowShown="0">

  <autoFilter ref="A1:E100"/>

  <tableColumns count="5">
    <tableColumn id="1" name="Product"/>
    <tableColumn id="2" name="Q1"/>
    <tableColumn id="3" name="Q2"/>
    <tableColumn id="4" name="Q3"/>
    <tableColumn id="5" name="Total"
                 totalsRowFormula="SUM([Total])"/>
  </tableColumns>

  <tableStyleInfo name="TableStyleMedium9" showFirstColumn="0"
                  showLastColumn="0" showRowStripes="1" showColumnStripes="0"/>

</table>
```

---

## 9. Pivot Tables

```xml
<!-- xl/pivotTables/pivotTable1.xml -->
<pivotTableDefinition xmlns="..." name="PivotTable1"
                       cacheId="1" dataCaption="Values"
                       updateOnLoad="1">
  <location ref="A3:D10" firstHeaderRow="1" firstDataRow="2" firstDataCol="1"/>

  <pivotFields count="5">
    <pivotField name="Category" axis="axisRow" showAll="0"/>
    <pivotField name="Month" axis="axisCol" showAll="0"/>
    <pivotField name="Amount" dataField="1" showAll="0"/>
  </pivotFields>

  <rowFields count="1">
    <field x="0"/>
  </rowFields>

  <colFields count="1">
    <field x="1"/>
  </colFields>

  <dataFields count="1">
    <dataField name="Sum of Amount" fld="2" subtotal="sum"/>
  </dataFields>

</pivotTableDefinition>
```

---

## 10. Charts (Reference to DrawingML)

Charts in XLSX are defined as DrawingML chart parts in `xl/charts/chart1.xml`. See [DrawingML](./08-drawingml.md) for chart element reference.

The worksheet drawing layer (`xl/drawings/drawing1.xml`) places charts and images:

```xml
<!-- xl/drawings/drawing1.xml -->
<xdr:wsDr xmlns:xdr="http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing">
  <xdr:twoCellAnchor moveWithCells="0" sizeWithCells="0">
    <xdr:from><xdr:col>0</xdr:col><xdr:colOff>0</xdr:colOff>
              <xdr:row>5</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:from>
    <xdr:to><xdr:col>7</xdr:col><xdr:colOff>0</xdr:colOff>
            <xdr:row>25</xdr:row><xdr:rowOff>0</xdr:rowOff></xdr:to>
    <xdr:graphicFrame macro="">
      <xdr:nvGraphicFramePr>
        <xdr:cNvPr id="2" name="Chart 1"/>
        <xdr:cNvGraphicFramePr/>
      </xdr:nvGraphicFramePr>
      <xdr:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/></xdr:xfrm>
      <a:graphic>
        <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/chart">
          <c:chart r:id="rId1"
              xmlns:c="http://schemas.openxmlformats.org/drawingml/2006/chart"/>
        </a:graphicData>
      </a:graphic>
    </xdr:graphicFrame>
    <xdr:clientData/>
  </xdr:twoCellAnchor>
</xdr:wsDr>
```

---

*Previous: [WordprocessingML ←](./05-wordprocessingml.md) | Next: [PresentationML →](./07-presentationml.md)*
