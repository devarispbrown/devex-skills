# Learning Task Risk Mapping

## Purpose

Classify learning tasks and map each risky task to a sandbox route. Classification happens before route design; a route is chosen by risk type, never by convenience.

## Risk classes

- **Destructive** — deletes, overwrites, resets, or mutates state that is not trivially recoverable. Examples: deleting a customer record, running a bulk delete, overwriting shared configuration, truncating a table, replaying a migration.
- **Quota-consuming** — consumes billable units, rate limits, quotas, or scarce resources. Examples: sending a message blast, generating media, running long jobs, calling a paid provider, exhausting a rate limit.
- **Production-touching** — reaches a production account, production data, or a live external service. Examples: calling a billing API, delivering a webhook to a live endpoint, rotating real keys, importing into a production database.
- **Safe** — read-only, isolated, free, and recoverable by construction. Examples: reading public documentation, rendering a template, computing a hash.

## Defaults

- when in doubt, classify as risky
- a task that touches billable or mutable state with an unknown target classifies as production-touching
- a task that could run against either a sandbox or a production target classifies by its production potential, never by good intentions

## Route mapping

| Risk type | Route requirements | Example route |
|---|---|---|
| destructive | resettable, isolated, seeded state | sandbox tenant plus fixture seed; destructive operations run against the seeded copy |
| quota-consuming | free or unbilled metering; test keys; mock provider | mock provider with test keys and simulated quota counters |
| production-touching | sandbox account or tenant; fake resources; mock webhooks | sandbox tenant, fake resources, mock webhook receiver |

A route must be concrete: the sandbox to use, the keys to create, the command to run, and how to verify. "Run it carefully" is not a route.

## Escalation rules

- a risky task with no route is a `NO_SANDBOX_FOR_RISKY_PATH` finding
- a route that touches a real production account or real money is the finding, not the fix
- when a product offers no sandbox for a documented task, the finding targets the product, not the documentation
- a task left safe without evidence is UNVERIFIED, not safe

## Evidence labels

- **Observed:** the classification and route were executed in the sandbox.
- **CI-observed:** executed in automation; useful for drift detection.
- **Estimated:** reasoned from steps without execution.

An estimate can never prove a classification or a route. A classification without an evidence label is UNVERIFIED.
