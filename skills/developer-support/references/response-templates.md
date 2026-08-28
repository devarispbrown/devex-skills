# Response Templates and Bot Boundaries

## Acknowledgment template

Every request is acknowledged on receipt. The acknowledgment confirms:

- what was received, restated in one line
- the classified request class and the routing target
- what happens next and the expected response time
- the missing diagnostic fields, named individually

Template:

> We received your report and classified it as a **{class}** request, routing it to **{channel}**.
> Next step: {expected action} within {response commitment}.
> Before we proceed, complete the missing fields: {fields}.

## Resolution template

Every request is closed with a resolution, never with silence. The resolution states:

- what happened (the cause)
- the fix, or the reason no fix is warranted
- how to verify the fix
- retry safety and any follow-up action
- where to reopen, with the ticket identifier

Template:

> Cause: {cause}. Fix: {fix}. Verify: {verification}.
> Retry safely: {retry guidance}. If this recurs, reply on {ticket id} — do not file a new one.

## Bot vs human boundaries

A bot may:

- acknowledge and restate the request
- classify the request class and route it
- request missing diagnostics and return incomplete tickets
- answer template-resolvable requests and close them

A human is required for:

- security, billing, outage, data-loss, and abuse requests
- any request whose reproduction is ambiguous
- closing a request that the bot could not resolve by template

A bot that cannot classify a request routes it to a human with the raw text; it never invents a class.

## Escalation handoff

An escalation message carries the ladder position, the full diagnostic set, what was tried at each prior rung, and the response commitment already given. The receiving rung re-acknowledges with its own commitment. Do not make the developer repeat themselves at a promotion.

## Verification

Walk one request through acknowledgment, classification, diagnostics, routing, and resolution. Each step answers: who acts, what they say, and what they cannot do.
