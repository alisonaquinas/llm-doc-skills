# m365 quality gate

Run the focused quality gate for the `m365` skill.

Recommended sequence:

```bash
python scripts/lint_skills.py m365
python scripts/validate_skills.py m365
powershell -File skills/m365/scripts/verify-m365-install.ps1
```

If the CLI is unavailable, record the install check as blocked and still run lint and validation.

For command-surface refreshes:

```bash
powershell -File skills/m365/scripts/collect-m365-help.ps1
git diff -- skills/m365/references/generated
```

Review generated output before committing. Help snapshots are evidence, not a substitute for current upstream docs.
