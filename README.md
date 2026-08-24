# Szondi3

Szondi3 is the clean authoritative restart of the Szondi project.

> **First preserve Szondi's doctrine faithfully. Only afterwards formalize what the software may do with that doctrine.**

## Authority

- `Szondi3` is the active authoritative development repository.
- `Szondi2` is predecessor, audit trail and oracle/archive reference only.
- No executable code from `Szondi2` is migrated into active use in `Szondi3`.

## Architecture

`Primary Sources -> Primary Doctrine Registry -> Executable Interpretation Layer -> Clinical Evidence/Graph -> Integration -> Reports`

Doctrine and executable formalization are separate by design.

## Migration classes

- `SOURCE_ASSET_TRANSFER`
- `CONSTITUTIONAL_TRANSFER`
- `ORACLE_ONLY`
- `ARCHIVE_ONLY`
- `RE_DERIVE_FROM_SOURCE`

`TRANSFER_AS_IS` is not an allowed category for executable code.

Read `docs/PROJECT_CONSTITUTION.md`, `docs/DOCTRINAL_FIDELITY_POLICY.md`, `docs/MIGRATION_MANIFEST.md` and `docs/SOURCE_ASSET_MANIFEST.md` before adding implementation code.
