# Obsidian vault health check

Run health checks on a local Obsidian vault.

## Broken wikilinks

Search for wikilinks whose targets do not exist as vault files:

```bash
# List all wikilink targets in Markdown files
grep -roh '\[\[[^\]]*\]\]' /path/to/vault --include="*.md" | sort -u
```

Cross-reference the output against the actual file list to identify unresolved links.
Obsidian highlights unresolved links in the editor; the graph view also shows them as disconnected nodes.

## Orphan notes

Find notes with no inbound or outbound wikilinks:

```bash
# Notes that contain no wikilinks at all
grep -rL '\[\[' /path/to/vault --include="*.md"
```

Review orphan notes to decide whether to integrate them into the vault graph or archive them.

## Canvas JSON validation

Validate all `.canvas` files parse as well-formed JSON:

```bash
for f in /path/to/vault/**/*.canvas; do
  python -c "import json,sys; json.load(open(sys.argv[1]))" "$f" \
    && echo "OK: $f" \
    || echo "INVALID: $f"
done
```

## Frontmatter validation

Check that all notes in a templates folder contain YAML frontmatter:

```bash
# Notes missing a frontmatter block (no leading ---)
grep -rL '^---' /path/to/vault/Templates --include="*.md"
```

For broader validation, use the Obsidian Linter community plugin to enforce frontmatter schemas vault-wide.

## Tag audit

List all tags used in the vault and their frequency:

```bash
grep -roh '#[A-Za-z0-9_/\-]*' /path/to/vault --include="*.md" \
  | sort | uniq -c | sort -rn
```

Review for inconsistent capitalization, unused tags, or tags that should be merged.

## Empty or near-empty notes

Flag notes under a minimum line threshold:

```bash
# Notes with fewer than 5 lines of content
find /path/to/vault -name "*.md" -not -path "*/.obsidian/*" | while read f; do
  lines=$(wc -l < "$f")
  [ "$lines" -lt 5 ] && echo "$lines $f"
done | sort -n
```

## Plugin configuration validation

Confirm community plugins list is valid JSON:

```bash
python -c "import json; json.load(open('/path/to/vault/.obsidian/community-plugins.json'))"
python -c "import json; json.load(open('/path/to/vault/.obsidian/app.json'))"
python -c "import json; json.load(open('/path/to/vault/.obsidian/appearance.json'))"
```
