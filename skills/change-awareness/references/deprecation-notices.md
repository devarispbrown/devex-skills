# Deprecation Notice Lifecycle

## Definition

Deprecation is a promise: the surface still works, for a documented window, with a documented replacement. The notice is the promise in writing. Deprecation without a notice is ambiguity; removal without a window is a breaking change.

## Lifecycle stages

1. **Announce** — the notice ships at deprecation time: surface deprecated, replacement named, timeline stated.
2. **Support window** — the deprecated surface stays functional for the documented window. Deprecation does not begin the clock on breaking it sooner.
3. **Removal** — a breaking change with its own changelog entry and migration notice, only after the window closes.

## Timeline rules

1. State the window at announcement: "supported until 3.0 or 2027-01-01, whichever comes first." Prefer an explicit date or version, not "eventually".
2. The window is governed by the compatibility policy: a deprecated surface stays functional for the documented window; removal is always a breaking change.
3. Separate "action due" (deadline to migrate) from "support ends" (removal) when they differ.
4. Extending a window is allowed and must be announced; silently extending is a broken promise. Shortening is not allowed without re-announcement and justification.
5. Removal may only ship in a MAJOR release.

## Notice content

Every deprecation notice states:

- the deprecated surface, exactly as referenced in code
- the replacement surface and how to migrate
- the deadline and the window that produced it
- what breaks if the reader ignores it
- who is affected (SDK, CLI, config, JSON consumers, generated code)

## Code markers

The code carries the marker at the same time the notice ships:

- Python: `warnings.warn(..., DeprecationWarning)` or a `@deprecated` doc tag
- Java/Kotlin: `@Deprecated`
- JS/TS: JSDoc `@deprecated`
- Rust: `#[deprecated]`
- Swift: `@available(*, deprecated)`
- C#: `[Obsolete]`

Markers make coverage verifiable: `scripts/check_change_notices.py` reports any deprecation marker whose surface is not noted in the changelog. A marker without a notice is debt; a notice without a marker is unverifiable.

## Removal checklist

At removal time:

1. The window from the original notice has closed.
2. The removal has its own changelog entry and migration notice.
3. The checker no longer reports the marker (the marker was removed with the code).
4. Reach for the original deprecation was verified before removal, not assumed.
