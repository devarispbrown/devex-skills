# Sanitization

Procedure for turning production-derived data into safe fixtures.

## Gate

Production data enters the fixture tree only through this procedure. A fixture containing a real email, name, address, phone, credential, card number, or production marker is a hygiene failure and a release blocker, not a test asset.

## Procedure

### 1. Inventory

List every field in the source and classify it: PII (name, email, phone, address, IP, identifiers), secrets (keys, tokens, passwords, certificates), card data, or benign (counts, timestamps, statuses).

### 2. Replace

- emails -> `user-{n}@example.com`
- names -> generated names from a seeded list
- phones and addresses -> test-pattern values (555 numbers, `123 Test St`)
- card numbers -> documented test cards (for example `4242 4242 4242 4242`)
- tokens and keys -> placeholder values or redaction
- IPs -> private-range or documentation addresses
- free text -> scrubbed of names, emails, and identifiers

### 3. Preserve what the tests need

- keep distributional realism where tests depend on it (cardinality, null rates, ranges)
- keep referential integrity and foreign keys; sanitize in place, never join after scrubbing
- deterministic mapping: the same input always maps to the same output

### 4. Verify

- search the original values against the output: nothing survives, including substrings and reversed forms
- run `scripts/check_fixture_hygiene.py` on the sanitized tree: zero findings
- check for derivative leakage: sanitized data that can be joined back to the source (unique attributes, rare timestamps, exact geographic coordinates)

### 5. Record

Record source, date, transforms, and verification in the fixture report. A sanitized snapshot without a record is treated as unsanitized.

## Production-data rules

- no production data enters the repository, logs, or CI without sanitization
- sanitized data is still sensitive if any value is reversible; treat it accordingly
- credentials and private keys are never sanitized into fixtures; they are replaced or removed
- real card numbers and cardholder data never enter fixtures or test environments
