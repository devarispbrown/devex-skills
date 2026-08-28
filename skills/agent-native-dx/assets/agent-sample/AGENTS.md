# AGENTS.md

## Build

```sh
python3 -m pip install -e .
```

## Test

Run the suite:

```sh
python3 -m pytest
```

Run a single test:

```sh
python3 -m pytest tests/test_core.py
```

## Run

```sh
python3 -m app.cli run <path>
```

## Verify

`python3 -m pytest` must pass before proposing changes.

## Invariants

- `app.core.parse` never raises; invalid input returns a `ParseError` result object.
- Commands never prompt; every operation has a non-interactive form.
