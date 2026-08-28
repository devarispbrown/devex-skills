# Template Design

Templates are the single source of truth for a generated kind. Everything that must be true about every generated project lives in the template, not in the generator's README.

## Layout

Templates live in `templates/<kind>/` and mirror the output tree:

```
templates/connector/
  config.py.tmpl
  tests/test_config.py.tmpl
  README.md.tmpl
  template.yaml
```

`template.yaml` declares the placeholders, their types, and their defaults. The generator renders the templates into the output tree at `<output>/<name>/`.

## Placeholder discipline

- Every variable value is a `<placeholder>` slot; never hardcode a value that varies.
- Every placeholder is declared in `template.yaml` with type, default, and description.
- Placeholders are detectable by the generator; an unresolved placeholder fails generation with the file and slot named.
- Placeholder names are stable across template versions; renaming one is a breaking change.
- Never use placeholders for secrets or machine-specific values: emit a clearly marked stub with instructions instead.

## Conditional blocks

- Conditional blocks use explicit delimiters (for example `[#if <flag>] ... [#endif]`) and stay minimal.
- Prefer generating the common case and documenting the rest; every conditional doubles the test surface.
- Every branch is covered by a fixture.

## Embedded best practices

Generated code ships correct by default. Embed in the templates:

1. **CI** — lint, test, and build jobs for the generated project.
2. **Tests** — a smoke test that passes on the fresh tree.
3. **Docs** — README with quickstart, configuration reference, and runbook stubs; complete except for the placeholders.
4. **Metadata** — registry entry, license header, ownership block, changelog stub.

If a practice cannot be embedded in generated output, it is not a template concern — document it instead.

## What NOT to generate

Never generate:

- credentials, tokens, keys, or personal configuration
- environment- or machine-specific values (hosts, paths, users)
- proprietary business logic that must be hand-authored
- files the developer must own and vary (design documents, decision records)

For these, generate a clearly marked stub that points to the canonical instructions.

## Fixtures

Every template has a fixture: a known-good generated tree that fresh generation must match. Fixtures run in CI as drift detection. `assets/scaffold-sample/` is the scanner fixture for candidate detection — keep it tiny and representative.
