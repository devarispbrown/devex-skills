# Self-Service Grant Design

## Objective

Every permission has one documented owner and one self-service request route. Time from denial to working access is the metric; grants that require knowing the right person, the right channel, or an untracked manual approval are defects.

## Request lifecycle

1. **Initiate.** The requester starts from the denial or the permission's page.
2. **State.** The request names the permission, the reason, and the expected turnaround before submission.
3. **Approve.** The owner or approver acts; the approval has an expiry.
4. **Grant.** The grant is least-privilege and time-bound unless the permission is documented permanent.
5. **Notify.** The requester learns the outcome with the granted scope and expiry.

## Approval chains

- approvers are explicit: who approves each permission, never "anyone on the team"
- multi-level chains are documented with the order and the conditions that trigger them
- approvals expire; an expired approval is renewed explicitly, never silently extended
- escalation is defined for stale requests
- a denied request states why and how to appeal

## Grant rules

- grants are least-privilege: the minimum scope for the stated reason
- time-bound by default; permanent only when the permission is documented as such
- no self-grant unless the system can justify and audit it
- every grant and revocation records requester, approver, scope, and timestamp

## Revocation

- revocation is as fast as grant and does not require the original approver
- the grantee is notified of revocation with the reason
- revocation takes effect at the enforcement layer, not just in the UI

## Denial of a request

A denied request is product surface too: it states why it was denied, what the requester can change, and the appeal route.
