# Szondi3

Szondi3 is the clean authoritative restart of the Szondi project.

> **First preserve Szondi's doctrine faithfully. Only afterwards formalize what the software may do with that doctrine.**

## Authority

- `Szondi3` is the active authoritative development repository.
- `Szondi2` is predecessor, audit trail and oracle/archive reference only.
- No executable code from `Szondi2` is migrated into active use in `Szondi3`.
- The repository, not a chat transcript, is the durable project memory.

## Architecture

`Primary Sources -> Canonical Access -> Deterministic Test Facts -> Primary Doctrine Registry -> Executable Interpretation Layer -> Clinical Evidence/Graph -> Integration -> Reports`

Doctrine and executable formalization are separate by design. No downstream layer may silently rewrite an upstream layer.

## Start here

Before implementation work, read in this order:

1. `docs/PROJECT_CONSTITUTION.md`
2. `docs/DOCTRINAL_FIDELITY_POLICY.md`
3. `docs/FOUNDATION_ARCHITECTURE.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. `docs/VALIDATION_AND_RECOVERY.md`
6. `docs/PROJECT_CHECKPOINT.md`
7. `docs/RESTART_ROADMAP.md`
8. `docs/MIGRATION_MANIFEST.md`
9. `docs/SOURCE_ASSET_MANIFEST.md`
10. `docs/CANONICAL_ACCESS_SPEC.md`

For continuation in a new conversation, use `docs/CHAT_TRANSFER_PACKAGE.md`.

## Foundation verification

The admitted evidence and required normative foundation are machine-checked by:

```bash
python scripts/verify_foundation.py
```

CI runs the same check read-only. The evidence lock is `config/evidence_lock.json`.

## Migration classes

- `SOURCE_ASSET_TRANSFER`
- `CONSTITUTIONAL_TRANSFER`
- `ORACLE_ONLY`
- `ARCHIVE_ONLY`
- `RE_DERIVE_FROM_SOURCE`

`TRANSFER_AS_IS` is not an allowed category for executable code.

## Current phase

See `docs/PROJECT_CHECKPOINT.md`. Do not infer phase completion from the existence of code or passing tests alone; phase gates require recorded acceptance evidence.
