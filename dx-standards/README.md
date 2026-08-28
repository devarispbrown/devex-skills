# dx-standards

Single source of truth for the suite's shared vocabulary: principles, metrics, severity, release gates, compatibility, terminology, community, SLOs, and domain mapping, plus shared methodology files promoted from the original two skills (`magic-path.md`, `api-dx.md`, `sdks.md`, `lifecycle.md`, `llm-ready-docs.md`, `style.md`, `inventory_docs.py`).

## Model

- Files here are canonical. Skills carry generated copies under their own `references/standards.md` (section subsets) and, where mapped, whole-file copies of promoted files.
- Generated copies are committed, so every skill directory is self-contained: plugin installs and manual copies work without this directory.
- Never hand-edit a generated file (it carries a header). Change the source here and re-sync.

## Sync workflow

```bash
python3 scripts/sync-standards.py           # apply: regenerate all targets
python3 scripts/sync-standards.py --check   # verify: exit 1 on drift
python3 scripts/sync-standards.py --list    # print the mapping
```

- The mapping lives in `dx-standards/sync-map.json`.
- Selectors name source headings by exact heading text. A selector that matches nothing fails the sync (exit 1) — renames are caught at sync time, not at use time.
- CI runs `--check` on every push.

## Rules for hand-written skill files

- Hand-written `references/` files are procedural only: walkthroughs, decision trees, how-to-apply guidance.
- Normative numbers, tables, and vocabulary live here and flow into generated `references/standards.md`. Never restate a threshold with a different value inside a skill.

## Promotion notes

- The six reference files and `inventory_docs.py` were promoted verbatim from `skills/developer-docs/` (they were byte-identical in both original skills). Their in-skill copies are now generated.
- `skills/developer-docs-auditor/references/audit-methodology.md` and `release-gating.md` keep skill-specific procedure and point to the generated `references/standards.md` for canonical severity, verdict, and gate vocabulary.
