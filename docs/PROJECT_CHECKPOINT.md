# SZONDI3 — PROJECT CHECKPOINT

**Checkpoint date:** 2026-08-25  
**Repository:** `danono2016/Szondi3`  
**Authoritative branch:** `main`  
**Current phase:** `P0 — Constitution + Sources`  
**P0 overall gate:** `IN_PROGRESS`  
**Foundation status:** `MERGED_AND_MACHINE_VERIFIED`  
**Canonical-access implementation gate:** `PASS_AND_MERGED`  
**Real-source visual spot-arbitration gate:** `PASS_AND_MERGED`  
**Predecessor canonical comparison gate:** `P0_ORACLE_COMPARISON_PASS`

## 1. Repository authority and required reading

Repository state is durable project memory. Before material work, read and obey:

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
13. `docs/P0_VISUAL_ARBITRATION_REPORT.md`
14. `docs/P0_ORACLE_COMPARISON_REPORT.md`
15. `docs/STIMULUS_MAPPING_MANIFEST.md`

Also read the succession/qualification documents when taking over from another chat.

## 2. Evidence boundary

Szondi3 contains exactly:

- 10 admitted DOCX source files;
- 8 admitted visual-arbitration PDF files;
- 48 admitted WebP stimulus images.

Evidence identity is machine locked by `config/evidence_lock.json` and enforced by `scripts/verify_foundation.py`:

- all 10 DOCX by SHA-256;
- all 8 PDFs by admitted Git blob identity;
- exact 48-WebP set by immutable Git tree `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`;
- required normative documents;
- catalog/source-set consistency.

Generated artifacts remain derivatives, never source authority.

## 3. Source layers and fidelity

The eight `SZ_*` entries are `SZONDI_PRIMARY`. `DERI_1949` and `MELON_1975` remain separate `POST_SZONDI_TRADITION` layers.

Szondi-primary wording must not be modernized, euphemized or politically sanitized. Genetics, heredity, genotropism, transgenerational formulations, sexual/pathological language and historically anachronistic terminology remain part of the primary evidence layer. Contemporary nuance or softer client language belongs only downstream and must not rewrite source evidence.

Historical metadata about photographed subjects is permanently excluded from scoring, doctrine, interpretation and reports.

## 4. Canonical-access gate — PASS

PR #6 implemented the independent deterministic canonical extractor and verifier from zero and merged as:

`f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`

The gate includes:

- `scripts/canonical_access.py`;
- `scripts/verify_canonical_access.py`;
- 20 specification-derived/regression tests;
- two full ten-source generations required to be byte-identical;
- inventory validation;
- independent real-source structure/provenance verification;
- fail-closed handling of unsupported meaningful OOXML.

Canonical content manifest SHA-256 remains:

`4629e5730f298043cfd42c541d0d319fecb6da45ec6cb9f8b5a807e91dc59479`

Per-source derivative hashes are recorded in `docs/P0_CANONICAL_ACCESS_VERIFICATION.md` and machine-readable identity is recorded in `verification/P0_CANONICAL_DERIVATIVE_MANIFEST.json` with status `DERIVATIVE_IDENTITY_ONLY_NOT_SOURCE_AUTHORITY`.

**No Szondi2 code/output was consulted to implement, tune or verify the independent Szondi3 canonical generation.**

## 5. Minimal source-access bridge

The canonical workflow now also provides unchanged admitted source bytes as transport artifacts on `main` so future chats can perform source checks without changing authority:

- `p0-canonical-access` — canonical derivative, 90-day retention;
- `p0-visual-arbitration-sources` — the 8 admitted PDFs, 90-day retention;
- `p0-canonical-source-docx` — the 10 admitted DOCX files, 90-day retention.

PR #8 established the canonical/PDF bridge and permanent derivative identity witness; PR #11 added only the DOCX transport step. The artifacts do not create new sources or new authority.

Post-merge canonical workflow on commit `59f68b02d0f9a30c4c19cb964c4b64a2a12e55d8` passed foundation, all 20 tests, two byte-identical generations, inventory, derivative identity, independent verifier, source-set validation and all three artifact uploads.

The downloaded DOCX artifact was independently checked: 10/10 files matched `config/source_catalog.json` SHA-256 exactly.

## 6. Real-source visual arbitration — PASS for required spot gate

PR #9 recorded the required DOCX/canonical-to-PDF spot arbitration across all 8 admitted DOCX/PDF pairs and merged as:

`6460c0ff28e899bab11231993bc3d6449260ee96`

See `docs/P0_VISUAL_ARBITRATION_REPORT.md`.

The arbitration demonstrated that PDF use is materially necessary. Examples include visibly distorted DOCX/canonical tokens around figures, percentages, captions and reaction notation. Those events are recorded explicitly; the canonical derivative was not silently rewritten.

No sampled case exposed a canonical traversal/order/provenance defect.

`SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` have no paired admitted PDF. Visual uncertainty that cannot be resolved from admitted evidence remains explicitly `UNRESOLVED_NO_PAIRED_PDF`; no missing original may be invented.

## 7. Szondi2 predecessor comparison — `P0_ORACLE_COMPARISON_PASS`

Only after independent canonical generation and visual arbitration were complete was Szondi2 inspected as `ORACLE_ONLY`.

Szondi2 had canonical witnesses for 8 sources; Triebpathologie was absent. The 8 predecessor raw DOCX SHA-256 values exactly match the corresponding admitted Szondi3 inputs.

The predecessor extractor/witness was independently regenerated from those identical bytes and reproduced all 8 recorded predecessor canonical hashes, block counts and character counts exactly.

A source-near common projection was then compared against the independent Szondi3 JSONL:

- all body/table paragraph wording matched after classifying predecessor-generated technical artifacts;
- all positive note text matched by source-native note ID and paragraph order;
- all header/footer paragraph wording matched by story part and order;
- 1,715 footnote/endnote references matched by kind, ID and paragraph order;
- all 335 source tables in the 8 comparable files are represented in Szondi3;
- **0 unexplained source-visible textual mismatches remain.**

The main predecessor differences are classified, not copied:

1. `ORACLE_STRUCTURAL_TAB_LEAK` — Szondi2 serialized `w:pPr/w:tabs/w:tab` formatting tab stops as literal text. Across 59,498 predecessor blocks this affected 14,426 blocks and injected 16,532 non-source-visible tabs. Raw OOXML accounts for the discrepancy exactly.
2. `REFERENCE_REPRESENTATION` — Szondi2 inserted non-source-visible `[FN:n]`/`[EN:n]` strings in text; Szondi3 keeps the same IDs as structured metadata.
3. `SPECIAL_NOTE_CLASSIFICATION` — Word continuation-separator notes are structural objects; Szondi3 labels them explicitly instead of treating a positive-ID blank separator as doctrinal note text.
4. `STRUCTURAL_ENRICHMENT_NOT_MISMATCH` — Szondi3 preserves hierarchical tables, story identities, fields, hyperlinks/bookmarks, visual/text-box objects and AlternateContent branches that the flat predecessor TXT does not encode structurally.

No verified predecessor comparison finding requires a change to `scripts/canonical_access.py`. Szondi3 was not tuned toward predecessor equality.

See `docs/P0_ORACLE_COMPARISON_REPORT.md` for the complete evidence and per-source counts/hashes.

`SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` remain `NOT_COMPARABLE_PREDECESSOR_ABSENT`; this is not a failure and must not be filled by inference.

## 8. Stimulus status — next unfinished P0 gate

The 48 image binaries are admitted and identity verified.

The predecessor series/position/factor mapping in `docs/STIMULUS_MAPPING_MANIFEST.md` is evidence only, **not runtime authority**. It has not yet passed the required independent primary-source revalidation.

The lowest unfinished P0 gate is now:

**independent primary-source revalidation of the 48-card series / position / factor mapping.**

The mapping must be established from authorized primary Szondi evidence, not by assuming the predecessor CSV/mapping is correct. Any uncertainty or conflict must remain explicit.

## 9. What is still NOT complete

Do not assume completion of:

- independent primary-source revalidation of the 48-card series/position/factor mapping;
- residual-limitations review of the full P0 source layer;
- final evaluation of all P0 acceptance conditions;
- explicit `P0_SOURCES_PASS`;
- P1 deterministic administration/scoring;
- Doctrine Registry;
- executable interpretations;
- Clinical Graph;
- integration/reporting engine.

P1 remains unauthorized until `P0_SOURCES_PASS` is explicitly recorded.

## 10. Immediate next safe work

Continue P0 in this order:

1. independently establish and verify the 48-card series/position/factor mapping from admitted primary-source evidence;
2. compare the independently established mapping with predecessor mapping only as evidence/oracle, never as target truth;
3. classify every discrepancy or unresolved point;
4. review residual limitations, including the absent paired PDFs for Triebpathologie;
5. evaluate the complete P0 source acceptance conditions;
6. only if all required conditions are satisfied, explicitly declare `P0_SOURCES_PASS`.

## 11. Hard prohibitions

Do not:

- copy/port Szondi2 executable logic;
- treat predecessor canonical output or mappings as source truth;
- make equality with predecessor artifacts a goal;
- silently correct or normalize source wording;
- modernize or sanitize Szondi-primary doctrine;
- silently discard meaningful OOXML or visual ambiguity;
- infer missing Triebpathologie PDF evidence;
- mix Deri/Mélon into primary Szondi doctrine;
- use photographed-person historical metadata clinically;
- begin P1/scoring/interpretation before explicit `P0_SOURCES_PASS`.

## 12. Established milestones

- PR #1 — source-structure inspection; merged `25abe9ac2adb149b40239a2562ab6f056b30f426`.
- PR #2 — earthquake-resistant foundation; merged `80a281b0c5f54eff96eb3ae5ea84c49d00c54544`.
- PR #5 — succession governance added to evidence lock; merged `3455e68ddde1692f28840eb048217737b7bc7e0c`.
- PR #6 — independent canonical-access gate; merged `f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`.
- PR #7 — canonical verification/checkpoint continuity documentation; merged `2d1e9a5da934294d1c5c737915ca2f1c992fe530`.
- PR #8 — minimal canonical/PDF source-access bridge; merged `9e263171e4de4be46df78caa9208e2b433fdf0bc`.
- PR #9 — real-source visual spot arbitration; merged `6460c0ff28e899bab11231993bc3d6449260ee96`.
- PR #11 — unchanged admitted DOCX transport for exact ORACLE comparison; merged `59f68b02d0f9a30c4c19cb964c4b64a2a12e55d8`.
- `P0_ORACLE_COMPARISON_PASS` — recorded in `docs/P0_ORACLE_COMPARISON_REPORT.md` by the current P0 verification change.

## Next safe sentence

> Reconstruct current state from the repository and CI. Canonical access, real-source visual spot arbitration and the ORACLE_ONLY predecessor canonical comparison have passed. Continue P0 with independent primary-source revalidation of the 48-card series/position/factor mapping. Do not begin P1 or declare `P0_SOURCES_PASS` early.
