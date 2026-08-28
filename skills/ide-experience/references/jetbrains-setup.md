# JetBrains Project Setup

## What to commit

Commit:

- `.idea/runConfigurations/*.xml` — run/debug configurations, one file per configuration
- `.idea/codeStyles/` — code style schemes shared by the team
- `.idea/inspectionProfiles/` — inspection profiles shared by the team
- `.editorconfig` — formatting ground truth across editors
- project SDK and language-level defaults when they are team-reproducible
- module `.iml` files only when clean of personal and absolute paths

Do not commit:

- `workspace.xml` — open editors, tool window layout, local state
- local history and cache indexes (`LocalHistory/`, `index/`)
- library and artifact definitions that embed absolute or machine-specific paths
- keymaps, themes, and UI preferences

When in doubt, commit nothing from `.idea/` except `runConfigurations/`, `codeStyles/`, and `inspectionProfiles/`, and let `.gitignore` say so.

## Run configurations

Run configurations live in `.idea/runConfigurations/`, one XML file per configuration. Design rules:

- configuration name matches the canonical script name (dev, build, test, lint)
- working directory is `$PROJECT_DIR$`, never an absolute path
- environment variables are declared in the configuration; secrets are not committed
- before-launch build steps are declared as `<method>` options (e.g., "Run Build Task"), never implied
- Node: reference `package.json` script by name; do not inline a divergent command
- Python: set interpreter, working directory, and env explicitly
- JVM: set the main class or module plus JRE selection; honor the build file's language level

## SDK and toolchain

- commit `jdk.table.xml` only when the project pins a team-standard JDK; otherwise document the required version in the README
- verify the Gradle/Maven wrapper is committed so toolchain discovery is reproducible
- language level and target compatibility come from the build files, not from the IDE default
- virtualenv/conda/uv interpreter paths are per-machine; document how to recreate them

## Verification

- open a clean checkout, run the canonical configuration, and confirm the debugger attaches
- reformat a file and confirm the diff is empty on a clean checkout (committed code style)
- run inspections and confirm the committed profile is active
- confirm each run configuration matches the commands declared in Makefile or package.json
