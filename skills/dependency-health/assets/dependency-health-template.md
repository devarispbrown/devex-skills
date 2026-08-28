# Dependency Health Report

## Scope

- Repository/revision: <repo> @ <ref>
- Date: <date>
- Manifests scanned: <list of manifest paths>
- Evidence labels: <Observed | CI-observed | Estimated> per claim

## Inventory summary

| Manifest | Format | Direct deps | Transitive (approx) | Pinned | Unpinned | Lockfile |
|---|---|---|---|---|---|---|
| <path> | <npm\|go\|cargo\|pip\|pyproject> | <count> | <count> | <count> | <count> | <present\|missing> |

## Classifications

| Dependency | Manifest | Why it exists (use site) | Class | Removability | Owner |
|---|---|---|---|---|---|
| <name> | <path> | <capability + use site> | <essential\|convenience\|incidental\|duplicate\|vestigial> | <remove\|keep\|revisit> | <owner> |

## Maintenance and upgrade risk

| Dependency | Activity | Releases | Security history | Bus factor | Abandonment signals | Upgrade risk | Severity |
|---|---|---|---|---|---|---|---|
| <name> | <signal + evidence> | <cadence> | <posture> | <count> | <none\|list> | <low\|medium\|high\|blocked> | <P0–P4> |

## Duplication

| Capability | Packages | Manifests | Survivor | Removal target | Behavioral parity |
|---|---|---|---|---|---|
| <capability> | <names> | <paths> | <name> | <name> | <compatible\|unverified> |

## Upgrade policy

- Cadence: <cadence, e.g. monthly review>
- Streaming vs batching: <stream\|batch> — <rationale>
- Pinning strategy: <per-format strategy>
- Breaking-change triage: <procedure>
- Update PR acceptance: <accept as-is \| batch \| defer \| migrate rules>

## Candidate decisions

| Candidate | Bump | Decision | Rationale | Revisit |
|---|---|---|---|---|
| <package> | <from → to> | <accept\|defer\|migrate> | <reason> | <date\|-> |

## Prioritized findings

| Severity | Finding | Dependency | Evidence | Remediation | Owner |
|---|---|---|---|---|---|
| <P0–P4> | <finding> | <name> | <evidence label> | <action> | <owner> |

## Backlog

| Priority | Item | Owner | Acceptance test | Due |
|---|---|---|---|---|
| <P0–P4> | <item> | <owner> | <how to verify resolved> | <date> |

## Sign-off

- Next review date: <date>
- Owners accountable: <list>
- Policy recommendation: <summary>
