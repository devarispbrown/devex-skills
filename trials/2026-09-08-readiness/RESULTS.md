# Agent readiness across fifteen public repositories

Measured 2026-09-08 with suite 2.9.4 at commit `de1abc85`, using
`skills/agent-native-dx/scripts/check_agent_readiness.py`.

Reproduce:

```bash
git clone --depth 1 https://github.com/<owner>/<repo>.git
python3 skills/agent-native-dx/scripts/check_agent_readiness.py <repo>
```

Each repository was shallow cloned fresh on the measurement date. Per-repository commit
hashes are in `scores.json`, so any figure here can be re-derived against the same trees.

## Scope

Fifteen widely used repositories across six ecosystems: Rust, Go, JavaScript, Python,
Ruby and C. They were chosen for popularity and ecosystem spread, not sampled randomly,
so this describes these fifteen and does not generalise to a population.

## Scores

| repository | surfaces present | | band |
|---|---|---|---|
| `uv` | 15/19 | 79% | partly agent-ready |
| `llm` | 11/19 | 58% | partly agent-ready |
| `ripgrep` | 9/19 | 47% | not agent-ready |
| `mdBook` | 8/19 | 42% | not agent-ready |
| `black` | 7/19 | 37% | not agent-ready |
| `clap` | 7/19 | 37% | not agent-ready |
| `express` | 7/19 | 37% | not agent-ready |
| `simdjson` | 7/19 | 37% | not agent-ready |
| `tinygrad` | 7/19 | 37% | not agent-ready |
| `axum` | 6/19 | 32% | not agent-ready |
| `cobra` | 6/19 | 32% | not agent-ready |
| `got` | 5/19 | 26% | not agent-ready |
| `jq` | 5/19 | 26% | not agent-ready |
| `bubbletea` | 4/19 | 21% | not agent-ready |
| `sinatra` | 4/19 | 21% | not agent-ready |

Spread: 79% down to 21%. The inventory discriminates rather than
flattering or condemning everything, which is the property that makes a low score worth
acting on.

## The gap that matters most

**13 of 15 give no way to tell that a green local run predicts a green CI run.**

The documented check command does not appear in CI configuration, so the two are not
known to be the same product. A person notices the failing CI email and iterates. An
unattended agent does not: it either ships work it believes is finished, or spends cycles
guessing. That condition is the `UNVERIFIABLE_CI_PARITY` gate.

Runners-up:

- 9 of 15 do not document a setup command, and 9 of 15 do not document a test command. An agent cannot find how to build or test the majority of these repositories without inference.
- 13 of 15 do not pin a toolchain version.
- 12 of 15 ship no `AGENTS.md` or `CLAUDE.md`.

## Two universal gaps that are not defects

`MCP server exposed` and `llms.txt` are absent in all fifteen. Elsewhere in this suite a
checklist item that every healthy project fails is treated as a bad standard rather than a
finding. These are different: both are emerging practices, so universal absence is the
observation. Recorded so the distinction is deliberate.

## Limits

One checker version on one date. Popularity-weighted selection, not a random sample.
Heuristic detection: a surface is scored present when its marker is found, which is a
weaker claim than the surface being good. The score is an inventory signal, never a
verdict, and the checker says so on every run.
