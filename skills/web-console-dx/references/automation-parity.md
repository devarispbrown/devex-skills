# Automation Parity for Console Operations

## Core principle

Every console operation must be expressible as an API call and, where the product ships a CLI, as a CLI command. A developer should never need the browser to do something a script must do.

Automation parity is a design rule, not a feature request: if an operation matters enough to ship in the UI, it matters enough to script.

## The parity rule

1. Every UI operation maps to a named API endpoint with documented parameters.
2. Where a CLI exists, every UI operation maps to a CLI command.
3. UI, API, and CLI operate on the same entities, IDs, and state.
4. An operation with no API or CLI equivalent is either a missing automation surface or a UI operation that should not exist.

## Parity bands

- **Covered** — API and CLI equivalents exist and are documented.
- **Partial** — one surface exists. Record which surface is missing and the fix.
- **Gap** — neither surface exists. Provide the automation surface or remove the UI operation.

## Copy-command contract

Where a CLI exists, the console offers a copyable command for every operation:

- the affordance is visible on the operation view, not hidden behind a menu
- the copied command is complete: auth context, required flags, and the entity from the current page
- the command works from a fresh terminal without editing
- the command uses the same ID the page shows, so it cannot drift from page state
- the copied command is the canonical way to do the operation, not an approximation

## What to copy

Prefer copying in this order:

1. the full command for the current entity and operation
2. a command with placeholders only when real values are unavailable, with placeholders clearly marked
3. a code snippet for the API call when no CLI exists — never nothing

A copy button that produces an un-runnable command is worse than no copy button: it manufactures a failure.

## Partial parity

Partial parity is a defect to close, not a state to keep:

- UI-only operations force automation through browser automation; record this friction
- API-only operations leave users on the CLI with no discovery path; record this friction
- each partial finding states the fix: add the missing surface or document the workaround

## Evidence

Every parity claim carries a label:

- **Observed** — the command was executed and the API call verified
- **CI-observed** — verified in automation
- **Estimated** — reasoned from docs without execution; never presented as proof

Never mark an operation covered without evidence.
