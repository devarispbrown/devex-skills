# SDK Design Principles

Procedural guidance for deciding what parity means and when deviation is justified.

## What mechanical translation looks like

A mechanically translated SDK copies the API's shape instead of designing for the language. Recognize it by:

- method names mirror operation IDs verbatim (`getWidget` in Python, `listWidgets` unmodified in Go)
- argument order mirrors URL template order instead of options objects
- raw JSON maps returned instead of typed resources
- status codes surfaced as bare numbers instead of typed errors
- one language's concurrency model copied where the target idiom differs
- error strings that replicate the API error body without structure

Any of these is a P2 defect; several together mean the client was generated or copied without a design pass. Run `scripts/check_parity.py` to find naming mismatches mechanically.

## Semantic parity definition

Two SDKs have parity when, for every operation, both hold:

1. **Reachability**: the operation is callable with equivalent inputs and outputs.
2. **Behavior**: authentication, retries, timeouts, pagination, streaming, idempotency, and error classification behave equivalently.

Shape may differ; behavior may not. Sync in Go and async in Python is parity. A Python client that retries 429s while the Go client does not is a defect, regardless of how each exposes the call.

## When to deviate intentionally

Deviation is allowed only to make the language surface idiomatic, and it must be documented:

- **Unexpressible shape**: the API shape cannot be expressed idiomatically (for example, no native equivalent of long-polling streaming) — provide the closest idiomatic equivalent and document the difference.
- **Contract defect**: the API has a defect the SDK cannot safely compensate for — do not silently patch it; report the contract defect and record the workaround as a tracked deviation.
- **Unsupported capability**: a capability is genuinely unsupported in a language — record `no` in the capability matrix with a finding ID, never a silent absence.

Every deviation records: finding ID and severity, affected operations, rationale, effect on behavior, and owner. An undocumented deviation is a P1 defect.

## Parity procedure

1. Inventory every operation from the canonical spec.
2. Check reachability per language against the capability matrix.
3. Check behavior equivalence: retries, timeouts, pagination, streaming, errors.
4. Check idiomatic shape: naming, error model, concurrency, packaging, docs.
5. Severity-tag each finding; escalate contract defects to the API owner.

Do not fix a contract defect by reinterpreting it inside one language only — that creates cross-language divergence.
