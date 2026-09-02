# Agent Trial Protocol

The operator procedure for the attribution trial described in `AGENT-DX-PROPOSAL.md`
§ The experiment, and for producing a trial log that `scripts/agent_trial_scorer.py`
can score.

That proposal is the authority. Where this file and the proposal disagree, the proposal
is correct and this file is stale.

## Scope: an operator procedure, never CI

The trial is run by a person, on their own machine and their own metered account. No
part of it runs in continuous integration.

- Scripts in this repository are stdlib-only and offline. `.github/workflows/ci.yml`
  compiles every script under `skills/*/scripts/` and runs `scripts/smoke_skills.py`,
  which asserts deterministic exit codes against committed fixtures. A script that
  needs a model endpoint fails both properties.
- GitHub withholds repository secrets from `pull_request` runs on forks, so a keyed
  runner could never gate a contributor pull request. It would pass for maintainers and
  error for everyone else.
- Execution is an operator activity exactly as magic-path timing already is:
  `developer-docs-auditor/scripts/magic_path_runner.py` prints the manifest and exits
  unless the operator passes `--execute`.

The split follows from this. A live driver executes agents and writes a trial log. The
offline scorer consumes that log and emits counts, distributions, and a verdict
deterministically. Only the scorer belongs in CI, exercised by fixture trial logs under
`assets/` wired into `assets/smoke.json`, per the convention in `CONTRIBUTING.md`.

## Pre-registration

Fix these fields and publish them in the pull request that adds the trial, before the
first run:

- repository count and the repositories themselves, named
- every task prompt, verbatim, with a stable id
- model, checkpoint, and temperature
- harness and tool set
- codebook version
- the coverage corpus, enumerated

A trial scored without a complete registration is not evidence. The scorer refuses such
a log rather than reporting a weaker result: every registration field is required, and
an empty value is treated as a missing one.

Pre-registration is the only control on prompt authorship, which dominates agent
outcome. It does not eliminate the threat. It makes the prompts inspectable by a
reviewer before the outcome is known.

## The coverage corpus

Coverage is decided against an enumerated corpus, registered in advance. A failure mode
is covered when a named corpus entry already fails a product that exhibits it.

- `dx-standards/release-gates.md` § Gate identifiers: the nine gate constants,
  `BROKEN_QUICKSTART` through `BROKEN_CANONICAL_INSTALL`.
- `dx-standards/community.md` § Community hard gates: the community gate constants,
  which use the same severity levels and verdict vocabulary.
- `dx-standards/metrics.md`: the named threshold constants, including
  `MAGIC_PATH_MAX_CREDENTIALS` under § Magic path thresholds, `LOCAL_DEV_MAX_MIN` under
  § Local development thresholds, and `TTR_TARGET_MIN` under § Recovery thresholds.
- Named skill-level contracts. The worked examples are `cli-designer`
  § Destructiveness contract and `web-console-dx` § Automation parity contract. The
  registration lists each contract by skill and heading in the pull request body; the
  trial log carries the single token `skill-contracts` for the group.

Scoping coverage to the nine gate constants alone biases the result toward proceeding.
It would score as uncovered every failure the suite already credits to
`MAGIC_PATH_MAX_CREDENTIALS` or to automation parity, including the case the proposal
names explicitly: dashboard-only credential creation, which the literal text of
`BROKEN_QUICKSTART` does not catch and which those two entries do. A corpus that omits
what the suite actually enforces manufactures the gap it is meant to test for.

The corpus is fixed at registration. An entry added after the first run is a new
registration and a new trial.

## The classification codebook

The codebook decides what counts as one distinct failure mode. `u` is a ratio over a
count of modes, so the codebook sets the denominator and is the most attackable part of
the design. State the rules, version them, and publish worked examples.

**Granularity.** A failure mode is a defect mechanism on a product surface, stated at
the level of the single product change that removes it. If one change removes every
observation in a group, the group is one mode.

**Product independence.** The same mechanism observed in two repositories is one mode.
Repository identity lives in `runs`, not in the mode.

**Occurrences never move `u`.** `u` is computed over distinct modes. The `occurrences`
field is reporting only. A mode observed once counts exactly as much as a mode observed
nine times, and modes are never filtered by frequency.

**Mechanism, not symptom.** Classify by what the product did, not by what the agent
said about it. Two agents narrating the same defect differently are one observation of
one mode.

**Near-duplicates.** The same mechanism on two commands in the same product is one
mode with two occurrences. Splitting near-duplicates inflates the denominator, which
drags `u` toward whatever the duplicated pair already is. Merging distinct mechanisms
does the reverse. When a split is genuinely arguable, record both readings in the pull
request and take the one the codebook's granularity rule dictates.

**Two surfaces.** When a failure spans two surfaces, assign it to the surface where the
product change lands. When a change on either surface would independently remove it,
assign it to the surface named by the corpus entry that catches it. When no corpus
entry catches it, assign it to the surface where the agent first lost the thread and
say so in the mode summary, because that mode is a candidate for the uncovered set and
its attribution must be auditable.

### Worked example: one mode

- Transcript A: `widget db migrate` stops at `Apply 3 migrations? [y/N]` and the session
  times out.
- Transcript B: `widget project init` stops at an interactive template picker.

One mode. Both are an interactive prompt with no non-interactive equivalent, both are
removed by the same product change class, and both are caught by the same corpus entry,
`agent-native-dx` § Automation-safety contract. Record it once with `occurrences` 2.

### Worked example: two modes

- Transcript C: `widget deploy` fails, prints a stack trace, and exits 0. The agent
  reads success and continues onto a broken deployment.
- Transcript D: `widget deploy` fails, prints `Error: could not complete request`, and
  exits 1 with no error code, no cause, and no remediation.

Two modes. The narrative symptom is the same, "the agent could not tell what to do
after a failed deploy", but the mechanisms differ, the product changes differ, and the
corpus entries differ: C is caught by `cli-designer` § Exit-code contract, D by
`UNEXPLAINED_ERROR`. Merging them would hide one of the two fixes.

### Versioning

The codebook version goes in `registration.codebook_version`. Changing the codebook
mid-trial voids the trial: the modes classified before the change and the modes
classified after are counted under different rules, and their ratio means nothing. A
codebook change is a new version, a new registration, and a re-run.

## Second rater

A second rater independently classifies a 20% sample of the failure observations, using
the registered codebook and without seeing the first rater's assignments. The
disagreement rate is published with the result and is printed by the scorer.

What this controls for: codebook ambiguity. A codebook that two people apply
differently does not support a count, and the disagreement rate is the measurement of
that.

What it does not control for, stated plainly:

- Stripping repository identity from transcripts is not blinding. Transcripts carry the
  product's own commands, flag names, and error strings, so the rater knows which
  product they are reading.
- Neither rater is blind to the hypothesis. That is not achievable with one operator.
- A single operator who writes the task prompts, sets mode granularity, and judges
  coverage is the same auditor-sets-the-score defect the proposal rejects when it
  withdraws `AGENT_RECOVERY_RATE`. Pre-registration, the enumerated corpus, and the
  second rater narrow that defect. They do not remove it, and the trial should not be
  reported as though they did.

## Problem-class attribution is reporting only

Every mode is also attributed to one of the nine problem classes in
`dx-standards/terminology.md` § Problem classification, by root cause. That attribution
never decides coverage.

The nine classes are exhaustive by construction: every mode lands in one of them.
Treating a successful classification as coverage would drive `u` to zero mechanically
and the trial would return "already covered" no matter what the agents did. Coverage is
decided only against the registered corpus, through `covered_by`.

## The trial log

The operator writes one JSON file per trial. The scorer consumes it and executes
nothing.

```json
{
  "schema": "agent-trial-log/v1",
  "registration": {
    "registered_at": "2026-03-04",
    "registration_url": "https://github.com/devarispbrown/devex-skills/pull/41",
    "repositories": ["acme-cloud/widget-cli", "acme-cloud/widget-sdk-python"],
    "task_prompts": [
      {"id": "t1", "prompt": "From a clean clone, build the project and run the full test suite. Report the command you used and its exit code."},
      {"id": "t2", "prompt": "Deploy the sample application to a sandbox environment and verify it responds. Do not ask the user for input."}
    ],
    "model": "claude-opus-4-6",
    "checkpoint": "2026-02-11",
    "temperature": 0,
    "harness": "claude-code 2.4.1",
    "tool_set": ["bash", "read", "edit", "web_fetch"],
    "codebook_version": "codebook-1.0",
    "coverage_corpus": [
      "release-gates.md#gate-identifiers",
      "community.md#gates",
      "metrics.md#thresholds",
      "skill-contracts"
    ]
  },
  "runs": [
    {"repository": "acme-cloud/widget-cli", "task": "t1", "n": 5, "outcomes": ["pass", "fail", "fail", "pass", "fail"]},
    {"repository": "acme-cloud/widget-cli", "task": "t2", "n": 5, "outcomes": ["fail", "fail", "fail", "fail", "fail"]},
    {"repository": "acme-cloud/widget-sdk-python", "task": "t1", "n": 5, "outcomes": ["pass", "pass", "pass", "pass", "pass"]}
  ],
  "failure_modes": [
    {"id": "fm-01", "summary": "Quickstart requires a credential created only in the web console", "covered_by": "MAGIC_PATH_MAX_CREDENTIALS", "problem_class": "Product", "occurrences": 4},
    {"id": "fm-02", "summary": "widget deploy exits 0 after a failed deploy", "covered_by": "cli-designer#exit-code-contract", "problem_class": "CLI", "occurrences": 3},
    {"id": "fm-03", "summary": "Tool description states a default the tool does not apply, so the agent omits a required argument", "covered_by": null, "problem_class": "Product", "occurrences": 3}
  ],
  "second_rater": {"sample_fraction": 0.2, "sampled": 4, "disagreements": 1}
}
```

Field notes:

- `runs[].outcomes` has exactly `n` entries, in execution order, one per session.
- `covered_by` names the single corpus entry that catches the mode, or `null` when
  nothing in the registered corpus does. `null` is what makes a mode count toward `u`.
  An empty string is treated the same as `null` by the scorer, but write `null`.
- `problem_class` is one of the nine in `terminology.md` § Problem classification. It is
  reported and never scored.
- `second_rater.sampled` is the count of failure observations re-classified, drawn from
  the pool of observations, so `sampled` is `sample_fraction` of that pool.
  `disagreements` is the count on which the two raters assigned different modes.
- Every outcome in the log is Observed evidence under `metrics.md` § Evidence labels: a
  session actually executed the path.

The example above is abridged. A real log lists every registered repository, every task
prompt, every run, and every observed mode.

## Decision rule

Fixed before the first run. Let `u` be the share of distinct failure modes the
registered coverage corpus does not catch.

The trial does not report `u` unless it observes at least 15 distinct failure modes.
Below that, the task set is re-scoped and re-run. At small mode counts the attainable
values of `u` are too coarse to sit inside the bands.

Bands, inclusive at the edges:

- `u <= 0.20`: proceed-no. Agent DX is the existing standards with the slack removed.
  Ship tightening edits to existing skills, and nothing new. Publish the negative
  result.
- `u >= 0.40`: the gap is real, and the classification is itself the list of what is
  missing. The conditional skill section in `AGENT-DX-PROPOSAL.md` § Skills: one, not
  six unlocks.
- `0.20 < u < 0.40`: inconclusive. One re-run at 2N against the same registration. If
  still inconclusive, withdraw the proposal.
- Zero failures observed: treated as `u <= 0.20`. Training-set contamination makes clean
  runs on popular repositories plausible, and a trial that surfaces no failures is
  evidence of nothing that warrants new surface area.

The thresholds 0.20 and 0.40 have no derivation. They are underived conventions chosen
before seeing data, and their only virtue is being fixed in advance.

The failure-mode inventory is a deliverable under every branch, including withdrawal.

## Threats to validity

None of these is fully resolvable. Publish them with the result.

- **Training-set contamination.** Public repositories are the ones most likely
  memorized, which inflates agent success independently of agent affordances and
  correlates with popularity, which correlates with documentation quality. State it as a
  scope limit.
- **Prompt authorship.** Task prompts dominate agent outcome and are written by the
  experimenter. Pre-registration mitigates this and does not eliminate it.
- **Model and harness.** Held fixed and declared, which makes the result a statement
  about one configuration rather than about agents in general. A model upgrade does not
  invalidate the failure-mode inventory, but it does invalidate any claim about rates.
- **Classifier bias.** Mitigated by the codebook and the second rater, not by blinding,
  which one operator cannot achieve.

## Cost

One trial is N >= 5 autonomous agent sessions per repository per task prompt, plus the
classification round and the second rater. The 8-repository matrix in the proposal is 40
or more sessions at one task prompt each, more with a task set per repository. That is a
metered bill and several operator days.

Two branches raise the bill after the fact: fewer than 15 distinct modes forces a
re-scope and a full re-run, and the inconclusive band forces one re-run at 2N.

The operator running the trial pays it. A suite that ships `developer-economics` states
its own cost envelope before asking anyone else to spend theirs.
