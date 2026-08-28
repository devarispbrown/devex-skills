# Ref App Sample

A complete stub reference application: a stdlib-only HTTP service that answers
token-gated health and echo requests. It demonstrates the reference-application
shape on one small tree. All code is wiring-level; production behavior is
emulated, not shipped.

## Run

    python3 -m app.main

The server listens on 127.0.0.1:8000 (see `app/config.py`).

## Verify

    python3 -m unittest

## What the tree demonstrates

- auth: token-gated routes that fail closed (`app/auth.py`)
- config: environment-driven settings with safe defaults (`app/config.py`)
- errors: typed errors with status codes (`app/errors.py`)
- retries: bounded backoff helper (`app/retries.py`)
- observability: logging and metrics export setup (`app/observability.py`)
- tests: unit tests covering failure paths (`tests/test_app.py`)
- deployment: container and Kubernetes artifacts (`deploy/`)
- security: secret handling and safe defaults (`app/security.py`)

One of the nine mandatory concerns from the production-readiness checklist is
intentionally absent. Run the checker to find it:

    python3 skills/reference-application-engineer/scripts/check_reference_app.py skills/reference-application-engineer/assets/ref-app-sample

This fixture is the negative case for the checker: eight concerns present, one
missing, exit code 1 naming the gap.
