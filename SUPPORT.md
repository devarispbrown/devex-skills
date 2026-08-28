# Support

## Where to ask

| You want to... | Go here |
|---|---|
| Ask a question about using the skills | [GitHub Discussions](https://github.com/devarispbrown/devex-skills/discussions) |
| Report a bug | Open an issue with the bug report template |
| Propose a feature or skill | Open an issue with the feature request template |
| Report a security vulnerability | See `SECURITY.md` — private disclosure only |
| Contribute | See `CONTRIBUTING.md` |

## Before you ask

Run the suite's own checks first; most failures explain themselves:

```bash
python3 scripts/sync-standards.py --check
python3 scripts/validate_skills.py
python3 scripts/smoke_skills.py
```

When reporting a bug, include the command, its output, your Python version, and the skill or script involved.
