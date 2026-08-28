# OSS Catalog Design

## Purpose

The OSS catalog answers the discovery questions developers ask before installing anything:

- which package do I install, and which version is current?
- is there an official SDK for my language?
- which plugin, connector, or extension integrates with my stack?
- where are the canonical docs, examples, and support paths?

The catalog is a machine-readable index of distributable artifacts. It is not a marketing page and not a replacement for docs.

## Entry types

Every entry has exactly one `kind`. The OSS types are:

- **package** — a versioned, distributable library or module published to a registry (npm, PyPI, crates.io, Go modules, and similar)
- **plugin** — an extension that runs inside a host product (IDE, editor, framework, gateway)
- **SDK** — an official client library for a specific language, with a stated parity status
- **connector** — an integration that moves data or operations between systems
- **extension** — any additional distributable capability not covered by the other types

If an artifact is ambiguous, choose the type that matches how developers search for it, and record the decision.

## Required fields

Every entry carries the skill's required fields:

| Field | Contract |
|---|---|
| `name` | canonical name, matches the published artifact exactly |
| `owner` | exactly one accountable team, per `ownership-metadata.md` |
| `lifecycle` | exactly one value from the vocabulary in `lifecycle-fields.md` |
| `docs_link` | resolved URL to current canonical docs |
| `status` | operational state: active, degraded, retired, or platform-defined |

## Recommended fields

| Field | When |
|---|---|
| `kind` | always; every entry needs one type |
| `version` | when the artifact versions |
| `language` / `runtime` | SDKs, packages, plugins |
| `registry` | where the package publishes |
| `install_command` | canonical install line |
| `host` / `host_version` | plugins, connectors, and extensions target a host |
| `parity_status` | SDKs: full, partial, or diverging vs. the canonical API |
| `repo` | source repository |
| `release_channel` | stable, beta, nightly where applicable |
| `aliases` | known search variants and common misspellings |
| `last_verified` | date the entry was checked against reality |

## Field guidance per type

- **Package**: version, registry, and install command are normative. An entry without a working install path is incomplete.
- **SDK**: state language, version, and parity status explicitly. A mechanically translated SDK with no parity statement hides its own defects.
- **Plugin / connector / extension**: always state the host product and the host versions supported. An entry that does not say what it runs inside is not findable by its users.

## Naming and search

- `name` matches the published artifact; aliases carry the search variants. Never create duplicate entries for synonyms.
- One canonical entry per artifact. Duplicate entries for the same thing are a P2 defect.
- Retired or replaced artifacts keep a `deprecated` entry with a replacement link rather than disappearing; a missing entry is a dead search result.

## Validation

Run `scripts/check_catalog_metadata.py` on every catalog file before commit. Machine checks are the floor: owner accuracy, version truth, and link resolution require the review steps in the skill's catalog design workflow.
