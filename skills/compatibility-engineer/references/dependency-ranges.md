# Dependency Version Range Policy

## Purpose

Define how dependency ranges are written, how minimum supported versions are maintained, and how transitive constraints are checked. Ranges are compatibility claims and carry the same evidence duty.

## Range policy

- Specify a minimum supported version plus a resolution policy; avoid unbounded upper ranges.
- Allow patch updates within a supported minor; gate minor and major bumps as release events.
- A dependency's support window constrains the product's: do not claim a runtime longer than its upstream support.
- Never widen a range to silence a conflict; resolve the conflict or document it.

## Minimum supported version maintenance

- Every minimum supported dependency version is a matrix cell and carries evidence.
- Bumping a minimum is a breaking change for users below it: changelog entry, migration note, release event.
- Test at the minimum, not only at latest; latest-only testing hides minimum-version breakage.

## Transitive constraint checking

- Resolve the full dependency tree for every supported platform; conflicts at the leaves are conflicts of the product.
- Check that transitive dependencies do not require versions outside the declared ranges.
- Security updates that move a minimum version force a re-run of the affected matrix cells.
- When ranges change, review lockfiles; never regenerate them blindly.

## Deprecation

- A dependency reaching end-of-support is announced and scheduled; the affected cells move to deprecated with a date.
- Silent removal is a defect; users must see the change in the changelog and the matrix.
