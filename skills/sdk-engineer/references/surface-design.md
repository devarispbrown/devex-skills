# Surface Design

Procedural guidance for method surfaces, options, pagination, streaming, resource objects, and the generation decision.

## Method surface

One method per operation, named per `references/language-idioms.md`. Do not invent verb prefixes (`getWidget` and `fetchWidget` for the same operation). Group operations on resource objects only when the language makes that natural; otherwise keep a flat client.

## Options and builders

- Long parameter lists are a defect: cap at about three positional parameters, then options.
- Go: functional options. Python: keyword arguments with defaults. TypeScript: one options object. Rust: builder pattern with `Default`.
- Options carry idempotency keys, request IDs, and per-call timeout/retry overrides — never a new positional parameter for each addition.
- Per-call options override client defaults; document precedence.

## Pagination helpers

- Expose cursors and pages, never URL strings.
- Provide a lazy iterator or generator when the language supports it (`for widget in client.widgets.list()`).
- Page size, ordering, and continuation are options; do not assume total counts.
- Every page must be reachable; a helper that silently drops pages is a P1 defect.

## Streaming

- Streams are first-class: Go `io.Reader` or channel, Python generator, TypeScript async iterator or `ReadableStream`, Rust `Stream`.
- Backpressure is the SDK's responsibility, never the caller's.
- Mid-stream errors surface through the stream's error channel; they are never swallowed or logged-and-dropped.

## Resource objects

- Typed resources with validation; never raw `map[string]interface{}`, `dict`, or `any` as a public result type.
- IDs, timestamps, enums, and nullable fields typed per language convention; nullability is explicit.
- Resources are immutable data; mutation helpers live on the client, not on the resource.

## Generation vs hand-written decision tree

1. Is the operation surface large (dozens+) and stable? → generate the transport, hand-write the surface.
2. Do language ergonomics dominate (options, builders, streaming)? → hand-write.
3. Can generation pin a spec version and re-run deterministically? → generation is viable.
4. Will hand-written code drift from the spec without automated checks? → generate, and run `scripts/check_parity.py` in CI.

Recommendations:

- Go, TypeScript: generation works well for the request/response layer; hand-write pagination and streaming helpers.
- Python, Rust: small stable surfaces hand-written; large surfaces generated from a pinned template, then hand-audited.
- Never mix: a hybrid SDK regenerates and re-reviews as one unit against one pinned spec version.
