# Compatibility Report — <product>

## Status

**Result:** PASS | FAIL  
**Generated:** <date>  
**Revision:** <git sha>  
**Matrix source:** <path to matrix JSON>  
**Evidence labels:** Observed | CI-observed | Estimated

## Matrix claim-vs-evidence

| Surface | Version | Tier | Evidence | Status |
|---|---|---|---|---|
| <surface> | <version> | <tier> | <evidence> | EVIDENCED | UNTESTED | MISSING |

## UNTESTED_SUPPORTED_VERSION findings

| Severity | Surface | Version | Finding | Evidence | Fix |
|---|---|---|---|---|---|
| P1 | <surface> | <version> | <finding> | <evidence> | <fix> |

## Gap list

| # | Gap | Impact | Owner | Fix |
|---|---|---|---|---|
| <n> | <gap> | <impact> | <owner> | <fix> |

## Upgrade / downgrade

- Upgrade ladder: <N-1/N-2 status per platform>
- Data migration checks: <executed checks and results>
- Downgrade: <tested | documented as unsupported>

## Wire / schema

- Wire tests: <old-to-new, new-to-old status>
- Schema evolution: <per persisted format>
- Serialization: <round-trip status>

## CI matrix

| Cell | Job | Cadence | Last run | Result |
|---|---|---|---|---|
| <cell> | <job> | push | nightly | <date> | <result> |

## Recommendations

<prioritized list of fixes, keyed to findings and gaps>
