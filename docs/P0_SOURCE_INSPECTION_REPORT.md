# SZONDI3 — P0 SOURCE STRUCTURAL INSPECTION REPORT

**Status:** VERIFIED INSPECTION WITNESS  
**Scope:** admitted 10 DOCX sources  
**Workflow:** `P0 source inspection`, run `32763754908`  
**Result:** `SUCCESS`  
**Artifact:** `p0-docx-inspection`  
**Artifact digest:** `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`

## Purpose

This report records the first independent read-only structural inspection of the admitted DOCX corpus before canonical extraction is implemented. It is evidence about package structure, not a canonical text derivative and not doctrinal interpretation.

The inspection was intentionally performed before extractor implementation so that the extractor specification can be constrained by the actual OOXML structures present in the sources rather than by assumptions inherited from Szondi2.

## Verification outcome

The pull-request workflow completed successfully. It inspected all 10 configured sources and produced a JSON artifact without modifying repository sources.

The source corpus is structurally non-trivial. The documents contain large numbers of tables, footnote references, drawings/legacy pictures, fields and hundreds of header/footer parts. Therefore a paragraph-only or `document.xml`-only extractor would be unsafe as a general canonical-access strategy.

## Structural summary

| sourceId | package parts | paragraphs* | tables* | table cells* | drawings* | legacy pictures* | fields* | footnote refs* |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `SZ_SA_1948` | 515 | 5,818 | 25 | 1,114 | 314 | 202 | 510 | 11 |
| `SZ_LEHR_1972` | 631 | 23,280 | 160 | 13,060 | 379 | 224 | 45 | 285 |
| `SZ_IA_1956_A` | 232 | 5,194 | 24 | 869 | 125 | 99 | 27 | 447 |
| `SZ_IA_1956_B` | 303 | 7,370 | 70 | 2,355 | 167 | 146 | 15 | 202 |
| `SZ_THER_1963_A` | 255 | 3,332 | 5 | 107 | 127 | 102 | 15 | 351 |
| `SZ_THER_1963_B` | 190 | 4,848 | 24 | 525 | 104 | 82 | 9 | 409 |
| `SZ_TRIEBPATH_1` | 474 | 10,586 | 95 | 5,671 | 252 | 194 | 84 | 107 |
| `SZ_TRIEBPATH_2` | 804 | 19,652 | 159 | 8,176 | 359 | 295 | 66 | 128 |
| `DERI_1949` | 1,115 | 4,650 | 11 | 698 | 358 | 333 | 6 | 8 |
| `MELON_1975` | 473 | 5,017 | 16 | 2,068 | 242 | 122 | 27 | 2 |

\* Counts aggregate the inspected `word/*.xml` story parts and are structural witnesses, not semantic content counts.

## Important observations

The corpus contains very large numbers of header/footer story parts. For example, `SZ_SA_1948` contains 234 inspected header parts and 155 footer parts; `DERI_1949` contains 537 header and 539 footer parts. Many may be repetitive or layout-related, but the extractor may not assume that without an explicit inclusion/deduplication rule.

Tables are substantial, especially in `SZ_LEHR_1972`, `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`. Table structure must therefore remain addressable rather than being flattened without provenance.

Footnote references are abundant in several primary works, including 447 in `SZ_IA_1956_A`, 409 in `SZ_THER_1963_B`, 351 in `SZ_THER_1963_A` and 285 in `SZ_LEHR_1972`. Notes cannot be treated as optional decoration.

Drawings and legacy pictures occur throughout the corpus. Their presence does not prove textual meaning, but it establishes that visual elements are common and that canonical text cannot replace PDF/image arbitration for signs, figures, tables or OCR-sensitive typography.

Fields/instruction text also occur. The canonical access layer must define whether each field contributes displayed text, metadata, navigation, page numbering or other non-doctrinal content; it may not silently concatenate raw field instructions into prose.

## What this report does NOT establish

It does not establish that every OOXML element found carries doctrinal meaning. It does not validate OCR correctness. It does not establish page correspondence between DOCX and PDF. It does not authorize omission of story parts merely because their text count is zero in this structural scan. It does not validate stimulus factor mapping.

## Consequence for canonical extraction

Before implementing canonical extraction, Szondi3 must specify and test at least:

- story-part inclusion/exclusion rules;
- body paragraph and table traversal order;
- table row/cell preservation and addressing;
- footnote/endnote addressing and reference linkage;
- header/footer treatment and safe deduplication, if any;
- field/displayed-text handling;
- hyperlinks/bookmarks;
- drawings/pictures and visual-arbitration markers;
- unknown/unsupported OOXML fail-closed behavior;
- stable source-unit identifiers;
- deterministic encoding/order/hash rules.

The structural inspection therefore confirms the central P0 design decision: **canonical access must be source-structure-aware, not a simple text dump.**
