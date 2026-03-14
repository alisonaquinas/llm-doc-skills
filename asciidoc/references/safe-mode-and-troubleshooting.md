# Asciidoctor Safe Mode and Troubleshooting

Authoritative source:
- Asciidoctor CLI docs: <https://docs.asciidoctor.org/asciidoctor/latest/cli/options/>

## Safe modes

- `unsafe`
- `safe`
- `server`
- `secure`

Safe mode affects includes, file access, and broader processor behavior.
Keep the chosen mode explicit in automation.

## Troubleshooting order

1. Confirm whether the backend is HTML, PDF, or DocBook.
2. Check safe-mode assumptions for includes and assets.
3. Verify document attributes and partial paths.
4. Reduce to a one-file example when backend-specific rendering diverges.
