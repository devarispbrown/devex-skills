# Step Elimination

The elimination playbook. Apply it to every step before the plan is final. The core question for each step:

**Why does the developer have to do this step at all?**

If the answer is "because the product is built that way", the product change is the fix, not another doc paragraph.

## Eliminations by category

**Defaults over prompts.** Every prompt is a decision, and decisions cost time and attention. The product should have one default that the quickstart uses implicitly. If a flag has one correct value for first success, make it the default.

**`--token` over signup.** A signup flow with email, password, and verification is the most expensive segment in the path. When the product can issue a sandbox or starter token from the CLI, it should. Production signup happens after first success, with the token already understood.

**Seeded fixtures.** Sample data, demo projects, and starter resources created by one command remove entire create-and-configure steps. A fixture must be real enough that the outcome is meaningful, and disposable enough that the developer can discard it.

**Project templates.** A template replaces scaffold-from-blank. `create-<product>-app` that produces a working project beats a blank directory plus five setup instructions.

**Merged command sequences.** Login + create + deploy can often be one command: the CLI authenticates, provisions, and deploys from a template in a single invocation. Merge when the product permits; do not merge when failure isolation matters more than speed.

**No-choice install.** One install mode, one command. Do not make the developer choose between brew, npm, and docker before seeing value.

## Elimination questions per step

For each step in the plan, run this checklist:

1. Does the developer need this step to reach the value outcome? If not, delete it.
2. Could the product do it? Move work into the product or the install command.
3. Could a default or fixture replace it? If yes, design the default or fixture.
4. Could it merge with the previous step? If yes, merge.
5. Is it here because of an edge case? Then it belongs in a troubleshooting note, not the path.

## What survives elimination

A step survives only when it is required for the outcome, cannot be automated, and cannot be defaulted. Survivors are the path.

The surviving count is a target, not an accident: keep interactive commands within `MAGIC_PATH_MAX_COMMANDS`, credentials within `MAGIC_PATH_MAX_CREDENTIALS`, and context switches within `MAGIC_PATH_MAX_CONTEXT_SWITCHES`. If the count is over target, eliminate more or file the product change.

## Recording eliminations

Record what you removed and why in the plan. A removed step that returns later in a different form is a regression; the record makes it visible. A step kept "for completeness" without an elimination answer is a defect.
