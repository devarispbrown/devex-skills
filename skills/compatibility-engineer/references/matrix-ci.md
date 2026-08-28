# CI Matrix Wiring

## Purpose

Turn the compatibility matrix into running evidence. A cell is supported only when CI proves it on the configured cadence, and CI output must be resolvable by `scripts/check_compat_matrix.py`.

## Cell-to-job mapping

- One job per supported cell (surface times version), or a parametrized workflow whose matrix expands to cover every supported cell.
- A supported cell with no job is a gap: report it; never delete the claim to hide the gap.
- Jobs must exercise the product's real behavior, not merely install it.

## Cadence and cost control

- Every push: cheap cells — the primary runtime on supported platforms, lint and build, fast unit suites.
- Nightly: expensive cells — the database version matrix, upgrade ladder N-1/N-2, schema evolution, cross-architecture compilation.
- Weekly or per release: the longest jobs — the full upgrade ladder on every supported database.
- When the full matrix is unaffordable, split it and keep claims only for cells that actually run.

## Evidence collection

- Every job emits a machine-readable artifact: JUnit XML, a JSON summary, or a marker file.
- Store artifacts where the matrix evidence paths resolve: repo-relative files or published URLs.
- The matrix's `evidence` entries point at those artifacts; the checker resolves them mechanically.
- Publish failure markers too; a stale or red marker is missing evidence, not evidence.

## Drift control

- CI regenerates the matrix report; a diff against the committed report fails the build.
- A tier change ships with its report change in the same change set.
- The checker runs in CI on every push; a supported claim with missing evidence fails the pipeline.
