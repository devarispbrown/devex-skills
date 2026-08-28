# Golden File Hygiene

Golden files are expected-output snapshots for formatters, compilers, report generators, and rendering pipelines.

## Production rules

1. Golden files are produced by a committed generator. The generation command is documented at the tree root.
2. Golden files change only through regeneration, and regeneration is reviewed as a diff.
3. The generator runs in a pinned environment (version, locale, timezone) so output is reproducible.
4. Update the golden file in the same change as the code that alters the output. Never update it separately "to see what changed".

## Update policy

- declare the policy per directory: `auto-bless` (regeneration is the review) or `human-reviewed` (the diff must be approved)
- a failing golden file is a signal to read the diff, not to bless blindly
- hand-editing a golden file to make a test pass hides drift and breaks the next regeneration

## Comparison discipline

- prefer semantic comparison (structure, values) over byte comparison when the output is not byte-stable
- pin the expected format (line endings, trailing newline, sort order) in the generator, not in the fixture
- platform-dependent output (paths, line separators) is normalized before comparison, not blessed per-platform

## Hygiene

- golden files obey the same hygiene rules as any fixture: no real emails, keys, cards, or production markers
- run `scripts/check_fixture_hygiene.py` on the golden tree before commit
