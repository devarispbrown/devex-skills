# Observability Views in the Console

## Core principle

Logs, metrics, webhooks, and events views are debugging surfaces. A developer opens them during an incident; every wasted click is time the incident grows. Views must be filterable the way the API is filterable, and each view must answer what happened and what API call produced the data.

## Logs

- logs are searchable, filterable by documented fields, and paginated
- filters match API filter parameters; a filter the API supports but the UI hides is a defect
- each entry shows timestamp, level, message, and structured fields
- entries link to the resource and API call they belong to
- export is available where the API supports it, and the export is automatable
- a view with no way to reach the specific log a user needs is a friction finding

## Metrics

- every chart states its metric, aggregation, and time range on the chart itself
- units and definitions are documented and match the API
- time-range and granularity controls map to API parameters
- series are labeled and legend entries link to metric definitions
- chart-to-data is traceable: the API call behind the chart is named

## Events and webhooks

- the events list shows type, timestamp, status, and the entity affected
- event payloads are inspectable and copyable in the raw format
- webhook subscriptions show endpoint, events, delivery status, and retry state
- failed deliveries show the error, the attempt count, and a retry action
- replay is an operation, not an accident: it maps to a documented API call and confirms before running
- event and webhook views offer a CLI equivalent where the product has one

## Errors

- error views group by message and show occurrence count, first/last seen, and affected entities
- each error links to the log entries and the API call that produced it
- remediation is stated: fix, retry-safety, and the next step
- error views are filterable the same way the error API is filterable

## Linking views to API calls

- every view states the API call that produced its data
- where a CLI exists, the equivalent command is copyable from the view
- filter state is representable as a command or query, so operators can reproduce the view

## Automation parity

- every observability view has an API equivalent for the same data
- exports and downloads map to API endpoints, never screen scraping
- webhook create, update, replay, and delete map to named API calls
