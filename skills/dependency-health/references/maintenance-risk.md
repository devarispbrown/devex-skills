# Maintenance and Upgrade Risk

## Purpose

Assess whether a dependency is maintained and what an upgrade would cost. Findings carry severity from the canonical vocabulary (P0–P4) and an evidence label: Observed, CI-observed, or Estimated.

## Maintenance signals

Gather for each dependency:

- **Activity:** commits, releases, and issue closure over the recent period. Inactivity is a signal, not a verdict.
- **Release cadence:** regular releases indicate active maintenance; long gaps between releases are a flag.
- **Security history:** advisories, disclosure latency, and whether fixes shipped promptly. Track posture here; verify specifics in security tooling or the `security-supply-chain` skill if available.
- **Bus factor:** how many maintainers? One-maintainer projects are structurally risky, however healthy today.

## Abandonment indicators

Never assert abandonment from inactivity alone. Require at least two independent signals:

- no release or commit over a long interval
- repository archived or read-only
- maintainer communication stopped: no issue responses, no roadmap, no notices
- dependents report unaddressed breakage
- a successor or fork is publicly recommended

Classify abandonment as a P1 finding when the dependency is essential, P2/P3 otherwise.

## Upgrade risk

Assess per candidate upgrade, never per PR:

- **Breaking-change surface:** removed APIs, changed defaults, changed behavior, dropped platform or language versions.
- **Dependency churn:** how many transitive dependencies move with the upgrade; a large subgraph move is a batch, not a patch.
- **Test coverage:** does the suite exercise the dependency's surface? Weak coverage raises the effective risk.
- **Maintenance state of the target:** upgrading to a newer version of an unmaintained package changes nothing about abandonment.

Rate the upgrade risk per dependency: low, medium, high, blocked. Blocked means a migration plan is required before the upgrade can merge.

## Severity guidance

- **P0/P1:** essential dependency abandoned or unmaintained with no replacement plan; upgrade that is blocked but required for security posture.
- **P2:** convenience dependency with no maintenance signal; medium-risk upgrade without coverage.
- **P3:** minor signals; low-risk upgrades.
- **P4:** presentation or process-only.

## Verify

- every recency claim carries an evidence label
- abandonment requires at least two independent signals
- upgrade risk is stated as breaking-change surface, never diff size or PR count
