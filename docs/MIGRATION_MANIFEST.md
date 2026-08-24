# SZONDI3 — MIGRATION MANIFEST

**Status:** AUTHORITATIVE MIGRATION CONTROL  
**Restart mode:** TOTAL SOFTWARE RESTART / EVIDENCE PRESERVATION

## Purpose

Szondi3 is not a copy, forked implementation, or cleaned continuation of Szondi2.

Szondi3 restarts the software architecture and executable logic from zero while preserving the documentary evidence and project lessons needed to avoid repeating earlier mistakes.

## Fundamental rule

> **No executable code from Szondi2 becomes executable code in Szondi3 by migration.**

Existing Szondi2 code may be inspected as historical evidence or as a behavioral oracle during revalidation, but implementation in Szondi3 must be reconstructed from authorized sources and newly specified invariants.

Passing tests in Szondi2 is not sufficient authority for reuse.

## What may enter Szondi3 directly

Only the following classes of material are candidates for direct transfer:

### 1. Primary source originals
- original Szondi PDFs;
- ABBYY/OCR DOCX source files used for deterministic text access;
- authorized Deri/Mélon source originals, clearly separated from Szondi-primary material.

These are documentary sources, not software inheritance.

### 2. Stimulus image assets
- the 48 test photographs/images required for administration;
- only the minimal mapping necessary for administration/scoring may later be reconstructed: stable card identity, series/position, factor, image.

Historical photograph-person metadata remains Help-only and must not enter runtime.

### 3. Constitutional project documents
- `PROJECT_CONSTITUTION.md`;
- `DOCTRINAL_FIDELITY_POLICY.md`;
- this migration manifest;
- later source-authority and evidence policies created specifically for Szondi3.

These are rules learned from the audit, not inherited implementation.

## What must NOT be transferred as active implementation

The following Szondi2 material is `ARCHIVE_ONLY` for Szondi3:

- all Java production code;
- all Java tests;
- KnowledgeClaim/KnowledgeRegistry implementations;
- all existing interpretive claims and guardrails;
- all trigger expressions;
- Clinical Graph drafts or report architecture code if any;
- legacy and current runtime CSV schemas;
- generated `project-state.json`;
- CI workflows;
- corpus exporter/verifier scripts;
- old roadmaps and architecture documents;
- legacy extraction scripts and 405-chunk reading ledger;
- any auto-generated canonical derivative whose reproducibility has not yet been independently re-established in Szondi3.

These materials remain available in Szondi2 for comparison, provenance, forensic audit and regression investigation only.

## Reuse of knowledge vs reuse of code

An idea discovered in Szondi2 may be used only by re-deriving it from its authorized source.

Example:
- Szondi2 contains a reaction-scoring table implementation.
- Szondi3 does not copy the implementation.
- Szondi3 re-reads the primary source table, specifies the formal rule, writes new tests from source examples/invariants, and then writes new implementation.
- Szondi2 may be compared afterwards as a secondary oracle; disagreement triggers investigation, not automatic deference.

## Migration decision classes

For documentary purposes every predecessor component may be classified as:

- `SOURCE_ASSET_TRANSFER` — original source or stimulus asset copied with identity verification;
- `CONSTITUTIONAL_TRANSFER` — a project rule intentionally retained after explicit review;
- `ORACLE_ONLY` — predecessor code/data usable only for comparison;
- `ARCHIVE_ONLY` — retained solely in Szondi2 and not used operationally;
- `RE_DERIVE_FROM_SOURCE` — concept known from Szondi2 but required to be reconstructed independently from canonical source evidence.

`TRANSFER_AS_IS` is deliberately not an allowed category for executable code.

## Required record for every transferred file

For every file actually copied into Szondi3, record:

- destination path;
- source repository/path;
- source commit or blob identity;
- classification from the list above;
- SHA-256 or equivalent identity when applicable;
- reason for transfer;
- verification performed;
- date/commit of admission into Szondi3.

## Initial admission plan

### Admit first
1. constitutional documents;
2. primary-source originals and their immutable identity manifest;
3. stimulus images and minimal asset identity manifest.

### Rebuild next
4. canonical text extraction and verification pipeline from zero;
5. deterministic administration model;
6. deterministic reaction scoring;
7. profiles/vectors;
8. repeated series and formal procedures;
9. only after P1 is independently validated: Primary Doctrine Registry;
10. only after Doctrine Registry exists: Executable Interpretation Layer.

## No hidden migration

Copy/paste from Szondi2 implementation is prohibited even if renamed or refactored.

If predecessor behavior materially influences a new Szondi3 rule, that influence must be documented as `ORACLE_ONLY` and the source-derived justification must still stand independently.

## Why this restart exists

The Szondi2 audit showed that a system can be computationally precise while still embedding:

- inherited assumptions;
- doctrinal omissions;
- contemporary neutralizations;
- overly broad anti-inferences;
- claims mixing doctrine and executability;
- legacy infrastructure with competing notions of authority.

Szondi3 eliminates these inheritance channels by making source re-derivation mandatory.

## Final migration rule

> **Preserve evidence, not implementation. Preserve lessons, not patches. Re-derive executable behavior from source.**
