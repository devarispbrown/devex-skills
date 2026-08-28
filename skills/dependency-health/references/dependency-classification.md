# Dependency Classification

## Purpose

For every direct dependency, state why it exists and whether it could leave. Classification precedes maintenance-risk assessment and upgrade policy; a dependency without a class is ungoverned.

## Why-does-this-exist review

For each direct dependency, answer in the report:

- What capability does it provide? Name the concrete use site: module, file, or feature.
- Is the use direct, or does the dependency exist for a sub-feature nobody uses?
- Could the standard library, platform, or first-party code replace it?
- Does another dependency already provide the same capability?
- How many places use it? A single use site is a removal candidate, not a commitment.

Never classify from the manifest alone. Grep for import and require statements first.

## Classes

- **Essential:** the project's core behavior depends on it; replacement cost is high and no in-house equivalent exists.
- **Convenience:** removes boilerplate the team could own; keep while maintained, review at cadence.
- **Incidental:** exists for a feature or path that is unused, disabled, or dead.
- **Duplicate:** another dependency provides the same capability.
- **Vestigial:** no import site remains; candidate for immediate removal.

A dependency can be essential for one surface and convenience for another. Record the dominant class and note the rest.

## Removability

Assess every non-essential dependency for removal:

- Is there a direct import site? Zero sites means vestigial.
- What would replacement cost: time, behavior changes, migration?
- Is it duplicated? Removing the duplicate is cheaper than maintaining both.
- Would a transitive consumer survive the removal?

Record a removal recommendation per dependency: remove, keep, or revisit at the next review.

## Duplicate-capability detection

Compare dependencies across manifests and lockfiles for packages serving the same role: parsers, HTTP clients, date handling, validation, logging, test utilities. Same-role pairs are findings even when the names differ.

Verify:

- the duplicate is confirmed at the use sites, not just by category
- the consolidation names the survivor and the removal target
- behavioral parity between the pair is stated before the recommendation

## Verify

- every direct dependency has exactly one dominant class
- classes are grounded in use sites
- a removal recommendation exists for every non-essential dependency
