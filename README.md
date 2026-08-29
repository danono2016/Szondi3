# Szondi3

Szondi3 is the clean authoritative restart of the Szondi project.

> **First preserve Szondi's doctrine faithfully. Only afterwards formalize what the software may do with that doctrine.**

## Mission first

Before governance, qualification or implementation procedure, read:

1. `docs/PROJECT_MISSION.md` — the clinical purpose, practical priorities, and proportional-rigor rule.

Szondi3 exists to become a real, versatile, trustworthy clinical instrument for psychotherapeutic practice. Governance protects that mission; it does not replace it.

## Current clinical grounding path

For the active P3/P4 and AI-grounding direction, read `docs/CLINICAL_GROUNDING_FOUNDATION.md` after the mission/foundation documents. It records the minimal architecture, anti-dinosaur budget, direct grounding contract and succession instructions for the current clinical workstream.

## Authority

- `Szondi3` is the active authoritative development repository.
- `Szondi2` is predecessor, audit trail and oracle/archive reference only.
- No executable code from `Szondi2` is migrated into active use in `Szondi3`.
- The repository, not a chat transcript, is the durable project memory.

## Architecture

`Primary Sources -> Canonical Access -> Deterministic Test Facts -> Primary Doctrine Registry -> Executable Interpretation Layer -> Clinical Evidence/Graph -> Integration -> Reports`

Doctrine and executable formalization are separate by design. No downstream layer may silently rewrite an upstream layer.

## Start here

After reading `docs/PROJECT_MISSION.md`, read the normative foundation in this order:

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
11. `docs/CLINICAL_GROUNDING_FOUNDATION.md` — current P3/P4 + AI-grounding succession anchor.

## New-chat succession

A new AI conversation does **not** receive write authority merely by reading the handoff.

Before beginning succession procedure, it must first read `docs/PROJECT_MISSION.md` so that qualification and governance remain subordinate to the clinical purpose of the project.

Then, when takeover qualification is actually warranted, use:

1. `docs/CHAT_TRANSFER_PACKAGE.md` — current state and recovery instructions;
2. `docs/CHAT_SUCCESSION_PROTOCOL.md` — READ ONLY cold-start procedure;
3. `docs/CHAT_QUALIFICATION_RUBRIC.md` — deterministic pass/fail and hard-failure rules;
4. `docs/CHAT_QUALIFICATION_REPORT_TEMPLATE.md` — standard takeover report.

For the active clinical-grounding workstream, also re-read `docs/CLINICAL_GROUNDING_FOUNDATION.md` before proposing new RAG, graph, ontology, integration or narrative-model infrastructure.

The successor must not infer write authority from the handoff. Qualification procedures should be applied proportionally to actual succession, uncertainty and risk rather than treated as ceremonial prerequisites to every useful task.

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

See `docs/PROJECT_CHECKPOINT.md` for formal gate state. Do not confuse formal gate completion with the only permissible development path: later clinical prototyping remains allowed where it does not manufacture authority for unfinished upstream layers.
