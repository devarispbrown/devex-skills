# Changelog and Release Note Contract

## Purpose

The changelog and release notes are the canonical record of what changed and what the reader must do about it. They are machine- and human-readable facts, not marketing copy.

Every entry answers five questions. A missing field is a missing notice.

| Field | Required | Definition |
|---|---|---|
| **Changed surface** | always | the exact API, CLI flag, config key, SDK method, webhook field, or behavior |
| **Who is affected** | always | the concrete consumer segments, never "users" |
| **Action required** | always | the exact steps; "upgrade to X" alone is not an action |
| **By when** | breaking changes and deprecations | the date or version, and the timeline that produced it |
| **What breaks if ignored** | always | the consequence in the severity vocabulary; name the concrete failure |

## Changelog rules

1. One entry per change, grouped by release, newest first.
2. Unreleased changes live in an `Unreleased` section and move to the release section at tag time.
3. Entry format: `type: surface — affected, action, by when, consequence if ignored`.
4. Breaking changes link the migration notice; they do not inline its steps.
5. A fix that changes observable behavior is a breaking change for notice purposes; never label it `fixed` to avoid the notice.
6. A breaking API, CLI, or config change without a changelog entry and migration guidance fails the `UNDOCUMENTED_BREAKING_API` gate regardless of how small the code change is.
7. Deprecations are announced in the changelog at deprecation time, not at removal time.

## Release note rules

1. Lead with the user-visible value, then the action the reader takes.
2. Use the same five fields as the changelog entry, written for the release context.
3. Internal-only changes do not appear.
4. Preview/beta releases state their stability promise and promotion path.
5. Every release note for a breaking change carries the migration pointer and the deadline.

## Example entry

```markdown
## [3.0.0] - 2026-08-28

### Breaking

- **`legacy_transform` removed** — affects all callers of `lib.legacy_utils`.
  Replace with `transform()` (see [Migration to 3.0](migrations/3.0.md)).
  Action due: before upgrading to 3.x. If ignored: imports fail at build time.
```

## Anti-patterns

- An entry that names the change but not the action.
- An entry that says "various fixes" — name the surfaces.
- A breaking change hidden under `Fixed` or `Chore`.
- A deprecation mentioned only in the release where removal happened.
