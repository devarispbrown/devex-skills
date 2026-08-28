# Reference Application Variant Taxonomy

The variant matrix maps audience and lesson to a reference application shape. Select exactly one variant per tree; a suite of variants shares a core and adds overlays, never forks.

## Variant matrix

| Variant | Purpose | Scale driver | Shape | Concerns stressed |
|---|---|---|---|---|
| minimal | first-value learning; smallest complete system | readability | one service, one data path, few files | all nine at minimum strength |
| production | customers and operations teams; default for most products | operability | hardened service, observability, deployment, lifecycle | shutdown, security, observability |
| multi-tenant | isolation between customers | tenancy | tenant resolution, scoped data, rate limits | auth (tenant scoping), security |
| event-driven | asynchronous delivery and decoupling | message volume | producers, consumers, queues, dead-letter | retries, observability |
| high-throughput | load and latency at scale | concurrency | pools, backpressure, batching, load tests | errors, retries, observability |
| serverless | platform-managed runtime | invocation volume | stateless handlers, platform lifecycle | config, observability, platform termination |
| Kubernetes | declarative operations | replica count | manifests, probes, autoscaling, RBAC | deployment, shutdown, security |

## Selection rules

- minimal is the default for zero-to-value learning; production is the default for customers and operations teams.
- Choose the variant whose stress point matches the lesson: tenancy leads to multi-tenant, delivery to event-driven, load to high-throughput, platform lifecycle to serverless, orchestration to Kubernetes.
- A reference application answers one question well. If the tree needs two stress points, that is two variants in one suite, not one hybrid.

## Suite structure

A multi-variant suite shares one core — domain, data model, config, tests — and adds a per-variant overlay directory. Overlays may add files but must not rewrite core files; drift between an overlay and the core is a defect.

## Per-variant obligations

- **minimal**: runs with no external services; every file earns its place.
- **production**: full-strength nine concerns; deployment and shutdown verified, not stubbed.
- **multi-tenant**: tenant identity resolved from the request before any data access; data and limits scoped per tenant; cross-tenant access is a P0 defect.
- **event-driven**: producers and consumers with at-least-once delivery, idempotent handling, and a dead-letter path.
- **high-throughput**: backpressure and bounded pools; load behavior measured and reported.
- **serverless**: handlers are stateless; config arrives via platform variables; termination is platform-managed and documented.
- **Kubernetes**: manifests with probes, resource bounds, and RBAC; SIGTERM behavior verified against the platform.
