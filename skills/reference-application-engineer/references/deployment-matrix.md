# Deployment Matrix

Deployment artifacts must match the variant. This matrix is the canonical mapping; a reference application's deployment concern is met when its artifact matches the row for its variant.

## Matrix

| Variant | Artifact | Health | Config delivery | Shutdown contract |
|---|---|---|---|---|
| minimal | run command in README | manual check | env vars | Ctrl-C suffices; state it |
| production | container image | /health endpoint | env vars / secret store | SIGTERM: drain, close, exit |
| multi-tenant | container image + shared store | /health plus tenant path | env vars / secret store | SIGTERM: drain, close, exit |
| event-driven | worker container(s) + queue | liveness plus consumer lag | env vars / secret store | SIGTERM: stop consuming, finish, ack |
| high-throughput | container image, bounded pool | /health plus load metrics | env vars / secret store | SIGTERM: stop intake, drain pool, exit |
| serverless | function or container platform config | platform health checks | platform env vars | platform-managed; document it |
| Kubernetes | Deployment plus Service manifests | liveness/readiness probes | ConfigMap plus Secret | SIGTERM under terminationGracePeriod; probes gate traffic |

## Rules

- Every variant ships a deployable artifact definition plus a health check and a config delivery path; the trio must appear in the tree.
- Container images must be buildable from committed files — a Dockerfile or platform build spec — never from a hand-described image.
- No secret or machine-specific value is baked into any artifact.
- The shutdown contract column states what the app must implement; a long-running variant that cannot drain its work on SIGTERM fails the shutdown concern.
- Local development may always use the simplest artifact; the deployed artifact follows the variant's row, not the local shortcut.
