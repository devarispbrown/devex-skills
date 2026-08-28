# Escalation Ladder

## Shape

error message → troubleshooting → search → community → ticket → engineering

Promotion is a decision, not a timeout. Each rung either resolves the request or promotes it with evidence. A rung that can neither resolve nor promote is a dead end and a defect.

## Rungs

### Error message

- **Entry:** the developer hits a failure.
- **Job:** the error itself states what happened, why, where, the corrective action, retry safety, and the correlation identifier. For error message content use the `error-experience` skill.
- **Promotion criteria:** the error text cannot fix the failure and names no further step.

### Troubleshooting

- **Entry:** the developer follows the troubleshooting guide for the error or symptom.
- **Job:** ordered recovery steps with verification after each step; the three most likely failures covered inline.
- **Promotion criteria:** documented steps are exhausted without success, or the guide has no entry for the symptom.

### Search

- **Entry:** the developer searches docs, the changelog, and known-issue lists.
- **Job:** canonical content surfaces in search results; known issues carry status and workarounds.
- **Promotion criteria:** no result explains the failure, or all results are stale.

### Community

- **Entry:** the developer asks in the community channel.
- **Job:** a searchable archive of answered questions; moderation that redirects duplicates to docs.
- **Promotion criteria:** no answer within the stated community response window, or the answer is "file a ticket". Design the community channel with the `developer-community` skill.

### Ticket

- **Entry:** the developer files through the issue form or support portal.
- **Job:** intake validates the diagnostic set, assigns the class, and states the acknowledgment and response commitments.
- **Promotion criteria:** the request is confirmed as a defect, or the response commitment expires. A ticket missing its diagnostics is returned for completion, not promoted.

### Engineering

- **Entry:** the ticket reaches engineering.
- **Job:** a named code owner takes the request with a response commitment and a repro path.
- **Promotion criteria:** none — engineering is the terminal rung.

## Jump rules

- Outage, data-loss, and security requests jump directly to their emergency channel: status page plus emergency ticket, emergency ticket, and dedicated private intake respectively.
- Jumping skips rungs; it never skips evidence. A jumped request carries the full diagnostic set on arrival.

## Promotion criteria summary

| From | Promote when | Evidence required |
|---|---|---|
| Error → troubleshooting | error text cannot fix it | error code, request ID |
| Troubleshooting → search | documented steps exhausted | what was tried, in order |
| Search → community | no result, or results stale | queries tried |
| Community → ticket | no answer in the stated window, or confirmed bug | thread link, full diagnostic set |
| Ticket → engineering | confirmed defect, or response commitment expired | repro steps, full diagnostic set |

## Dead-end rule

Every rung must either resolve the request or promote it. When a rung fails both, fix the rung before shipping the design.
