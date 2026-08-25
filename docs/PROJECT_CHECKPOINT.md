# SZONDI3 — PROJECT CHECKPOINT

**Checkpoint date:** 2026-08-25  
**Repository:** `danono2016/Szondi3`  
**Authoritative branch:** `main`  
**Current phase:** `P0 — Constitution + Sources`  
**P0 overall gate:** `IN_PROGRESS`  
**Foundation status:** `MERGED_AND_MACHINE_VERIFIED`  
**Canonical-access implementation gate:** `PASS_AND_MERGED`

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
11. `docs/P0_CANONICAL_ACCESS_TEST_PLAN.md`
12. `docs/P0_CANONICAL_ACCESS_VERIFICATION.md`

The earthquake-resistant foundation was merged through PR #2 as commit `80a281b0c5f54eff96eb3ae5ea84c49d00c54544` after Foundation verification and P0 source-inspection passed on the PR head.

The succession-governance documents were added to the machine evidence boundary through PR #5, merged as `3455e68ddde1692f28840eb048217737b7bc7e0c`. The foundation verifier now requires 14 normative documents.

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

After the canonical-access merge, Foundation verification run `32794400019` passed on `main` commit `f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`, confirming 10 DOCX, 8 PDF, 48 WebP, stimulus tree `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`, and 14 required normative documents.

This verifier establishes identity/structural integrity only; it does **not** validate OCR correctness, doctrine or factor mapping.

## 4. Source layers

Primary Szondi doctrine consists of the eight `SZ_*` source entries in `config/source_catalog.json`.

`DERI_1949` and `MELON_1975` are separate `POST_SZONDI_TRADITION` layers and may supplement but never silently overwrite Szondi-primary doctrine.

No modernization, euphemization or contemporary normalization may rewrite Szondi-primary doctrine. Genetics, heredity, genotropism, transgenerational formulations, sexual/pathological terminology and historically anachronistic or politically incorrect source formulations remain source evidence and must be preserved faithfully at the primary-doctrine layer. Softer contemporary communication belongs only to explicitly downstream layers such as client reporting.

## 5. Stimulus status

The 48 image binaries are admitted and identity-verified.

The predecessor series/position/factor mapping is recorded in `docs/STIMULUS_MAPPING_MANIFEST.md` as evidence only. It is **not yet runtime authority** and must be independently revalidated against authorized primary source material before P1 administration code is implemented.

Historical metadata about photographed persons is permanently excluded from runtime interpretation and reports.

## 6. Canonical access status — implementation gate PASS

Generated canonical TXT from Szondi2 was deliberately not imported.

A source-structure inspector was first written from zero and run in read-only CI. PR #1 (`P0 canonical source inspection gate`) passed and was merged into `main` as commit `25abe9ac2adb149b40239a2562ab6f056b30f426`. Inspection workflow run `32763754908` produced artifact `p0-docx-inspection`, digest `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`.

That inspection established that the DOCX corpus is structurally complex: tables, notes, fields, drawings/legacy pictures and hundreds of header/footer story parts. A paragraph-only dump is unsafe. `docs/CANONICAL_ACCESS_SPEC.md` was hardened from this evidence before extractor trust.

PR #6 (`Implement P0 canonical access gate`) then implemented the independent Szondi3 extractor from zero and merged it to `main` as commit:

`f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`

Final PR head:

`46587f75d494ef896ae99482bcb73c102631abbf`

The merged source-access implementation consists of:

- `scripts/canonical_access.py` — deterministic fail-closed canonical extractor;
- `scripts/verify_canonical_access.py` — independent real-source structure/provenance verifier;
- `tests/test_canonical_access.py` and `tests/test_canonical_access_regressions.py` — 20 passing tests;
- `.github/workflows/p0-canonical-access.yml` — read-only full-corpus CI;
- `docs/P0_CANONICAL_ACCESS_TEST_PLAN.md` — pre-implementation contract;
- `docs/P0_CANONICAL_ACCESS_VERIFICATION.md` — durable verification/hashes record.

Post-merge `main` run `32794400061` passed all canonical steps: foundation verification, 20 tests, two full ten-source generations, byte-identical `diff -ru`, canonical inventory, independent source/provenance verification and artifact upload. P0 source inspection run `32794400074` also passed.

The post-merge canonical artifact is ID `9544306267`. The generated `canonical-hashes.json` has SHA-256:

`4629e5730f298043cfd42c541d0d319fecb6da45ec6cb9f8b5a807e91dc59479`

The final cleaned PR artifact and post-merge `main` artifact are byte-identical after unpacking. Per-source JSONL/inventory hashes are recorded in `docs/P0_CANONICAL_ACCESS_VERIFICATION.md`.

**No Szondi2 exporter/code/output was consulted to implement, tune or verify this independent generation.**

This is a canonical-access implementation gate only. Generated derivatives remain below admitted source evidence in authority.

## 7. What has NOT yet been done

Do not assume any of the following are complete:

- real-source DOCX/PDF visual spot arbitration required after canonical generation;
- comparison of independently generated Szondi3 canonical output with Szondi2 canonical witnesses as `ORACLE_ONLY`;
- investigation/classification of every predecessor mismatch;
- independent primary-source revalidation of the 48-card series/position/factor mapping;
- resolution of residual visual limitations for `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`, which have no paired admitted PDFs;
- `P0_SOURCES_PASS`;
- P1 deterministic administration/scoring engine;
- Doctrine Registry;
- executable interpretations;
- Clinical Graph;
- integration/reporting engine.

No P1/scoring or clinical interpretation implementation is authorized yet.

## 8. Immediate next safe work

The independent extractor/regeneration gate is complete. Continue P0 in this order:

1. perform real-source DOCX/PDF spot arbitration where visual/layout fidelity matters, using the paired PDFs as visual evidence where available;
2. preserve unresolved visual ambiguity explicitly; do not infer missing originals for the two Triebpathologie parts;
3. use the recorded new canonical hashes as derivative identity witnesses;
4. only then inspect Szondi2 canonical witness hashes/text as `ORACLE_ONLY` comparison evidence;
5. investigate and classify every difference; predecessor equality is never the target;
6. separately revalidate the 48-card series/position/factor mapping from primary source evidence;
7. record residual limitations and evaluate the complete P0 acceptance conditions;
8. only if all P0 source conditions pass, declare the explicit `P0_SOURCES_PASS` gate.

P1 must not begin before that explicit gate.

## 9. Hard prohibitions for the next chat/developer

Do not:

- copy or port Szondi2 Java/exporter code;
- treat predecessor canonical output as source truth;
- make equality with predecessor output a goal;
- import old canonical TXT as authority;
- treat predecessor tests as doctrine;
- silently skip tables/notes/fields/visual constructs/unknown OOXML;
- destructively deduplicate primary header/footer provenance;
- normalize, soften or modernize Szondi-primary terminology at the doctrine/source layer;
- mix Deri/Mélon into Szondi-primary doctrine;
- use photographed-person historical metadata in runtime;
- begin P1/scoring/interpretation because canonical access now passes;
- declare `P0_SOURCES_PASS` before visual/source arbitration, predecessor comparison/mismatch classification and stimulus mapping revalidation are complete.

## 10. Repository as project memory

If conversational history is unavailable, trust repository documents and verified gate records over remembered chat details.

When a significant milestone is accepted, refresh this checkpoint and `docs/CHAT_TRANSFER_PACKAGE.md` rather than relying on chat continuity.

## 11. Established milestones

- PR #1 — source-structure inspection gate; merged `25abe9ac2adb149b40239a2562ab6f056b30f426`.
- PR #2 — earthquake-resistant foundation; merged `80a281b0c5f54eff96eb3ae5ea84c49d00c54544`.
- PR #5 — succession governance documents locked in evidence boundary; merged `3455e68ddde1692f28840eb048217737b7bc7e0c`.
- PR #6 — independent canonical-access implementation gate; merged `f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`.

The implementation shell may change in future without changing evidence authority, provenance rules or layer boundaries.

## Next safe sentence

> Read `docs/CHAT_TRANSFER_PACKAGE.md` and the normative documents it lists. Verify repository/CI state first. The independent canonical-access gate is complete; continue P0 with real-source DOCX/PDF visual arbitration, then `ORACLE_ONLY` predecessor comparison and mismatch classification, then primary-source stimulus-mapping revalidation. Do not begin P1 or declare `P0_SOURCES_PASS` early.
