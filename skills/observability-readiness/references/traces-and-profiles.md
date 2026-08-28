# Trace Span and Profiling Design

Procedure for span design, instrumentation points, sampling, and profiling. Read before auditing traces or profiles.

## Span design

- Start a span at every entry point (HTTP, queue consumer, job runner) and end it at exit. One root span per correlation ID.
- Name spans verb + noun: "POST /orders", "consume.order", "query.user". Never put dynamic values in span names.
- Span attributes: service, operation, status, correlation ID, and the few identifiers that matter. Bounded attributes, never full payloads.
- Record duration and outcome on the span; child spans cover the steps.

## Instrumentation points

- Instrument at the middleware/boundary layer, outbound client calls, database and cache calls, queue publishes and consumes, and job steps.
- Prefer automatic instrumentation (SDK auto-instrumentors); add manual spans only where semantics matter: retries, circuit breaks, branch decisions.
- Instrument external dependency calls with the dependency name as an attribute. A failing dependency must be visible as a dependency, not as a mystery.

## Sampling

- Head-sample at the edge by rate for high-volume traffic; keep the decision stable per service.
- Never sample away errors: tail-sample or always-keep spans with error status and their parent chain.
- Cap span attributes and events. A span with unbounded attributes is a cardinality leak into the trace backend.

## Profiles

- Use CPU and memory profiles when latency or memory behavior is unexplained by spans and metrics.
- Enable on-demand profiling per process for investigation; prefer low-overhead always-on sampling when the platform supports it.
- Correlate profiles with the correlation ID of slow requests where the platform allows; otherwise profile the deployment under investigation.
- Memory profiles diagnose growth and leaks; pair them with heap metrics over time. They do not explain a single slow request.

## Verification

- Follow one request through the trace explorer: entry span, dependency spans, error span, and correlation ID all present.
- Confirm error traces are retained, not sampled away.
- Confirm attribute cardinality is bounded on the three hottest spans.
