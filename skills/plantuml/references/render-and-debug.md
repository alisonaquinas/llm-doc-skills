# Render and Debug

PlantUML debugging is usually fastest when the render path is made explicit and the source is reduced quickly.

## Render strategy

- prefer a local PlantUML executable when available
- fall back to a Java plus JAR workflow if that is the documented environment
- render SVG first when visual diffing matters
- use PNG when a destination does not handle SVG well

## Debug flow

1. confirm Java or the PlantUML launcher is available
2. confirm include paths resolve from the current working directory
3. render a minimal file with the same theme or include structure
4. add complexity back one block at a time

## Common failure modes

- Java is missing even though the PlantUML JAR exists
- includes resolve locally but not in CI
- notes or long labels cause unreadable wrapping
- layout hints fight each other and produce unstable output
