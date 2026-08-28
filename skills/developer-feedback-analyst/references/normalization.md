# Normalization and Labeling

## Labeling taxonomy

Label every signal with three fields. All three are required before clustering.

### Journey stage

Where the developer was when friction happened:

- discovery — finding the product, evaluating fit
- install — getting the product installed
- account-auth — signup, login, credentials
- configure — setup, files, environment
- execute — running the core workflow
- debug — understanding failures
- production — deploying, operating, upgrading

When the stage cannot be determined, set it to unknown. Do not guess.

### Failure mode

What happened, in the developer's terms, not yours:

- blocked — cannot proceed past this point
- unclear — does not understand what to do or what happened
- slow — works but costs too much time
- wrong-result — completes but produces the wrong outcome
- broken — completes with an error or crash
- missing — a capability, value, or behavior is absent

### Surface

Which product surface the friction touched:

- docs, api, cli, sdk, config, website, platform, third-party

## Deduplication

Multiple signals about the same underlying event are one signal with a count:

1. Match by unique identifier when available: exception fingerprint, error code, issue number, telemetry event name.
2. Otherwise match by normalized text: lowercase, strip URLs, parameters, version numbers, and stack traces before comparing.
3. Keep one canonical record per event with per-source counts and first and last timestamps.
4. Record the count so the cluster reflects frequency.

Do not deduplicate by title alone. Do not collapse distinct failure modes that happen to mention the same feature.

## Noise handling

Exclude or tag:

- bot posts and automated template issues
- one-off environment quirks that do not reproduce
- unrelated product complaints outside the collection scope
- repeated spam from a single account

Tag each excluded item with a reason. Do not silently drop; the report lists excluded categories and counts.

## Output

Normalization produces the labeled JSONL working set with fields: source, text, journey_stage, failure_mode, surface, count, timestamp, evidence.
