# Health Checks, Dashboards, and Alert Wiring

Procedure for liveness/readiness design, graceful degradation reporting, and dashboard and alert wiring. Read before auditing health endpoints or alert configurations.

## Liveness and readiness

- **Liveness:** the process is alive. Check only what would kill the process if stuck: heartbeat, internal loop liveness.
- **Readiness:** the instance can serve traffic. Check the dependencies required to serve: config load, database, cache, essential upstreams.
- Use separate endpoints, separate checks, and separate lifecycle hooks. Never collapse liveness and readiness into one endpoint.
- Never fail readiness on a non-critical dependency (analytics, feature flags) unless serving genuinely depends on it.
- Check dependencies with timeouts and caching. A health check that blocks on a hung dependency is a self-inflicted outage.

## Graceful degradation

- Report degraded state truthfully: readiness returns an explicit degraded status, metrics emit a degraded gauge, and a log line names the missing dependency.
- Serve reduced functionality when possible and say so. A page that still works with a broken recommendations engine is degraded, not down.
- Document the degradation policy per dependency: what breaks, what still works, and what the operator should do.
- Never report healthy when a required dependency is failing. Orchestrators act on lies and kill healthy instances.

## Dashboard design

- Design each dashboard to answer a question: "why is latency high?", "which region is failing?", "what changed before the incident?"
- One pane per surface: logs, metrics, traces, health, SLOs. Link panes; a dashboard that requires tab-switching mid-incident is a gap.
- Include SLO burn and error budget panes. A dashboard without the SLO is a graph, not a status board.
- Keep dashboards to one service or one journey. A dashboard that contains everything answers nothing.

## Alert wiring procedure

- For each alert, record: the condition, why it matters, the severity, page or ticket, owner, runbook link, and how to test it.
- Wire alerts to SLO error budgets: budget burn rate and exhaustion lead the page; individual 500s and latency blips ticket unless critical.
- Test every alert with a fault injection before shipping. An untested alert is a gap, not a safeguard.
- Set a silence and maintenance policy. Noise from known maintenance must not page.
- Keep every alert configuration in the repository with the code it monitors. Unversioned alert config is a gap.

## Verification

- Confirm liveness and readiness are separate, each with a timeout and a caching policy.
- Confirm degraded states are observable in readiness, metrics, and logs simultaneously.
- Confirm every alert has a runbook, an owner, and a tested firing condition.
