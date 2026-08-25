# SZONDI3 — P0 `ORACLE_ONLY` PREDECESSOR CANONICAL COMPARISON

**Status:** `PASS — ORACLE_COMPARISON_AND_MISMATCH_CLASSIFICATION`  
**Phase:** `P0 — Constitution + Sources`  
**Comparison class:** `ORACLE_ONLY`  
**P0 overall gate:** `IN_PROGRESS` — **`P0_SOURCES_PASS` is NOT declared**

## 1. Purpose and authority boundary

This report records the first comparison between the independently generated Szondi3 canonical derivative and the historical Szondi2 canonical witness.

The comparison was deliberately postponed until both of the following Szondi3-native gates had passed independently:

1. deterministic canonical generation/verification from the admitted Szondi3 DOCX sources;
2. real-source DOCX/PDF visual spot arbitration.

Szondi2 is used here strictly as `ORACLE_ONLY` evidence under `docs/MIGRATION_MANIFEST.md`. Its exporter, normalized text, block identifiers and behavior are not source authority and are not copied into Szondi3 implementation. Equality with the predecessor is not a target.

No Szondi3 extractor rule was changed or tuned in response to this comparison.

## 2. Witness identities

### Szondi3

Comparison baseline after visual arbitration:

- visual-arbitration report merge: `6460c0ff28e899bab11231993bc3d6449260ee96`
- current source-access baseline used for durable DOCX transport: `59f68b02d0f9a30c4c19cb964c4b64a2a12e55d8`
- independent canonical milestone: `f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`
- extractor version: `szondi3-canonical-access/0.1.0`
- extractor Git blob: `cf394843c6c2f05c72e49f89d933890d74e34d5c`
- canonical content manifest SHA-256: `4629e5730f298043cfd42c541d0d319fecb6da45ec6cb9f8b5a807e91dc59479`

### Szondi2 historical oracle

- repository: `danono2016/Szondi2`
- inspected `main`: `66f19b15a328dff01bfb05891a5660c0fd1f5cc5`
- oracle manifest: `CORPUS_MANIFEST.md`
- historical extractor: `scripts/extract_docx_corpus.py`
- extractor SHA-256 recorded by Szondi2: `344fc77ace90fa993c0c834003b86a0d759ba39ce41e205e2ff3754874fb9263`
- old unit form: `[P######][KIND][LOCATION] text`

The predecessor manifest records canonical hashes rather than relying on an imported old TXT file in Szondi3.

## 3. Critical input-identity result

All **eight** DOCX files shared by the two projects have the **same SHA-256** in Szondi2 and Szondi3.

Therefore, for the shared corpus:

`SOURCE_VERSION_DIFFERENCE = 0`

Any canonical difference is attributable to extraction/representation/structural-preservation behavior, not to different source bytes.

Szondi3 additionally admits `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`. Szondi2's corpus manifest explicitly states that Triebpathologie was absent from its available raw corpus. Those two sources therefore have no predecessor canonical oracle and are not forced into a false comparison.

## 4. Oracle regeneration before comparison

The historical Szondi2 extraction behavior was inspected only after the independent Szondi3 gates above had passed.

For comparison, the historical normalized witness was regenerated locally from the byte-identical admitted DOCX inputs. Before any text comparison was accepted, the regenerated outputs were required to reproduce Szondi2's recorded canonical hashes, block counts and normalized character counts.

All eight did so exactly:

| Source | Szondi2 blocks | Szondi2 normalized chars | Regenerated Szondi2 SHA-256 | Witness reproduction |
|---|---:|---:|---|---|
| `SZ_SA_1948` | 5,814 | 1,048,563 | `3fbe1766dffe0460b9923ffaf23004b2cc8926ad0c8c8a992a39d724f1616a8c` | EXACT |
| `SZ_LEHR_1972` | 23,279 | 1,956,809 | `8c6a2bb43214fcfce16146e37e7419e125ce3e989e66bfdf9a7d3de555a1e7fd` | EXACT |
| `SZ_IA_1956_A` | 5,193 | 933,343 | `76e2faa58102a532f21212ad36a1e213d090b0617c940e8733674baf9d190d13` | EXACT |
| `SZ_IA_1956_B` | 7,369 | 1,064,067 | `5b2900b13106b26ee1fc22eb559f943ea79c7c3632f958b41d5f96febe486042` | EXACT |
| `SZ_THER_1963_A` | 3,331 | 883,903 | `04635199a5b2467c3b2173d1b87b163bb9045f2c4651d523f3254c8af96bc4d3` | EXACT |
| `SZ_THER_1963_B` | 4,847 | 975,041 | `14d4a1d7409b8997b54c8c7b1f198110c9519b65dbe3bec645d4d301d86d4a14` | EXACT |
| `DERI_1949` | 4,649 | 854,820 | `f20cf222c20be21d1b3a194e49572e2cb8f3f46b71b4ad7bc83c233b6273ab3b` | EXACT |
| `MELON_1975` | 5,016 | 434,517 | `38011edfaf8ebd34228b0211ba7d0528c279c1f429406ca765c2d4253d96f8a3` | EXACT |

This establishes that the predecessor side of the comparison is a reproduced historical witness rather than an approximation.

The historical extractor was not copied into the Szondi3 repository and does not become Szondi3 implementation.

## 5. Why raw canonical hashes are expected to differ

The two canonical formats have intentionally different semantics and serialization:

- Szondi2 emits a flat, line-oriented normalized TXT with `P######` blocks;
- Szondi3 emits structured JSONL with source-local per-stream `U######` identifiers, hierarchical tables, separate note/story streams and explicit structural/visual metadata.

Consequently, equality of the old TXT SHA-256 and the new JSONL SHA-256 would have no evidentiary meaning.

The current Szondi3 JSONL identities for the eight shared sources are:

| Source | Szondi3 JSONL SHA-256 |
|---|---|
| `SZ_SA_1948` | `c5a0abc75aff24d7fba1f53f958878bc7805ae474f81f35af60cc71ece81f968` |
| `SZ_LEHR_1972` | `568f14f6fa2805d5e045febd8ab80fd3852a4106429eea66727ac205a3bf48e3` |
| `SZ_IA_1956_A` | `6c01a36bf66a1c42d29a654b4da329a9db4d887c02c8ec2fe1116252c6d13b33` |
| `SZ_IA_1956_B` | `7e1b530666d92644aae99ec53831cccdcfba25df425fbb17ba6447f88d348b7b` |
| `SZ_THER_1963_A` | `76133a2f3668c137187731f9b1f824376ce424d4fb963489e52ea21740b674d3` |
| `SZ_THER_1963_B` | `ce594ab1c368517b56a98bacc2d5db8b4f0ef0e60478c4ca83ed80c67a8ac859` |
| `DERI_1949` | `6d452ac913172d76ec79f0a8916dfe280d741e74237813506b451e4d9dce4319` |
| `MELON_1975` | `ad458a802f8b618b2b3263a98ffd0c092bddb30b5b32b1711bec186f6581cd95` |

Classification:

`SERIALIZATION_SCHEMA_DIFFERENCE = EXPECTED / NON-REGRESSION`

## 6. Content-comparison projection

A comparison projection was used only for analysis; it is not a new canonical format and is not committed as authority.

For each shared source, the following textual units were compared in source order:

- all body paragraphs, recursively including paragraphs inside tables;
- all positive footnote/endnote paragraphs, keyed by source-native note ID and paragraph order;
- all header/footer/comment paragraphs in package-part order, including text-box paragraphs represented structurally by Szondi3.

The projection preserves wording, punctuation, Unicode, visible tabs and soft hyphens. It does **not** modernize or normalize source text.

Only two predecessor-specific representation effects were removed before exact string comparison:

### A. Structural tab-stop pollution

The historical Szondi2 walker treated every `w:tab` descendant of a paragraph as visible text. This included `w:tab` elements inside paragraph formatting (`w:pPr/w:tabs`) that define tab stops but are not visible tab characters.

Szondi3 distinguishes visible run-level tabs from paragraph tab-stop definitions. This exact distinction was independently exercised during the Szondi3 real-corpus verifier work.

Across the eight shared sources, the old normalized TXT contained **17,782** such formatting-tab characters:

| Source | Old non-visible formatting tabs serialized as text |
|---|---:|
| `SZ_SA_1948` | 1,761 |
| `SZ_LEHR_1972` | 5,270 |
| `SZ_IA_1956_A` | 2,230 |
| `SZ_IA_1956_B` | 2,104 |
| `SZ_THER_1963_A` | 1,262 |
| `SZ_THER_1963_B` | 2,510 |
| `DERI_1949` | 1,385 |
| `MELON_1975` | 1,260 |

Classification:

`STRUCTURAL_PRESERVATION_IMPROVEMENT` — the predecessor contains formatting artifacts in its textual stream; Szondi3 does not.

### B. Inline note-reference tokens

Szondi2 injected synthetic markers such as `[FN:12]` into paragraph wording and then inserted referenced note text into the flat block stream.

Szondi3 preserves the source paragraph wording separately and stores the note reference as structured metadata linked to separately addressable note records.

The shared sources contain **1,715** predecessor-injected footnote-reference markers.

Classification:

`SERIALIZATION / PROVENANCE REPRESENTATION DIFFERENCE` — not a wording omission.

## 7. Exact comparable-content result

After accounting for only the two documented representation differences above, the textual projection matches **exactly** across the complete shared corpus:

| Source | Body paragraphs | Positive note paragraphs | Peripheral paragraphs | Total compared | Text mismatches |
|---|---:|---:|---:|---:|---:|
| `SZ_SA_1948` | 4,989 | 12 | 813 | 5,814 | **0** |
| `SZ_LEHR_1972` | 22,031 | 332 | 916 | 23,279 | **0** |
| `SZ_IA_1956_A` | 4,324 | 477 | 392 | 5,193 | **0** |
| `SZ_IA_1956_B` | 6,580 | 223 | 566 | 7,369 | **0** |
| `SZ_THER_1963_A` | 2,510 | 399 | 422 | 3,331 | **0** |
| `SZ_THER_1963_B` | 4,028 | 499 | 320 | 4,847 | **0** |
| `DERI_1949` | 2,898 | 9 | 1,742 | 4,649 | **0** |
| `MELON_1975` | 4,428 | 3 | 585 | 5,016 | **0** |
| **TOTAL** | **51,788** | **1,954** | **5,756** | **59,498** | **0** |

Therefore, for all textual content represented by the historical Szondi2 canonical corpus:

`POTENTIAL_TEXT_OMISSION_OR_REGRESSION = 0 detected`

This is stronger than raw-hash equality would have been because the comparison deliberately allows the new representation to remain structurally richer while testing the inherited textual content exhaustively.

## 8. Structural differences classified

The remaining observed differences are expected improvements or representation changes:

### `STRUCTURAL_PRESERVATION_IMPROVEMENT`

Szondi3 preserves information that the predecessor flattened or reduced to text/location labels, including:

- hierarchical tables, nested blocks, cell coordinates and merge metadata;
- row structural metadata such as reviewed `w:tblPrEx`;
- separate header/footer story-part identity, including empty parts;
- source-native note identity as separate streams;
- field boundaries/events, instructions and displayed results;
- hyperlink target provenance and bookmarks;
- drawings, legacy pictures, embedded objects, text boxes and `mc:AlternateContent` branches;
- explicit `visualArbitrationRequired` markers rather than a drawing counter only.

The content comparison shows that these additions were not purchased by dropping the old textual wording.

### `SOURCE_COVERAGE_IMPROVEMENT`

Szondi3 contains two admitted Szondi-primary DOCX sources absent from the predecessor canonical corpus:

- `SZ_TRIEBPATH_1`
- `SZ_TRIEBPATH_2`

They have independently generated Szondi3 canonical records but no Szondi2 oracle counterpart.

### `SOURCE_ACCESS / OCR DIFFERENCE`

For the eight shared DOCX files: **none at input level**. The bytes are identical.

The separate PDF visual-arbitration report documents source-near OCR/DOCX distortions that the admitted PDF can resolve. Those distortions are inherited from the shared DOCX source access and therefore are not a Szondi3-vs-Szondi2 extraction regression.

### `OMISSION / REGRESSION`

**None detected in the complete comparable textual projection.**

### `UNRESOLVED ORACLE MISMATCH`

**None for the eight shared textual corpora.**

The absence of a predecessor Triebpathologie oracle is a coverage limitation, not a mismatch. Their separate lack of paired admitted PDFs remains the visual limitation already recorded by P0.

## 9. What was deliberately not inherited

The following predecessor properties remain historical witness behavior only:

- `P######` identifiers;
- flat insertion of notes into body sequence;
- synthetic `[FN:id]` prose markers;
- formatting-tab pollution;
- old chunk boundaries/405-chunk reading ledger;
- predecessor exporter/verifier implementation;
- predecessor canonical TXT serialization.

None becomes Szondi3 runtime or canonical authority.

## 10. Gate result

The required post-independent-generation predecessor comparison and mismatch classification is complete:

`ORACLE_COMPARISON_AND_MISMATCH_CLASSIFICATION = PASS`

The result is:

- byte-identical shared source inputs: **8/8**;
- historical oracle reproduction: **8/8 exact hashes**;
- comparable textual units checked: **59,498**;
- unexplained textual mismatches: **0**;
- detected textual omission/regression: **0**;
- predecessor formatting artifacts explicitly classified: **17,782**;
- predecessor synthetic note-reference tokens explicitly classified: **1,715**;
- additional Szondi3 primary sources without predecessor oracle: **2**.

This PASS does **not** declare `P0_SOURCES_PASS`.

## 11. Next safe P0 work

The next unfinished P0 source gate is independent revalidation of the 48-card series/position/factor mapping from authorized primary source evidence.

After that revalidation, P0 must record residual limitations — especially the lack of paired admitted PDFs for `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` — and evaluate the complete P0 acceptance boundary.

Only if those remaining conditions pass may the explicit `P0_SOURCES_PASS` gate be considered.

P1 administration/scoring remains prohibited until that explicit gate.
