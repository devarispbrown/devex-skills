# Console Audit Method

## Why docs and UI walkthroughs

Most consoles are audited without live credentials or a running environment. A disciplined walkthrough of the console docs plus any available UI screens yields a solid operation inventory — the same method a developer uses when deciding whether to trust the console for real work.

Audit as a skeptical external developer and operator. Do not reward polished screens when the operation cannot be repeated, automated, or verified.

## Evidence hierarchy

Prefer:

1. observed execution against a live console or environment
2. implementation and tests in the console codebase
3. API docs and generated interface references
4. console docs and screenshots
5. product description and prose

Label every finding: **Observed**, **CI-observed**, or **Estimated**. An estimate is never proof.

## What to record per operation

For each operation in the inventory, record:

- surface — where it lives and how many clicks it takes
- inputs — required, optional, pre-filled
- success state — what the UI shows when it works
- failure state — what the UI shows when it fails, and whether it names the error
- API call — the endpoint, method, and parameters that implement it
- CLI equivalent — the command, if one exists
- copy affordance — whether a runnable command is one action away
- automation status — covered, partial, or gap
- evidence — the label and source for each claim

## Walkthrough procedure

1. Enumerate the navigation: every item becomes a candidate operation.
2. Walk each surface in order: list, create, read, update, delete, and any bulk actions.
3. For each operation, answer the four questions: what happened, what API call, can it be automated, can the CLI be copied.
4. Trace operations to the API surface in the codebase or docs; never guess the endpoint.
5. Probe failure paths: what happens on a rejected input, a missing permission, a failed webhook delivery.
6. Check observability surfaces: logs, metrics, webhooks, events, errors, usage.
7. Check keys and permissions: create, scope, rotate, revoke, expiry, grants.
8. Record gaps and partial gaps with a required fix for each.

## Recording format

Keep the operation inventory as JSON with fields `name`, `has_api_equivalent`, `has_cli_equivalent`, and `docs_link` — see `assets/console-ops.example.json` for the shape. Use `scripts/check_console_ops.py` to render the automation-parity checklist from the manifest.

Record prose findings in the report template `assets/console-audit-template.md`, one entry per finding with severity, surface, evidence, and an acceptance test.

## Reporting

The report must distinguish:

- friction the console can fix (UI changes)
- friction the product must fix (missing API or CLI surface)
- friction that is only a docs gap (undocumented behavior)

Do not blame the console for product friction the console cannot remove.
