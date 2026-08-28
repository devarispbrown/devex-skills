# Extension API Stability

## Purpose

Assign every exported extension surface exactly one stability tier, and define the breaking-change policy that governs each tier. Unlabeled exports are the failure mode this reference exists to prevent.

## Stability tiers

- **Internal**: host-only. Never part of the extension API. May change without notice. Do not expose.
- **Experimental**: opt-in, documented as unstable. May change or disappear without notice. Excluded from the compatibility window. Must carry a visible label and a defined promotion path (criteria, owner, target version).
- **Stable**: covered by behavioral compatibility. Changes require deprecation, migration guidance, and the SemVer contract applied to the extension API as a public surface.
- **Deprecated**: still functional for the documented window; removal is a breaking change requiring the full policy.

Every exported surface carries exactly one tier. A surface with no declared tier is treated as internal: no guarantee, and a checklist gap until labeled.

## Where tiers live

- In source: JSDoc/doc-comment tags (`@stable`, `@experimental`, `@deprecated`, `@public`), Python decorators, Rust attributes.
- In the manifest: the manifest declares the tier for each registered hook, interface, and config point.
- In the checklist: `scripts/check_extension_surface.py` flags exported interfaces with no tier annotation.

## Breaking-change policy

Breaking-change doctrine follows the `SemVer contract` and `Behavioral compatibility` sections of `dx-standards/compatibility.md`. Consequences for the extension API:

- A breaking change to a stable surface is a MAJOR event: changelog entry, migration guide, deprecation of the old surface for the documented window.
- A fix that changes observable extension behavior is never presented as compatible.
- Behavioral compatibility is judged per consumer: installed extensions, published extensions, scaffolded templates, test harnesses.
- Preview/beta consumers relying on documented-but-unstable behavior are accounted for, not silently broken.

## Deprecation lifecycle

1. Announce: label deprecated, state replacement and timeline, changelog entry.
2. Keep functional for the documented window.
3. Migrate: provide a path, automate what can be automated.
4. Remove: a breaking change, subject to the full policy.

## Enforcement

- CI fails on newly exported surfaces without a tier annotation.
- The manifest and the source agree on tiers; disagreement is a defect.
- The scaffolded skeleton ships with every surface already labeled.
