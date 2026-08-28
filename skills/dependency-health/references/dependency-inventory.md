# Dependency Inventory

## Purpose

Produce the complete, labeled list of every manifest and every direct dependency before any assessment begins. The inventory is the ground truth; every later step cites it.

## Manifests to find

Walk the tree for:

- **package.json** (npm) — `dependencies`, `devDependencies`, `peerDependencies`, `optionalDependencies`
- **go.mod** (Go) — `require` blocks and single-line `require` statements
- **Cargo.toml** (Rust) — `[dependencies]`, `[dev-dependencies]`, `[build-dependencies]`, and `[dependencies.*]` subtables
- **requirements.txt** and `requirements/*.txt` (pip) — every non-comment, non-flag line
- **pyproject.toml** (Python) — `[project]` `dependencies` array, `[project.optional-dependencies]`, and `[tool.poetry.dependencies]`

Skip vendor and build directories: `node_modules`, `vendor`, `target`, `.venv`, `venv`, `dist`, `build`, `.git`, `__pycache__`.

## Direct vs transitive

- **Direct:** declared in the manifest and used by the project's own code or configuration. Count and govern these individually.
- **Transitive:** resolved through a direct dependency and recorded in the lockfile. Govern through the direct dependency and the lockfile, never individually.
- A dependency imported only by tests or build scripts is direct but classified by section (dev, build).

Never count lockfile entries as direct dependencies. Lockfiles record resolved state; manifests record intent.

## Procedure

1. Run `scripts/check_dependency_health.py` for a first-pass map. Heuristic output; confirm before acting.
2. Walk the tree for manifests. Record each path and which package or workspace it belongs to.
3. Extract direct dependency names and declared version specs per manifest.
4. Record lockfile presence per manifest: package-lock.json, yarn.lock, pnpm-lock.yaml, go.sum, Cargo.lock, poetry.lock, uv.lock. A missing lockfile is a finding.
5. Estimate transitive counts from lockfiles or dependency tooling only; label every estimate.
6. Note name aliases and case variants (`yaml` vs `PyYAML`) instead of silently normalizing.

## Verify

- every manifest in the tree appears in the inventory
- direct and transitive labels are explicit per entry
- lockfile presence is recorded per manifest
- transitive counts are labeled approximate when not resolved from a lockfile
