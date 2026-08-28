# Documentation Accessibility

Rules for documentation pages, code blocks, and embedded charts: headings, alt text, links, tables, diagrams, and color. For documentation architecture and content, use the `developer-docs` skill.

## Headings

1. One h1 per page, then a logical hierarchy that never skips levels.
2. Headings are descriptive: they say what the section contains.
3. Heading structure carries the hierarchy; style alone never marks levels.

## Alt text and links

1. Meaningful images have alt text that conveys the same information; decorative images use empty alt.
2. Screenshots are avoided when text would carry the information better.
3. Diagrams have a text equivalent: a description, an accessible table, or structured text.
4. Link text says where it goes; no "click here" or "read more" alone.

## Tables

1. Real table semantics with headers for genuinely tabular data.
2. A caption or surrounding text states what the table contains.
3. Never use tables for layout.

## Color and contrast

1. Admonitions, badges, and status pills never rely on color alone; the severity word is always printed.
2. Syntax highlighting keeps contrast between code and background and never uses red/green-only distinctions.
3. Code blocks and inline code meet the same contrast thresholds as body text.

## Charts

1. Every chart has a title, axis labels, series labels, and units.
2. Series are distinguishable without color (patterns, shapes, position, direct labels).
3. A data table or text description carries the same information as the chart.
4. The chart meets contrast thresholds in light and dark themes.

## Verify

- a headings outline reads as a table of contents
- every image and diagram has a text equivalent
- every link is self-describing out of context
- no meaning is lost in grayscale or under a color-vision simulation
- each chart passes together with its table or description
