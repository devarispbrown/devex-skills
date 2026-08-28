# Terminology Consistency

Developer trust erodes when the same concept has multiple names across code, API, CLI, UI, SDKs, docs, and errors.

Maintain a canonical glossary when needed:

- canonical term
- allowed aliases for search/migration
- forbidden/deprecated terms
- scope/context exceptions

Use `scripts/check_terminology.py` with a project-specific JSON policy for deterministic candidate detection. Review matches semantically because words may be valid in historical or explanatory contexts.
