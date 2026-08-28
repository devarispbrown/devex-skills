# Environment Configuration

## Discovery

Find every environment variable the code reads before designing anything:

- grep for `os.getenv`, `process.env`, `getenv`, `environ`, and config loaders across source, config, and CI files
- check CI workflow files: they encode the exact set production expects
- check the config loader (dotenv, `config`, framework settings) for defaults and precedence

Never write `.env.example` from memory. The code is the source of truth.

## `.env.example` as contract

`.env.example` is the canonical list of variables, and it is a contract:

- one entry per variable the code reads, in the order code or config expects
- safe development defaults inline, so the app boots with a copy of `.env.example` alone
- a comment for every non-obvious value: what it is, what breaks without it
- no real secrets, no personal tokens, no machine-specific values

Verify: copy `.env.example` to `.env` in a fresh clone and the dev target boots.

## Safe local secrets

- Real values live in gitignored files (`.env`, `.env.local`) or a local secret store; `.env.example` never contains them.
- Provide a documented way to obtain real values (local generation, a one-time setup command, or a secret manager) — never a shared doc with plaintext passwords.
- Prefer dev-only defaults that need no secret at all (local auth, seeded tokens, self-signed certs).
- Check that `.gitignore` covers every local env file variant before committing anything.

## Precedence

- Document and use the framework's canonical precedence. The common shape is code defaults < `.env` < `.env.local` < process environment, but verify per stack.
- Do not invent a load order that contradicts the framework, and do not let two loaders disagree.
- Never read the same variable two different ways in different parts of the app.

## Failure modes

- **Missing variable:** fail at startup with the variable name and its role, or fall back to an explicitly safe default. Never a silent wrong value.
- **Wrong value:** validate format early (URL, port, boolean) and name the invalid variable.
- **Case drift:** `DATABASE_URL` vs `database_url` — pick canonical casing, enforce it, and document that env vars are case-sensitive.
- **Stale `.env`:** a committed `.env.example` change must come with a detection path — a startup diff check or a setup step that compares the local `.env` against the example.
