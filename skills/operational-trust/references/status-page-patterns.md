# Status Page Patterns

Design guidance for the consumer-facing status page: component granularity, degraded-state vocabulary, and update cadence. Read this when auditing or building a status page.

## Components

Model components after independently failing surfaces, not the org chart:

- API (public endpoints, auth)
- Dashboard / web app
- Ingestion (events, inbound webhooks)
- Processing (background jobs)
- Storage / data plane
- Delivery (outbound webhooks, email)
- Billing (when separately operated)

Verify:

- every component has an automated check; manual toggles are the exception
- a failure in one component does not force the whole page red
- component names are stable terms users already know
- a single "everything" status is never the only signal

## Degraded states

Use a fixed vocabulary, never euphemisms:

- **Operational**: normal.
- **Degraded performance**: available but slower or partially failing; some requests may fail.
- **Partial outage**: a subset of users or components is unavailable.
- **Major outage**: the component is broadly unavailable.
- **Maintenance**: planned work; say when it starts, when it ends, and whether impact is expected.

Verify:

- a degraded state is declared as soon as impact is confirmed, never only after recovery
- "degraded performance" is not used to hide an outage
- each degraded component links to the current incident or maintenance entry

## Update cadence

Apply the no-news-is-bad-news rule:

- first update: within 5 minutes of confirmed impact, or as soon as you know more than nothing
- follow-ups: every 30 minutes during active incidents, or at each meaningful change, whichever is sooner
- resolution: announce resolution with a link to the postmortem; never reopen silently
- maintenance: announce at least 24 hours ahead; begin and end updates within 15 minutes of the actual window

Verify:

- an incident with no update in 30 minutes is a communication failure, not a quiet one
- updates are written for users: impact, action (if any), next update time
- the cadence is stated in the first update and honored

## History

Keep incident history public, searchable, and machine-readable (RSS/Atom, JSON feed).

Verify:

- historical incidents remain after resolution with statuses that cannot be silently rewritten
- history links to postmortems
- a third party can determine availability from the history alone

## Placement

Verify:

- docs, SDKs, dashboards, and error messages link to the status page
- the status page is hosted so it stays up when the product is down
- a user who cannot reach the product can reach the status page in one hop
