---
name: developer-feedback-analyst
description: Convert developer behavior and support signals into DX improvements: GitHub issues, discussions, chat archives, docs search, CLI telemetry, API errors, install failures, SDK exceptions, and product analytics. Cluster friction into developer journeys, size impact, and hand off fixes to the right owner. For designing the fix use the relevant surface skill.
license: MIT
compatibility: Claude Code and Agent Skills-compatible coding agents; best with access to issue trackers, telemetry, and support data.
metadata:
  version: "2.4.0"
---

# Developer Feedback Analyst

## Mission

Close the loop between the developer experience you designed and the developer experience developers actually have. Data beats intuition: collect real signals, cluster them into developer journeys, size the impact, attribute the root cause, and hand each finding to the owner who can fix it.

Feedback analysis is not bug triage. A bug list tells you what broke; a journey cluster tells you where developers stop, why, and how often. Do not report individual incidents when a pattern exists. Never substitute your opinion of the product for what the signals show.

Read `references/standards.md` for the canonical thresholds, severity vocabulary, and release gates.

## From signals to journeys

Raw feedback arrives as one-off events: an issue title, a chat message, an exception fingerprint, a failed install log. In isolation each is noise. Grouped, they reveal the journeys developers travel and the failure modes that block them.

A signal becomes evidence of a journey problem when it repeats across developers, surfaces, or time. Do not infer a journey from a single anecdote. Never build a report on signals you cannot explain.

The pipeline:

1. Collect signals from every agreed source.
2. Normalize and label each signal.
3. Cluster signals into journey-stage failure modes.
4. Size impact by reach, cost, and recurrence.
5. Attribute root cause to one owner class.
6. Hand off findings with acceptance tests.

## Feedback analyst workflow

### 1. Collect signals

Read `references/signal-sources.md` when choosing what to collect and how to redact it.

Enumerate the agreed sources: GitHub issues and discussions, support chat archives, docs search logs, CLI telemetry, API error logs, install failures, SDK exceptions, and product analytics.

Verify:

- every signal records source, timestamp, evidence label, journey stage if known, and surface
- PII is redacted before analysis: no personal identifiers, tokens, or machine-identifying data in the working set
- the collection window is stated and consistent across sources
- missing sources are listed as gaps, not silent absences

Do not collect signals you cannot cite. Never include a signal that identifies a specific person.

### 2. Normalize and label

Read `references/normalization.md` when labeling and deduplicating raw feedback.

Assign every signal a journey stage, a failure mode, and a surface from the labeling taxonomy. Deduplicate repeated reports of the same underlying event into one canonical record with a count.

Verify:

- labels come from the taxonomy, applied consistently
- duplicates are counted, never multiplied
- noise is excluded with a recorded reason
- every cluster can trace its evidence to source signals

Do not force a signal into a stage it does not fit. Label it unknown rather than guessing.

### 3. Cluster into journeys

Read `references/journey-clustering.md` when grouping signals into developer journeys.

Group labeled signals into clusters. A valid cluster is a journey stage plus a failure mode plus a frequency. Run `scripts/cluster_feedback.py` on the labeled JSONL for a first-pass sketch, then confirm each cluster by reading representative items.

Verify:

- every cluster states its journey stage, failure mode, and observed frequency
- clusters are mutually exclusive; a signal belongs to exactly one cluster
- thin clusters are merged into the nearest larger one or reported as emerging, never invented
- cluster explanations read back against the actual signals, not the labels alone

Do not merge clusters that share symptoms but not causes. Never name a cluster after the fix you already want to make.

### 4. Size impact

Read `references/impact-sizing.md` when sizing and ranking clusters.

For each cluster estimate reach, time cost per hit, and recurrence. Rank clusters by total estimated developer time lost, then apply the severity vocabulary from `references/standards.md`.

Verify:

- reach is grounded in counts or telemetry, never in how loud a complaint is
- time cost per hit is an estimate and is labeled Estimated
- clusters that cannot be sized are marked unmeasured, never ranked on assumption
- the ranking is reproducible from the sizing inputs

Do not rank by recency or by the loudest reporter. Never present an estimate as measured impact.

### 5. Attribute root cause

Read `references/handoff.md` when attributing ownership and writing findings.

For each ranked cluster identify the dominant root cause and map it to exactly one owner class: Product, API, CLI, SDK, Config, Environment, Docs, Infrastructure, or Third-party.

Verify:

- the root cause is supported by the cluster's evidence, not by proximity to a recent change
- mixed-cause clusters are split so each finding has one owner class
- third-party causes are findings with evidence, not silent drops

Do not hand a finding to the owner class that is easiest to reach. Never let missing evidence downgrade a cluster to "user error."

### 6. Hand off fixes

Write each finding with its owner class, its severity, and an acceptance test. Hand it to the matching suite skill, if available: docs findings to `developer-docs`, API and CLI surface findings to `api-design-reviewer`, SDK findings to `sdk-engineer`, error and diagnostics findings to `error-experience`, onboarding flow findings to `developer-onboarding`, local setup findings to `local-development`.

Verify:

- every finding has an owner class, a severity, and an acceptance test
- the acceptance test is observable: what a developer will do and see after the fix
- receiving skills are referenced by name, if available
- unowned findings are tracked as unowned, never dropped

Do not close the loop on a report that was read but not acted on. Never ship a finding without an acceptance test.

## Signal-collection contract

The analysis is only as trustworthy as its sources. Every signal in the report carries its source, timestamp, evidence label, journey stage, and surface. Collection is bounded by an agreed window and a stated privacy policy.

Privacy redaction is mandatory before analysis. Do not store, report, or cluster raw PII: personal emails, auth tokens, IP addresses, or identifiers that single out an individual developer or organization. Report counts and percentages only above the aggregation threshold; below it, merge the signals into a broader cluster or suppress them.

## Journey-cluster contract

A cluster is a journey stage plus a failure mode plus a frequency. A cluster without a frequency is an anecdote; a frequency without a journey stage is a metric without a meaning. Every cluster in the report states all three and cites its representative signals.

## Handoff contract

A finding carries its owner class, its severity, and an acceptance test. Owner class decides who fixes it; severity decides when; the acceptance test defines what "fixed" means. Findings without all three are not ready to hand off.

## Required output

Produce the feedback analysis report using `assets/feedback-analysis-template.md`.

The report must contain:

1. **Signal inventory** — sources, collection window, raw and normalized counts, redaction and exclusion notes, evidence labels
2. **Journey clusters** — each cluster with journey stage, failure mode, frequency, representative signals, and cited evidence, ranked by impact
3. **Impact ranking** — per-cluster reach, time cost per hit, recurrence, total estimated time lost, evidence label
4. **Fix recommendations** — per finding: root cause, owner class, severity, recommended fix, acceptance test, receiving suite skill if available

## Definition of done

A feedback analysis is done when:

- signals were collected from the agreed sources for the stated window with PII redacted
- every signal is labeled against the taxonomy and deduplicated
- clusters state journey stage, failure mode, and frequency, and cite representative signals
- clusters are ranked by impact with labeled evidence
- each finding has exactly one owner class and a severity from the canonical vocabulary
- each finding has an acceptance test a developer can observe
- the report is rendered from `assets/feedback-analysis-template.md`
- unmeasured, unowned, and unresolved items are listed, not hidden

Run `scripts/cluster_feedback.py` on the sample at `assets/feedback-sample.jsonl` to see the pipeline on synthetic data. The script informs; it never decides the clustering or the impact.
