# Versioning

The version recommendation is derived from the highest-impact change class, never from diff size, elapsed time, or preference.

## SemVer application

- **MAJOR** — any breaking class entry: a documented consumer's behavior changes, or public surface is removed. Includes renames, changed defaults, removed fields, and changed wire formats.
- **MINOR** — added class only: new backward-compatible public surface.
- **PATCH** — fixed or internal class only.
- **Deprecated** — the deprecation lands as MINOR (it adds the deprecation marker); the removal lands as MAJOR.

## When a fix is a MAJOR

- the fix changes the observable behavior of a documented consumer
- consumers built around the old, buggy behavior will break
- the corrected behavior differs from what was promised or documented
- a fix that only restores documented behavior with no observable consumer impact remains a PATCH

A tiny code change can be a MAJOR. Class, not size, decides.

## Pre-release and LTS

- Pre-release versions (`-alpha`, `-beta`, `-rc`) signal unstable surface; state what stability is promised.
- Promotion from preview to stable is a contract event: verify gates, update the support matrix, document the promotion.
- LTS releases extend the compatibility window; state the window and the backport policy.
- A breaking change on an LTS line without the documented backport path is a policy violation.

## Procedure

1. Take the highest-impact class from the classification table.
2. Map the class to a bump per the rules above.
3. State the concrete target version: current version plus the bump, with pre-release or LTS adjustments.
4. State the rationale in one or two sentences tied to the classification.
5. Record the recommendation in the verdict report before the tag exists.

Do not recommend a version before the classification and consumer analysis are complete.
