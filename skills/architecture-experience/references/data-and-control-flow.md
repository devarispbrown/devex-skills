# Data and Control Flow

## Hard objective

Trace every relevant flow type so the mental model explains both what moves (data) and what executes when (control) for the representative request.

Trace data flow and control flow separately. They rarely share a hop table.

## Request/response (synchronous)

1. Entry point: the route, handler, or method that receives the request.
2. Each hop: transport, middleware, service, domain, repository, store.
3. Record at each hop: input transform, validation, side effects, return path.
4. Verify the return path is the mirror of the entry path, or document why not.

## Event/async

1. Entry point: the event, topic, or channel the request publishes or consumes.
2. Each hop: producer, broker, consumer, handler, effect.
3. Record: payload schema, delivery semantics, ordering assumptions, dead-letter path.
4. Verify consumers in code or tests; a handler that is never wired is a finding.

## Batch

1. Entry point: the scheduler, cron, or trigger that starts the job.
2. Each hop: job, stage, store, checkpoint.
3. Record: idempotency, resume/checkpoint behavior, failure and retry semantics.

## Config-driven

1. Entry point: the config read that changes behavior.
2. Each hop: config source, schema, validation, propagation, effect.
3. Record: precedence, defaults, environment scoping, and what a config change affects.

## Recording

For every hop record:

- layer and component
- data transform (input → output)
- control flow (who calls, who waits, who forks)
- side effects and failure modes

Label each hop's evidence: Observed, CI-observed, or Estimated. Hops inferred without verification are the top source of mental-model drift.

## Stop condition

The flow is traced when each hop is verified and the terminal effect matches the effect named before the trace began.
