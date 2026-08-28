# Publishing the Certification Matrix

## Purpose

Put the matrix where users can find it, label it honestly, and remove claims the evidence no longer supports.

## Where to publish

- A dedicated compatibility or integrations page in the docs, linked from the README and any support matrix.
- The README may carry a compact summary table; the full matrix with evidence lives on the page.
- Keep the published page in sync with the machine-readable matrix; generate the page from the JSON where possible.

## Honest labeling

Every published cell shows:

- the tier: Certified / Certified with caveats / Stale / Uncertified
- the last-tested date
- the evidence link
- the evidence label: Observed, CI-observed, or Estimated

Do not publish a matrix that hides stale or uncertified cells. The checker output is the basis for the published table.

## Handling uncertified claims

When a claim cannot be certified:

1. Remove the claim from marketing and README text.
2. Mark the matrix cell uncertified with the reason.
3. Rewrite "supports X" as "X is under evaluation" only when the roadmap is real and time-boxed; otherwise drop the claim.
4. Never publish "technically supported" or "compatible with X" without a certified cell.

## Deprecating claims

When a service version is retired or an integration is dropped:

- Keep the historical row visible but labeled Uncertified or Deprecated, with the date and reason.
- State the replacement, if any.
- Remove the claim from current-surface text (README, quickstart, feature lists) in the same change.

## Report

Publish a certification report at each recertification using `assets/certification-report-template.md`, and link the report from the matrix page.
