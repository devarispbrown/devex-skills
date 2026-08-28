# Record-Replay Cassettes

VCR-style capture and replay of external API interactions.

## Capture rules

1. Record against a sandbox or test environment. Never record against production.
2. Record the interaction date, provider version, and request context in the cassette header.
3. Scrub the cassette before commit: Authorization headers, tokens, keys, cookies, personal data.
4. Prefer recording the smallest interaction that covers the test, not the whole session.

## Replay rules

1. Cassettes are read-only artifacts; tests assert on behavior, not on cassette bytes.
2. Match requests by method and path by default; add query or body matchers only when the contract needs them.
3. An unmatched request fails loudly with the request details, never falls through to the network.
4. Re-record deliberately when the provider contract changes; regenerating to absorb a failure is a defect.

## Staleness

- mark cassettes with the recorded date; a re-record or review cadence keeps them honest
- on re-record, diff the cassette: changed responses are a contract change, not noise
- when the provider is unstable, prefer a fake backed by the cassette's shapes instead of replaying bytes

## Hygiene

- run `scripts/check_fixture_hygiene.py` on the cassette tree before commit
- a cassette containing a live token or a real email is a hygiene failure, even if the test passes
