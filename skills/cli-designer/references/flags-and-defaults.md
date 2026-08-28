# Flags, Arguments, and Defaults

Procedure for flag shapes, boolean flags, defaults, deprecation, and precedence.

## Flag shapes

1. Long flags accept both `--name value` and `--name=value`; document one, accept both.
2. Short flags are one letter and reserved for the most common options only.
3. Boolean flags take no value. Never `--force true`; `--force` alone.
4. Repeatable flags collect lists; document the order guarantee.
5. A value-requiring flag with a missing value fails with a usage error; never guess.

## Boolean pitfalls

1. A flag defaulting to false cannot express explicit false; add `--no-<name>` only when callers must override an enabled default.
2. Do not pair `--force` and `--no-force` unless both are meaningful defaults.
3. Never use a boolean to select between two values; use a value flag.

## Defaults policy

1. The default is the safe choice: fail-closed, read-only, or no-op when ambiguity exists.
2. Defaults are stable across releases; changing a default is a behavioral change and a release event.
3. A default that destroys, uploads, or spends is a P0/P1 finding.
4. Document every default in help text at the flag level.

## Deprecating a flag

1. Keep the old flag working; emit a warning naming the replacement and the removal version.
2. Deprecate in a minor or major; remove only in a major release.
3. Never silently rename: no old flag, no warning, no removal notice.

## Config-vs-flag precedence procedure

1. Write down the order: flags > config file > environment > built-in default.
2. Implement the order in exactly one code path, never scattered per flag.
3. Verify each layer: a flag overrides config; config overrides environment; environment overrides the built-in default.
4. Document the order in the flag help and the manual.
5. Test one conflict per layer: flag vs config, config vs env, env vs default.

## Verify

- every flag has one shape, one meaning, one default
- no boolean takes a value
- no deprecated flag is undocumented
- precedence is single-path and tested
