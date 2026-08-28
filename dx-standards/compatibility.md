# Compatibility Standards

Shared compatibility rules for API, CLI, SDK, config, and release work across the suite.

## SemVer contract

- MAJOR: incompatible behavioral change to a public surface.
- MINOR: backward-compatible addition.
- PATCH: compatible fix.
- A "fix" that changes observable behavior is not a PATCH. Public surface includes APIs, CLIs, config schemas, wire protocols, database schemas, and SDKs.

## Behavioral compatibility

A change is breaking if any documented consumer's behavior changes — not only when a signature changes. Seemingly compatible additions can break: JSON consumers, enum exhaustiveness/`switch`, generated SDKs, CLI scripts parsing output, database migrations, configuration parsers, serialization, resource limits, performance assumptions.

## Compatibility consumers

When analyzing a change, walk the consumer list:

1. JSON/response parsers (added or renamed fields, type changes, null vs omitted)
2. enum exhaustiveness (`switch` statements, generated code)
3. generated SDKs and client code
4. database migrations and persisted schemas
5. configuration parsers (renamed/removed keys, changed defaults, changed precedence)
6. webhook handlers (payload changes, new event shapes)
7. log/metric/dashboard consumers
8. shell scripts and automation parsing CLI output
9. preview/beta users relying on documented-but-unstable behavior

## Compatibility tiers

- **Breaking**: documented consumer behavior changes — requires major bump + migration guidance.
- **Behavioral**: observable behavior changes in edge cases or performance — assess per consumer list; document explicitly.
- **Additive**: new surface without changing existing behavior — minor bump.
- **Internal**: no public surface touched — patch bump.

## Cadence and policy

- State a compatibility window (how far back supported versions go) and verify claims with CI evidence.
- Preview/beta semantics must be explicit: opt-in, stability promise, promotion path.
- Sunset policy: deprecated surface stays functional for the documented window; removal is a breaking change.
