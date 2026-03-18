# Document deck quality

For text conversion workflows:

- inspect target `SKILL.md`
- ensure the workflow command is domain-correct
- run repository validations from `make test` and `make all`

For OOXML deck workflows:

- follow office package validation commands from the relevant skill
- include visual QA after generated deck output

For release checks:

- `make clean`
- `make build`
- `make verify`
