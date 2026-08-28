# DX Principles

Shared principles for the entire skills suite. Skills apply them; none may contradict them.

## Truth before prose

Source, specs, tests, and observed behavior outrank narrative documentation. Establish truth before writing or judging.

## Time to value is a metric

The getting-started experience has an explicit SLA: `MAGIC_PATH_MAX_MIN` from `metrics.md`. Time to value is measured, not assumed.

## Interfaces are products

APIs, CLIs, SDKs, and config surfaces are products with their own UX. Review them as products, not as technical plumbing.

## One canonical path

There is one canonical onboarding route. Choices come after success. Parallel getting-started routes are a P2 defect.

## Failures are product surface

Error semantics, diagnostics, and troubleshooting are first-class interfaces. An unexplained expected error is a gate failure (`UNEXPLAINED_ERROR`).

## Docs ship with code

Public behavior changes imply documentation impact review in the same change. Docs and code cannot diverge silently.

## Reproducibility over tribal knowledge

Any setup step that only works on one machine or one person's memory is a defect. Committed automation is the standard.

## SDKs are first-class surfaces

Each official language deserves parity and idiomatic UX. A mechanically translated SDK is a product defect.

## Test by system type

Test strategy follows the system's failure modes, not a universal coverage percentage. Coverage is a signal, never a target.

## Releases are contracts

Every release is a compatibility event. Version recommendation, migration requirements, and gate verification precede the tag, not follow it.

## Humans and agents share the corpus

Structure interfaces, docs, and errors so both humans and coding agents can retrieve current authoritative facts and act safely.
