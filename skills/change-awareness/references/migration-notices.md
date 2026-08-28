# Migration Notice Contract

## Definition

A migration notice is the written upgrade path for a breaking change. It exists to make the reader's next deploy succeed with the fewest surprises. A breaking change without one fails the `UNDOCUMENTED_BREAKING_API` gate.

## When a migration notice is mandatory

- any breaking change to a public surface (API, CLI, config schema, SDK, wire format, database schema)
- any behavioral change with a documented rollback path requirement
- any removal after a deprecation window closes

## Content contract

| Section | Required | Definition |
|---|---|---|
| **What changed** | always | the exact surface and the old vs new shape |
| **Why** | always | the reason in one paragraph, not a history essay |
| **Affected** | always | the consumer segments that must act |
| **Upgrade steps** | always | ordered, copyable before/after steps that run from a clean checkout of the old version |
| **Rollback path** | risky changes | how to return to the previous version and what is lost |
| **Deadline** | always | by when the action must be complete |

## Writing rules

1. Steps are executable: every command, snippet, and config diff is complete and validated.
2. Version the notice with the release it belongs to; readers land here from changelogs, search, and link checkers.
3. Link from the changelog entry and the release note; do not inline migration steps in the changelog.
4. State the consequence of ignoring the notice per step, not only at the top.
5. A step that depends on a preview flag or beta feature says so explicitly.

## Verification

Before publishing:

- a reader can complete the steps from the documented starting version
- the rollback path, when required, is concrete (command or procedure)
- the deadline is unambiguous
- the migration notice is linked from the changelog entry for the breaking change

## Anti-patterns

- "Refer to the docs" as a step.
- Steps written only as prose ("update your config accordingly").
- A rollback path that says "revert the merge".
- A deadline of "soon" or "in a future release".
