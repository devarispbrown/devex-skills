# Finding Scaffold Candidates

A scaffold candidate is a workflow that is structurally repeated: same file shapes, same wiring, same failure modes, differing only in names and values. Find candidates from three signal sources, then decide.

## Signal 1: PR archaeology

1. Run the scanner as a first-pass signal: `python3 scripts/scan_scaffold_candidates.py <repo-root>`.
2. Search git history for repeated structure: `git log --all --name-only` filtered by the file shapes the scanner reports, or `git log --all --grep` for PR titles with a family prefix ("add X connector", "integrate Y", "new Z pipeline").
3. Count instances in the last `SCAN_WINDOW_DAYS` days. Count merges that create a new member of a family (a new directory or file set), not fixes to existing members.
4. Confirm by diffing two representative instances: are they identical beyond names and values? If the deltas are real design decisions, the workflow is varied, not repeated.

## Signal 2: onboarding friction

1. Collect the steps a new contributor follows to start a new project, connector, integration, or pipeline.
2. Compare against the platform's documented procedure. Steps reconstructed from memory, copied from a teammate's machine, or recovered from chat logs are candidates.
3. Check setup scripts and runbooks for divergence: the same procedure implemented differently in different places.
4. Check docs for fill-in markers: TODO-fill-in stubs and "replace me" templates indicate a half-built scaffold.

## Signal 3: support questions

1. Collect the recurring "how do I create a ..." questions from support channels and office hours over the `SCAN_WINDOW_DAYS` window.
2. Group by the workflow being created, never by the asker.
3. Note error reports from the same workflows: setup failures, misconfiguration, registration mistakes. Error-prone manual steps are stronger evidence than repetition alone.

## Frequency thresholds

Constants, cited by name:

- `SCAN_WINDOW_DAYS` = 90: the evidence window for all three signals.
- `DOCUMENT_ONLY_MAX_INSTANCES` = 2: at or below 2 instances in the window, document the path instead. Hand the path to the `developer-docs` or `developer-onboarding` skill if available.
- `SCAFFOLD_WORTHY_MIN_INSTANCES` = 3: 3–4 instances with error-prone steps justify a generator.
- `GENERATOR_REQUIRED_MIN_INSTANCES` = 5: 5+ instances in the window make the generator the default; the drift cost is already being paid.

The thresholds are a decision aid, not a gate. Two instances of an actively defect-producing manual path can justify a generator; six instances of a trivial, varied path may not. Confirm every candidate with at least two signal sources before designing.

## Example candidates

- **Connectors** — connector-* families: directory plus config, tests, and docs, each hand-copied and edited.
- **Integrations** — webhook handlers, auth flows, event subscriptions: same shape, different provider.
- **Projects** — service or package skeletons: boilerplate config, CI, and metadata repeated per repo.
- **Pipelines** — data or deployment pipelines: same stages, different sources and sinks.

For each candidate, name the workflow, enumerate its steps end-to-end, and state the cost of one manual instance before building anything.
