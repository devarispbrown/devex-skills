# Synthetic Datasets

Generated test data for volume, distribution, and privacy-free realism.

## When synthetic data wins

- volume tests need more rows than hand-authored fixtures can provide
- distributional realism matters (cardinality, null rates, skew, correlations)
- the data must be free of real personal data by construction

## Realism rules

1. Shape follows the schema: types, constraints, nullability, enums, referential integrity.
2. Cardinality and distributions match the production profile under test, and the profile is stated.
3. Correlation matters: an order belongs to a real customer in the set; do not join random ids.
4. Values are realistic but safe: `user-{n}@example.com`, generated names, test addresses.
5. Dates are bounded and relative to a pinned "now" so the dataset does not rot.
6. Seeded RNG, recorded seed: a dataset regenerates to identical bytes.

## Generation

- the generator is committed with the dataset and is the only way the dataset is produced
- generated datasets are checked for schema conformance and hygiene before commit
- store small datasets as files; generate large ones at test time and cache by seed
- never commit generated data that took hours to produce without the generator beside it

## Hygiene

- synthetic data must pass `scripts/check_fixture_hygiene.py` with zero findings
- a generator that emits real-looking emails, keys, or card-like numbers is a hygiene bug in the generator, not in the data
