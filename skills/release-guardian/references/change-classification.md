# Change Classification

Every changed path maps to exactly one change class. The class drives compatibility analysis, the version recommendation, and migration requirements.

## Classes

- **Breaking** — a documented consumer's behavior changes. Renamed or removed public surface, changed defaults, removed fields, changed wire formats, tightened validation, removed config keys. Requires a MAJOR bump and a migration guide.
- **Behavioral** — observable behavior changes in edge cases, performance, or error semantics without changing the primary contract. Assess per consumer and document explicitly.
- **Deprecated** — public surface is marked deprecated with a named replacement and a timeline. The surface stays functional for the documented window; removal is a breaking change.
- **Added** — new public surface that does not change existing behavior. Requires a MINOR bump.
- **Fixed** — a correction that preserves observable behavior. Requires a PATCH bump.
- **Internal** — no public surface touched. At most a PATCH bump; usually no release note.

## Procedure

1. Enumerate changed paths from the diff.
2. For each path, read the actual diff hunks; never classify from the path alone.
3. Ask: does any documented consumer observe this change? If yes, it is breaking or behavioral.
4. Ask: does this change the public surface? If no, it is internal.
5. Assign the highest-impact class to the release as a whole.

## Edge cases

- **A fix that changes behavior is not a PATCH.** If observable behavior changes, it is breaking or behavioral even when the old behavior was a bug. Consumers built around the bug will break.
- **A rename is breaking.** Renames break imports, generated code, and scripts even when behavior is identical.
- **A field added to a response is usually additive** — unless a consumer does exhaustive parsing, strict schema validation, or serialization round-trips. Check the consumer list first.
- **A changed default is breaking** when consumers depend on the old default.
- **A new optional request field is additive; a new required request field is breaking.**
- **Performance regressions are behavioral** — documented latency or throughput expectations matter.
- **Error changes are breaking** when consumers branch on error codes or messages.
- **A deprecation without a named replacement is incomplete** — it is not a class entry until replacement and timeline exist.

Do not classify from commit message alone. A commit message can lie; the diff cannot.
