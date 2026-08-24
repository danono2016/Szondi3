# SZONDI3 — COMPLETE CHAT TRANSFER PACKAGE

**Purpose:** recover the project safely in a new ChatGPT conversation even if the previous conversation is unavailable.  
**Repository:** `danono2016/Szondi3`  
**Current project phase:** `P0 — Constitution + Sources`  
**Overall P0 gate:** `IN_PROGRESS`

---

## A. Paste this into the new chat

Copy the block below as the first substantive message in the new conversation:

> We are continuing the Szondi3 project in repository `danono2016/Szondi3`. Treat the repository as durable project memory; do not rely on assumptions from Szondi2 or on missing chat history.
>
> Before changing anything, read these files in this order:
> 1. `docs/PROJECT_CONSTITUTION.md`
> 2. `docs/DOCTRINAL_FIDELITY_POLICY.md`
> 3. `docs/FOUNDATION_ARCHITECTURE.md`
> 4. `docs/DEVELOPMENT_GOVERNANCE.md`
> 5. `docs/VALIDATION_AND_RECOVERY.md`
> 6. `docs/PROJECT_CHECKPOINT.md`
> 7. `docs/RESTART_ROADMAP.md`
> 8. `docs/MIGRATION_MANIFEST.md`
> 9. `docs/SOURCE_ASSET_MANIFEST.md`
> 10. `docs/ASSET_ADMISSION_VERIFICATION.md`
> 11. `docs/CANONICAL_ACCESS_SPEC.md`
> 12. `docs/P0_SOURCE_INSPECTION_REPORT.md`
> 13. `docs/STIMULUS_MAPPING_MANIFEST.md`
> 14. `config/source_catalog.json`
>
> Then verify the current repository/PR/CI state instead of assuming it. Continue only from the next safe P0 step recorded in `PROJECT_CHECKPOINT.md`.
>
> Fundamental constraints: preserve Szondi-primary doctrine without modernization; keep Deri/Mélon as separate post-Szondian layers; no executable Szondi2 code or old canonical TXT may become authority; predecessor material is `ORACLE_ONLY` after independent derivation; photograph-person historical metadata is excluded from runtime; doctrine and executable interpretation are separate objects; ambiguity must be preserved; unsupported source structures fail closed rather than being silently dropped.
>
> The admitted evidence is 10 DOCX, 8 PDF and 48 WebP images, already identity-verified byte-for-byte. PR #1 source-structure inspection passed and was merged into `main` as commit `25abe9ac2adb149b40239a2562ab6f056b30f426`. Workflow run `32763754908` succeeded; artifact `p0-docx-inspection` had digest `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`.
>
> Do NOT declare P0 complete yet. Canonical extractor implementation, deterministic regeneration, new canonical hash inventory, comparison to Szondi2 witness hashes and primary revalidation of stimulus mapping are still pending.
>
> Your immediate task is to inspect current branch/PR status, ensure the foundation-and-handoff policy work has been merged or review it if still open, and then harden `CANONICAL_ACCESS_SPEC.md` from the structural inspection before implementing the new extractor. Work specification-first and test-before-trust. Record durable decisions/checkpoints back in the repository so another chat can recover without conversational memory.

---

## B. Project mission

Szondi3 is a clean restart intended to preserve, formalize and operationalize Szondian doctrine without allowing software convenience, contemporary taste, inherited code or narrative fluency to rewrite the primary sources.

Canonical direction:

`Primary Sources -> Canonical Access -> Deterministic Test Engine -> Primary Doctrine Registry -> Executable Interpretation -> Clinical Evidence Graph -> Integration -> Reports`

No downstream layer may silently mutate an upstream layer.

---

## C. Why Szondi3 exists

Szondi2 demonstrated that technically precise software can still inherit assumptions, omit doctrine, overgeneralize anti-inferences, mix doctrine with executability and accumulate competing notions of authority.

Szondi3 therefore uses a total software restart. Evidence and lessons are preserved; executable implementation is re-derived from source.

No copy/paste port of Szondi2 code is allowed.

---

## D. Source authority hierarchy

1. Original Szondi primary sources.
2. Verified canonical derivatives for access only.
3. Original PDF page/image for visual arbitration where available.
4. Deri, Mélon and other post-Szondian authors in separate layers.
5. Contemporary psychological/scientific context as a separately labeled layer.
6. Legacy software only as technical/oracle evidence after independent derivation.

The eight `SZ_*` entries in `config/source_catalog.json` are Szondi-primary. `DERI_1949` and `MELON_1975` are `POST_SZONDI_TRADITION`.

---

## E. Evidence admitted into Szondi3

The repository contains and has verified:

- 10 DOCX source files;
- 8 PDF visual-arbitration files;
- 48 WebP stimulus images.

The image set matches the immutable predecessor Git tree witness. DOCX/PDF identities match recorded source hashes/blob identities.

Not admitted as authority:

- Szondi2 Java implementation/tests;
- old canonical TXT;
- old exporter/verifier scripts;
- old project state;
- 405-chunk reading ledger;
- predecessor runtime CSV schemas;
- old interpretive claims/guardrails/triggers.

---

## F. Stimulus rule

The 48 image binaries are admitted. The predecessor series/position/factor mapping is only evidence pending independent primary-source revalidation.

The future runtime asset model may contain only stable card identity, series, position, factor and image identity/path.

Historical metadata about photographed persons must never enter scoring, doctrine, interpretation, clinical graph, integration or reports.

---

## G. Canonical-access status

Szondi3 intentionally did not import predecessor canonical TXT.

A new `CANONICAL_ACCESS_SPEC.md` exists. A new read-only OOXML inspector was written independently and executed in CI before writing the extractor.

The inspection showed that the corpus contains substantial structural content: body tables, hundreds of footnote references, fields, drawings/legacy pictures, and in some documents hundreds of header/footer story parts. This proves that a simplistic paragraph-only extraction would be unsafe.

Examples from the verified structural report:

- `SZ_LEHR_1972`: 160 tables, 13,060 aggregated table cells, 285 footnote references;
- `SZ_IA_1956_A`: 447 footnote references;
- `SZ_THER_1963_B`: 409 footnote references;
- `SZ_TRIEBPATH_2`: 159 tables, 8,176 aggregated table cells;
- `DERI_1949`: 537 header parts and 539 footer parts inspected.

These are structural witnesses, not semantic doctrine counts.

---

## H. Current P0 work still required

Before `P0_SOURCES_PASS`, complete all of the following:

1. harden canonical-access rules using real OOXML inspection evidence;
2. explicitly define body/table traversal and stable unit ordering;
3. define notes and reference linkage;
4. define header/footer inclusion/deduplication behavior;
5. define fields and displayed text behavior;
6. define drawings/pictures/visual arbitration markers;
7. define unknown OOXML fail-closed behavior;
8. implement the new extractor from zero;
9. create tests from source structures/invariants rather than predecessor output;
10. regenerate from clean inputs at least twice and prove deterministic identity;
11. inventory new canonical hashes;
12. only after independent generation, compare new hashes to Szondi2 witness hashes;
13. investigate every mismatch rather than selecting an automatic winner;
14. revalidate stimulus mapping from primary source evidence;
15. record residual source limitations, especially the lack of paired visual PDF arbitration for the two Triebpathologie DOCX files.

Only then evaluate `P0_SOURCES_PASS`.

---

## I. Foundation invariants

A new collaborator must preserve these even if technology changes:

- admitted evidence immutable;
- generated output never promoted to source authority;
- doctrine separate from executability;
- stable provenance through every material layer;
- ambiguity preserved;
- no certainty inflation;
- no silent omission;
- deterministic core reproducible;
- unsupported meaningful structure fails closed;
- stable IDs never recycled;
- source corrections trigger downstream blast-radius review;
- repository, not chat, is durable project memory;
- implementation shell may be replaced without losing epistemic core.

Read `FOUNDATION_ARCHITECTURE.md` for the normative version.

---

## J. How to work safely in the new chat

Start by reading, not coding. Verify repository state, branches, open PRs and CI results. Do not assume the transfer package is newer than the repository.

For each material change, identify the layer, specification/source basis, tests, invariants and unresolved conditions. Prefer branch + PR + read-only CI.

When the work reaches another stable milestone, update `PROJECT_CHECKPOINT.md` and this handoff package if the next safe action materially changes.

---

## K. Red flags that require stopping

Stop and investigate rather than improvising if:

- a source hash mismatches;
- a configured source is absent;
- unknown OOXML may contain meaning;
- a field/table/note cannot be represented without loss;
- new and old canonical outputs differ unexpectedly;
- source wording conflicts with predecessor behavior;
- a mapping cannot be verified from primary evidence;
- an executable claim lacks doctrine linkage;
- later clinical work would require inventing a missing condition;
- a proposed convenience would mix source layers or leak photograph metadata.

---

## L. Current repository checkpoint identifiers

Last merged P0 inspection PR: **#1**  
Merged commit: `25abe9ac2adb149b40239a2562ab6f056b30f426`  
Verified workflow run: `32763754908`  
Inspection artifact digest: `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`

Foundation/handoff work branch created after that checkpoint:

`work/foundation-and-handoff`

The new chat must verify whether that branch has already been merged before continuing.

---

## M. Definition of success for the transfer

The transfer is successful if a new chat can, using only repository state plus this package, correctly determine:

- what the project is trying to preserve;
- which sources are authoritative;
- what has been admitted and verified;
- what is still provisional;
- what must never be imported from Szondi2;
- what phase the project is in;
- what has passed CI;
- what the next safe task is;
- which actions would violate the architecture.

No information essential to those questions should require the old conversation.

---

## Final transfer rule

> **Do not continue from remembered momentum. Reconstruct the state from the repository, verify it, and then continue from the lowest unfinished gate.**
