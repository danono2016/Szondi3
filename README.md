# Szondi3

Szondi3 is the clean authoritative restart of the Szondi project.

> **First preserve Szondi's doctrine faithfully. Only afterwards formalize what the software may do with that doctrine.**

## Mission

Read `docs/PROJECT_MISSION.md` for the clinical purpose, practical priorities and proportional-rigor rule.

Szondi3 exists to become a real, versatile, trustworthy clinical instrument for psychotherapeutic practice. Governance protects that mission; it does not replace it.

## Authority

- `Szondi3` is the active authoritative development repository.
- `Szondi2` is predecessor, audit trail and oracle/archive reference only.
- No executable code from `Szondi2` is migrated into active use in `Szondi3`.
- The repository, not a chat transcript or handoff document, is the durable project record.

## Architecture

`Primary Sources -> Canonical Access -> Deterministic Test Facts -> Primary Doctrine Registry -> Executable Interpretation Layer -> Clinical Evidence/Graph -> Integration -> Reports`

Doctrine and executable formalization are separate by design. No downstream layer may silently rewrite an upstream layer.

## Stable foundation

Read only the documents relevant to the task. The core normative set is:

1. `docs/PROJECT_MISSION.md`
2. `docs/PROJECT_CONSTITUTION.md`
3. `docs/DOCTRINAL_FIDELITY_POLICY.md`
4. `docs/SOURCE_AUTHORITY_POLICY.md`
5. `docs/FOUNDATION_ARCHITECTURE.md`
6. `docs/DEVELOPMENT_GOVERNANCE.md`
7. `docs/VALIDATION_AND_RECOVERY.md`
8. `docs/CANONICAL_ACCESS_SPEC.md`
9. `docs/P2A_PRIMARY_DOCTRINE_SPEC.md`
10. `docs/P2B_EXECUTABLE_CLAIM_DATA_CONTRACT.md`

`docs/PROJECT_STATE.md` is the concise mutable operational summary. It never outranks live branch state, Git history, source/provenance records, code or CI.

There is no chat succession protocol. Do not create mandatory handoff packages, chat qualification procedures or conversational checkpoints.

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

## Current development state

For the live frontier and immediate next action, see `docs/PROJECT_STATE.md`, then verify the current branch HEAD and CI before writing.
