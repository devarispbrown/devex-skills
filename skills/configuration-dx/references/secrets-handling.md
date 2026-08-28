# Secrets Handling

A secret is any value whose disclosure harms the product or its users: passwords, API keys, tokens, credentials, private keys, connection strings with credentials. Config handling decides whether secrets stay secret.

## Secrets in config vs secret stores

- **Allowed for secrets:** environment variables injected by the platform or CI, and secret stores (Vault, cloud secret managers, CI secret registries).
- **Never allowed:** committed config files, code defaults, flags with default values, example files with real values, `.env` committed to the repository.

A committed secret is a leak the moment it exists, regardless of rotation plans. Treat it as a P0/P1 finding per the canonical severity vocabulary.

A secret in a config file that is not committed may still be a finding: any file that is easy to commit, diff, or share (logs, dumps, screenshots) is a leak waiting to happen.

## .env discipline

- `.env` files are local and gitignored; verify the ignore rule exists.
- Commit `.env.example` or `.env.template` with placeholder values only (`API_KEY=your-key-here`, never a real or sample key).
- Load `.env` only in local development, not in production paths.
- Never document real values as examples in READMEs or issues.

## Redaction in logs and errors

- Logs, stack traces, and error messages never contain secret values.
- Startup banners and debug output that echo the resolved config redact secret-pattern keys by default.
- Config introspection (a `config explain`-style command, config dumps) redacts values of secret-pattern keys.
- Diff output and audit reports redact values too; never paste a secret into a finding.

Verify redaction by exercising the path that prints config, not by reading the code once.

## Rotation implications

Rotation is the test of secret handling. Ask: if this secret is compromised, what must change?

- A secret readable from one place (environment) rotates in one step.
- A secret duplicated across config files, flags, defaults, and docs rotates in many steps and is forgotten somewhere — that is the duplication cost, in concrete terms.
- Any config value that looks like a rotated secret (old tokens in files, versioned config with embedded keys) is evidence the model leaks secrets into the wrong layer.

Recommend: secrets reach the process through exactly one channel, and every other mechanism that references them does so by reference, never by value.
