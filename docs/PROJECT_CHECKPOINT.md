# SZONDI3 — PROJECT CHECKPOINT

**Checkpoint date:** 2026-08-24  
**Repository:** `danono2016/Szondi3`  
**Authoritative branch:** `main`  
**Foundation work branch at this checkpoint:** `work/foundation-and-handoff`  
**Current phase:** `P0 — Constitution + Sources`  
**P0 overall gate:** `IN_PROGRESS`

## 1. What is already authoritative

The following documents define the project and must be read before implementation work:

1. `docs/PROJECT_CONSTITUTION.md`
2. `docs/DOCTRINAL_FIDELITY_POLICY.md`
3. `docs/FOUNDATION_ARCHITECTURE.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. `docs/VALIDATION_AND_RECOVERY.md`
6. `docs/MIGRATION_MANIFEST.md`
7. `docs/RESTART_ROADMAP.md`
8. `docs/SOURCE_ASSET_MANIFEST.md`
9. `docs/CANONICAL_ACCESS_SPEC.md`

The foundation documents on the current work branch are intended to become normative after review/merge.

## 2. Evidence already admitted and verified

Szondi3 contains exactly:

- 10 admitted DOCX source files;
- 8 admitted visual-arbitration PDF files;
- 48 admitted WebP stimulus images.

Binary transfer was verified byte-for-byte against predecessor evidence using Git identities/hashes. The 48-image set matches the immutable predecessor tree identity. No predecessor Java implementation, runtime CSV, generated canonical TXT, old project state or legacy extraction scripts were admitted as authority.

See `docs/ASSET_ADMISSION_VERIFICATION.md` and `docs/SOURCE_ASSET_MANIFEST.md`.

## 3. Source layers

Primary Szondi doctrine consists of the eight `SZ_*` source entries in `config/source_catalog.json`.

`DERI_1949` and `MELON_1975` are separate `POST_SZONDI_TRADITION` layers and may supplement but never silently overwrite Szondi-primary doctrine.

## 4. Stimulus status

The 48 image binaries are admitted and identity-verified.

The predecessor series/position/factor mapping is recorded in `docs/STIMULUS_MAPPING_MANIFEST.md` as evidence only. It is **not yet runtime authority** and must be revalidated against authorized primary source material before P1 administration code is implemented.

Historical metadata about photographed persons is permanently excluded from runtime interpretation and reports.

## 5. Canonical access status

Generated canonical TXT from Szondi2 was deliberately not imported.

Szondi3 has a new `docs/CANONICAL_ACCESS_SPEC.md` and a new source catalog. A source-structure inspector was written from zero and run in read-only CI.

PR #1 (`P0 canonical source inspection gate`) passed its workflow and was merged into `main` as commit `25abe9ac2adb149b40239a2562ab6f056b30f426`.

Workflow run `32763754908` completed `SUCCESS` and produced artifact `p0-docx-inspection`, digest:

`sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`

The inspection confirmed that the DOCX corpus is structurally complex: many tables, footnote references, fields, drawings and hundreds of header/footer story parts. A simple paragraph dump would be unsafe. See `docs/P0_SOURCE_INSPECTION_REPORT.md`.

## 6. What has NOT yet been done

Do not assume any of the following are complete:

- canonical extractor implementation;
- canonical derivative generation;
- deterministic canonical regeneration proof;
- comparison of new canonical hashes with Szondi2 witness hashes;
- primary-source revalidation of the 48-card factor mapping;
- P1 deterministic administration/scoring engine;
- Doctrine Registry;
- executable interpretations;
- Clinical Graph;
- integration/reporting engine.

No clinical interpretation implementation is authorized yet.

## 7. Immediate next safe work

The next task is **not** to write broad interpretation code. The next safe task is to harden the canonical-access design using the structural inspection evidence, then implement the extractor from that specification.

Recommended order:

1. refine `CANONICAL_ACCESS_SPEC.md` with explicit handling for body tables, notes, header/footer repetition, fields, drawings/visual markers and unknown OOXML;
2. write source-structure-focused tests/fixtures from admitted documents without copying Szondi2 exporter behavior;
3. implement new deterministic extractor;
4. run twice from clean inputs and prove deterministic identity;
5. inventory new canonical output hashes;
6. only then compare against Szondi2 canonical witness hashes;
7. investigate every difference before accepting P0 canonical access;
8. separately revalidate stimulus mapping from primary sources.

## 8. Hard prohibitions for the next chat/developer

Do not:

- copy Szondi2 Java or exporter code;
- import old canonical TXT as authority;
- treat predecessor tests as source truth;
- skip tables/notes/unknown OOXML silently;
- normalize source terminology to contemporary psychology;
- mix Deri/Mélon into Szondi-primary doctrine;
- use photographed-person historical metadata in runtime;
- begin interpretation because scoring seems obvious;
- declare `P0_SOURCES_PASS` before canonical regeneration and comparison are complete.

## 9. Repository as project memory

If conversational history is unavailable, trust the repository documents and verified commit/gate records over remembered chat details.

When a new significant milestone is accepted, update this checkpoint rather than relying on chat continuity.

## 10. Current branch intent

`work/foundation-and-handoff` exists to add the earthquake-resistant governance/recovery foundation and the complete next-chat transfer package. It should be reviewed as policy/documentation work before merging.

## Next safe sentence

A new chat can begin with:

> Read `docs/CHAT_TRANSFER_PACKAGE.md` and the normative documents it lists. Verify repository state before doing any work. Continue P0 from the canonical-access hardening step; do not import Szondi2 implementation.
