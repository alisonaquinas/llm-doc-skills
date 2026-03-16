# LaTeX Error Triage

Authoritative sources:
- TeX FAQ: <https://texfaq.org/>
- learnlatex: <https://www.learnlatex.org/en/>

## Frequent failure patterns

- Undefined control sequence
- Missing `$` inserted
- Runaway argument
- Missing package or class file
- Font not found under XeLaTeX or LuaLaTeX
- Citation or reference labels unresolved after one pass

## Triage order

1. Read the first real error, not the last line in the console.
2. Check the `.log` file around the first line-number reference.
3. Reduce to a minimal source if package interactions are suspected.
4. Re-run with a single engine choice pinned.
5. Confirm bibliography tool and output directory assumptions.

## Recovery patterns

- Replace smart quotes or copied rich-text punctuation in the source.
- Verify package names and class availability.
- Move recently added macros into a minimal test file.
- Rebuild from a clean intermediate set if auxiliary state is stale.
