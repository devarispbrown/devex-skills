## Summary

<!-- What this PR ships and why. -->

## Release checklist

- [ ] `python3 scripts/sync-standards.py --check` clean
- [ ] `python3 scripts/validate_skills.py` zero failures
- [ ] `python3 -m py_compile scripts/*.py skills/*/scripts/*.py` clean
- [ ] New checker scripts smoke-test green: `python3 scripts/smoke_skills.py`
- [ ] Every new skill description names its near-twin with a "use X instead for Y" pointer
- [ ] Constants referenced by name only; no restated numeric values in hand-written files
- [ ] CHANGELOG entry matches the plugin version

## Commit review

<!-- Reviewer: walk `git log main..<branch> --oneline` commit-by-commit. Each commit must independently pass CI. -->
