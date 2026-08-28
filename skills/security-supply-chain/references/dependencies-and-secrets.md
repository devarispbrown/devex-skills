# Dependencies and Secrets

Dependencies and secrets share one property: both are trust extended outward and inward. Audit them together because a leaked secret often hides in a dependency's lockfile history.

## Lockfile and pinning policy

1. Commit lockfiles for every package manager in use. An uncommitted lockfile means every install resolves a different tree; that is a P2 finding.
2. Pin runtime dependencies to exact versions (or lockfile-equivalents), and treat transitive updates as intentional changes with review.
3. Keep pinning policy per surface: libraries may allow ranges to avoid dependency conflicts, but the build and release surfaces must resolve from the committed lockfile.
4. Never depend on a registry snapshot that is unverifiable: prefer integrity hashes in the lockfile where the ecosystem supports them.
5. Do not copy dependency code into the repository unless the source, license, and origin are documented.

Verify: a clean checkout builds from the committed lockfile with no network resolution drift.

## Vulnerability triage procedure

Run a vulnerability scan (OSV, advisory databases, or the platform's dependency scanner) and triage every finding:

1. **Affected**: does the vulnerable version actually ship in the release artifact? A dev-only dependency is lower severity than a runtime one.
2. **Exploitable**: is the vulnerable path reachable with attacker-controlled input? A reachable runtime vuln is P0; an unreachable dev-only one is P3.
3. **Patched**: upgrade to the fixed version, or apply the ecosystem's backported patch. Record the fixed version.
4. **Accepted**: if a fix cannot land, document the exposure, the reason, and a review date. Accepted without a review date is a P2 finding.

Assign every entry a severity from the canonical severity vocabulary and a status: affected, exploitable, patched, or accepted. Re-scan on every dependency change, not quarterly.

Verify: every known vulnerability in the tree has a triage entry with severity and status, and no P0 entry is unreviewed.

## Secret detection patterns

Wire secret detection into CI and pre-push hooks for:

- API keys, tokens, and passwords in any language's conventional format
- private keys and certificate material
- connection strings and DSNs with embedded credentials
- URLs and URIs that embed credentials
- placeholder-to-real drift: `sk-live-` versus `sk-test-` style prefixes and dummy values that were later replaced

Detect on the diff, not only the tree: a secret introduced and removed in the same PR still touched history.

## Historical exposure remediation

1. Assume an exposed secret is compromised from the moment it was pushed, not from when it was found.
2. Revoke and rotate the credential first. Revocation precedes scrubbing; scrubbing a live secret just hides it.
3. Purge the secret from history: filter-repo or equivalent rewriting, then force-push per the platform's protected-branch process.
4. Tell every consumer of the rotated credential, and update downstream configuration in the same change.
5. Audit access logs for use of the exposed credential between push and revocation, and record the evidence label of that check.

Never rotate a secret you have not revoked, and never report a scrubbed secret as fixed. Fixed means revoked, rotated, purged, and consumers updated.
