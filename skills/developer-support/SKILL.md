---
name: developer-support
description: Design post-self-service support routing: bug, feature, how-to, security, billing, outage, and data-loss channels; the escalation ladder from error message through troubleshooting, search, community, ticket, to engineering; and automatic diagnostic collection of version, SDK version, request ID, trace ID, environment, config, and sanitized logs. For designing the community channels use developer-community; for error message content use error-experience.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and support tooling context.
metadata:
  version: "2.5.1"
---

# Developer Support Routing

## Mission

Support routing is a designed surface, not a leftover. Every developer who hits a problem must reach a working channel without guessing, and every channel must know what it receives, what it does with it, and when it promotes the request onward. The error message the developer sees, the docs page they are on, and the form they open must all agree on the next step.

Self-service is the first channel, not the last resort. The product should resolve routine problems in the error message, troubleshooting docs, search, and community before a human is ever involved. Routing exists to make that path fast and to catch what it cannot.

Design the routing before the support load arrives: cover every request class, every rung of the escalation ladder, and automatic diagnostic collection so a request carries its own evidence. Measure routing efficiency and escalation rates to prove the design works, not to assume it does.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Support routing design

### 1. Inventory existing support surfaces

Run `scripts/scan_support_channels.py` against the repository root and review the report. Add what the scanner cannot see: status pages, community forums, support mailboxes, ticket systems, and in-product help entry points.

Verify:

- every support entry point the product exposes is named
- surfaces the scanner cannot see are added manually
- no surface is silently accepted as "not applicable"

### 2. Enumerate request classes

Every supported request is exactly one of seven classes: bug, feature, how-to, security, billing, outage, data-loss.

Verify:

- the class list matches the request types the product actually receives
- a request that fits two classes has a tie-break rule that routes by the more urgent class
- a class that appears in practice but not in the matrix is treated as a routing hole, not an ad hoc case

### 3. Map every request class to a channel

Read `references/channel-design.md` before mapping.

Give each request class exactly one primary channel and one secondary channel. Never make developers guess where a problem goes: every entry point a developer can land on — error message, README, docs page, CLI output, form — must state the next step for the classes it can produce.

Verify:

- exactly one primary channel per class, with an owner and a response commitment
- a secondary channel exists for every class
- security, outage, and data-loss never route first through public channels

### 4. Design the escalation ladder

Read `references/escalation-ladder.md` before designing.

Define each rung — error message, troubleshooting, search, community, ticket, engineering — with entry conditions, promotion criteria, and evidence requirements. Walk the three most likely failures for each class up the ladder and verify no rung is a dead end.

Verify:

- every rung either resolves the request or promotes it; a rung that cannot promote is a dead end
- urgent classes jump, they do not queue
- every promotion carries the full diagnostic set

### 5. Design automatic diagnostic collection

Read `references/diagnostic-collection.md` before designing.

Collect version, SDK version, request ID, trace ID, environment, config, and sanitized logs at every entry point, automatically wherever the product can supply them. A request that arrives without its diagnostic set is returned with instructions, not routed onward.

Verify:

- the seven fields are collected at every entry point
- automation supplies the fields the product can provide; forms prefill and require the rest
- sanitization removes secrets, tokens, credentials, and PII before collection
- a ticket missing request ID or trace ID bounces with instructions, not guesses

### 6. Define response behavior and bot boundaries

Read `references/response-templates.md` before designing.

Define what a bot may acknowledge, classify, collect, and route, and what requires a human. Security, billing, outage, data-loss, and abuse requests are never closed by a bot.

Verify:

- bot scope and human scope are explicit for every situation
- acknowledgment and resolution templates exist and are versioned
- escalation handoffs carry the ladder position and the full diagnostic set

### 7. Instrument routing metrics

Read `references/support-metrics.md` before designing.

Measure routing efficiency, escalation rate, and time-to-recovery against `TTR_TARGET_MIN`. Unmeasured routing is unverified routing.

Verify:

- routing efficiency and escalation rate are measurable from the design's entry points
- time-to-recovery is measured against `TTR_TARGET_MIN`
- every metric carries an evidence label: Observed, CI-observed, or Estimated

### 8. Author the support artifacts

Render the design from `assets/support-design-template.md`. Use `assets/support-channel-sample/` as a reference example. Produce:

- `SUPPORT.md` at the repository root, linked from the README
- issue forms or templates for every public request class
- a security reporting route: a dedicated `SECURITY.md` or a security section in `CONTRIBUTING.md`
- docs feedback links on the pages developers land on after an error or a dead end

Verify:

- `SUPPORT.md` is reachable from the README
- every public request class has a form or template
- the security route exists and is private
- error-landing docs pages carry feedback links

### 9. Validate the routing

Re-run `scripts/scan_support_channels.py`. Close every reported gap or record it as debt with an owner and a date. A gap that survives the design pass is a shipped defect.

Verify:

- the scanner output is clean, or every gap has an owner and a date
- gaps are not closed by deleting the artifact that exposes them

## Channel contract

Every request class has exactly one primary channel and one secondary channel, named in the routing matrix, each with an owner and a response commitment. No entry point is silent: the error message, docs page, CLI output, and README all state the next step for the classes they can produce. For error message content use the `error-experience` skill.

Security, outage, and data-loss requests never route first through public channels. Security has a dedicated private intake; outage and data-loss go to the emergency channel before any ladder.

Community channels are designed with the `developer-community` skill. The community channel must have a searchable archive, stated moderation, and a documented path back into the ticket system when answers stall.

## Escalation contract

The ladder is fixed: error message, troubleshooting, search, community, ticket, engineering. Promotion happens only when the current rung's promotion criteria are met; every promotion carries the full diagnostic set. A promotion without evidence is a re-routing, not an escalation.

Outage, data-loss, and security requests jump directly to their emergency channel; they never wait out the ladder. Engineering is the terminal rung: an engineering handoff names a code owner and a response commitment.

## Diagnostic collection contract

Every entry point collects the full diagnostic set: version, SDK version, request ID, trace ID, environment, config, and sanitized logs. Automation supplies the fields the product can provide; forms prefill and require what automation cannot. A ticket missing request ID or trace ID bounces with instructions, not guesses.

Logs and config are sanitized before collection. Secrets, tokens, credentials, and PII are redacted by policy, never by convention. Sanitization is verified on a sample before the design ships.

## Response contract

Every request receives an acknowledgment on receipt and a resolution when closed, using `references/response-templates.md`. A bot may acknowledge, classify, collect diagnostics, route, and close requests resolvable by template. A human is required for security, billing, outage, data-loss, abuse, and any request whose reproduction is ambiguous.

## Required output

Return the support routing design rendered from `assets/support-design-template.md`, containing:

1. **Routing matrix** — request class, primary channel, secondary channel, owner, response commitment
2. **Escalation ladder** — rungs, entry conditions, promotion criteria, jump rules, evidence requirements
3. **Diagnostic fields** — field, collection point, required or optional, sanitization rule
4. **Response behavior** — bot scope, human scope, acknowledgment and resolution templates
5. **Metrics** — routing efficiency, escalation rate, time-to-recovery against `TTR_TARGET_MIN`, evidence labels
6. **Gap ledger** — every scanner-reported gap with fix, owner, and due date

## Definition of done

Support routing is done when:

- every request class has exactly one primary and one secondary channel, both with owners
- no entry point leaves a developer guessing the next step
- the escalation ladder has promotion criteria at every rung and jump rules for urgent classes
- every entry point collects the full diagnostic set, sanitized
- bot and human boundaries are explicit for every situation
- routing efficiency and escalation rates are measurable against `TTR_TARGET_MIN`
- `scripts/scan_support_channels.py` reports no open gaps, or every gap is debt with an owner and a date
- community channels hand off to `developer-community` and error message content to `error-experience`
