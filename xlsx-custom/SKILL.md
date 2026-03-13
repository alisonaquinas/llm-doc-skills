---
name: xlsx-custom
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
---

# Requirements for Outputs

## Intent Router

Load sections based on the task:
- **Create new spreadsheet** → "Creating new Excel files" for openpyxl patterns with formulas
- **Edit existing file** → "Editing existing Excel files" for load/modify/save workflow
- **Data analysis** → "Reading and analyzing data" for pandas operations
- **Formulas** → "CRITICAL: Use Formulas, Not Hardcoded Values" + "Recalculating formulas" for Excel formula patterns
- **Financial models** → "Financial models" section for color coding, number formatting, and formula construction rules
- **Validation** → "Formula Verification Checklist" and "Recalculating formulas" for error detection
- **Best practices** → "Best Practices" for library selection (pandas vs openpyxl) and working patterns

## All Excel files

### Professional Font

- Use a consistent, professional font (e.g., Arial, Times New Roman) for all deliverables unless otherwise instructed by the user

### Zero Formula Errors

- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preserve Existing Templates (when updating templates)

- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards

Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions

- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Number Formatting Standards

#### Required Format Rules

- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

### Formula Construction Rules

#### Assumptions Placement

- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

#### Formula Error Prevention

- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

#### Documentation Requirements for Hardcodes

- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

## XLSX creation, editing, and analysis

### Overview

A user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.

## Important Requirements

**LibreOffice Required for Formula Recalculation**: You can assume LibreOffice is installed for recalculating formula values using the `xlsx-custom/scripts/recalc.py` script. The script automatically configures LibreOffice on first run, including in sandboxed environments where Unix sockets are restricted (handled by `office-custom/scripts/soffice.py`)

## Reading and analyzing data

### Data analysis with pandas

For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Excel File Workflows

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.

### ❌ WRONG - Hardcoding Calculated Values

```text
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### ✅ CORRECT - Using Excel Formulas

```text
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

This applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.

## Common Workflow

1. **Choose tool**: pandas for data, openpyxl for formulas/formatting
2. **Create/Load**: Create new workbook or load existing file
3. **Modify**: Add/edit data, formulas, and formatting
4. **Save**: Write to file
5. **Recalculate formulas (MANDATORY IF USING FORMULAS)**: Use the xlsx-custom/scripts/recalc.py script

   ```bash
   python xlsx-custom/scripts/recalc.py output.xlsx
   ```

6. **Verify and fix any errors**:
   - The script returns JSON with error details
   - If `status` is `errors_found`, check `error_summary` for specific error types and locations
   - Fix the identified errors and recalculate again
   - Common errors to fix:
     - `#REF!`: Invalid cell references
     - `#DIV/0!`: Division by zero
     - `#VALUE!`: Wrong data type in formula
     - `#NAME?`: Unrecognized formula name

### Creating new Excel files

```text
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editing existing Excel files

```text
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## Recalculating formulas

Excel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `xlsx-custom/scripts/recalc.py` script to recalculate formulas:

```bash
python xlsx-custom/scripts/recalc.py <excel_file> [timeout_seconds]
```

Example:

```bash
python xlsx-custom/scripts/recalc.py output.xlsx 30
```

The script:
- Automatically sets up LibreOffice macro on first run
- Recalculates all formulas in all sheets
- Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.)
- Returns JSON with detailed error locations and counts
- Works on both Linux and macOS

## Formula Verification Checklist

Quick checks to ensure formulas work correctly:

### Essential Verification

- [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model
- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK)
- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)

### Common Pitfalls

- [ ] **NaN handling**: Check for null values with `pd.notna()`
- [ ] **Far-right columns**: FY data often in columns 50+
- [ ] **Multiple matches**: Search all occurrences, not just first
- [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!)
- [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!)
- [ ] **Cross-sheet references**: Use correct format (Sheet1!A1) for linking sheets

### Formula Testing Strategy

- [ ] **Start small**: Test formulas on 2-3 cells before applying broadly
- [ ] **Verify dependencies**: Check all cells referenced in formulas exist
- [ ] **Test edge cases**: Include zero, negative, and very large values

### Interpreting xlsx-custom/scripts/recalc.py Output

The script returns JSON with error details:

```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## Best Practices

### Library Selection

- **pandas**: Best for data analysis, bulk operations, and simple data export
- **openpyxl**: Best for complex formatting, formulas, and Excel-specific features

### Working with openpyxl

- Cell indices are 1-based (row=1, column=1 refers to cell A1)
- Use `data_only=True` to read calculated values: `load_workbook('file.xlsx', data_only=True)`
- **Warning**: If opened with `data_only=True` and saved, formulas are replaced with values and permanently lost
- For large files: Use `read_only=True` for reading or `write_only=True` for writing
- Formulas are preserved but not evaluated - use xlsx-custom/scripts/recalc.py to update values

### Working with pandas

- Specify data types to avoid inference issues: `pd.read_excel('file.xlsx', dtype={'id': str})`
- For large files, read specific columns: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- Handle dates properly: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## Code Style Guidelines

**IMPORTANT**: When generating Python code for Excel operations:
- Write minimal, concise Python code without unnecessary comments
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

**For Excel files themselves**:
- Add comments to cells with complex formulas or important assumptions
- Document data sources for hardcoded values
- Include notes for key calculations and model sections

---

## API Reference

> Sources: [openpyxl docs](https://openpyxl.readthedocs.io/), [pandas docs](https://pandas.pydata.org/docs/)

### openpyxl (version 3.x)

#### Workbook

```python
from openpyxl import Workbook, load_workbook

wb = Workbook()                              # New workbook
wb = load_workbook("file.xlsx")              # Load existing
wb = load_workbook("file.xlsx", data_only=True)   # Read cached values (formulas lost on save)
wb = load_workbook("file.xlsx", read_only=True)   # Memory-efficient read
```

| Method | Parameters | Returns | Notes |
|--------|-----------|---------|-------|
| `wb.active` | — | `Worksheet` | First sheet |
| `wb[name]` | `str` | `Worksheet` | Access by name |
| `wb.create_sheet(title, index)` | `str`, `int` | `Worksheet` | Append or insert |
| `wb.remove(sheet)` | `Worksheet` | `None` | |
| `wb.copy_worksheet(from_ws)` | `Worksheet` | `Worksheet` | |
| `wb.save(filename)` | `str` | `None` | |
| `wb.close()` | — | `None` | |
| `wb.add_named_style(style)` | `NamedStyle` | `None` | |

**Properties:** `wb.sheetnames`, `wb.worksheets`, `wb.defined_names`

#### Worksheet

```text
ws = wb.active
ws.title = "Summary"
ws["A1"] = "Hello"
ws.cell(row=1, column=1).value = "Hello"   # 1-based indexing
ws.append(["a", "b", "c"])                  # Add row
```

| Method | Parameters | Notes |
|--------|-----------|-------|
| `ws["A1"]` | cell ref | Returns `Cell` |
| `ws["A1:C3"]` | range | Returns tuple of tuples |
| `ws.cell(row, column, value)` | 1-based | |
| `ws.iter_rows(min_row, max_row, min_col, max_col, values_only)` | | Generator of rows |
| `ws.iter_cols(min_row, max_row, min_col, max_col, values_only)` | | Generator of cols |
| `ws.append(iterable)` | list/dict | Append row |
| `ws.insert_rows(idx, amount)` | | |
| `ws.delete_rows(idx, amount)` | | |
| `ws.insert_cols(idx, amount)` | | |
| `ws.delete_cols(idx, amount)` | | |
| `ws.merge_cells(range_string)` | `"A1:C3"` | |
| `ws.unmerge_cells(range_string)` | | |
| `ws.add_chart(chart, anchor)` | `Chart`, `"E1"` | |
| `ws.add_image(img, anchor)` | `Image`, `"A1"` | |
| `ws.add_table(table)` | `Table` | |
| `ws.set_printer_settings(paper_size, orientation)` | | |
| `ws.freeze_panes` | `str` | e.g., `"B2"` freezes row 1 and col A |
| `ws.auto_filter.ref` | `str` | e.g., `"A1:F1"` |
| `ws.sheet_state` | `str` | `"visible"`, `"hidden"`, `"veryHidden"` |

**Dimensions:** `ws.dimensions`, `ws.min_row`, `ws.max_row`, `ws.min_column`, `ws.max_column`

**Column/row sizing:**

```text
ws.column_dimensions["A"].width = 20
ws.row_dimensions[1].height = 30
ws.column_dimensions["A"].hidden = True
ws.row_dimensions[1].hidden = True
```

#### Cell

```text
cell = ws["A1"]
cell.value = "Hello"
cell.value = "=SUM(B1:B10)"    # Formula (string starting with "=")
cell.number_format = "$#,##0.00"
cell.comment = Comment("Note", "Author")
```

| Property | Type | Notes |
|----------|------|-------|
| `.value` | any | `None`, `int`, `float`, `str`, `datetime`, formula string |
| `.data_type` | `str` | `"n"` (number), `"s"` (string), `"b"` (bool), `"f"` (formula) |
| `.row`, `.column` | `int` | 1-based |
| `.column_letter` | `str` | e.g., `"A"`, `"BL"` |
| `.coordinate` | `str` | e.g., `"A1"` |
| `.font` | `Font` | |
| `.fill` | `PatternFill \| GradientFill` | |
| `.border` | `Border` | |
| `.alignment` | `Alignment` | |
| `.number_format` | `str` | |
| `.protection` | `Protection` | |
| `.comment` | `Comment \| None` | |
| `.hyperlink` | `str \| Hyperlink \| None` | |

#### Styling

```python
from openpyxl.styles import Font, PatternFill, GradientFill, Border, Side, Alignment, Protection, numbers
from openpyxl.styles import NamedStyle
from openpyxl.utils import get_column_letter, column_index_from_string

# Font
cell.font = Font(
    name="Arial",          # Typeface
    size=12,               # pt
    bold=True,
    italic=True,
    underline="single",    # "single", "double", "singleAccounting", "doubleAccounting"
    strike=False,
    color="FF0000",        # Hex ARGB (no "#"): "FF" prefix = fully opaque
    vertAlign="superscript"  # "superscript", "subscript"
)

# Fill
cell.fill = PatternFill(
    fill_type="solid",     # "solid", "darkGray", "mediumGray", "lightGray", "gray125", "gray0625"
    start_color="FFFF00",  # Hex ARGB
    end_color="FFFF00",
)

# Gradient fill
cell.fill = GradientFill(
    type="linear",
    degree=90,
    stop=["000000", "FFFFFF"]
)

# Border
thin = Side(border_style="thin", color="000000")
cell.border = Border(
    left=thin, right=thin, top=thin, bottom=thin,
    diagonal=Side(border_style="thin"), diagonal_direction=1,  # 1=up-right, 2=up-left, 3=both
)
# Border styles: "thin", "medium", "thick", "dashed", "dotted", "double",
#                "hair", "mediumDashed", "dashDot", "mediumDashDot",
#                "dashDotDot", "mediumDashDotDot", "slantDashDot"

# Alignment
cell.alignment = Alignment(
    horizontal="center",     # "left", "center", "right", "fill", "justify", "centerContinuous", "distributed"
    vertical="middle",       # "top", "center", "bottom", "justify", "distributed"
    wrap_text=True,
    shrink_to_fit=False,
    text_rotation=45,        # degrees
    indent=0,
)
```

#### Number formats

```text
cell.number_format = "$#,##0"              # Currency, no decimals
cell.number_format = "$#,##0.00"           # Currency, 2 decimals
cell.number_format = "$#,##0;($#,##0);-"  # Currency, negative in parens, zero as "-"
cell.number_format = "0.0%"               # Percentage 1 decimal
cell.number_format = "0.0x"              # Multiple (1.5x)
cell.number_format = "#,##0"             # Thousands separator
cell.number_format = "0.00E+00"          # Scientific
cell.number_format = "YYYY-MM-DD"        # Date
cell.number_format = "General"           # Auto
cell.number_format = "@"                 # Text (forces text even for numbers)
```

#### Charts

```python
from openpyxl.chart import BarChart, LineChart, PieChart, ScatterChart, Reference, Series

chart = BarChart()
chart.type = "col"              # "col" (vertical), "bar" (horizontal)
chart.grouping = "clustered"    # "clustered", "stacked", "percentStacked"
chart.overlap = 0               # % overlap for clustered
chart.title = "Revenue"
chart.y_axis.title = "USD ($mm)"
chart.x_axis.title = "Year"
chart.style = 10                # Excel built-in style (1-48)
chart.width = 15                # cm
chart.height = 10               # cm
chart.legend.position = "b"     # "b", "t", "l", "r", "tr"

data = Reference(ws, min_col=2, min_row=1, max_col=5, max_row=10)
cats = Reference(ws, min_col=1, min_row=2, max_row=10)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)

ws.add_chart(chart, "G1")
```

**Available chart types:** `BarChart`, `LineChart`, `PieChart`, `DoughnutChart`, `ScatterChart`, `BubbleChart`, `AreaChart`, `RadarChart`, `StockChart`, `SurfaceChart` — all with 3D variants via `chart.type = "3D"`.

#### Data validation

```python
from openpyxl.worksheet.datavalidation import DataValidation

dv = DataValidation(
    type="list",
    formula1='"Option1,Option2,Option3"',  # Dropdown list
    showDropDown=False,                     # False = show dropdown arrow
    showErrorMessage=True,
    errorTitle="Invalid",
    error="Choose from list",
)
ws.add_data_validation(dv)
dv.add("A1:A100")
```

#### Conditional formatting

```python
from openpyxl.styles import PatternFill
from openpyxl.formatting.rule import ColorScaleRule, DataBarRule, IconSetRule, Rule, FormulaRule, CellIsRule
from openpyxl.styles.differential import DifferentialStyle

# Color scale
ws.conditional_formatting.add("B2:B100",
    ColorScaleRule(start_type="min", start_color="FF0000",
                   mid_type="percentile", mid_value=50, mid_color="FFFF00",
                   end_type="max", end_color="00FF00"))

# Formula rule
red_fill = PatternFill(bgColor="FFC7CE")
dxf = DifferentialStyle(fill=red_fill)
rule = Rule(type="expression", dxf=dxf, formula=["$B1<0"])
ws.conditional_formatting.add("A1:Z100", rule)
```

#### Utility functions

```python
from openpyxl.utils import get_column_letter, column_index_from_string, coordinate_to_tuple, absolute_coordinate

get_column_letter(1)          # "A"
get_column_letter(64)         # "BL"
column_index_from_string("A") # 1
column_index_from_string("BL")# 64
coordinate_to_tuple("A1")    # (1, 1)
absolute_coordinate("A1")    # "$A$1"
```

---

### pandas (data analysis & I/O)

#### Reading

```python
import pandas as pd

df = pd.read_excel("file.xlsx")
df = pd.read_excel("file.xlsx", sheet_name="Sheet1")
df = pd.read_excel("file.xlsx", sheet_name=None)      # All sheets → dict
df = pd.read_excel("file.xlsx",
    header=0,            # Row index of header (0-based), None = no header
    skiprows=2,          # Skip N rows before header
    usecols="A:F",       # Columns to parse (letter range, list, or callable)
    nrows=100,           # Read only N rows
    dtype={"id": str},   # Force dtypes
    parse_dates=["date"],# Parse as datetime
    na_values=["N/A", "-"],  # Additional NA strings
    engine="openpyxl",   # Required for .xlsx
)
df = pd.read_csv("file.csv", sep=",", encoding="utf-8")
df = pd.read_csv("file.tsv", sep="\t")
```

#### Writing

```text
df.to_excel("output.xlsx", index=False, sheet_name="Data", startrow=0, startcol=0)

# Multiple sheets
with pd.ExcelWriter("output.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="Sheet1", index=False)
    df2.to_excel(writer, sheet_name="Sheet2", index=False)

# Append to existing file
with pd.ExcelWriter("existing.xlsx", engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
    df.to_excel(writer, sheet_name="NewSheet", index=False)
```

#### Key DataFrame operations

```text
df.shape          # (rows, cols)
df.dtypes         # Column types
df.info()         # Summary
df.describe()     # Statistics
df.head(n)        # First n rows
df.tail(n)        # Last n rows

# Selection
df["col"]                    # Series
df[["col1","col2"]]          # DataFrame
df.loc[row_label, col_label] # Label-based
df.iloc[row_idx, col_idx]    # Integer-based
df.loc[df["col"] > 0]        # Boolean mask

# Operations
df["new_col"] = df["a"] + df["b"]
df.rename(columns={"old": "new"}, inplace=True)
df.drop(columns=["col"], inplace=True)
df.fillna(0, inplace=True)
df.dropna(subset=["col"], inplace=True)
df.sort_values("col", ascending=False, inplace=True)
df.groupby("col").agg({"value": "sum"})
df.pivot_table(values="sales", index="region", columns="year", aggfunc="sum")

# Type handling
df["col"] = pd.to_numeric(df["col"], errors="coerce")
df["date"] = pd.to_datetime(df["date"])
df["col"] = df["col"].astype(str)
```

#### Common Excel formula equivalents

| Excel | pandas |
|-------|--------|
| `SUM(A:A)` | `df["A"].sum()` |
| `AVERAGE(A:A)` | `df["A"].mean()` |
| `COUNT(A:A)` | `df["A"].count()` |
| `COUNTA(A:A)` | `df["A"].notna().sum()` |
| `MAX(A:A)` | `df["A"].max()` |
| `MIN(A:A)` | `df["A"].min()` |
| `IF(A1>0, "Yes","No")` | `df["A"].apply(lambda x: "Yes" if x>0 else "No")` |
| `VLOOKUP` | `df.merge(ref, on="key", how="left")` |
| `COUNTIF(A:A, "x")` | `(df["A"] == "x").sum()` |
| `SUMIF` | `df[df["A"]>0]["B"].sum()` |
