# Services and Infrastructure

## Kinds of backing services

Databases, caches, queues, object storage, search, auth providers, and third-party APIs — anything the app needs before the dev loop can run.

## Emulators vs real services

Prefer the local option that most faithfully reproduces the production interface:

- **Containers:** `docker compose` services for postgres, redis, rabbitmq, minio, and similar. One command brings up the full set.
- **Emulators:** localstack (AWS), testcontainers (managed lifecycles), cloud emulators for GCP/Azure, mailcatcher for SMTP. Good when the real service is proprietary, heavy, or requires remote accounts.
- **Local processes:** sqlite, mailpit, or dev-only binaries when the stack is light enough.

Do not default the dev loop to a shared staging or remote sandbox: it couples every developer's productivity to a shared environment and a network.

## When a real service is required

Use the real service or its official emulator when:

- the emulator observably diverges from production behavior that matters to the dev loop
- the app depends on proprietary behavior (auth flows, provider-specific APIs)
- the team ships integration work daily and needs fidelity

When a real service is required, it must still be reachable through a documented one-command path or a single documented credential, and it must never require access to production data.

## Seeded fixtures

- Commit fixtures as code (SQL dumps, JSON/CSV, factories) and apply them with a `seed` step after migrate.
- Make the fixture set minimal but realistic: enough rows that queries, pagination, and the UI look real.
- Never depend on fixtures that live on a developer's machine or in a shared database.

## Test credentials

- Generate credentials locally at setup time (self-signed certs, local auth keys, dev tokens) or use documented well-known dev values that only work in dev.
- Never commit real credentials, production keys, or personal tokens. Rotate immediately if one leaks.

## One-command bring-up

Verify:

- one command starts every service (`make services` or `docker compose up -d`)
- each service has a healthcheck or readiness probe
- the dev target waits for ready services before starting the app
- teardown is also one command and leaves nothing running

## Failure modes

- **Port conflicts:** detect and report the owning process; prefer documented alternate ports.
- **Missing images:** pull happens during setup; a registry outage must surface clearly, not as a generic connect error.
- **Empty databases:** the migrate-plus-seed chain must be part of setup, never a manual reminder.
