# Isolation and Sandboxing

## Purpose

Extensions are untrusted code running inside the host. Design the boundary that contains them, the failure behavior when they misbehave, and the security model that makes hosting extensions safe.

## Assumptions

- An extension is hostile by default. Assume worst-case behavior, not good intentions.
- No ambient authority: the extension has exactly the access the contract grants, nothing more.
- Isolation is a design requirement of the extension API, not a deployment option.

## Security boundary

Define, per extension, what it may:

- read: which files, env vars, configuration, and host state
- write: which paths, caches, and settings
- execute: which commands, binaries, and runtimes
- reach: which network endpoints, sockets, and services

Express the boundary as a permission set declared in the manifest. The host enforces it; the extension cannot broaden it at runtime. Secrets never cross the boundary except through an explicit, scoped credential API.

## Failure containment

A failing extension must not take down the host:

- timeouts on every extension call, with a documented default
- resource limits: memory, CPU, event budget, recursion depth
- quarantine: repeated failure disables the extension with a clear message
- disable without uninstall: the host stays healthy and the author can fix and re-enable

Define the failure taxonomy the author sees: refused (permission), timed out, exceeded limit, crashed, quarantined. Each failure mode needs distinct, actionable messaging.

## DoS resistance

- Bounded work per call: wall-clock, CPU, and allocation budgets.
- Bounded event processing: rate limits, queue depth, backpressure.
- Bounded side effects: the extension cannot spawn unbounded processes or connections.

## Data flow

- The extension sees only what the contract passes it, in the documented shape.
- Sanitize inputs to and outputs from the extension at the boundary.
- No implicit access to host internals, host credentials, or other extensions' data.
- Logging and telemetry from extensions are metered and redacted.

## Escalation and revocation

- Document the vulnerability disclosure path.
- Support remote revocation: a kill switch that disables a compromised extension without a host release.
- Support registry takedown for published extensions.

## Parity with tests

The sandbox used by the testing harness must match the production sandbox. A test that runs unsandboxed proves nothing about production behavior.
