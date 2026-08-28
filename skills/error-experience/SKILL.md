---
name: error-experience
description: Design and audit the error experience across APIs, CLIs, SDKs, diagnostics, logs, and traces so every expected error answers what happened, why, where, how to fix it, whether retry is safe, and how to correlate with support. Use to build error taxonomies, per-surface contracts, error playbooks, and Time to Recovery measurements. For API error-model design use api-design-reviewer; for release gate enforcement use release-guardian.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access to the product's error surfaces.
metadata:
  version: "2.2.0"
---

# Error Experience Design and Audit

## Mission

Errors are product surface. An expected error is an interface: it is how the product talks to a user, a caller, or an operator at the moment they most need help. Treat error semantics, diagnostics, and troubleshooting as first-class product features, not as leftover strings.

Time to Recovery (TTR) is the metric: the time from hitting an expected error to completing its corrective action, measured against `TTR_TARGET_MIN`. Recovery that depends on tribal knowledge, support tickets, or source spelunking is a defect.

Design so every expected error answers the six questions. Audit to find gaps. Fix root causes in the product, not wording. Measure TTR to prove recovery. Do not polish an error message around an error model that is itself broken.

## Scope

This skill covers four error surfaces plus the artifacts that bind them:

- **API**: HTTP status codes, structured error bodies, machine-readable codes.
- **CLI**: exit codes, stream discipline, actionable error text.
- **SDK**: typed error classes, cause chains, retry signals, cross-language parity.
- **Diagnostics**: logs, traces, and correlation identifiers that make errors findable.

Artifacts: an error taxonomy, per-surface contracts, per-error playbooks, and TTR measurements. The audit workflow is the primary path; design mode applies the same standards before code exists.

## The six questions

Every expected error must let the reader answer:

1. **What happened?** A plain statement of the failure.
2. **Why?** The proximate cause, stated in user terms.
3. **Where?** The surface, operation, resource, and field path.
4. **How to fix it?** The concrete corrective action.
5. **Is retry safe?** Retryable or not, and the retry policy.
6. **How do I correlate with support?** The identifier that ties the error to logs, traces, and a ticket.

A public, expected error that cannot answer all six is an `UNEXPLAINED_ERROR` gate failure.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

Read `references/error-taxonomy.md` before classifying errors or designing an error taxonomy.

## Error audit workflow

### 1. Inventory error surfaces

Run `scripts/error_inventory.py` against the repository root and review the catalog. Add what the scanner cannot see: API error schemas and status tables, CLI exit-code documentation, SDK exception classes, log and trace field conventions, support playbooks, and error documentation pages.

Do not skip a surface without reporting it. An unlisted surface is an unmeasured one.

### 2. Classify errors

Classify every inventoried error:

- expected or unexpected
- user-caused or system-caused
- severity P0–P4 per the canonical vocabulary
- retry policy: safe, safe with backoff, or never

Expected errors get the full six-question treatment. Unexpected errors still need capture, correlation, and classification so they can become expected.

### 3. Audit each surface

Apply the per-surface contract and record per-error findings:

- API surfaces: Read `references/api-errors.md`.
- CLI surfaces: Read `references/cli-errors.md`.
- SDK surfaces: Read `references/sdk-errors.md`.
- Logs, traces, and telemetry: Read `references/diagnostics.md`.

Verify: each error states what happened, why, where, the fix, retry safety, and a support-correlation identifier. Do not accept "an error occurred" or "internal error" on an expected path.

### 4. Fix the taxonomy

Fix the root cause, not the wording. Prefer contract and error-model changes over message rewrites. Then:

- update or regenerate the error reference and any schemas
- update the per-error playbook entries
- add tests that assert the six questions and the stable code for each expected error

Do not change a stable code's meaning across releases. Do not rename a code while keeping its meaning ambiguous.

### 5. Measure Time to Recovery

Read `references/time-to-recovery.md` before measuring.

Measure TTR for the three most likely failures against `TTR_TARGET_MIN`. Label every measurement Observed, CI-observed, or Estimated. Never present an estimate as proof of meeting the target.

### 6. Verify the correlation path

Walk one failure end to end: error → correlation identifier → log line → trace → support ticket → corrective action. Verify the identifier is present at every hop and echoed in the error output. If any hop is missing, the correlation path fails and the error remains an `UNEXPLAINED_ERROR` gate failure.

For API error-model design use the `api-design-reviewer` skill if available; for release gate enforcement use the `release-guardian` skill if available.

## Design mode

When designing a new error model or surface rather than auditing one, apply the questions at design time:

1. Enumerate the expected failure modes for each operation before writing code.
2. Assign stable machine-readable codes and retry policies from the taxonomy.
3. Draft the user-facing text against the six questions.
4. Draft the playbook entry in parallel with the implementation.
5. Build the correlation identifier into the design, not as an afterthought.

Use `assets/error-playbook-template.md` when authoring per-error playbooks.

## API contract

Every API error response must carry a stable machine-readable code, a human message, a docs link, and the request identifier. Status codes must be honest and precise. Retryability must be explicit. Field-level problems must name the field path.

Read `references/api-errors.md` before designing or auditing API errors.

## CLI contract

Every CLI failure must set a documented exit code, write errors to stderr, and print an actionable message that includes the exact command to run. Data goes to stdout; diagnostics never pollute it. Non-TTY and piped invocations must behave identically to interactive ones.

Read `references/cli-errors.md` before designing or auditing CLI errors.

## SDK contract

Every SDK must surface failures as typed, stable error classes with the machine-readable code preserved. Wrapping must never destroy the root cause or the original code. Retryable errors must carry a retry signal. Official SDKs must expose the same error classes with the same semantics in every language.

Read `references/sdk-errors.md` before designing or auditing SDK errors.

## Diagnostics contract

Errors must be observable: structured log lines carrying the correlation identifier, code, and message; trace spans annotated on failure; sampling that never drops error traces. Emit where the failure crosses a boundary or where a retry decision is made. Do not log the same failure at every layer.

Read `references/diagnostics.md` before auditing logs, traces, or telemetry.

## Required output

Return an error audit containing:

1. Inventory: surfaces found, files scanned, catalog counts.
2. Per-error findings: error code, surface, severity P0–P4, six-question coverage (each question answered or missing), retry policy, and `UNEXPLAINED_ERROR` gate verdict.
3. Taxonomy defects: unstable codes, misclassified errors, missing classes.
4. Correlation-path findings: identifier coverage across responses, logs, traces, and tickets.
5. TTR measurement: the three most likely failures, per-failure TTR versus `TTR_TARGET_MIN`, with evidence labels.
6. Prioritized backlog: severity, gate, and acceptance test per fix.

Label every number. An unlabeled measurement is UNVERIFIED.

## Definition of done

The error audit is done when:

- every surface is inventoried
- every expected error answers all six questions or carries a gate verdict
- stable codes are assigned and documented
- retry policy is explicit per error
- the correlation path works end to end for at least the three most likely failures
- TTR is measured against `TTR_TARGET_MIN` and labeled
- findings separate product/error-model defects from wording defects
- the backlog has severity, gate, owner type, and acceptance test
