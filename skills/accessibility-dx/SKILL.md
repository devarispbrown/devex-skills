---
name: accessibility-dx
description: Make developer surfaces accessible: docs, portals, consoles, terminal colors, screen readers, keyboard navigation, contrast, motion, and charts, including CLI errors that never rely on red/green alone. For documentation architecture and content use developer-docs.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the surfaces to audit.
metadata:
  version: "2.3.2"
---

# Developer-Surface Accessibility

## Mission

Every developer surface is an interface that must work without color alone, animation alone, or the mouse alone. Screen readers, keyboard-only navigation, low-vision contrast, and reduced motion are supported paths, not edge cases.

Audit and fix accessibility across the surfaces developers touch: terminal and CLI output, consoles and portals, documentation, charts, and error messages. An error that is only red is a defect. A spinner that is only animation is a defect. A chart whose series differ only in color is a defect.

Accessibility failures are product failures. Classify them with the suite severity vocabulary and fix them before release, not after.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

This skill covers the accessibility of developer surfaces. For documentation architecture and content, use the `developer-docs` skill. For doc audits use `developer-docs-auditor`; for whole-product audits use `developer-experience-auditor`.

## Developer-surface accessibility

Run the audit as a fixed sequence. Skip steps whose surfaces do not exist; record every skip in the report.

### 1. Inventory the developer surfaces

Enumerate every developer-facing surface in the repository:

- terminal/CLI output and errors, including build tools, daemons, and scripts
- consoles, portals, admin UIs, dashboards, and devtools panels
- documentation pages, code blocks, and embedded diagrams
- charts and data visualizations
- progress indicators, spinners, and status output

Record where each surface lives. A missed surface is a missed audit.

### 2. Scan terminal output for color-only signaling

Run `scripts/check_cli_colors.py` against the tree as a first-pass signal.

Verify, per surface:

- colored output always pairs with a text marker such as ERROR, WARN, or SUCCESS
- red/green never appears as the only channel distinguishing states
- NO_COLOR is honored and explicit color flags exist
- spinners have text labels and a final static summary line
- nothing essential depends on animation

Read `references/terminal-accessibility.md` for the full procedure. The script output is heuristic; confirm every finding in source before reporting.

### 3. Audit console and portal interaction

Read `references/console-accessibility.md`.

Verify:

- every interaction is keyboard-operable with a visible focus and no traps
- focus order follows reading order; dialogs trap and restore focus
- forms label every control and announce errors with their field
- status changes are announced through live regions
- contrast meets the thresholds; motion never carries essential meaning

### 4. Audit documentation accessibility

Read `references/docs-accessibility.md`.

Verify:

- one h1 per page, logical heading hierarchy, no skipped levels
- meaningful alt text and link text; diagrams have text equivalents
- admonitions and syntax highlighting never rely on color alone
- tables use real table semantics with headers

For documentation architecture and content, hand off to the `developer-docs` skill.

### 5. Audit charts and data visualizations

Charts are developer surfaces in dashboards, docs, and reports.

Verify:

- every chart has a title, axis labels, series labels, and units
- series are distinguishable without color (patterns, shapes, position, direct labels)
- a data table or text description carries the same information as the chart
- marks, labels, and backgrounds meet the contrast thresholds in light and dark themes

### 6. Measure color pairs and contrast

Read `references/color-and-contrast.md`.

Verify:

- every text/background pair meets the ratio thresholds
- no state distinction depends on a red/green pair or color alone
- ratios are computed, never eyeballed

### 7. Test with a screen reader

Read `references/screen-reader-testing.md`.

Verify per surface:

- errors are announced as text, not silence plus color
- spinners and status output are announced sensibly
- every console control is named, reachable, and operable by keyboard
- a keyboard-only traversal completes the main flows

Label every test Observed, CI-observed, or Estimated.

### 8. Render the report

Use `assets/accessibility-audit-template.md`.

Apply the severity vocabulary from `references/standards.md`: P0/P1 findings are release blockers and force FAIL; P2/P3 form the debt backlog; P4 is polish.

Return exactly one verdict: PASS, PASS WITH DEBT, FAIL, or UNVERIFIED. A score never overrides a gate.

## CLI output contract

1. Meaning is never carried by color alone; every colored signal pairs with a text marker (ERROR, WARN, SUCCESS) on the same output.
2. Color only when the stream is a TTY; honor NO_COLOR; provide --color/--no-color flags.
3. Every spinner or progress indicator has a static text label and a final plain-text summary line; nothing essential depends on animation.
4. Errors go to stderr with a severity word, cause, and recovery; exit codes follow the documented table.
5. Piped output loses no meaning: no escape bytes, no animated-only state, no color-only distinction.

## Console and portal contract

1. Full keyboard operability with visible focus, logical order, and no traps.
2. Every control has an accessible name; forms label inputs and announce errors with their field.
3. Text/background contrast meets the thresholds in `references/color-and-contrast.md` in every theme.
4. Motion honors prefers-reduced-motion; no essential information is conveyed by animation.
5. Status changes use live regions; dialogs manage focus; tabular data uses real table semantics.

## Docs and charts contract

1. One h1 per page; heading hierarchy is logical and descriptive.
2. Meaningful link text and alt text; diagrams have text equivalents.
3. Admonitions and syntax highlighting are readable without color.
4. Charts have titles, axis and series labels, units, and a text equivalent; series are distinguishable without color.

## Required output

Produce the accessibility audit report using `assets/accessibility-audit-template.md`.

The report must contain:

1. **Verdict** — exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED
2. **Evidence** — repository/revision, environment, checks executed and not executed, with evidence labels
3. **Surface inventory** — every surface found and its status
4. **Findings table** — severity, surface, finding, evidence, acceptance test
5. **Terminal color scan** — the `scripts/check_cli_colors.py` result and per-finding confirmation
6. **Screen-reader test log** — reader, surface, what was announced, defects
7. **Prioritized backlog** — ordered fixes with acceptance tests

## Definition of done

An accessibility audit is done when:

- every surface in the inventory is audited or explicitly skipped in the report
- `scripts/check_cli_colors.py` findings are confirmed, and each defect has a fix or a severity
- no meaning anywhere depends on color alone, animation alone, or the mouse alone
- contrast ratios are computed for the surfaces that exist
- a screen reader test is executed, or marked not executed with an evidence label
- every finding carries a severity from the canonical vocabulary and an acceptance test
- the verdict is exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED
- the report is rendered from `assets/accessibility-audit-template.md`

Fix P0/P1 findings before release; report P2/P3 as debt. Hand off documentation architecture and content to the `developer-docs` skill, doc audits to `developer-docs-auditor`, and whole-product audits to `developer-experience-auditor`.
