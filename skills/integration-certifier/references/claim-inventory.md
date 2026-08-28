# Integration Claim Inventory

## Purpose

Find every place the product claims to integrate with something, and turn each prose claim into a testable (integration, version, configuration) triple. Claims that cannot be made testable are removed, not kept.

## Sources to sweep

1. **Docs** — integration guides, support pages, compatibility tables, setup pages, and troubleshooting pages that name specific services.
2. **README** — badges, feature lists, "Works with" sections, quickstart services.
3. **Marketing** — landing pages, feature announcements, changelog prose, blog posts.
4. **Packaging metadata** — dependency lists, peer/optional dependencies, extras, `package.json`, `pyproject.toml`, `Cargo.toml`, Helm chart requirements, `docker-compose` services.
5. **Code** — adapter files, provider registries, plugin manifests, CI service matrix, test fixtures referencing external services.
6. **Support artifacts** — issue templates, support documentation, sales collateral.

## Claim extraction

For each source, extract the claim as a sentence with a source reference, then:

1. Identify the integrated system by exact product name, never by category ("database", "ERP").
2. Identify the claimed version range or exact version. "Supports Postgres" is a versionless claim: turn it into explicit versions or drop it.
3. Identify the configuration the claim covers: protocol, auth mode, runtime/OS, SDK, feature flag, deployment topology.
4. Write the claim as: "integration X with version V under configuration C."
5. Record the source for every claim: file, URL, or commit.
6. Deduplicate claims that resolve to the same (X, V, C).

Do not expand "supports X" into every conceivable configuration. The claim is only what the source said, plus the minimal configuration needed to test it.

## Testability test

A claim is testable when a reader can answer:

- what is being integrated
- which version of the integration target
- which version of our product
- what configuration was exercised
- what test produced the evidence

Prose that fails the testability test is either:

- **uncertifiable** — remove the claim or rewrite it as a roadmap item; never leave it in the support matrix
- **under-specified** — ask the claim owner for the version and configuration before adding it to the matrix

## Output

A claims list: one row per (integration, version, configuration) with source, owner, and status (claimed / in-matrix / dropped). This list is the input to the certification matrix.
