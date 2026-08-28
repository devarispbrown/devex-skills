# Wire and Schema Compatibility

## Purpose

Keep persisted formats and on-the-wire contracts safe across versions. Compatible means an older consumer keeps working against a newer producer and vice versa, within the documented contract.

## Wire protocol rules

- Requests and responses are contracts. Changing a contract is a release event; version recommendation belongs to `release-guardian` if available.
- Additive changes are safe: new optional fields, new enum values, new endpoints.
- Removing or renaming fields, tightening validation, and reordering required fields are breaking.
- Test both directions: old client against new server, and new client against old server.
- Prefer protocol negotiation (versioned headers, capability discovery) over silent behavior switches.

## Schema evolution rules

- Persisted schemas evolve additively: add fields with defaults; keep old fields until the documented window.
- Expanding contracts: readers accept unknown fields; writers emit new fields only when consumers tolerate them.
- Old readers must not error on new data; old writers must not produce data new readers cannot read.
- Enum sets grow, never shrink; removing an enum value is breaking.

## Serialization changes

- Any serialization change (format, field order, number formats, timezones, defaults) gets a round-trip test.
- Round-trip means serialize, deserialize, serialize yields equivalent output.
- Test parser strictness: a stricter parser breaks old writers; a laxer one breaks old readers.

## Cross-version test matrix

| Case | Must hold |
|---|---|
| old client → new server | additive contract, no errors |
| new client → old server | old server tolerates new optional fields |
| old reader ← new data | unknown fields ignored |
| new reader ← old data | defaults fill missing fields |

Breaking changes require a new contract version plus a migration path before they ship.
