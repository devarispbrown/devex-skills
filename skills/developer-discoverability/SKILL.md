---
name: developer-discoverability
description: Make APIs, services, owners, versions, and docs findable: package, plugin, SDK, connector, and extension catalogs for OSS; service, team, owner, datastore, and runbook catalogs for internal platforms, with Backstage-style ownership and lifecycle metadata. For understanding one codebase's architecture use architecture-experience.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with repository access and platform metadata.
metadata:
  version: "2.6.0"
---

# Developer Discoverability

## Mission

Make APIs, services, owners, versions, and docs findable. Every developer should answer "where is the thing?" in seconds: which package to install, who owns this service, what version is current, and where the runbook lives.

Design and maintain catalogs as machine-readable contracts. Entries carry ownership and lifecycle metadata so the answer stays correct as the system changes. A catalog that cannot be mechanically validated is a page, not a catalog.

Read `references/oss-catalog.md` for OSS catalog design.

Read `references/internal-catalog.md` for internal platform catalogs.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## Discovery is a product

Discoverability is the first stage of the developer journey, and it is a product with its own funnel. Treat the funnel as the specification and the catalog as its implementation:

1. **Find** — the search box, registry, or docs index returns the thing.
2. **Identify** — the entry tells the developer exactly what the thing is and which one they need.
3. **Confirm** — name, version, lifecycle, and owner match the developer's situation.
4. **Use** — the entry routes to the canonical install, docs, and support path.

A gap at any stage is a discoverability defect with a severity and a fix, never a mystery. Read `references/discoverability-feedback-loops.md` for the measurement and improvement loop.

## Catalog design

### 1. Establish truth about the surface

Inventory the real surface before designing entries:

- published packages, modules, and their versions
- plugins, connectors, and extensions distributed
- official SDKs per language and their parity state
- services, teams, datastores, and runbooks on internal platforms
- canonical docs and support paths for each entry

Never invent entries, versions, owners, or docs links. An entry that does not correspond to a released, owned thing is noise that poisons search.

### 2. Choose entry types and scope

Declare the catalog's scope and entry types, and record the decision.

For OSS products the canonical types are: package, plugin, SDK, connector, extension. For internal platforms: service, team, owner, datastore, runbook. Use the field sets and conventions in `references/oss-catalog.md` or `references/internal-catalog.md`.

One catalog may mix types, but every entry has exactly one `kind`. Duplicate entries for the same thing are a P2 defect; the canonical location is a stated contract.

### 3. Define the entry contract

Every entry carries the required fields: `name`, `owner`, `lifecycle`, `docs_link`, `status`.

- `name` — the canonical, searchable name; matches the published artifact or service id.
- `owner` — exactly one accountable team, per the contract in `references/ownership-metadata.md`.
- `lifecycle` — exactly one value from the vocabulary in `references/lifecycle-fields.md`.
- `docs_link` — a resolved, current link to the canonical documentation.
- `status` — the operational state of the thing (for example active, degraded, retired), not the lifecycle.

Add type-specific fields (`version`, `runtime`, `language`, `host`, `install`, `api_spec`, `repo`, `oncall`) as needed; never drop a required field to fit a type.

### 4. Assign ownership metadata

Read `references/ownership-metadata.md`.

Every entry has exactly one accountable owner recorded in a stable, machine-matchable form: team name or group id, not a personal handle when a team exists. Record where to reach the team: handbook, Slack, codeowners, on-call rotation. Define escalation: first responder, on-call, owner lead, and the path when ownership is disputed or unclaimed.

An entry whose owner cannot be reached is an operational defect, not a cosmetic one.

### 5. Assign lifecycle metadata

Read `references/lifecycle-fields.md`.

Classify every entry against the canonical lifecycle vocabulary (for example experimental, production, maintenance, deprecated, retired) and record the transition rules: deprecation announcements, sunset dates, replacement links. Never mark a deprecated thing as production without a migration path.

Staleness is a lifecycle defect. Entries that silently drift from reality (wrong version, moved docs, dead links) lose trust faster than missing entries. Record `last_verified` and treat age beyond the platform threshold as a P2 backlog item.

### 6. Validate mechanically

Run `scripts/check_catalog_metadata.py <catalog.json>` against every catalog file. It checks each entry for the required fields and exits 1 when any entry is missing one. JSON only: the stdlib has no YAML parser, so catalogs are committed as JSON.

The script is a floor, not a ceiling. It catches missing fields; it cannot catch wrong owners, stale versions, or broken links. Pair it with human review and the feedback loop in step 7.

### 7. Close the feedback loop

Read `references/discoverability-feedback-loops.md`.

Measure how developers find things: search logs, 404 pages, support tickets, and repeated "where is the thing" questions. Convert the top unanswered queries into entries, aliases, and links. Re-measure after changes, and label every metric per the standards.

A catalog that is not measured is unverifiable, and unlabeled metrics are UNVERIFIED.

## Entry contract

Every entry, regardless of type, must be:

1. **real** — corresponds to a released, owned, documented thing
2. **findable** — the canonical name matches how developers search
3. **owned** — exactly one accountable team, reachable and current
4. **classified** — exactly one lifecycle value and one status value
5. **linked** — the docs link resolves and points to current canonical documentation
6. **versioned** — version information is explicit where the thing versions
7. **non-duplicated** — one canonical entry per thing; aliases point to it

## OSS catalog contract

For products that publish packages, plugins, SDKs, connectors, or extensions:

- every distributable artifact has an entry or is explicitly out of scope
- each official SDK entry states its language, version, and parity status
- plugins, connectors, and extensions state the host product and versions they target
- install and integration instructions live in docs linked from `docs_link`, not in the catalog
- naming matches the published artifact, with aliases for common search variants and misspellings

Read `references/oss-catalog.md`.

## Internal catalog contract

For internal platforms:

- every production service has an entry with a service id and an owning team
- every team is discoverable as a first-class entry with charter, scope, and contact
- every runbook is linked from its service and lists escalation order
- every datastore states its owning service, sensitivity, and access path
- entries never expose secrets, credentials, or unauthorized access paths

Read `references/internal-catalog.md`.

## Docs contract

- `docs_link` always resolves; a dead or redirected canonical link is P1
- docs pages state the versions and lifecycle they cover
- migration and deprecation pages are linked from the entries they affect
- coding agents can retrieve the same facts humans can, in clean structured text

For authoring the docs themselves, hand off to `developer-docs`; for docs release gating, `developer-docs-auditor`; for product release gating, `release-guardian`.

## Required output

For every catalog design or audit, produce the catalog audit report using `assets/discoverability-audit-template.md`.

The report must contain:

1. **Scope** — catalogs and entry types covered, and the funnel stages measured
2. **Coverage** — entries present vs. surface inventoried, per type
3. **Field completeness** — entries missing `name`, `owner`, `lifecycle`, `docs_link`, or `status`, with the mechanical check result
4. **Ownership** — unowned, unreachable, stale, and conflicting-owner entries
5. **Lifecycle** — misclassified, stale, and undocumented deprecations
6. **Docs** — unresolvable or outdated `docs_link` entries
7. **Feedback findings** — top unanswered search queries and 404 paths with proposed fixes
8. **Backlog** — prioritized P0–P4 findings, each with an owner type and acceptance test
9. **Verdict** — PASS / PASS WITH DEBT / FAIL / UNVERIFIED, per the standards vocabulary

## Definition of done

A discoverability change is done when:

- the surface is inventoried and every entry corresponds to a real, released, owned thing
- every entry carries `name`, `owner`, `lifecycle`, `docs_link`, and `status`
- `scripts/check_catalog_metadata.py` exits 0 on the catalog
- owners are reachable and recorded in machine-matchable form
- lifecycle values come from the canonical vocabulary, with deprecation paths
- docs links resolve to current canonical documentation
- aliases cover the top search variants and common misspellings
- the top unanswered queries and 404s from the feedback loop are addressed or backlogged with severity
- the audit report is rendered from `assets/discoverability-audit-template.md`
- no defect is hidden by an unlabeled metric or an assumption
