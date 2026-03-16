# Validation and Recovery Workflows

Use this guide when the task is not just "look up an element" but actually
validate XML, confirm package invariants, or triage why a document package will
not open.

## Preflight

Before doing schema work, check what is available locally:

```bash
command -v unzip
command -v zipinfo
command -v python3
command -v xmllint || command -v xmlstarlet || true
python3 - <<'PY'
try:
    import lxml  # noqa: F401
    print("lxml: ok")
except Exception as exc:
    print(f"lxml: missing ({exc})")
PY
```

Prefer `scripts/validate_xml.py` for schema validation because the bundled
OOXML XSD files are canonical and spread across multiple directories; the
helper stages the dependency closure automatically.

## OOXML Validation Workflow

1. Identify the package and part to validate.
   - `.docx` main body → `word/document.xml` with `--schema wml`
   - `.xlsx` workbook or worksheet parts → SpreadsheetML with `--schema sml`
   - `.pptx` presentation or slide parts → PresentationML with `--schema pml`
2. Validate from the package directly when possible.
3. Use `--strict` only for parts that already use the Strict `purl.oclc.org`
   namespaces.

```bash
python scripts/validate_xml.py \
  --family ooxml --schema wml --package document.docx --part word/document.xml
```

## ODF Validation Workflow

1. Extract or point at `content.xml`, `styles.xml`, or another ODF XML part.
2. Let the helper detect `office:version` when the XML uses 1.3 or 1.4.
3. If the document is older ODF 1.2, stop and explain that this skill bundles
   only ODF 1.3 and 1.4 schemas.

```bash
unzip -p document.odt content.xml > content.xml
python scripts/validate_xml.py --family odf --xml content.xml
```

## Common Failure Modes

| Symptom | Likely Cause | Next Move |
| --- | --- | --- |
| Schema root fails to load | OOXML XSD imports are not staged together | Use `scripts/validate_xml.py` instead of a direct `xmllint --schema ...` call |
| Strict validation says no global declaration for `w:document` | Transitional namespace used with Strict schema | Rewrite to the Strict `purl.oclc.org/ooxml/...` namespace or use Transitional validation |
| ODF validation fails immediately on `office:version="1.2"` | Only ODF 1.3 and 1.4 schemas are bundled locally | Call out the version mismatch; validate semantically or obtain a 1.2 schema set |
| Package opens as ZIP but not in Office/LibreOffice | Missing `[Content_Types].xml`, `.rels`, or manifest invariants | Triage package structure before editing any XML |
| ODF package will not open after repack | `mimetype` not first and stored | Rebuild with `mimetype` first and uncompressed |

## Broken Package Triage

### OOXML

Check these first:

- `[Content_Types].xml`
- `_rels/.rels`
- the expected main part such as `word/document.xml`, `xl/workbook.xml`, or `ppt/presentation.xml`
- part-local relationship files when references are broken

### ODF

Check these first:

- `mimetype` exists, is the first entry, and is stored (not deflated)
- `META-INF/manifest.xml` lists every file you added
- `content.xml` and `styles.xml` both remain well-formed XML

Use `zipinfo -v document.odt` when you need proof that `mimetype` is first and
stored.
