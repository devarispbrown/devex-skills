# Wiring Generated Output

A generated project is not done until it is validated in CI, discoverable in docs, registered in metadata, and owned by a team. An unregistered generated project is a folder, not a paved road.

## CI

1. Add a validation job per generated kind: generate a sample project with fixed inputs, run its checks (lint, test, build), and compare the result against the fixture. Any mismatch fails the job.
2. Add a drift job: regenerate all shipped generated projects on a schedule; an unexpected diff fails the pipeline.
3. Run generator unit tests on every change to the generator or its templates.

## Docs

1. Register the kind in the docs index: one page per generated kind with the command, the inputs, and the output tree.
2. Link the generated project's README stub to the canonical docs.
3. Generated quickstarts point at generated code, never at an older hand-copied version.

## Metadata

1. Registry or service catalog: the generator registers each generated project at creation with owner, kind, generator version used, and creation timestamp.
2. Generated projects carry the generator version in their marker so provenance is traceable.
3. CODEOWNERS entries: generated projects and the generator templates each have explicit owners.

## Ownership

- Every generated project has an owner team; the generator records it at creation.
- Generator and template changes require the generator owner's review.
- Template changes that alter output notify every affected generated project; each project owner reviews the regeneration.

## Validation of generated output

Verify:

- a fresh generation passes its own checks in CI
- the generated tree matches the fixture
- registration records exist for every generated project
- no generated project exists without an owner
