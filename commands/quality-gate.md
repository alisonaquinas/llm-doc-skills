# Document and publishing quality gate

Run the quality gates for `llm-doc-skills`.

- If a skill name is provided:
  - `python scripts/lint_skills.py <skill-name>` (if script is present)
  - `python scripts/validate_skills.py <skill-name>` (if script is present)
- For repository-wide checks:
  - `make test`
  - `make all`
- For packaging checks:
  - `make clean`
  - `make build`
  - `make verify`
