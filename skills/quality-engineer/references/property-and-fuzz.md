# Property-Based and Fuzz Testing

## Property-based tests

Property tests assert invariants over generated inputs instead of hand-picked examples. They pay off when the input domain is wide and the behavior is specifiable:

- parsers and decoders
- validators and normalization logic
- serializers and round-trips (encode → decode → identity)
- pure functions with complex branch structure
- state machines (model-based: generated command sequences against a reference model)
- idempotency, commutativity, and ordering invariants

Procedure:

1. Write the invariant as a property: round-trip, no-crash, sorted/unique, monotonic, equivalent to a reference implementation.
2. Generate inputs across the domain, including edge generators (empty, null, max-length, unicode, malformed bytes).
3. Shrink failing cases to a minimal reproducer and record it as a regression test.
4. Run a bounded property budget in CI so the suite stays fast.

Skip property tests when examples already cover the domain or the invariant is trivial to exhaust.

## Fuzzing

Fuzzing feeds a coverage-guided stream of mutated inputs at a target and reports crashes, hangs, and sanitizer failures. It pays off on:

- parsers, deserializers, and protocol decoders
- anything that accepts bytes from a network or untrusted file
- code with allocation or bounds assumptions (with sanitizers enabled)

Procedure:

1. Choose fuzz targets around input entry points, not internal helpers.
2. Ship a seed corpus of realistic inputs; the fuzzer mutates from it.
3. Run short bounded fuzz campaigns in CI (minutes, not hours) on every change.
4. Keep a crash corpus; every crash becomes a regression test.
5. Use sanitizers (address, undefined behavior) for memory-unsafe languages.

Never fuzz against production data or production systems. Fuzzing runs in CI or a dedicated environment.

## When each pays off

- Property tests: deterministic, fast, catch semantic bugs — use wherever invariants exist.
- Fuzzing: catches crashes and memory errors on hostile input — use wherever untrusted bytes enter the system.
- If the surface has no external input, neither technique is warranted; do not add them to hit a checklist.
