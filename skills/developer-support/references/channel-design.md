# Channel Design: Request Class to Routing Matrix

## Principle

Never make developers guess where a problem goes. Every request class has exactly one primary channel and one secondary channel, owned and named. Every entry point a developer can land on — error message, README, docs page, CLI output, form — states the next step for the classes it can produce.

## Request classes

Seven classes, one per request:

- **Bug** — the product behaves contrary to its documented contract.
- **Feature** — a new capability, change, or enhancement to an existing surface.
- **How-to** — a question about using an existing capability.
- **Security** — a vulnerability, credential exposure, or abuse report.
- **Billing** — charges, invoices, plan changes, quota purchase, payment issues.
- **Outage** — the service is down, degraded, or failing for many users.
- **Data loss** — user data is missing, deleted, or corrupted and needs recovery.

## Routing matrix

| Request class | Primary channel | Secondary channel | Terminal owner |
|---|---|---|---|
| Bug | Issue form | Community (reproduction check) | Engineering |
| Feature | Issue form / roadmap | Community discussion | Product |
| How-to | Docs + search | Community | Docs |
| Security | Dedicated private intake | Security contact | Security |
| Billing | Billing ticket | Support portal | Billing / Support |
| Outage | Status page + emergency ticket | — | Engineering on-call |
| Data loss | Emergency ticket | Support portal | Engineering / SRE |

## Rules

1. Exactly one primary channel per class. A request that fits two classes routes by the more urgent class.
2. Security, outage, and data-loss requests never route first through public channels.
3. Every channel has an owner and a documented response commitment.
4. Self-service channels come before human channels: error message, troubleshooting, search, community, then ticket.
5. The community channel must be searchable and must have an escalation path back into the ticket system. For designing the community channels use the `developer-community` skill.
6. No entry point is silent: error messages, README, docs pages, CLI output, and forms state the next step for the classes they can produce.

## Coverage test

Walk each class from the point of failure:

- the error message names the next step
- the docs page routes to a channel
- the form or intake exists
- the channel answers, or promotes

Any class that fails the walk has a routing gap. Record the gap in the gap ledger; do not ship it.
