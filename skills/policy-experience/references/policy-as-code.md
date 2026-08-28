# Policy as Code

Rules are data in the repository, versioned with the code, reviewed in PRs, and machine-checkable. Policy files are the single source of truth; everything else derives from them.

## Canonical location

- policy files live in the repository, near the surface they govern
- a rule enforced anywhere exists in exactly one policy file
- tickets and compliance dashboards are generated evidence, never policy

## Rule anatomy

Each rule records:

- `policy_id` — stable identifier used by guardrails, violations, and exception requests
- `source_requirement` — the compliance framework, standard, or org policy it derives from
- `scope` — paths, resources, environments the rule applies to
- `severity` — P0-P4, from `references/standards.md`
- `rationale` — why the rule exists; violations quote this
- `check` — the machine-readable condition, with a test fixture
- `remediation` — the fix the violation message will carry
- `exception_route` — the self-service request path when the rule cannot be satisfied

## Rule kinds

- **advisory** — informational; never blocks
- **warn-with-deadline** — non-blocking with an expiry; escalates if unmet
- **blocking** — fails the guardrail until fixed or an exception is approved

Severity drives kind: P0/P1 rules are blocking, P2 warn-with-deadline, P3/P4 advisory.

## Guardrail wiring points

Wire each rule to the earliest checkpoint where the violation is actionable:

| Checkpoint | Enforces | Trade-off |
|---|---|---|
| pre-commit / pre-push | local | fastest, easy to bypass, no central record |
| PR check | merge | reviewable, blocks merge, needs CI runner |
| CI job | branch/pipeline | broad tree coverage, slower |
| merge queue | integration | blocks merge after review, central record |
| deploy pipeline | rollout | blocks bad releases, late for developers |
| runtime enforcement | production | protects live traffic, last line |

Prefer the leftmost column that still produces a fixable message. A rule enforced only at runtime is a rule discovered at incident time. See `guardrail-design.md` for enforcement semantics.

## Policy changes are code changes

- policy edits go through the same PR review as code
- policy tests prove the rule fires on violations and stays silent on compliant input
- policy rollback is a code rollback; never hot-edit policy in production
- a rule with no test is unverified automation

## Dual-write failure

When policy exists in both the repository and a ticket system, they drift and the ticket system wins by inertia. The repository is authoritative. If a process requires ticket records, generate them from the policy files on a schedule — never the reverse.

## Boundaries

Rules about dependencies, artifacts, and supply-chain integrity belong to the `security-supply-chain` skill's inventory; permission-model rules belong to `access-and-permissions-dx`. Encode only rules this repository owns.
