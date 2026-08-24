# SZONDI3 — COMPLETE CHAT TRANSFER PACKAGE

**Purpose:** recover the project safely in a new ChatGPT conversation even if the previous conversation is unavailable.  
**Repository:** `danono2016/Szondi3`  
**Current project phase:** `P0 — Constitution + Sources`  
**Overall P0 gate:** `IN_PROGRESS`  
**Foundation status:** `MERGED_AND_MACHINE_VERIFIED`

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
> 6. `docs/DECISION_LOG.md`
> 7. `docs/PROJECT_CHECKPOINT.md`
> 8. `docs/RESTART_ROADMAP.md`
> 9. `docs/MIGRATION_MANIFEST.md`
> 10. `docs/SOURCE_ASSET_MANIFEST.md`
> 11. `docs/ASSET_ADMISSION_VERIFICATION.md`
> 12. `docs/CANONICAL_ACCESS_SPEC.md`
> 13. `docs/P0_SOURCE_INSPECTION_REPORT.md`
> 14. `docs/STIMULUS_MAPPING_MANIFEST.md`
> 15. `config/source_catalog.json`
> 16. `config/evidence_lock.json`
> 17. `scripts/verify_foundation.py`
>
> Then verify the current repository/PR/CI state instead of assuming it. Run or inspect the result of `python scripts/verify_foundation.py` before touching source-access logic. Continue only from the next safe P0 step recorded in `PROJECT_CHECKPOINT.md`.
>
> Fundamental constraints: preserve Szondi-primary doctrine without modernization; keep Deri/Mélon as separate post-Szondian layers; no executable Szondi2 code or old canonical TXT may become authority; predecessor material is `ORACLE_ONLY` only after independent derivation; photograph-person historical metadata is excluded from runtime; doctrine and executable interpretation are separate objects; ambiguity must be preserved; unsupported possibly meaningful source structures fail closed rather than being silently dropped.
>
> The admitted evidence is 10 DOCX, 8 PDF and 48 WebP images, already identity-verified byte-for-byte. The evidence set is additionally locked in `config/evidence_lock.json` and machine-checked by `scripts/verify_foundation.py`: DOCX by SHA-256, PDF by Git blob identity, and the whole 48-stimulus directory by immutable Git tree `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`.
>
> PR #1 source-structure inspection passed and was merged into `main` as commit `25abe9ac2adb149b40239a2562ab6f056b30f426`. Workflow run `32763754908` succeeded; artifact `p0-docx-inspection` had digest `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`.
>
> The earthquake-resistant foundation was then merged through PR #2 as commit `80a281b0c5f54eff96eb3ae5ea84c49d00c54544`. The final PR #2 head `596016159011ed93347fa66ca31d5bc23ef1b370` passed Foundation verification run `32765424821` and P0 source inspection run `32765424816` before merge.
>
> The structural inspection showed substantial tables, footnotes, fields, drawings/legacy pictures and hundreds of header/footer story parts. `docs/CANONICAL_ACCESS_SPEC.md` is already hardened from those findings: no implicit “other = ignore”; tables remain hierarchical; notes retain source identity/reference linkage; header/footer primary provenance is not destructively deduplicated; fields distinguish instruction from displayed result; visual/object constructs preserve provenance/visual-arbitration markers; unknown possibly meaningful OOXML fails closed; deterministic serialization/reproducibility is required.
>
> Do NOT declare P0 complete yet. Canonical extractor tests/implementation, deterministic regeneration proof, new canonical hash inventory, comparison to Szondi2 witnesses, and primary revalidation of stimulus mapping are still pending.
>
> Your immediate technical task is to derive tests directly from the hardened canonical-access specification and admitted source structures, then implement the independent Szondi3 extractor from zero. Do not inspect/copy the Szondi2 exporter or old canonical output merely to make Szondi3 match it. Only after independent Szondi3 canonical generation and verification may predecessor output be used as `ORACLE_ONLY` comparison evidence.
>
> Work specification-first and test-before-trust. Keep CI read-only. Record durable decisions and refresh `PROJECT_CHECKPOINT.md` / this transfer package at the next stable milestone.

---

## B. Project mission

Szondi3 is a clean restart intended to preserve, formalize and operationalize Szondian doctrine without allowing software convenience, contemporary taste, inherited code or narrative fluency to rewrite the primary sources.

Canonical direction:

`Primary Sources -> Canonical Access -> Deterministic Test Facts -> Primary Doctrine Registry -> Executable Interpretation -> Clinical Evidence Graph -> Integration -> Reports`

No downstream layer may silently mutate an upstream layer.

---

## C. Why Szondi3 exists

Szondi2 demonstrated that technically precise software can still inherit assumptions, omit doctrine, overgeneralize anti-inferences, mix doctrine with executability and accumulate competing notions of authority.

Szondi3 therefore uses a total software restart. Evidence and lessons are preserved; executable implementation is re-derived from source.

No copy/paste port of Szondi2 executable code is allowed.

---

## D. Earthquake-resistant foundation now established

The foundation is designed so that programming language, framework, database, UI, AI model and chat can all be replaced without destroying the epistemic core.

The durable core consists of immutable evidence, provenance, normative policies/specifications, stable identities, gate decisions and accepted source-derived doctrine. The technical shell remains replaceable.

Key invariants:

- original admitted evidence is immutable;
- generated artifacts never become authority by repetition;
- doctrine and executability are distinct objects;
- every material downstream result must trace back to evidence;
- uncertainty may be preserved/reduced, never inflated;
- ambiguity and contradiction are data;
- no silent omission of possibly meaningful source structure;
- deterministic core must be reproducible;
- source corrections trigger explicit downstream blast-radius review;
- critical state lives in the repository, not in chat memory;
- failure/rewrite recovery reconstructs from source/specs, not from predecessor code.

See `FOUNDATION_ARCHITECTURE.md`, `DEVELOPMENT_GOVERNANCE.md`, and `VALIDATION_AND_RECOVERY.md`.

---

## E. Source authority hierarchy

1. Original Szondi primary sources.
2. Verified canonical derivatives for access only.
3. Original PDF page/image for visual arbitration where available.
4. Deri, Mélon and other post-Szondian authors in separate layers.
5. Contemporary psychological/scientific context as a separately labeled layer.
6. Legacy software only as technical/oracle evidence after independent derivation.

The eight `SZ_*` entries in `config/source_catalog.json` are Szondi-primary. `DERI_1949` and `MELON_1975` are `POST_SZONDI_TRADITION`.

---

## F. Evidence admitted into Szondi3

The repository contains and has verified:

- 10 DOCX source files;
- 8 PDF visual-arbitration files;
- 48 WebP stimulus images.

The image set matches immutable predecessor Git tree `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`. DOCX/PDF identities match recorded source hashes/blob identities.

`config/evidence_lock.json` + `scripts/verify_foundation.py` make this boundary machine-enforceable in CI.

Not admitted as authority:

- Szondi2 Java implementation/tests;
- old canonical TXT;
- old exporter/verifier scripts;
- old project state;
- 405-chunk reading ledger;
- predecessor runtime CSV schemas;
- old interpretive claims/guardrails/triggers.

---

## G. Stimulus rule

The 48 image binaries are admitted. The predecessor series/position/factor mapping is only evidence pending independent primary-source revalidation.

The future runtime asset model may contain only stable card identity, series, position, factor and image identity/path.

Historical metadata about photographed persons must never enter scoring, doctrine, interpretation, clinical graph, integration or reports.

---

## H. Verified canonical-source structural findings

A read-only OOXML inspector was written independently and executed before extractor implementation.

Verified workflow run: `32763754908`  
Verified inspection artifact digest: `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`

The corpus contains substantial structural content. Examples:

- `SZ_LEHR_1972`: 160 tables, 13,060 aggregated table cells, 285 footnote references;
- `SZ_IA_1956_A`: 447 footnote references;
- `SZ_THER_1963_B`: 409 footnote references;
- `SZ_TRIEBPATH_2`: 159 tables, 8,176 aggregated table cells;
- `DERI_1949`: 537 inspected header parts and 539 footer parts.

These are structural witnesses, not semantic/doctrinal counts.

A simplistic paragraph-only or `document.xml`-only extractor is therefore prohibited.

---

## I. Hardened canonical-access contract

`docs/CANONICAL_ACCESS_SPEC.md` is specification-ready for implementation. It requires, among other things:

- explicit classification of every relevant `word/*.xml` part;
- no default ignore branch for unknown possibly meaningful structure;
- document-order traversal;
- hierarchical table preservation;
- note IDs and body-reference linkage;
- non-destructive primary header/footer provenance;
- field instruction/result distinction;
- hyperlink/bookmark provenance;
- explicit visual-object records and `VISUAL_ARBITRATION_REQUIRED` behavior;
- parsing or failure for text boxes/alternate content with visible text;
- structured canonical records as primary output, not TXT blobs;
- stable source-local unit IDs;
- deterministic UTF-8 serialization without timestamps/random/host-specific content in hashed output;
- repeated clean-run identity verification;
- real-source spot checks plus synthetic/adversarial fixtures;
- comparison with Szondi2 only after independent Szondi3 generation.

---

## J. Current P0 work still required

Before `P0_SOURCES_PASS`, complete all of the following:

1. derive canonical-access tests from the hardened specification and actual admitted-source structures;
2. implement the new extractor from zero;
3. verify unsupported possibly meaningful OOXML fails closed;
4. regenerate from clean inputs at least twice and prove deterministic identity;
5. validate schema/unit ordering/provenance;
6. perform DOCX/PDF spot arbitration where needed;
7. inventory new canonical hashes;
8. only then compare new output with Szondi2 witness hashes/text as `ORACLE_ONLY`;
9. investigate/classify every mismatch;
10. independently revalidate the 48-card series/position/factor mapping from primary source evidence;
11. record residual limitations, especially missing paired PDFs for the two Triebpathologie DOCX sources.

Only then evaluate `P0_SOURCES_PASS`.

---

## K. How to work safely in the new chat

Start by reading and verifying, not coding from memory. Check repository state and CI, and do not assume this package is newer than Git.

For each material change, identify the layer, specification/source basis, tests, invariants and unresolved conditions. Prefer branch + PR + read-only CI.

Do not let “the tests pass” substitute for source correctness. Do not let predecessor equality substitute for independent derivation.

At the next stable milestone, update `PROJECT_CHECKPOINT.md`, `DECISION_LOG.md` when needed, and this transfer package if the next safe action changes.

---

## L. Red flags requiring an immediate stop

Stop and investigate rather than improvising if:

- a source hash/blob/tree mismatches the evidence lock;
- a configured source is absent;
- unknown OOXML may contain meaning;
- a field/table/note/visual object cannot be represented without loss;
- extraction only succeeds by discarding unsupported constructs;
- independent new and old canonical outputs differ unexpectedly;
- source wording conflicts with predecessor behavior;
- stimulus mapping cannot be verified from primary evidence;
- an executable claim lacks doctrine linkage;
- a downstream clinical feature would require inventing an unavailable discriminating condition;
- a proposed convenience would mix source layers or leak photograph metadata.

---

## M. Repository checkpoint identifiers

P0 structural-inspection milestone:

- PR **#1** — `P0 canonical source inspection gate`
- merged commit: `25abe9ac2adb149b40239a2562ab6f056b30f426`
- verified workflow run: `32763754908`
- inspection artifact digest: `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`

Foundation milestone:

- PR **#2** — `Establish earthquake-resistant foundation and chat continuity`
- merged commit: `80a281b0c5f54eff96eb3ae5ea84c49d00c54544`
- final verified PR head: `596016159011ed93347fa66ca31d5bc23ef1b370`
- Foundation verification run: `32765424821` — PASS
- P0 source inspection run: `32765424816` — PASS

The new chat must still inspect current `main` because later work may have occurred after this checkpoint.

---

## N. Definition of successful transfer

A new chat, using only repository state plus this package, must be able to determine:

- what Szondi3 is protecting;
- which evidence is authoritative and immutable;
- which source layers are separate;
- what has passed verification;
- what is still provisional;
- what is machine-enforced;
- what must never be imported from Szondi2;
- what phase/gate is active;
- what the next safe technical task is;
- what conditions require stopping rather than guessing.

No essential answer to those questions should require the old conversation.

---

## Final transfer rule

> **Do not continue from remembered momentum. Reconstruct the state from the repository, verify it, and continue from the lowest unfinished gate.**
