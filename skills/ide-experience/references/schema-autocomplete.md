# Schema Autocompletion

## Association methods

Associate a configuration file with its schema by one of:

1. a `$schema` key inside the file:

```json
{ "$schema": "https://example.com/schemas/app-config@1.json" }
```

2. a relative schema path in the file's `$schema` key: `"$schema": "./schemas/app-config.schema.json"`
3. settings.json `json.schemas` for files that cannot carry a `$schema` key:

```json
"json.schemas": [
  { "fileMatch": ["/*.config.json"], "url": "./schemas/app-config.schema.json" }
]
```

4. built-in associations for known files: `.vscode/settings.json`, `.vscode/launch.json`, `.vscode/tasks.json`, `devcontainer.json`, `tsconfig.json`

## Rules

- every fixed-format configuration file gets an association; none are "obvious enough" to skip
- prefer the file's own `$schema` key; it travels with the file and works in any editor
- pin schema URLs to a version or tag; unpinned URLs let autocompletion drift
- relative schema paths resolve from the file's directory; keep them inside the repository
- when the schema changes, update the file and the validator in the same change

## Authoring schemas

A useful schema provides autocompletion, not just validation:

- `title` and `description` at the document root
- per property: `description`, `type`, `enum` for allowed values, `default`, `examples`
- `markdownDescription` for rich hover when the editor supports it
- a `required` array that matches the runtime validator
- `additionalProperties: false` when unknown keys must be flagged
- `oneOf`/`anyOf` for polymorphic config blocks
- `$ref` to shared definitions instead of duplicating shapes

Write the schema as the source of truth, then derive docs from it. A schema that documents itself replaces a wiki page.

## Verification

- open each config file and confirm completion offers descriptions, enums, and defaults
- confirm an invalid value produces a squiggle before runtime
- validate the sample configs in CI with a JSON Schema validator so the schema cannot rot
- confirm the schema URL resolves; a 404 association is worse than none
