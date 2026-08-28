# Discoverability Audit Report

## Scope

- Catalogs covered: <catalog files / platform>
- Entry types covered: <package, plugin, sdk, connector, extension | service, team, owner, datastore, runbook>
- Funnel stages measured: <find | identify | confirm | use>
- Evidence labels: <Observed | CI-observed | Estimated> per claim

## Coverage

| Entry type | Surface inventoried | Entries present | Coverage | Notes |
|---|---|---|---|---|
| <type> | | | | |

## Mechanical validation

- Checker run: `scripts/check_catalog_metadata.py <catalog>` — exit <0 | 1>
- Entries missing `name`: <list or "none">
- Entries missing `owner`: <list or "none">
- Entries missing `lifecycle`: <list or "none">
- Entries missing `docs_link`: <list or "none">
- Entries missing `status`: <list or "none">

## Ownership

| Finding | Severity | Entry | Evidence |
|---|---|---|---|
| <unowned | unreachable | stale | conflicting> | | | |

## Lifecycle

| Finding | Severity | Entry | Evidence |
|---|---|---|---|
| <misclassified | undocumented deprecation | missing replacement | stale> | | | |

## Docs links

| Entry | docs_link | Resolves | Current | Evidence |
|---|---|---|---|---|
| | | <yes | no | untested> | <yes | no | untested> | |

## Feedback findings

Top unanswered queries and 404 paths, with proposed fixes:

| Signal | Count | Funnel stage | Fix class | Proposed fix |
|---|---|---|---|---|
| | | <find | identify | confirm> | <entry | alias | link | docs | product> | |

## Backlog

| Priority | Finding | Owner type | Acceptance test |
|---|---|---|---|
| <P0–P4> | | | |

## Verdict

**Verdict:** <PASS | PASS WITH DEBT | FAIL | UNVERIFIED>

Evidence for the verdict, and which funnel stages remain unmeasured: <notes>
