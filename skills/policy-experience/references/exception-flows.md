# Self-Service Exception Flows

An exception is a temporary, scoped, approved deviation from a rule — with an owner, a duration, and an approver. It is not an escape hatch.

## When to grant

Approve an exception when:

- the deviation is temporary and carries a remediation plan
- an external dependency or third-party constraint blocks compliance
- the fix requires a change that cannot land in the current release window
- compliance debt is explicit, owned, and tracked

Refuse when:

- the team proposes a permanent workaround — fix the rule or the system
- the request has no owner, no duration, or no rationale
- the request is a workaround for a broken guardrail — fix the guardrail

## Request anatomy

A self-service exception request contains:

1. `policy_id` and the rule being deviated from
2. scope — resources, paths, environments
3. duration and expiry
4. rationale and risk assessment
5. remediation plan
6. requester, owner, and the approval chain for the severity

## Approval chains

The chain scales with severity (severity levels from `references/standards.md`):

- P0 — security/compliance owner plus a second independent approver
- P1 — the senior owner of the surface
- P2 — team lead
- P3/P4 — self-service with a record

No self-approval at any severity. The chain and its outcome are written to the audit trail (see `approval-auditability.md`).

## Jira-free mechanics

Requests live in the repository: a PR that adds the exception record, a markdown form in the repo, or a command that creates the record. The request is versioned, reviewable, and greppable. A ticket queue is ticket-ops; if the process produces tickets, the queue is the failure mode, not the solution.

## Expiry and renewal

- exceptions expire at the end of their duration and the guardrail re-blocks
- renewal is a new request with fresh rationale; expired exceptions do not renew silently
- expired exceptions that still hold in active configuration are a P1 finding

## Denials

A denial returns remediation guidance: what to fix, where, and how. Silence is not a process.

## SLAs and health

Set approval targets per severity band and measure them in the audit report. An exception queue that grows is ticket-ops in disguise; report it as a finding.
