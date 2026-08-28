# Magic Path Design

Design-side companion to the magic-path gate. Use when choosing the canonical route and its default choices. The gate itself, bands, and timer are in `references/standards.md`.

## Choose the single canonical route

Exactly one recommended getting-started route exists per product. Everything else — other platforms, other SDKs, advanced installs — is a link offered after first success.

Steps for choosing it:

1. Name the smallest meaningful end-to-end outcome.
2. Pick the platform and language your target developer most likely has.
3. Walk the route yourself with the benchmark persona's constraints.
4. Time each transition with a stopwatch on first pass; treat that as `Estimated`.
5. Fix the route, then write alternatives as post-success links.

Do not let the quickstart present a menu of routes before first success. A menu is a context switch and a decision the developer should not have to make.

## Parallel routes are a defect

Parallel getting-started routes are a P2 defect, per the canonical principles. Why:

- each extra route multiplies the surfaces that can drift from the product
- an audit cannot establish which route is canonical, so the gate becomes unverifiable
- effort is split between routes that could have made one route excellent
- support receives "which one do I use?" questions

If a second route exists, fold it into the canonical route as a step option, or demote it to a post-success link. Do not ship a second full quickstart.

## Default SDK and language

When the product supports many languages, choose one default for the canonical route:

- the language with the largest share of your target developers
- the SDK with the best parity and maintenance
- the path that finishes fastest when equal

Document the other SDKs after first success. Never present an SDK picker before the developer has seen value.

## Sandbox-first

Production setup almost never fits the budget. Design the sandbox route first:

- a test mode or sandbox environment that requires no production data
- starter credentials: a token issued by the quickstart command, not a signup form
- seeded fixtures: sample data, projects, or resources created by one command
- ephemeral resources that cost nothing and can be discarded

The sandbox route must exercise the real product path, not a stub. A mock that proves nothing is worse than a slow real path because it passes the gate dishonestly.

## Expected observable output per transition

Every transition must leave the developer able to verify progress without guessing:

| Transition | Expected observable output |
|---|---|
| After install | version or usage prints |
| After auth | token cached; next command works without re-auth |
| After configure | config file exists with the expected values |
| After execute | resource id, URL, or result object printed |
| After verify | the core value is confirmed, not just "command ran" |

Do not let the developer reach the end unsure whether it worked. If the outcome is not obviously visible, add a verification step to the plan.

## Budget the transitions

The segment budget guidance from the canonical metrics is the planning shape: orientation and verify are the smallest segments; auth, configure, and execute carry the weight; the plan must leave spare buffer for recovery. Only the aggregate `MAGIC_PATH_MAX_MIN` is a gate — but a plan that uses the entire budget on happy-path segments has no room for the failures you designed for.
