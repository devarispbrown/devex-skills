---
name: access-and-permissions-dx
description: Design auth and RBAC as a self-service experience: what permission is needed, why a 403 happened, who grants it, how to request it, what the token will permit, and when it expires, per the 403-explanation standard. For supply-chain security review use security-supply-chain; for policy-as-code enforcement use policy-experience.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and the auth/RBAC implementation.
metadata:
  version: "2.7.1"
---

# Access and Permissions DX

## Mission

Permissions are product surface. Access control is a self-service experience: a developer who hits a denial must be able to understand it, fix it, or escalate it without tribal knowledge, support tickets, or source spelunking.

Design and audit auth and RBAC so every permission interaction answers the six questions. Audit to find gaps; fix root causes in the product, not wording.

The metric is time from denial to working access: the span from hitting a 403 to completing the corrective action. Grants that depend on knowing the right person, the right channel, or an untracked manual approval are defects.

This skill covers permission modeling, 403 denial explanations, grant and request flows, token scope previews, and expiry and rotation UX. Design mode applies the same standards before code exists; audit mode is the primary path and judges existing surfaces.

## The six questions

Every permission interaction must let the reader answer:

1. **What permission is needed?** The exact permission for the action they attempted.
2. **Why this 403?** The denial states the reason, never a bare "forbidden".
3. **Who grants it?** The role, team, or owner empowered to grant the permission.
4. **How to request it?** A concrete, self-service request route with expected turnaround.
5. **What will the token permit?** Token creation and access review show the exact scope the credential will carry.
6. **When does it expire?** Expiry is displayed, warned, and renewable without tribal knowledge.

Questions 1-4 are the 403-explanation standard. Questions 5-6 govern token creation, review, and rotation surfaces.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Permission UX audit

Audit first. Do not rewrite permission surfaces before reporting what is broken, because rewriting can destroy evidence of systemic friction.

Record findings with severity P0-P4 from the canonical severity vocabulary, each labeled Observed, CI-observed, or Estimated. An unlabeled finding is UNVERIFIED.

### 1. Model the permission surface

Read `references/permission-modeling.md`.

Enumerate the actual permission model from implementation and policy, never from prose:

- every action, endpoint, command, or operation that can be denied
- every permission constant, scope, and role, with its exact name
- which roles contain which permissions, and how scopes narrow them
- every wildcard and blanket role, with how many permissions each grants

Verify: each permission is named exactly once, requestable in isolation, and granted at least-privilege granularity. A permission that cannot be requested or granted without a wildcard is a defect.

### 2. Audit 403 denial explanations

Read `references/denial-explanation.md`.

Run `scripts/check_403_explanations.py` against `assets/403-examples.json` or a project sample of real denials. The script checks each denial for the required permission, the grant route, and role context; its output is heuristic, never a verdict. `assets/403-examples.clean.json` is the all-complete fixture for verifying the script.

Then review by hand:

- every expected denial names the required permission by its canonical name
- the denial states the requester's current role and the roles containing the permission
- the denial gives a concrete request route with expected turnaround
- no expected denial is a bare "forbidden", "access denied", or "insufficient permissions"
- denial text is derived from the permission model, not a paraphrase of it

A public expected 403 that cannot state the required permission is an `UNEXPLAINED_ERROR`-class failure.

### 3. Audit grant and request flows

Read `references/grant-flows.md`.

Verify:

- every permission has one documented owner and one self-service request route
- request forms state the permission, reason, and expected turnaround before submission
- approval chains are explicit: who approves, how many levels, and what happens on approval expiry
- grants are least-privilege and time-bound by default; permanent grants are the documented exception
- every grant is auditable end-to-end: requester, approver, scope, and timestamp
- revocation is as fast as grant, and revocation notice reaches the grantee

### 4. Audit token scope previews

Read `references/token-scope-preview.md`.

Verify:

- token creation surfaces show the exact permissions the token will carry before creation
- the preview is generated from the same policy the token will enforce, never a hard-coded copy
- previews are human-readable and machine-readable, with the scope in the token artifact itself
- scoped tokens are the default; broad tokens require explicit opt-in
- creating, listing, and revoking tokens are themselves permissioned actions with audit records

### 5. Audit expiry and rotation

Read `references/expiry-and-rotation.md`.

Verify:

- every token and grant displays its expiry, wherever it is listed, in one consistent format
- warnings precede expiry with a renewal path that does not require an admin
- rotation is documented per credential class: what to rotate, what breaks, and the rollback path
- leaked or revoked credentials invalidate immediately and propagate to dependent sessions
- impersonation surfaces (service accounts, impersonated sessions) show who the credential acts as, not just who created it

### 6. Score and report

Apply the severity vocabulary exactly and return the report with evidence labels and a prioritized backlog. A high aggregate score never overrides a P0/P1 finding.

## Contracts

### Permission contract

- every action maps to exactly one named permission; there are no unnamed denials
- permissions are requestable, grantable, and revocable individually
- wildcard or blanket grants are named, counted, and justified
- the permission model is machine-readable and is the source the denial text and token previews cite

### 403 explanation contract

A denial states, in the same surface where it occurs:

1. the required permission
2. the requester's current role
3. the roles containing the permission
4. the request route, with expected turnaround

A denial that omits any part is incomplete, regardless of how well the rest is written.

### Grant contract

- every permission has one documented owner and one self-service request route
- approval chains are explicit and tracked; approvals have an expiry
- grants are least-privilege and time-bound unless the permission is documented permanent
- grant and revocation events record requester, approver, scope, and timestamp

### Token contract

- token creation shows what the token will permit before the token exists
- token scope is enforceable, reviewable, and revocable independently of the user
- scoped tokens are the default; unscoped tokens are a P1 defect unless documented
- token listing and creation are themselves permissioned and audited

### Expiry contract

- expiry is displayed on every token and grant listing, in one consistent format
- renewal is self-service and does not require admin approval
- rotation procedures exist for every credential class and are tested
- revocation propagates immediately to sessions and downstream consumers

## Required output

For every audit, produce the permission UX report using `assets/permission-ux-audit-template.md`.

The report must contain:

1. **Verdict** — PASS / PASS WITH DEBT / FAIL / UNVERIFIED
2. **Evidence** — repository/revision, environment, checks executed and not executed, evidence labels
3. **Permission model** — inventory, naming, wildcard count, least-privilege gaps
4. **403 findings** — per-denial pass/fail against the four-part standard, with locations
5. **Grant flow findings** — owners, request routes, approval chains, auditability
6. **Token preview findings** — preview accuracy, scope enforcement, defaults
7. **Expiry and rotation findings** — display, warnings, renewal, revocation propagation
8. **Prioritized backlog** — severity, surface, finding, evidence, acceptance test

## Definition of done

The audit is done when:

- the permission model is enumerated from implementation and policy, not prose
- every expected 403 is checked against the four-part standard, with locations
- every permission has a documented owner and a self-service request route
- token previews are verified against the policy that enforces them
- expiry and rotation surfaces are verified, including revocation
- findings carry severity and evidence labels; nothing is guessed
- the report is rendered from `assets/permission-ux-audit-template.md`
- P0/P1 findings are surfaced, never smoothed over

Hand off supply-chain security review to the `security-supply-chain` skill and policy-as-code enforcement to the `policy-experience` skill. This skill designs and audits the permission UX; it does not replace either.
