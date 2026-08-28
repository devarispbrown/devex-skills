# Discoverability Feedback Loops

## The "where is the thing" funnel

Discoverability is measured as a funnel:

1. **Find** — the developer's query returns the thing.
2. **Identify** — the entry matches what they need.
3. **Confirm** — name, version, lifecycle, and owner match their situation.
4. **Use** — they reach docs, install, or support without another search.

Every funnel stage is measurable, and every failure is attributable to a stage. A query that returns the wrong thing is a Find failure; a query that returns nothing is a gap.

## Signals to instrument

- **Search logs** — queries, top results, zero-result queries, queries that exit to search engines or docs 404s
- **404 pages** — docs 404s, API 404s, registry misspellings, dead `docs_link` targets
- **Support intake** — "how do I find X", "which package", "who owns Y" questions answered repeatedly
- **Repeated human pointers** — every pointer a human sends by hand is a missed catalog entry
- **Agent queries** — coding agents failing to resolve the same questions; agents and humans share the corpus

## Search log analysis

- rank queries by frequency and by zero-result rate
- group near-duplicate queries into one intent
- for each top intent, decide: existing entry not surfaced (alias or finding fix), missing entry (add it), or out of scope (document the decision)
- add the query's canonical phrasing as an `alias` on the entry; never create duplicate entries for synonyms

## 404-driven improvements

- every 404 on a canonical path is a P1 or P2 defect depending on whether a redirect or a missing entry is the right fix
- dead `docs_link` targets are fixed in the catalog and the docs, not silently replaced by search-engine results
- common misspellings and versioned URLs get aliases and redirects, not new entries

## The loop

1. **Measure** — collect funnel signals with evidence labels (Observed / CI-observed / Estimated) per `references/standards.md`.
2. **Triage** — attribute each top failure to a funnel stage and a fix class (entry, alias, link, docs, product).
3. **Fix** — change the catalog, aliases, links, or docs; verify mechanically with `scripts/check_catalog_metadata.py`.
4. **Re-measure** — repeat at the platform's cadence; record before/after numbers with labels.

Unlabeled metrics are UNVERIFIED. An improvement without a before/after measurement is a claim, not a result.

## Cadence

- search and 404 logs are reviewed at least once per release or per month, whichever is more frequent
- the top unanswered query list is a standing backlog item, re-ranked each cycle
- coverage is a signal, never a target: the goal is the funnel, not a percentage
