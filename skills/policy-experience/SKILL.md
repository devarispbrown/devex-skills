---
name: policy-experience
description: Turn security and compliance into self-service: policy-as-code, automatic guardrails, self-service exception requests, auditable approvals, and actionable violations instead of Jira ticket-ops. For auth and RBAC user experience use access-and-permissions-dx; for dependency and artifact risk use security-supply-chain.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and policy/compliance tooling.
metadata:
  version: "2.5.1"
---

# Policy Experience

## Mission

Turn security and compliance into self-service. Policy lives in the repository as code, guardrails enforce it automatically at the right checkpoint, developers request exceptions through an approval chain instead of filing tickets, and every approval leaves an audit trail that survives a compliance review.

The failure mode this skill exists to eliminate is ticket-ops: developers discovering policy at release time, human-run checklists, approval queues, and violations that say only "policy check failed". Policy experience is developer experience: the rule is the guardrail, the message is the fix, and the exception is a request, not a ticket.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Policy work is distributed by domain. For auth and RBAC user experience use the `access-and-permissions-dx` skill; for dependency and artifact risk use the `security-supply-chain` skill; for whole-product experience measurement use the `developer-experience-auditor` skill. This skill owns the policy-as-code machinery: rules, guardrails, exceptions, approvals, and violation quality.

## Policy as self-service

Run the seven steps in order. Every step ends in a verifiable artifact; step 7 assembles the report.

### 1. Inventory the policy surface

Map every policy that applies to this repository: compliance frameworks, security standards, organizational policy, and product risk appetite.

For each policy record:

- the source requirement it derives from
- the rule that encodes it
- the enforcement point that will check it
- the severity band (P0-P4 from `references/standards.md`)

A requirement with no rule is unmet compliance exposure. A rule with no requirement is unowned automation. Both are findings.

Do not re-inventory domains owned by sibling skills: dependency and artifact rules belong to `security-supply-chain`; permission-model rules belong to `access-and-permissions-dx`. Duplicate rule inventory is how policies drift.

### 2. Encode policies as code

Read `references/policy-as-code.md`.

Rules are data in the repository, versioned with the code, reviewed in PRs, and machine-checkable. Policy files are the single source of truth. Tickets, dashboards, and compliance reports derive from them; nothing is written back to a ticket system.

Verify:

- every rule has a stable policy id and names its source requirement
- policy changes go through the same review flow as code changes
- the guardrail test suite proves the rule fires on violations and stays silent when compliant

### 3. Wire guardrails into the flow

Read `references/guardrail-design.md`.

Attach each rule to the earliest checkpoint where a violation is actionable: pre-commit, PR check, CI, merge queue, deploy pipeline, or runtime enforcement.

Verify:

- P0/P1 rules block; P2 warns with a deadline; P3/P4 advise
- pre-deploy guardrails default to blocking, runtime guardrails to log-and-alert
- every guardrail run records a result and evidence; no silent failures
- a guardrail that cannot run reports UNVERIFIED, never PASS

### 4. Write actionable violations

Read `references/violation-actionability.md`.

Every violation stands alone: what happened, why, how to fix, and the request-exception route. Validate violation samples with `scripts/check_policy_actionability.py`; an opaque sample set exits 1.

An opaque violation is a defect in the policy system, not a developer failure. Severity P1, and it triggers the `UNEXPLAINED_ERROR` release gate.

### 5. Design self-service exceptions

Read `references/exception-flows.md`.

Exceptions are requested in the repository — a PR, a form, a command — never filed in a ticket queue. The request names the policy, the scope, the duration, and the rationale; the approval chain scales with severity; the exception expires and the guardrail re-blocks.

Verify:

- no self-approval, at any severity
- every request records an outcome: approved, denied, expired, revoked
- a denial returns remediation guidance, not silence

### 6. Make approvals auditable

Read `references/approval-auditability.md`.

Every approval and denial appends to an immutable trail: actor, action, policy id, timestamp, evidence, justification. The trail is the compliance evidence.

Verify:

- the trail is append-only and tamper-evident
- guardrail runs are recorded alongside approvals
- active exceptions reconcile with approved requests; expired exceptions are gone

### 7. Verify and report

Re-run the guardrail suite, re-check violation samples, and render the audit report from `assets/policy-audit-template.md`.

Return exactly one verdict: PASS / PASS WITH DEBT / FAIL / UNVERIFIED. A gate failure forces FAIL; a score never overrides a gate; missing evidence is UNVERIFIED, never PASS by assumption.

## Guardrail contract

Every guardrail records its id, the policy id it enforces, its checkpoint, and its blocking flag. Every run records a result — PASS, FAIL, or UNVERIFIED — with evidence. No silent failures. Guardrail configuration changes go through the same PR flow as code; disabling a guardrail is a policy change that is reviewed, recorded, and reversible.

## Violation message contract

A machine-readable violation carries the four actionability fields, keyed as used by `scripts/check_policy_actionability.py`:

- `what_happened` — the policy id and the concrete observation: rule, target, and value
- `why` — the rule and its rationale
- `how_to_fix` — the exact remediation, preferably copy-paste commands
- `request_exception` — the self-service route when the rule cannot be satisfied

Every violation must also identify its policy id and where the problem lives (file:line or resource). A violation missing any field is opaque: severity P1, and it triggers `UNEXPLAINED_ERROR` at release gates. The developer never needs to open the policy file to act.

## Exception request contract

A self-service exception request contains:

1. policy id and rule being deviated from
2. scope: resources, paths, environments
3. duration and expiry
4. rationale and risk assessment
5. remediation plan for the deviation
6. requester and the approval chain for its severity

Approval chains scale with severity; no self-approval at any level. The chain and the outcome are recorded in the audit trail. Exceptions expire; renewal is a new request with fresh rationale.

## Audit trail contract

Every entry records timestamp, actor, action, policy id, scope, evidence hash, and justification. Entries are append-only and tamper-evident; retention follows compliance requirements; the trail is exportable in JSON or CSV. The trail must answer who approved what, why, when, for how long, and on what evidence.

## Required output

For every policy engagement, produce the policy audit report using `assets/policy-audit-template.md`.

The report must contain:

1. **Verdict** — exactly one of PASS / PASS WITH DEBT / FAIL / UNVERIFIED
2. **Evidence** — repository/revision, environment, checks executed and not executed, with evidence labels
3. **Policy inventory** — policy id, source requirement, rule location, severity, guardrail checkpoint
4. **Guardrail results** — per-guardrail result with evidence; no unrecorded runs
5. **Violation actionability** — per-violation field coverage; opaque violations listed as findings
6. **Exceptions** — request, scope, duration, approver chain, status, expiry, evidence
7. **Audit trail summary** — recent entries and reconciliation of active exceptions
8. **Gate results** — per-gate result keyed by gate constant, with evidence
9. **Backlog** — prioritized P0-P4 debt

## Definition of done

Policy experience work is done when:

- every requirement maps to a rule and every rule maps to a requirement
- policy files live in the repository and are reviewed like code
- guardrails enforce at the earliest actionable checkpoint with recorded evidence
- every violation passes the actionability check; none is opaque
- exceptions are self-service, approved by the right chain, and expire
- the audit trail proves who approved what, why, and until when
- the report is rendered from `assets/policy-audit-template.md` with one verdict
- no gate failure is hidden by a score, a missing run, or an assumption
