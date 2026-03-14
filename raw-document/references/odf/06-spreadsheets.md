# ODF Spreadsheets (ODS)

> **Cross-references:** [Namespaces](./04-xml-namespaces.md) | [Styles & Formatting](./09-styles-formatting.md) | [Specification §2 (OpenFormula)](./02-specification.md) | [OOXML SpreadsheetML](../ooxml/06-spreadsheetml.md)

---

## 1. Overview

OpenDocument Spreadsheet (`.ods`) is the ODF format for spreadsheet documents. The spreadsheet content is contained in the `office:spreadsheet` body element within `content.xml`.

Key structures:

- **Tables** (`table:table`) correspond to sheets
- **Rows** (`table:table-row`) contain cells
- **Cells** (`table:table-cell`) contain values, formulas, and content
- **Named ranges**, **data pilots** (pivot tables), **database ranges**, and **charts** are all supported

---

## 2. Document Structure

```xml
<office:document-content ...>
  <office:automatic-styles>
    <!-- Column, row, and cell styles -->
  </office:automatic-styles>

  <office:body>
    <office:spreadsheet>

      <!-- Named ranges (optional) -->
      <table:named-expressions>
        <table:named-range table:name="MyRange"
                           table:base-cell-address="$Sheet1.$A$1"
                           table:cell-range-address="$Sheet1.$A$1:$D$10"/>
      </table:named-expressions>

      <!-- Sheets (tables) -->
      <table:table table:name="Sheet1" table:style-name="ta1">
        <!-- Sheet content -->
      </table:table>

      <table:table table:name="Sheet2">
        <!-- Second sheet -->
      </table:table>

    </office:spreadsheet>
  </office:body>
</office:document-content>
```

---

## 3. Sheet Structure

### Column Definitions

```xml
<table:table table:name="Sheet1" table:style-name="ta1"
             table:print="false">

  <!-- Column widths and styles -->
  <table:table-column table:style-name="co1"
                      table:number-columns-repeated="2"
                      table:default-cell-style-name="Default"/>
  <table:table-column table:style-name="co2"
                      table:default-cell-style-name="Default"/>
  <!-- ... more column definitions ... -->
```

Key attributes:

- `table:number-columns-repeated` — efficient repetition of identical columns
- `table:style-name` — column style (width, etc.)
- `table:visibility` — `visible` or `collapse` or `filter`

### Row Structure

```xml
  <table:table-row table:style-name="ro1">
    <table:table-cell office:value-type="string">
      <text:p>Header A</text:p>
    </table:table-cell>
    <table:table-cell office:value-type="string">
      <text:p>Header B</text:p>
    </table:table-cell>
    <table:table-cell table:number-columns-repeated="256"/>  <!-- empty cells -->
  </table:table-row>
```

Row attributes:

- `table:style-name` — row style (height, etc.)
- `table:visibility` — `visible`, `collapse`, `filter`
- `table:number-rows-repeated` — for identical consecutive rows

---

## 4. Cell Types and Values

### String Cell

```xml
<table:table-cell office:value-type="string"
                  table:style-name="ce1">
  <text:p>Hello World</text:p>
</table:table-cell>
```

### Numeric Cell

```xml
<table:table-cell office:value-type="float"
                  office:value="42.5"
                  table:style-name="ce2">
  <text:p>42.50</text:p>
</table:table-cell>
```

### Boolean Cell

```xml
<table:table-cell office:value-type="boolean"
                  office:boolean-value="true">
  <text:p>TRUE</text:p>
</table:table-cell>
```

### Currency Cell

```xml
<table:table-cell office:value-type="currency"
                  office:currency="USD"
                  office:value="1234.56">
  <text:p>$1,234.56</text:p>
</table:table-cell>
```

### Date Cell

```xml
<table:table-cell office:value-type="date"
                  office:date-value="2024-03-15">
  <text:p>03/15/2024</text:p>
</table:table-cell>
```

### Time/Duration Cell

```xml
<table:table-cell office:value-type="time"
                  office:time-value="PT2H30M0S">
  <text:p>2:30:00</text:p>
</table:table-cell>
```

### Error Cell

```xml
<table:table-cell office:value-type="string"
                  table:formula="of:=1/0">
  <text:p>#DIV/0!</text:p>
</table:table-cell>
```

### Empty Cell (Efficient Repetition)

```xml
<table:table-cell table:number-columns-repeated="100"/>
```

---

## 5. Formulas (OpenFormula Syntax)

ODF spreadsheets use the **OpenFormula** language for cell formulas (defined in ODF Part 2/4):

```xml
<table:table-cell table:formula="of:=SUM([.B2:.B10])"
                  office:value-type="float"
                  office:value="450">
  <text:p>450</text:p>
</table:table-cell>
```

### Reference Syntax

| Reference | Syntax | Example |
| --- | --- | --- |
| Relative cell | `[.COL ROW]` | `[.A1]` |
| Absolute cell | `[$COL$ROW]` | `[$A$1]` |
| Mixed | `[$COL ROW]` or `[.COL$ROW]` | `[$A1]`, `[.A$1]` |
| Range | `[.A1:.D10]` | `[.A1:.D10]` |
| Sheet reference | `[$Sheet.$A$1]` | `[$Sheet1.$B$3]` |
| Cross-sheet range | `[$Sheet1.$A$1:$Sheet2.$D$10]` | Multi-sheet range |
| Named range | `MyRange` | `SUM(MyRange)` |

### Common Functions

```text
SUM(range)             AVERAGE(range)        COUNT(range)
MAX(range)             MIN(range)            COUNTA(range)
IF(test, true, false)  IFERROR(expr, alt)    VLOOKUP(val, range, col)
HLOOKUP(val, range, row)   INDEX(range, row, col)   MATCH(val, range, type)
CONCATENATE(a, b, ...)  TEXT(value, format)  LEN(text)
LEFT(text, n)          RIGHT(text, n)        MID(text, start, n)
ROUND(num, digits)     INT(num)              ABS(num)
SQRT(num)              POWER(base, exp)      MOD(num, divisor)
TODAY()                NOW()                 DATE(year, month, day)
YEAR(date)             MONTH(date)           DAY(date)
```

Formula formula prefix is `of:` to identify OpenFormula syntax:

```xml
table:formula="of:=VLOOKUP([.A2],[$Sheet2.$A$1:$B$100],2,0)"
```

---

## 6. Merged/Spanned Cells

```xml
<!-- Cell spanning 2 columns and 2 rows -->
<table:table-cell table:number-columns-spanned="2"
                  table:number-rows-spanned="2"
                  office:value-type="string">
  <text:p>Merged Cell</text:p>
</table:table-cell>

<!-- Covered cells (placeholders) -->
<table:covered-table-cell/>
<table:covered-table-cell/>

<!-- On next row, also needs covered cells: -->
<table:table-row>
  <table:covered-table-cell/>
  <table:covered-table-cell/>
</table:table-row>
```

---

## 7. Sheet Tabs and Visibility

```xml
<!-- Sheet with tab color and visibility -->
<table:table table:name="HiddenSheet"
             table:style-name="ta1"
             table:display="false">
  <!-- Hidden sheet -->
</table:table>

<!-- Sheet tab color (LibreOffice extension) -->
<table:table-properties table:tab-color="#FF0000"/>
```

---

## 8. Named Ranges and Named Expressions

```xml
<table:named-expressions>

  <!-- Named range -->
  <table:named-range
      table:name="SalesData"
      table:base-cell-address="$Sheet1.$A$1"
      table:cell-range-address="$Sheet1.$A$1:$E$100"/>

  <!-- Named formula (calculated name) -->
  <table:named-expression
      table:name="LastRowIndex"
      table:base-cell-address="$Sheet1.$A$1"
      table:expression="of:=COUNTA($Sheet1.$A:$A)"/>

</table:named-expressions>
```

---

## 9. Data Validation

```xml
<table:content-validations>
  <table:content-validation table:name="val1"
                             table:condition="of:cell-content-is-between(1,100)"
                             table:allow-empty-cell="true"
                             table:display-list="no">
    <table:error-message table:display="true"
                         table:message-type="stop"
                         table:title="Invalid Input">
      <text:p>Value must be between 1 and 100.</text:p>
    </table:error-message>
    <table:help-message table:display="true"
                        table:title="Enter a Number">
      <text:p>Please enter a number between 1 and 100.</text:p>
    </table:help-message>
  </table:content-validation>
</table:content-validations>
```

---

## 10. Conditional Formatting

```xml
<table:conditional-formats>
  <table:conditional-format table:target-range-address="$Sheet1.$A$1:$A$100">
    <table:condition table:apply-style-name="GreenFill"
                     table:base-cell-address="$Sheet1.$A$1"
                     table:condition="of:cell-content()&gt;50"/>
    <table:condition table:apply-style-name="RedFill"
                     table:base-cell-address="$Sheet1.$A$1"
                     table:condition="of:cell-content()&lt;=50"/>
  </table:conditional-format>
</table:conditional-formats>
```

---

## 11. Data Pilot Tables (Pivot Tables)

```xml
<table:data-pilot-table table:name="PivotTable1"
                         table:application-data="true"
                         table:target-range-address="$Sheet2.$A$1"
                         table:source-cell-range-addresses="$Sheet1.$A$1:$E$100"
                         table:button-minimized="false"
                         table:show-filter-button="true">
  <table:source-cell-range
      table:cell-range-address="$Sheet1.$A$1:$E$100"/>

  <table:data-pilot-field table:source-field-name="Category"
                           table:orientation="row"/>
  <table:data-pilot-field table:source-field-name="Month"
                           table:orientation="column"/>
  <table:data-pilot-field table:source-field-name="Sales"
                           table:orientation="data"
                           table:function="sum"/>
</table:data-pilot-table>
```

---

## 12. Freeze and Splits

```xml
<!-- In settings.xml -->
<config:config-item config:name="HorizontalSplitMode" config:type="short">2</config:config-item>
<config:config-item config:name="VerticalSplitMode" config:type="short">2</config:config-item>
<config:config-item config:name="HorizontalSplitPosition" config:type="int">0</config:config-item>
<config:config-item config:name="VerticalSplitPosition" config:type="int">1</config:config-item>
<config:config-item config:name="PositionRight" config:type="int">0</config:config-item>
<config:config-item config:name="PositionBottom" config:type="int">1</config:config-item>
```

---

*Previous: [Text Documents ←](./05-text-documents.md) | Next: [Presentations →](./07-presentations.md)*
