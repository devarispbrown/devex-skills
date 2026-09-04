# Agent DX: proposal

Status: **resolved 2026-09-03, and not in the way this document specified.** The sections
below are preserved as written. Read this resolution first.

## Resolution

`agent-integration-dx` was built. The suite is at forty-three skills.

**The decision rule below was not satisfied. It was bypassed.** The trial ran as a
two-repository pilot and returned `TOO-FEW-FAILURES`: one distinct failure mode against a
pre-registered minimum of fifteen, so no uncovered share was ever computed and the
`u >= 0.40` gate that this document made the skill conditional on was never met. The
remaining six repositories were not run, for the reasons in
`trials/2026-09-03-agent-dx/RESULTS.md`.

The skill was built on different evidence, gathered afterwards: a static audit of fifteen
public repositories in six ecosystems found that none exposed an MCP server, that `MCP`
appeared in two of five hundred and seventy-eight files in this repository, and that no
checker in the suite looked for one. That is a coverage gap with no owner, which is a
legitimate reason to write a skill. It is not the reason this document said would count.

The distinction matters and is recorded rather than smoothed over. The trial asked whether
agents fail in ways existing standards miss. The audit asked whether a surface exists that
the suite does not cover at all. Those are different questions, and the second one was
answered first because it was cheaper and did not need the trial to conclude.

Anyone reading this document as a record of how the decision was made should know that the
pre-registered mechanism did not make it. A maintainer did, on other grounds, and wrote
that down here instead of editing the gate to match the outcome.

## What else changed

- `agent-native-dx` remains the agent auditor and was reframed around the question a
  developer actually asks, with the readiness inventory extended from seven surfaces to
  nineteen.
- The trial machinery it describes exists and works: `agent_trial_driver.py`,
  `agent_trial_scorer.py`, and `references/trial-protocol.md` in `agent-native-dx`.
- The five cut skills stayed cut. Nothing in the audit argued for reinstating them.
- The augmentation half of this proposal is still open: promoting agent-facing
  requirements from mentioned to gated inside the skills that already own them. The audit
  named the highest-value one, CI parity, missing in thirteen of fifteen repositories.

---

Status of the original document below: proposed. Nothing in it was adopted on its own
strength. No file in `dx-standards/` changed because of it.

Owner: repository maintainer. Review by 2026-12-01. If the trial described under
"The experiment" has not run by that date, withdraw this proposal rather than leave
it standing as unexecuted intent.

This is the output of four adversarial reviews of an earlier draft that proposed six
new skills, eight new gates, six numeric constants, a four-persona model, and a
parallel nine-stage agent journey. The reviews cut it to one new skill, zero gates,
and zero constants pending evidence. A second round of reviews against the rewrite
found a fabricated citation, four non-reproducible figures, and an experiment whose
control arm does not exist. Those are corrected below, and the corrections are the
most useful part of the document.

## Method for every count in this document

All greps are case-insensitive file counts over `skills/` and `dx-standards/`,
578 tracked files:

```
git ls-files skills dx-standards | wc -l          # 578
grep -ril '<term>' skills dx-standards | wc -l    # file count
```

An earlier version of this document said "608 files." That was `find skills -type f`,
which counts 48 gitignored `.pyc` artifacts and omits `dx-standards/` entirely. The
term counts were correct; the denominator was not.

## What the suite already covers

Verified by reading each cited location:

- Determinism, idempotency, non-interactive parity, dry-run defaults, destructive
  guardrails, and secrets hygiene: `agent-native-dx/references/automation-safety.md`,
  six sections.
- MCP tool names, descriptions, argument matching, structured error failure modes:
  `agent-native-dx/references/machine-surfaces.md` § MCP servers.
- Stable machine-readable error code with explicit retryability and a request
  identifier: `error-experience/SKILL.md` § API contract, gated by
  `UNEXPLAINED_ERROR`.
- `--json` on every data command, an exit-code contract, and `--dry-run`:
  `cli-designer/SKILL.md` § Output contract, § Exit-code contract, § Destructiveness
  contract.
- Delegation identity, stated as showing "who the credential acts as, not just who
  created it", plus least-privilege and time-bound grants:
  `access-and-permissions-dx/SKILL.md` § Permission UX audit.
- N-run nondeterminism testing: `quality-engineer/references/specialized-techniques.md`,
  "run the same suite N times and fail on flapping results".
- Distributions over single runs: `performance-engineer/SKILL.md`, "numbers are
  medians or distributions, never a single run".

Citations are by heading and symbol name rather than line number. Line numbers in a
repository with this commit rate go stale within days, and nothing in CI checks them.
`sync-standards.py` already hard-fails on a renamed heading, so headings are the only
anchors this repo actually enforces.

## Where coverage is thin

Three areas, stated as insufficient depth rather than absence. The distinction matters:
an earlier draft claimed `MCP` appearing in 2 files proved a gap, while separately
citing one of those same 2 files as already covering MCP. Grep counts measure strings,
not coverage.

1. **Tool definitions as a shipped product artifact.** `machine-surfaces.md` verifies
   that tool names and descriptions are accurate. It does not treat the description as
   a prompt the vendor authored and shipped, and nothing in the suite reviews prose as
   an executable artifact. Depth, not absence.
2. **Untrusted content returned into an agent's context.** A product returning
   third-party text an agent may read as instruction. `untrusted` appears in 8
   files, all of them treating human supply chain or plugin isolation:
   `security-supply-chain`, `extensibility-engineer`, `quality-engineer`. None reach
   agent context as a hazard surface. Depth, not absence, again.
3. **The measuring instrument.** Every existing measurement is a wall clock, a command
   count, or a credential count. Token counts and N-run variance are new capability,
   not a stricter stopwatch.

Everything else the draft proposed was a rename, a severity bump, or an anthology of
contracts that already have owners.

## The experiment

The earlier design was: run agent trials on 8 public repos, correlate against
`developer-experience-auditor`'s `journey_runner.py` scores, and treat decorrelation as
justification to proceed. That design is void, for a reason worth recording.

`journey_runner.py` cannot score a repository. `load_manifest` requires a hand-authored
14-stage JSON manifest, and `load_scores` requires a hand-supplied per-area 0 to 100
JSON. Without `--scores` it prints `Overall DX: UNVERIFIED`. So the proposed control arm
was a number a human auditor assigned by judgment, over a journey that same auditor
authored, compared against agent tasks that same auditor wrote. This document rejects
`AGENT_RECOVERY_RATE` because the auditor authors the injected error and therefore sets
the score. The correlation design had that defect on both axes at once.

At 8 repositories a Pearson correlation is also underpowered: the critical value at
alpha .05 two-tailed is approximately r = 0.707, so every result between no
relationship and a strong one falls in one undifferentiated band. And "decorrelation"
was operationalized as a single off-diagonal repository, which is an existence proof
rather than a correlation, so both branches could be satisfied at once and the author
would choose.

### Replacement design

Drop the correlation. Test attribution instead, which needs no human-DX baseline and
produces a directly actionable output.

**Claim under test:** agent failures are attributable to product surfaces that existing
gates already cover.

**Procedure.**

1. Pre-register, before any run: the repository count and the repositories themselves,
   the task prompts, the model, the checkpoint, the temperature, the harness, the tool
   set, and the classification codebook. Publish the registration in the pull request
   that adds the trial.
2. Run the trial driver against each repository, N ≥ 5.
3. For every observed agent failure, ask whether the existing standards already catch
   it. Coverage is decided against an enumerated corpus, registered in advance:
   `release-gates.md` § Gate identifiers, the community gates in `community.md`, the
   thresholds in `metrics.md`, and named skill-level contracts such as
   `cli-designer` § Destructiveness contract and `web-console-dx`'s automation parity.
   Scoping coverage to the nine gate constants alone would score as uncovered every
   failure this document itself credits to `MAGIC_PATH_MAX_CREDENTIALS` or to
   automation parity, biasing the result toward proceeding.
4. Separately, attribute each failure to one of the nine problem classes in
   `terminology.md`. That classification is for reporting only and never decides
   coverage: the nine classes are exhaustive by construction, so treating a successful
   classification as coverage would drive the result to zero mechanically.
5. Classification follows the pre-registered codebook. A second rater classifies a 20%
   sample independently and the disagreement rate is published. Stripping repository
   identity from transcripts is not blinding, since transcripts carry the product's own
   commands and error strings; the codebook and the second rater are the actual
   controls on the operator who wrote the prompts also judging the outcomes.

**Decision rule, fixed before the first run.** Let `u` be the share of distinct failure
modes the registered coverage corpus does not catch.

`u` is a ratio over a count, so it inherits the granularity problem this document
rejects elsewhere: over 5 observed modes the only attainable values are 0, .20, .40,
.60, .80, 1.0, and strict inequalities would put both .20 and .40 inside the
inconclusive band. Two guards. The trial does not report `u` unless it observes at
least 15 distinct failure modes; below that the task set is re-scoped and re-run. And
the bands are inclusive at the edges:

- `u ≤ 0.20`: agent DX is the existing standards with the slack removed. Ship tightening
  edits to existing skills, and nothing new. Publish the negative result.
- `u ≥ 0.40`: the gap is real, and the classification is itself the list of what is
  missing. The conditional section below unlocks.
- `0.20 < u < 0.40`: inconclusive. One re-run at 2N against the same registration. If
  still inconclusive, withdraw this proposal.
- Zero failures observed: treated as `u ≤ 0.20`. Training-set contamination makes
  clean runs on popular repositories plausible, and a trial that surfaces no failures
  is evidence of nothing that warrants new surface area.

The thresholds 0.20 and 0.40 have no derivation. They are conventions chosen before
seeing data, and their only virtue is being fixed in advance. Stating that plainly is
the difference between a convention and the fake precision this document rejects.

**Threats to validity, none of them fully resolvable.**

- *Training-set contamination.* Public repositories are the ones most likely memorized,
  which inflates agent success independently of agent affordances and correlates with
  popularity, which correlates with documentation quality. Unresolvable; state it as a
  scope limit.
- *Prompt authorship.* Task prompts dominate agent outcome and are written by the
  experimenter. Mitigated only by pre-registration, not eliminated.
- *Model and harness.* Held fixed and declared, which makes the result a statement about
  one configuration rather than about agents in general.
- *Classifier bias.* Mitigated by stripping repository identity, not by blinding the
  classifier to the hypothesis, which is not achievable with one operator.

The failure-mode inventory is a deliverable under every branch, including withdrawal.
The verdict is not secondary: it decides whether anything below the "If the experiment
justifies a constitution change" heading happens at all.

### Why the runner splits in two

- A **live driver**, run by an operator, never by CI. It executes an agent N ≥ 5 times
  and writes a trial log as JSON with model, checkpoint, temperature, harness, and tool
  set as required fields.
- A **stdlib-only offline scorer** that consumes that log and emits counts and
  distributions deterministically, with fixture logs under `assets/` so `smoke.json`
  exercises it offline.

The split is forced by CI. 44 of the 48 scripts under `skills/*/scripts/` declare
"Stdlib only." verbatim, two more declare a variant, and no script in the repository
imports a third-party package. CI compiles every script and `smoke_skills.py` asserts
deterministic exit codes. Separately, GitHub withholds secrets from `pull_request` runs
on forks, so a keyed runner could never gate a contributor pull request. Execution stays
an operator activity, exactly as magic-path timing already is.

**Cost, which no reviewer priced and the draft omitted.** One trial is N ≥ 5 autonomous
agent sessions. A matrix of 8 repositories is 40 or more sessions, plus operator time to
author 8 task sets and classify the failures. That is a metered bill and several
operator days, plus the classification round and the second rater. It is charged to
whoever runs the trial. A suite that ships `developer-economics` should state its own
cost envelope before asking anyone else to spend it. Note this design is cheaper than
the correlation design it replaces: the same agent sessions, minus the hand-authored
14-stage manifests and per-area score sets that design needed for every repository.

## Constants: why all six were withdrawn

| Proposed | Why it does not survive |
|---|---|
| `AGENT_TASK_DETERMINISM_RATE` ≥ 90% at N=5 | Arithmetically impossible. Attainable values at N=5 are 0, 20, 40, 60, 80, 100. Gating at 90% silently means 5 of 5. |
| `AGENT_FIRST_CALL_SUCCESS_RATE` ≥ 80% at N=5 | A true-80% product fails a 4-of-5 gate 26.3% of the time; a true-60% product passes 33.7% of the time. Both recomputed independently. That cannot support an unappealable FAIL. The numerator is undefined besides, since the agent chooses which call is first. |
| `AGENT_RECOVERY_RATE` | The auditor authors the injected error, so the auditor sets the score. Restates `TTR_TARGET_MIN`, owned by `error-experience`, in a different form. |
| `AGENT_TASK_MAX_TOOL_CALLS` = 10 | Measures the harness, not the product. A shell tool chains three commands into one call where an MCP-only harness spends three. |
| `AGENT_CONTEXT_BUDGET_TOKENS` = 25000 | 2.5% of a 1M-token context window. Also the wrong kind of metric: `MAGIC_PATH_MAX_MIN` budgets the user's finite attention, while a token count budgets a vendor cost the user does not pay. |
| `SUPERVISOR_REVIEW_BUDGET_MIN` = 10 | A wall-clock metric, contradicting this document's own thesis that time is the wrong currency. Scores the agent's output rather than the audited product, and names no owning skill, which `slo.md` § SLO ownership requires. |

**The asymmetry.** Human constants anchor to attention span, flow state, and a
volunteer's free evening. Agent constants anchor to a model generation. That is a decay
liability the existing constitution does not carry, and labelling a number "provisional"
does not fix it, because readers copy numbers rather than disclaimers.

If a budget is ever needed, express it relative to the target model's context window so
it ages with the models rather than against them. The one mechanically measurable form
is entry-corpus size as a byte count over a declared manifest with a named tokenizer:
static, offline, and fixture-testable. It ships as a P2 target, never a hard gate.

## Gates: why none ship yet

Duplicates. Extend the existing `fails when` text rather than minting a constant:

- `NO_MACHINE_ERROR_CONTRACT` is inside `UNEXPLAINED_ERROR`, which already requires
  retry-safety and a correlation identifier.
- `AGENT_PATH_REQUIRES_HUMAN_UI` is inside `BROKEN_QUICKSTART`, which fails when manual
  approval or support is required with no sandbox route. Note this is a near miss rather
  than an exact one: dashboard-only credential creation is caught by
  `MAGIC_PATH_MAX_CREDENTIALS` and by `web-console-dx`'s automation-parity requirement,
  not by the literal text of `BROKEN_QUICKSTART`.
- `SILENT_SCHEMA_DRIFT` duplicates `STALE_PUBLIC_REFERENCE` and `SDK_API_DRIFT`, both P1.
  The draft called it "upgraded from P1", which was false: the constant has zero
  occurrences in the repository. A P0 bump would require amending the P0 and P1
  definitions in `severity.md`, which every skill pulls, and re-rating both siblings.
- `UNBOUNDED_DESTRUCTIVE_TOOL` is covered by
  `cli-designer/references/destructive-operations.md`, which specifies dry-run,
  blast-radius-scaled friction, reversibility, and recovery. Extend it to non-CLI tool
  surfaces.

Not gates:

- `UNATTRIBUTED_AGENT_CHANGE` was proposed at P2, but `severity.md` makes FAIL a P0 or
  P1 condition, so a P2 gate cannot fail anything. It also audits the consumer's
  repository hygiene rather than the audited product.
- `AMBIGUOUS_TOOL_SURFACE` and `NON_DETERMINISTIC_AGENT_PATH` are real conditions with
  no decidable check. Lexical similarity does not measure selection error: `create_user`
  and `create_org` are near-identical and unambiguous, while `send` and `dispatch` are
  distant and ambiguous. The eval form needs a gold set the auditor writes, so it scores
  the auditor. Ship them the way `guessability_check.py` ships: `candidate:` lines and
  an explicit refusal to issue a verdict. Note that script exits 1 when it emits
  candidates, so "non-gating" here means "no PASS or FAIL verdict", not "exit 0". An
  earlier version of this document had that backwards.

The one genuinely new condition:

- `UNLABELED_UNTRUSTED_CONTENT`. Reachable by no existing gate. As written it is
  undecidable: whether a `description: string` field carries operator-authored or
  user-submitted data is invisible in the schema, and no wire format standardizes
  "labeled". A detector that cannot see the hazard reports "not detected", which becomes
  PASS. A P0 that can only produce false negatives launders unexamined risk into a
  passing verdict.

  Implementable form: the product declares which response fields are third-party-sourced
  and what its labeling contract is, and the script checks declaration coverage against
  the schema. That is a disclosure gap at P1, not a P0 safety proof. Its owner, if the
  trial confirms the gap, is `agent-integration-dx`. Routing it to
  `security-supply-chain` would contradict the
  claim that it has no human analogue, since those skills are built around human supply
  chain and human permission models.

## Skills: one, not six

**This section is conditional on `u ≥ 0.40`.** Nothing here is authorized by the
document itself. An earlier version stated the skill imperatively, with a name, a
domain, a count, a scope, handoffs, and an owned gate, while separately claiming the
experiment gated it. That is the pre-registration defect the experiment exists to
avoid, committed in the same document.

The cuts below are not conditional. They are redundancy findings against the current
suite and hold regardless of what the trial returns.

If the gap is confirmed: add `agent-integration-dx` in the Build domain, taking the
suite from 42 to 43, and nothing else.

Scope: tool definitions and MCP servers as a shipped product artifact. Description-as-prompt
authoring, argument-schema design, response shaping against a context budget, pagination
and truncation.

It cites rather than restates: the MCP specification and SEP-986 on tool naming,
Anthropic's "Writing effective tools for AI agents", and AWS's `DESIGN_GUIDELINES.md`.
The suite already does this with SemVer, Diátaxis, CHAOSS, and OpenTelemetry. The
analogy is imperfect and the difference must be handled: those four are dated, versioned
standards with deprecation policies, while a vendor engineering post and a file in
someone else's repository tree can move or change silently. Each citation therefore
pins a dated revision and carries a re-verification cadence, and drift in a cited source
is treated the way `STALE_PUBLIC_REFERENCE` treats drift in a generated reference.

What it contains beyond links: the adversarial audit. A tool surface reviewed by someone
trying to prove the agent will pick the wrong tool. That check ships as non-verdict
candidates until the experiment produces enough failure data to make it decidable, which
is a real limitation and the reason this skill follows the experiment rather than
preceding it.

Required handoffs, or the boundary stays ambiguous: `machine-surfaces.md` § MCP servers
gains an explicit pointer, and `api-design-reviewer` gains one for tool surfaces.

**Cut, with the owner that absorbs each:**

| Cut | Absorbed by |
|---|---|
| `agent-experience-auditor` | A second orchestrator voids the README's strongest line: "You do not need to learn forty-two skills. You need one." Two front doors is no front door. This argument stands alone and does not depend on `agent-native-dx` being complete. |
| `agent-eval-engineer` | One system-type row in `quality-engineer/references/test-strategy.md`, whose classification table is § Step 1: Classify each production surface, and one fixture type in `test-data-and-fixtures`. N-run discipline is already doctrine. |
| `autonomous-operations-dx` | An anthology of seven skills' contracts, and prohibited by `policy-experience/SKILL.md`: "Do not re-inventory domains owned by sibling skills... Duplicate rule inventory is how policies drift." |
| `agent-trust-and-provenance` | Scopes the wrong company's product. A tool vendor cannot ship provenance for a diff their product did not author. Residue is one bullet in `access-and-permissions-dx`. |
| `context-engineering` | `dx-standards/llm-ready-docs.md`, 37 lines, plus a token-budget bullet. **This is the weakest of the five cuts.** The absorber is a static standards file with no skill, no script, and no owner, while `slo.md` § SLO ownership requires an owning skill for any measured value. If the experiment surfaces documentation-side context failures, reopen this one first. |

`agent-native-dx` is not narrowed to a sub-persona. The draft proposed amputating the
suite's only agent skill to make room for six that do not exist. It stays the agent
auditor and gains token-budget measurement in `references/agent-audit.md`
§ 4. Record tool-use traces. It does not gain determinism measurement, which its
automation-safety contract already specifies.

## Augmentations: all nine

No-ops, already written, drop entirely:

1. `cli-designer`: `--json`, exit codes, and `--dry-run` are all present.
2. `access-and-permissions-dx`: delegation identity is present.
3. `error-experience`: the machine error contract is present.
4. `agent-native-dx`: the determinism half is present in the automation-safety contract.

Partially redundant:

5. `api-design-reviewer`: guessability already asks whether a developer can predict the
   endpoint, parameters, response shape, error, and enum values without reading the
   docs. Tool-selection is that question with a different consumer. New only as an eval
   harness, which the experiment must supply first.

Worth doing, small:

6. `sdk-engineer`: tool definitions as a capability-matrix row. Best of the nine, costs
   one row.
7. `developer-economics`: one sentence on limits sized for retry loops.
8. `observability-readiness`: the agent run as a trace root.
9. `developer-onboarding`: CAPTCHA and email-click specificity as a bullet under the
   existing `BROKEN_QUICKSTART`.

## Personas: one audience and one axis

The draft asserted four. Three do not survive.

A coding agent running a migration is the operator, so the builder and operator personas
are one actor at different blast radius, which the suite already models as severity and
as permission scope. The supervisor is not a persona of the audited product, since they
consume the agent's output, which the harness authors. The tool consumer is real and is
the gap.

No persona column in `domains.md`. `validate_skills.py` anchors its domain-count regex to
a leading `| <Domain name> (<count>) |` cell, so a persona first column yields a claimed
count of zero and a hard failure. Tagging any skill with two personas, which is the point
of personas, trips the same file's duplicate-row check. If persona tagging ever ships it
belongs in `SKILL.md` frontmatter with a separate cross-check.

## Journey stages: no new vocabulary

The draft claimed a nine-stage agent journey was an overlay on the canonical 14. It was
not. `plan`, `interpret`, and `report` have no canonical stage, and 8 of the 14
(install, configure, modify, break, diagnose, test, deploy, upgrade) were absent.
`terminology.md` requires that a secondary list name only stages that already exist.

Express the agent-specific acts as evidence recorded inside existing stages. Do not add
canonical stages. `report` is a high-frequency term in `skills/` and names the suite's
two flagship artifacts, the DX Report and the Community Health Report, while 40 of 42
skills use `## Required output` as the heading for that artifact. `plan` collides with
ordinary prose. Promoting either to a stage name creates a collision no checker can
resolve.

## If the experiment justifies a constitution change

Not before, and only for the failure modes the trial actually observed.

Agent constants and gates would live in a new `dx-standards/agent-dx.md` with stable
`## ` headings, since a non-matching selector is a hard failure in `sync-standards.py`.
`release-gates.md` would get a short pointer section modeled on its existing
`## Community gates`, rather than inlining agent gate rows into `## Gate identifiers`.

The reason is fan-out. 23 skills consume `§ Gate identifiers`; `agent-native-dx` is not
one of them, so inlining would grow 23 unrelated skills' generated standards while the
agent skill gained nothing. The pointer pattern confines the change to the skills that
need it, with one exception: `developer-docs-auditor`, `developer-experience-auditor`,
and `release-guardian` pull `release-gates.md` as a whole file, so they absorb any new
section regardless. An earlier version of this document attached specific byte and percentage
projections to that argument. Those figures did not reproduce and have been removed:
projecting three significant figures for content nobody has written is the same error as
`AGENT_CONTEXT_BUDGET_TOKENS = 25000`, in a different unit.

`severity.md` is the one file all 42 skills pull in full, so it takes a single clause and
nothing more. `slo.md` would need its "exactly one home" rule amended in the same commit,
and SLO rows land in the phase their owning skill ships, since a row cannot name an owner
that does not exist.

**On the evidence label:** do not add "Agent-observed". `metrics.md` § Evidence labels
already defines Observed as "a human or agent actually executed the path". A fourth label
either duplicates it or silently demotes every existing agent-produced measurement.

If a distinct label ever ships it must carry the rule mirroring "an estimate can never
prove a PASS": agent-produced evidence may fail a gate and can never prove one. A capable
agent failing is an existence proof of a defect. One agent succeeding once, on one model,
on one day, proves nothing about the agent population a product faces, and expires
silently when the model is upgraded.

## Positioning

Do not call the output an "AX Report". Netlify ships AXIS, an MIT-licensed Agent
Experience Index Score at `github.com/netlify/axis`, documented at `axis.run`.
Separately, `agentexperience.ax` holds the broader AX term and its vocabulary.

The defensible position is not a competing agent score. It is scoring human DX and agent
DX in one report against one vocabulary, and naming where they trade off. That claim is
currently a slogan: the suite names zero such tradeoffs today. Candidates the experiment
should confirm or kill:

- Verbose structured errors help agents parse and hurt humans scanning a terminal.
- Interactive confirmation protects humans and blocks unattended agents.
- Short quickstarts help humans and starve agents of the context they need.

If the experiment returns "existing gates already cover it", there are no tradeoffs to
name and this positioning dies with the thesis. That is the correct outcome, not a
failure of the experiment.

## The objection this proposal must keep answering

Forty-two skills, zero external users, five days of git history, and no evidence any of
them changed an outcome for anyone. Six more is not a strategy, it is avoidance.

The objection is correct. The trial is the cheapest path to the first externally
verifiable output this suite has produced, for the human thesis as much as the agent one.
The constitution is an instance of the problem, which is why it now comes last.

## Cost checklist for any change to the skill count

Atomic, or CI breaks: the `plugin.json` skills array and the spelled-out count in its
description; `domains.md` counts, which must re-sum against the plugin array; the README,
which must name every skill and stay under its enforced byte cap; a `CHANGELOG.md`
version heading; and, if the plugin version bumps, every `SKILL.md` `metadata.version` in
lockstep.

Known unenforced gap: the README states the skill count in prose in four places and
`validate_skills.py`'s stale-phrase list does not catch a stale count.

## Known limitations of this document

- Roughly 40 references to repository locations, cited by heading and symbol rather than
  line number to reduce staleness. Nothing in CI verifies them. Treat any reference that
  fails to resolve as this document being stale, not the repository being wrong.
- It restates the names and semantics of existing constants and gates, which
  `dx-standards/README.md` forbids for skill files. It is not a skill file and carries no
  sync path, but the tension is real: if this content outlives the proposal stage, the
  normative parts belong in `dx-standards/` and the rest should be deleted.
- Per `GOVERNANCE.md`, pull requests and their reviews are this repository's decision
  records, and design rationale belongs in the pull request description. A committed file
  is a deliberate exception, made because this document is meant to be reviewed as a unit
  and revised. It should be deleted or promoted once the experiment resolves it.
