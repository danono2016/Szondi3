# SZONDI3 — PROJECT CHECKPOINT

**Checkpoint date:** 2026-08-24  
**Repository:** `danono2016/Szondi3`  
**Authoritative branch:** `main`  
**Foundation work branch at this checkpoint:** `work/foundation-and-handoff`  
**Current phase:** `P0 — Constitution + Sources`  
**P0 overall gate:** `IN_PROGRESS`

## 1. What defines the project

Read these before implementation work:

1. `docs/PROJECT_CONSTITUTION.md`
2. `docs/DOCTRINAL_FIDELITY_POLICY.md`
3. `docs/FOUNDATION_ARCHITECTURE.md`
4. `docs/DEVELOPMENT_GOVERNANCE.md`
5. `docs/VALIDATION_AND_RECOVERY.md`
6. `docs/DECISION_LOG.md`
7. `docs/MIGRATION_MANIFEST.md`
8. `docs/RESTART_ROADMAP.md`
9. `docs/SOURCE_ASSET_MANIFEST.md`
10. `docs/CANONICAL_ACCESS_SPEC.md`

The foundation documents on the current work branch are intended to become normative after PR #2 review/merge.

## 2. Evidence already admitted and verified

Szondi3 contains exactly:

- 10 admitted DOCX source files;
- 8 admitted visual-arbitration PDF files;
- 48 admitted WebP stimulus images.

Binary transfer was verified byte-for-byte against predecessor evidence using Git identities/hashes. The 48-image set matches immutable predecessor tree `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`. No predecessor Java implementation, runtime CSV, generated canonical TXT, old project state or legacy extraction scripts were admitted as authority.

See `docs/ASSET_ADMISSION_VERIFICATION.md`, `docs/SOURCE_ASSET_MANIFEST.md`, and machine lock `config/evidence_lock.json`.

## 3. Machine-enforced foundation

`python scripts/verify_foundation.py` is the fail-closed repository verifier. It checks:

- all 10 catalogued DOCX files by SHA-256;
- all 8 PDFs by admitted Git blob identity;
- exact 48-WebP stimulus set through immutable Git tree identity;
- catalog/source-set consistency;
- required normative documents;
- absence of narrow forbidden predecessor-authority artifacts (`project-state.json`, `sources/canonical-text`, legacy `cards.csv`).

`.github/workflows/foundation.yml` runs this read-only on PRs and `main` pushes.

This verifier establishes identity/structural integrity only; it does **not** validate OCR correctness, doctrine or factor mapping.

## 4. Source layers

Primary Szondi doctrine consists of the eight `SZ_*` source entries in `config/source_catalog.json`.

`DERI_1949` and `MELON_1975` are separate `POST_SZONDI_TRADITION` layers and may supplement but never silently overwrite Szondi-primary doctrine.

## 5. Stimulus status

The 48 image binaries are admitted and identity-verified.

The predecessor series/position/factor mapping is recorded in `docs/STIMULUS_MAPPING_MANIFEST.md` as evidence only. It is **not yet runtime authority** and must be revalidated against authorized primary source material before P1 administration code is implemented.

Historical metadata about photographed persons is permanently excluded from runtime interpretation and reports.

## 6. Canonical access status

Generated canonical TXT from Szondi2 was deliberately not imported.

A source-structure inspector was written from zero and run in read-only CI. PR #1 (`P0 canonical source inspection gate`) passed and was merged into `main` as commit `25abe9ac2adb149b40239a2562ab6f056b30f426`.

Workflow run `32763754908` completed `SUCCESS` and produced artifact `p0-docx-inspection`, digest:

`sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`

The inspection confirmed that the DOCX corpus is structurally complex: many tables, footnote references, fields, drawings and hundreds of header/footer story parts. A simple paragraph dump would be unsafe. See `docs/P0_SOURCE_INSPECTION_REPORT.md`.

`docs/CANONICAL_ACCESS_SPEC.md` has now been hardened from that evidence. It explicitly defines:

- an OOXML part-classification registry with no implicit “other = ignore” branch;
- body/table hierarchy and document-order traversal;
- note identity/reference linkage;
- non-destructive header/footer preservation (dedup only in secondary views);
- field instruction vs displayed-result handling;
- hyperlink/bookmark provenance;
- drawings/pictures/text boxes/alternate-content visual markers and fail-closed rules;
- deterministic structured records and serialization constraints;
- explicit unknown-construct failure;
- clean-run reproducibility requirements before comparison with Szondi2 witnesses.

The specification is ready to drive tests and extractor implementation; the extractor itself does not yet exist.

## 7. What has NOT yet been done

Do not assume any of the following are complete:

- canonical extractor implementation;
- canonical derivative generation;
- deterministic canonical regeneration proof;
- new canonical hash inventory;
- comparison of new canonical hashes/text with Szondi2 witnesses;
- primary-source revalidation of the 48-card factor mapping;
- P1 deterministic administration/scoring engine;
- Doctrine Registry;
- executable interpretations;
- Clinical Graph;
- integration/reporting engine.

No clinical interpretation implementation is authorized yet.

## 8. Immediate next safe work

The next task is **tests/spec-conformance before extractor trust**, not clinical interpretation.

Recommended order:

1. derive source-structure-focused tests/fixtures from the hardened `CANONICAL_ACCESS_SPEC.md` and admitted real-corpus structures without consulting Szondi2 exporter behavior;
2. implement the new deterministic extractor from zero;
3. make unsupported possibly meaningful OOXML fail closed;
4. run extraction at least twice from clean identical inputs and prove byte-identical structured outputs;
5. run schema/unit/order/provenance validation;
6. perform real-source spot checks against DOCX and paired PDFs where visual arbitration matters;
7. inventory the new canonical output hashes;
8. only then compare against Szondi2 canonical witness hashes/text as `ORACLE_ONLY`;
9. investigate and classify every difference;
10. separately revalidate stimulus mapping from primary sources.

Only after these requirements and remaining P0 source conditions pass may `P0_SOURCES_PASS` be considered.

## 9. Hard prohibitions for the next chat/developer

Do not:

- copy Szondi2 Java or exporter code;
- inspect predecessor canonical output before independent Szondi3 generation merely to make the new output match;
- import old canonical TXT as authority;
- treat predecessor tests as source truth;
- skip tables/notes/fields/visual constructs/unknown OOXML silently;
- destructively deduplicate primary header/footer provenance;
- normalize source terminology to contemporary psychology;
- mix Deri/Mélon into Szondi-primary doctrine;
- use photographed-person historical metadata in runtime;
- begin interpretation because scoring seems obvious;
- declare `P0_SOURCES_PASS` before canonical regeneration/comparison and mapping revalidation are complete.

## 10. Repository as project memory

If conversational history is unavailable, trust repository documents and verified gate records over remembered chat details.

When a significant milestone is accepted, refresh this checkpoint and `docs/CHAT_TRANSFER_PACKAGE.md` rather than relying on chat continuity.

## 11. Current branch/PR intent

`work/foundation-and-handoff` / PR #2 (`Establish earthquake-resistant foundation and chat continuity`) adds:

- normative foundation architecture;
- development/change governance;
- validation/disaster-recovery policy;
- verified P0 structural report;
- decision log;
- machine-readable evidence lock;
- fail-closed foundation verifier + CI;
- hardened canonical-access specification;
- durable checkpoint and complete new-chat transfer package;
- README entrypoint and constitutional bindings.

A new chat must verify whether PR #2 is merged before continuing.

## Next safe sentence

> Read `docs/CHAT_TRANSFER_PACKAGE.md` and the normative documents it lists. Verify repository/PR/CI state first. Continue P0 by writing spec-derived canonical extractor tests and then the independent extractor; do not consult Szondi2 implementation/output until independent Szondi3 canonical generation is complete.
