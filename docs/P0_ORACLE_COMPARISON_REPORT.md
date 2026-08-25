# P0 ORACLE_ONLY canonical comparison report

**Date:** 2026-08-25  
**Phase:** P0 — Constitution + Sources  
**Status:** `PASS_RECORDED` for the predecessor-comparison requirement  
**Authority rule:** Szondi2 is `ORACLE_ONLY`; equality with predecessor output is not a target and predecessor material does not become source authority.

## 1. Purpose and sequencing

This report records the comparison required after the independent Szondi3 canonical-access implementation and real-source visual spot arbitration.

The sequencing constraint was respected:

1. Szondi3 canonical access was specified, implemented and verified independently from Szondi2.
2. The final independent extractor was merged through PR #6 as `f8a71972f06bb28b5ecc99ac9feb8f3e27af3110`.
3. Real-source DOCX/PDF visual spot arbitration was then completed and recorded in `docs/P0_VISUAL_ARBITRATION_REPORT.md`.
4. Only after those gates were complete was the Szondi2 canonical extractor/witness inspected for comparison.

No Szondi2 code/output was used to design, tune or repair the Szondi3 extractor.

## 2. Comparable predecessor corpus

Szondi2 has canonical witnesses for eight source files only:

- `SZ_SA_1948`
- `SZ_LEHR_1972`
- `SZ_IA_1956_A`
- `SZ_IA_1956_B`
- `SZ_THER_1963_A`
- `SZ_THER_1963_B`
- `DERI_1949`
- `MELON_1975`

`SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` were absent from the Szondi2 raw corpus and therefore have no valid predecessor canonical witness. Their comparison status is:

`NOT_COMPARABLE_PREDECESSOR_ABSENT`

They must not be reconstructed from citations or secondary sources.

For all eight comparable sources, the raw DOCX SHA-256 recorded by Szondi2 is identical to the admitted Szondi3 DOCX SHA-256. The comparison therefore concerns two derivative representations generated from the same input bytes.

## 3. Qualification of the Szondi2 witness

The Szondi2 witness was not trusted merely because hashes were recorded in the predecessor repository.

The predecessor extraction algorithm was inspected only after the independence gate. The eight admitted/common DOCX files were then supplied unchanged from the Szondi3 evidence boundary, and the predecessor canonical projection was regenerated locally.

The regenerated result matched the recorded Szondi2 witness simultaneously on canonical block count, character count and SHA-256 for all eight sources:

| source | blocks | canonical chars | regenerated Szondi2 SHA-256 |
|---|---:|---:|---|
| `SZ_SA_1948` | 5,814 | 1,048,563 | `3fbe1766dffe0460b9923ffaf23004b2cc8926ad0c8c8a992a39d724f1616a8c` |
| `SZ_LEHR_1972` | 23,279 | 1,956,809 | `8c6a2bb43214fcfce16146e37e7419e125ce3e989e66bfdf9a7d3de555a1e7fd` |
| `SZ_IA_1956_A` | 5,193 | 933,343 | `76e2faa58102a532f21212ad36a1e213d090b0617c940e8733674baf9d190d13` |
| `SZ_IA_1956_B` | 7,369 | 1,064,067 | `5b2900b13106b26ee1fc22eb559f943ea79c7c3632f958b41d5f96febe486042` |
| `SZ_THER_1963_A` | 3,331 | 883,903 | `04635199a5b2467c3b2173d1b87b163bb9045f2c4651d523f3254c8af96bc4d3` |
| `SZ_THER_1963_B` | 4,847 | 975,041 | `14d4a1d7409b8997b54c8c7b1f198110c9519b65dbe3bec645d4d301d86d4a14` |
| `DERI_1949` | 4,649 | 854,820 | `f20cf222c20be21d1b3a194e49572e2cb8f3f46b71b4ad7bc83c233b6273ab3b` |
| `MELON_1975` | 5,016 | 434,517 | `38011edfaf8ebd34228b0211ba7d0528c279c1f429406ca765c2d4253d96f8a3` |

This qualifies the regenerated predecessor text as a reproducible comparison witness, not as authority.

## 4. Comparison method

A raw byte comparison between the Szondi2 TXT witness and Szondi3 JSONL would be meaningless because the representations intentionally differ.

The comparison therefore used a source-near common projection and preserved distinctions rather than normalizing them away:

- body paragraphs were compared in source document order;
- table paragraphs were traversed in their source order while Szondi3 retained the table hierarchy;
- soft hyphens and visible run-level tabs were reconstructed from Szondi3 segments and compared character-for-character;
- footnote/endnote reference IDs and order were compared separately from paragraph wording;
- positive note text was compared by source-native note ID and paragraph order;
- header/footer paragraphs were compared by OOXML story-part identity and paragraph order;
- AlternateContent/text-box paragraph wording was included in both projections;
- no spelling correction, OCR correction, modernization, case folding, punctuation normalization or whitespace normalization was applied.

Where the predecessor extractor itself inserted non-source-visible material, that material was classified rather than treated as a Szondi3 defect.

## 5. Result — source-visible wording

After classification of predecessor-only technical artifacts, the common textual projection has:

**0 unexplained textual mismatches across all eight comparable sources.**

This includes body text, table-contained text, positive footnote/endnote text, and header/footer text.

Per-source body comparison:

| source | body paragraphs | source tables | note refs | unexplained text mismatches |
|---|---:|---:|---:|---:|
| `SZ_SA_1948` | 4,989 | 25 | 11 | 0 |
| `SZ_LEHR_1972` | 22,031 | 160 | 285 | 0 |
| `SZ_IA_1956_A` | 4,324 | 24 | 447 | 0 |
| `SZ_IA_1956_B` | 6,580 | 70 | 202 | 0 |
| `SZ_THER_1963_A` | 2,510 | 5 | 351 | 0 |
| `SZ_THER_1963_B` | 4,028 | 24 | 409 | 0 |
| `DERI_1949` | 2,898 | 11 | 8 | 0 |
| `MELON_1975` | 4,428 | 16 | 2 | 0 |

The reference comparison covered 1,715 footnote/endnote references. The source-native IDs and their paragraph-level order matched exactly.

All 335 source tables in the eight comparable files were present in Szondi3. The predecessor flattened their paragraphs; Szondi3 preserves the table hierarchy.

## 6. Classified predecessor differences

### 6.1 `ORACLE_STRUCTURAL_TAB_LEAK`

The principal apparent text mismatch came from the Szondi2 extractor treating every OOXML `w:tab` descendant as visible text. This includes `w:pPr/w:tabs/w:tab`, which is a paragraph-formatting tab-stop definition, not a typed tab character.

Consequently, the predecessor witness contains non-source-visible tab characters. Across its 59,498 canonical blocks, this affected 14,426 blocks and injected 16,532 structural tab-stop definitions as literal text tabs.

| source | affected predecessor blocks | leaked structural tabs |
|---|---:|---:|
| `SZ_SA_1948` | 1,314 | 1,417 |
| `SZ_LEHR_1972` | 4,432 | 5,162 |
| `SZ_IA_1956_A` | 1,810 | 2,198 |
| `SZ_IA_1956_B` | 1,888 | 2,068 |
| `SZ_THER_1963_A` | 1,057 | 1,226 |
| `SZ_THER_1963_B` | 2,345 | 2,454 |
| `DERI_1949` | 767 | 777 |
| `MELON_1975` | 813 | 1,230 |

The classification was verified against the raw OOXML per paragraph. Exactly the number of `w:pPr//w:tab` formatting nodes was removed from the corresponding predecessor paragraph prefix. After this source-derived correction, all remaining visible tabs matched Szondi3 exactly.

This is a predecessor extraction artifact, not a Szondi3 loss.

### 6.2 `REFERENCE_REPRESENTATION`

Szondi2 injects tokens such as `[FN:2]` and `[EN:3]` into its normalized wording. Those bracketed strings do not occur as visible source text; they are extractor markers.

Szondi3 keeps the visible text unchanged and records the same source-native reference IDs separately in paragraph `references` metadata.

All 1,715 comparable reference occurrences matched by kind, ID and paragraph order.

This is a representation difference, not a content mismatch.

### 6.3 `SPECIAL_NOTE_CLASSIFICATION`

In seven of the eight comparable DOCX files, the Word package uses positive source-native note ID `1` for an empty continuation-separator note. The predecessor's rule retains any positive note ID and therefore serializes that structural separator as one blank unreferenced footnote block.

Szondi3 preserves the same package object but classifies it explicitly as `noteType: continuationSeparator` instead of treating it as doctrinal note text.

No source-visible text is lost.

### 6.4 `STRUCTURAL_ENRICHMENT_NOT_MISMATCH`

Szondi2 deliberately produces a reading-oriented flat textual witness. Szondi3 preserves additional source structure required by `CANONICAL_ACCESS_SPEC.md`, including:

- hierarchical table rows/cells and merge metadata;
- separate note streams with source-native IDs;
- explicit header/footer story-part identity, including empty parts;
- fields and field lifecycle/result metadata;
- hyperlinks and bookmarks;
- drawing/legacy-picture/object metadata;
- text boxes;
- AlternateContent Choice/Fallback branches without silently choosing one;
- visual-arbitration markers;
- structural properties such as row/table exceptions where source-near structure may matter.

Absence of those structures from the predecessor flat TXT witness is not evidence against Szondi3. Conversely, predecessor equality must never be used as a reason to remove this information from Szondi3.

## 7. Relationship to visual arbitration

Textual agreement with the predecessor does **not** mean that the DOCX wording is always visually faithful to the printed source.

The preceding PDF arbitration found real source-near distortions around figures, captions, percentages, reaction notation and other layout-sensitive material. Those findings remain authoritative for visual arbitration and are recorded in `docs/P0_VISUAL_ARBITRATION_REPORT.md`.

Therefore:

- this report validates the independent extraction relationship between Szondi3 and the reproducible predecessor witness;
- it does not cancel PDF-based visual findings;
- the canonical derivative must not be silently rewritten to imitate either the predecessor or the PDF;
- visually resolved readings remain explicit arbitration evidence downstream from the immutable source bytes.

## 8. Findings about the Szondi3 extractor

The ORACLE_ONLY comparison found **no verified textual traversal, ordering or source-provenance defect that requires a change to `scripts/canonical_access.py`**.

The strongest result is not that Szondi3 equals Szondi2. It is that, after independently identifying and removing only predecessor-generated non-source-visible artifacts, the source-visible textual projection agrees completely while Szondi3 retains substantially richer structure.

No extractor tuning was performed as a consequence of predecessor comparison.

## 9. Residual limitations

This comparison does not cover:

- `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`, because Szondi2 had no corresponding raw/canonical corpus;
- visual truth beyond the separately recorded PDF arbitration;
- the 48-card series/position/factor mapping;
- doctrine registry construction, interpretation, scoring or any P1 concern.

The absence of a predecessor witness for Triebpathologie is recorded uncertainty, not permission to infer one.

## 10. Gate consequence

The P0 predecessor canonical-comparison requirement is satisfied:

`P0_ORACLE_COMPARISON_PASS`

This does **not** imply `P0_SOURCES_PASS`.

The next unfinished P0 gate is independent primary-source revalidation of the 48-card series/position/factor mapping, followed by residual-limitations review and evaluation of the complete P0 acceptance conditions.

P1 remains blocked until an explicit repository-recorded `P0_SOURCES_PASS` is reached.
