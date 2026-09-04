---
name: cli-designer
description: Design and audit command-line interfaces as products: command hierarchy, naming, flags, arguments, defaults, prompts, exit codes, stdout/stderr discipline, JSON output, TTY behavior, autocomplete, config discovery, and non-interactive modes. Great for humans, stable for automation. For error text and recovery use error-experience; for config model design use configuration-dx; for release compatibility of CLI output use release-guardian.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the CLI's source or binary.
metadata:
  version: "2.9.1"
---

# CLI Designer

## Mission

A command-line interface is often the de facto product UX: the first and only surface many users touch. Design and audit CLIs as products, not plumbing. Every command, flag, prompt, and byte of output is product surface.

Human users need a surface that is predictable, discoverable, and forgiving. Automation needs one that is deterministic, parseable, and versioned. The same binary serves both.

For error text and recovery design, use the `error-experience` skill if available. For config model design, use the `configuration-dx` skill if available. For release compatibility of CLI output, use the `release-guardian` skill if available.

## Core principle

Great for humans, stable for automation.

Humans get interaction: sane defaults, helpful prompts, colors, progress, forgiving errors. Automation gets the contract: `--json` output with stable field names, documented exit codes, no prompts, no colors on pipes. When the two conflict, the interaction follows the human and the bytes follow the automation.

Never change a byte that a script depends on without a release event. Never prompt when stdin is not a TTY and no interactive mode was requested.

## References

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/hierarchy-and-naming.md` when designing or reviewing command hierarchy, naming, and alias policy.

Read `references/flags-and-defaults.md` when reviewing flag shapes, defaults, deprecation, and config-vs-flag precedence.

Read `references/output-contract.md` when auditing stdout/stderr discipline, exit codes, JSON output, and TTY behavior.

Read `references/automation-modes.md` when auditing non-interactive behavior and scripted usage.

Read `references/destructive-operations.md` when auditing delete, overwrite, and other destructive operations.

## CLI design workflow

### 1. Inventory the command surface

Run `scripts/check_cli_surface.py` against the CLI's source tree for a first-pass catalog, or pass `--helpfile` a captured `--help` text when only the binary or docs are available.

Verify:

- every public command, flag, and argument is enumerated, including legacy and hidden commands
- captured help matches the shipped binary; regenerate help text, never edit it by hand
- `--version` output and autocomplete definitions are captured and reviewed

Never audit from memory. Help output and source are the ground truth.

### 2. Audit hierarchy and naming

Read `references/hierarchy-and-naming.md`.

Verify:

- structure is verb-noun: actions are verbs, targets are nouns (`sync dataset`, `delete dataset`)
- one verb per concept; no near-synonym commands for the same action
- aliases exist only for established muscle memory and are documented
- a command run with no arguments shows help or runs a safe read-only default
- the tree stays shallow; depth beyond two levels is a finding

### 3. Audit flags, arguments, and defaults

Read `references/flags-and-defaults.md`.

Verify:

- boolean flags take no values; never `--force true`
- short flags exist only for the most common options and do not collide
- defaults are the safe choice, never the dangerous one
- deprecated flags still work and warn with the replacement and removal version
- flag-over-config-over-environment precedence is documented and implemented in one code path
- a missing required value fails fast with a usage error, never a mid-run prompt

### 4. Audit the I/O contract

Read `references/output-contract.md`.

Verify:

- data on stdout only; diagnostics, progress, and logs on stderr
- `--json` exists on every command that emits data, with stable field names
- exit codes are documented per command and correct for success, usage, and each failure class
- color and progress appear only on a TTY; pipes and redirection stay clean
- piped output is line- or JSON-complete; a consumer never loses bytes

### 5. Audit automation modes

Read `references/automation-modes.md`.

Verify:

- every prompt has a non-interactive path: `--yes`, `--no-input`, or a documented flag
- the tool never hangs waiting for input when stdin is closed or non-interactive
- CI-safe behavior is verified, not assumed
- scripted usage is exercised: `cmd --json | jq`, `cmd 2>/dev/null`, `cmd < /dev/null`
- repeated runs are idempotent or documented as not

### 6. Audit destructive operations

Read `references/destructive-operations.md`.

Verify:

- destructive commands confirm before acting in interactive mode
- automation bypasses confirmation only via an explicit `--force` or `--yes`, never implicitly
- a dry-run mode exists or the operation reports what it will change before acting
- reversibility is stated: what is lost, what survives, how to verify
- guardrails scale with blast radius; the more irreversible, the more friction

### 7. Design improvements

Prioritize every finding by severity from `references/standards.md`. Do not polish cosmetics before P0/P1 issues are resolved.

- group related changes into one coherent revision of the surface
- preserve the automation contract: deprecate instead of breaking, warn in one release, remove in a major
- ship help text, man page, autocomplete, and tests in the same change as the command or flag
- re-run the inventory and the automation test matrix after every change

## Output contract

Machine-readable output is a contract, not a convenience.

- every data command supports `--json`; the JSON payload goes to stdout alone
- field names, types, nullability, and ordering are stable across releases; renaming a field is a breaking change
- errors in `--json` mode are structured fields, never prose spliced into the payload
- human-readable text is a rendering of the same data, never a second schema
- progress and logs never reach stdout

Check release compatibility of CLI output with the `release-guardian` skill if available.

## Exit-code contract

Exit codes are documented, stable, and meaningful.

- 0 on success; a distinct documented nonzero code per failure class; a dedicated code for usage errors
- never repurpose an exit code for a new meaning; scripts depend on the old one
- document exit codes in help and the manual, and keep them stable across releases
- never exit 0 on failure; never exit nonzero on success

## Destructiveness contract

Destructive operations are delete, drop, purge, wipe, reset, overwrite, and anything irreversible or wide-blast-radius.

- interactive mode: require explicit confirmation before acting
- automation: an explicit `--force` or `--yes` is the only bypass; never infer consent from a non-TTY, an env var, or an unrelated flag
- offer `--dry-run` wherever a change can be previewed
- state reversibility in output and docs: what is lost, what remains, how to verify

## Required output

Produce the CLI review using `assets/cli-review-template.md`.

The review must contain:

1. **Findings** — each with severity from `references/standards.md`, the command or area, evidence, and a proposed change
2. **Per-command audit table** — command, help completeness, JSON output, exit codes, automation safety, destructive protection
3. **Automation test matrix** — command, scripted invocation, expected exit code, stdout/stderr expectations, result

Label every claim with evidence per `references/standards.md`: Observed, CI-observed, or Estimated. An estimate never proves a claim about output bytes or exit codes.

## Definition of done

A CLI review or design is done when:

- the full command surface is inventoried from help output and source
- hierarchy and naming follow the verb-noun structure with documented aliases
- flags, arguments, and defaults are audited, and unsafe defaults are removed
- the I/O contract is verified: stdout/stderr, exit codes, JSON output, TTY behavior
- automation modes are verified with scripted usage tests
- destructive operations confirm interactively and require an explicit flag in automation
- every finding carries a severity and a proposed change
- the review renders from `assets/cli-review-template.md` with the per-command audit table and automation test matrix

Hand off CLI documentation to the `developer-docs` skill if available, and error text and recovery to the `error-experience` skill if available. CLI Designer covers the surface; adjacent skills cover their slices.
