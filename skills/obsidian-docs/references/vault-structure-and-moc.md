# Vault Structure and Maps of Content

An Obsidian vault is a folder of plain Markdown files.
Structure it to match how the work is actually retrieved, not how it was originally created.

## Folder strategies

**Flat vault**: all notes in one folder, organized entirely by links and tags.
Works well for small vaults or workflows where search replaces folders.

**PARA**: Projects, Areas, Resources, Archives — four top-level folders that separate active work from reference material.
Projects contain goal-bound work; Areas hold ongoing responsibilities; Resources hold reference notes; Archives hold completed or inactive material.

**Topic-based**: top-level folders mirror major knowledge domains.
Suits reference-heavy vaults where browsing by subject is common.

## Maps of Content (MOC)

An MOC is a note whose primary purpose is to list and link related notes.
MOCs are not folders — they are navigable indexes that grow with the vault.

A minimal MOC structure:

```markdown
# MOC - Machine Learning

## Foundations
- [[Linear Algebra Review]]
- [[Probability Basics]]

## Models
- [[Decision Trees]]
- [[Neural Networks Overview]]

## Projects
- [[Sentiment Classifier - 2025]]
```

## Index note conventions

- Name the vault home note `000 Home`, `Index`, or `MOC - Home`.
- Link every major topic MOC from the home note.
- Keep MOC notes lean — they should point outward, not contain prose.
- Use heading sections within an MOC to group sub-topics.

## Linking hierarchy

Prefer bidirectional awareness: when note A links to note B, check whether note B should also link back.
Deep nesting of folders raises navigation cost; prefer shallower hierarchies with richer links.
