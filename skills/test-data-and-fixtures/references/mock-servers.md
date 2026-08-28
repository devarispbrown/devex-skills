# Fake Services and Mock Servers

When to fake a dependency, when to mock it, and when to record it.

## Decision table

| Situation | Choice |
|---|---|
| dependency is owned or controlled; behavior is testable locally | fake (in-process implementation of the real contract) |
| only the interaction contract matters, not the behavior | mock (stub with assertions on the call) |
| external API with a stable contract; tests need real wire behavior | record-replay cassette |
| the dependency's own failure modes matter | contract test or real dependency in a sandbox |
| latency or availability of a third party blocks the test | fake or cassette, never a real prod call |

## Fake services

- implement the documented contract: endpoints, status codes, error shapes, rate-limit headers
- hold no real credentials; auth is simulated with test tokens
- live in test support, started and stopped by the harness (fixture server, ephemeral port)
- stateful where the consumer depends on state transitions; stateless where it does not

## Mocks

- assert on the interaction: called once, with these arguments, returning this
- never assert on implementation details (call order, private helpers)
- one behavior per test; do not mock the whole dependency surface

## Common rules

- prefer a fake with real behavior over a canned mock when the seam allows
- failure injection and fault modeling are covered by the `quality-engineer` skill; this skill supplies the data the fakes serve
- a fake that quietly diverges from the real contract is a drift defect; keep it in sync with the contract, not with an implementation
- never point a test at a real third-party endpoint just to have "real" data
