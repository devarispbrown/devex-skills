# External checker audit, 2026-09-03

The suite's checkers had never been run against a codebase the author does not own.
Fifteen public repositories were audited across six ecosystems: Rust, Go, JavaScript,
Python, Ruby and C.

`astral-sh/uv`, `tinygrad/tinygrad`, `simonw/llm`, `BurntSushi/ripgrep`, `spf13/cobra`,
`sindresorhus/got`, `psf/black`, `sinatra/sinatra`, `clap-rs/clap`,
`charmbracelet/bubbletea`, `jqlang/jq`, `expressjs/express`, `rust-lang/mdBook`,
`tokio-rs/axum`, `simdjson/simdjson`.

780 checker invocations.

## What held up

No checker that takes a repository root crashed on any of the fifteen. Across six
ecosystems and repository sizes from a few megabytes to fifty, the repo-root checkers
are robust. That is worth stating because it was not knowable before.

## What did not

**Seven scripts emitted a raw traceback when handed a directory instead of a file.**
`agent_trial_driver.py`, `agent_trial_scorer.py`, `estimate_architecture_path.py`,
`check_terminology.py`, `magic_path_runner.py`, `journey_runner.py` and
`cluster_feedback.py` all failed with `IsADirectoryError` and a stack trace.

Passing a repository root to a checker is the most obvious mistake a first-time user
makes. The suite ships `error-experience`, whose standard requires an expected error to
say what happened, why, where, and how to fix it, and whose `UNEXPLAINED_ERROR` gate is
P1. Seven of the suite's own scripts failed that gate on the most predictable input error
there is.

Fixed: each now names the file, says a file was expected rather than a directory, and
says what kind of file. Missing files and malformed JSON are handled the same way.

## Signal quality, reported not fixed

Four checklist items were reported as gaps on **all fifteen** repositories:
`CODEOWNERS`, `SUPPORT.md`, `GOVERNANCE.md` and `MAINTAINERS.md`, plus a maintainer
ladder.

These fifteen include some of the most successful developer tools in their ecosystems.
A checklist item that every one of them fails is not measuring a gap. It is encoding one
governance style as a universal requirement.

This is not filed as a bug because the scripts label their output an informational
inventory rather than a verdict, which is the correct pattern and matches
`guessability_check.py`. But a report whose first four lines are items that ripgrep,
express and black all "fail" spends the reader's attention before reaching anything
specific to their project. Worth revisiting when community scoring is next touched.

## Note on method

This audit cost no metered agent sessions. It is fifteen shallow clones and 780
subprocess calls, and it found more defects per unit effort than the thirty-session agent
trial did.
