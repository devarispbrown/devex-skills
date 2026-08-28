# Destructive Operations

Destructive means delete, drop, purge, wipe, reset, overwrite, or anything irreversible or wide-blast-radius.

## Confirmation design

1. Interactive mode asks for explicit confirmation before acting.
2. The prompt states exactly what will be destroyed and in what scope.
3. For high blast radius, require typing the target name, not a bare "yes".
4. Re-prompt when the confirmation is stale.
5. Ctrl-C cancels with no partial destruction.

## Force and yes flags

1. Automation bypasses confirmation only via an explicit `--force` or `--yes`.
2. Never bypass on implicit signals: non-TTY stdin, an env var, verbose output, or config presence.
3. `--force` and `--yes` are documented in help with the destruction they permit.
4. A command that can destroy is never destructive by default in automation.

## Dry-run mode

1. Provide `--dry-run` whenever a change can be previewed.
2. Dry-run prints the exact actions a real run would take, with no side effects.
3. Dry-run exits 0 when the plan is valid; the plan is the output.

## Reversibility reporting

1. State in help and output what is lost, what survives, and how to verify.
2. Offer backup or snapshot where data can be lost; name the mechanism.
3. Report what happened: counts of items destroyed, skipped, and failed.

## Guardrails

1. Blast radius scales friction: deleting one item asks once; deleting many or all asks harder.
2. Scope selectors are validated before any destruction begins.
3. Confirmation happens before the first destructive action, never after half the work.
4. Recovery instructions are part of the error path.

## Verify

- interactive delete confirms; automation delete requires an explicit flag
- dry-run changes nothing and prints a plan
- output states exactly what was destroyed
- no path destroys without either confirmation or an explicit automation flag
