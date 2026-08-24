# SZONDI3 — P0 CANONICAL ACCESS TEST PLAN

**Status:** P0 implementation contract  
**Change class:** `SOURCE_ACCESS`  
**Normative basis:** `docs/CANONICAL_ACCESS_SPEC.md`  
**Real-corpus witness:** `docs/P0_SOURCE_INSPECTION_REPORT.md`

## Purpose

This test plan is derived before extractor implementation. It converts the accepted canonical-access specification and the already verified DOCX structural inspection into executable acceptance tests without consulting Szondi2 exporter code or canonical output.

The extractor is an access/provenance derivative only. Passing these tests cannot establish doctrinal correctness, OCR correctness, or stimulus mapping authority.

## Required test matrix

| Contract area | Required test | Spec basis | Real-corpus reason |
|---|---|---|---|
| Input identity | Reject DOCX bytes whose SHA-256 differs from `config/source_catalog.json` | §§3,16,18 | all ten source identities are locked |
| OOXML part registry | Classify every encountered `word/*.xml` part; reject an unclassified text-capable part | §§5,16 | corpus contains hundreds of story parts plus structural parts |
| Body order | Preserve paragraph/table/paragraph order | §7 | corpus contains substantial tables |
| Tables | Preserve rows, cells, cell coordinates, merge metadata and nested blocks | §7 | `SZ_LEHR_1972`, `SZ_TRIEBPATH_1/2` contain thousands of cells |
| Paragraph controls | Preserve tabs, line breaks and page breaks distinctly | §7 | thousands of tabs occur in the corpus |
| Notes | Emit notes separately, retain note IDs and resolve body references | §§6,8 | hundreds of footnote references occur in several primary works |
| Header/footer stories | Preserve every story part independently, including empty parts | §§6,9 | several sources contain hundreds of header/footer parts |
| Fields | Separate field instruction from displayed result | §10 | verified field instructions and field chars occur in the corpus |
| Hyperlinks | Keep visible text as text and relationship target as metadata | §11 | hyperlinks occur in several admitted sources |
| Bookmarks | Preserve source-native bookmark identity as metadata without turning it into prose | §11 | bookmark starts occur in all major source groups |
| Visual constructs | Preserve object kind, source order, relationships/alt text and set `VISUAL_ARBITRATION_REQUIRED` | §§12,17 | drawings and legacy pictures are common throughout the corpus |
| Text boxes / graphic text | Parse visible text explicitly or fail closed | §12 | visual-object handling is required before trust |
| Alternate content | Preserve explicit branch variants rather than silently choosing/duplicating visible content | §§12,16 | specification requires explicit handling even where synthetic adversarial fixture is needed |
| Unknown content | Fail on unsupported possibly meaningful content rather than silently dropping it | §§5,16,20 | foundational fail-closed invariant |
| Unit identity | Deterministic zero-padded `U######` IDs unique within each stream | §13 | citation addresses must be stable |
| Serialization | UTF-8, LF, deterministic key/record order, no timestamps/random/host paths | §§14,15 | byte-identical reproducibility is a P0 gate requirement |
| Repeated generation | Two clean runs over identical inputs must be byte-identical | §§15,18 | deterministic regeneration is required before Szondi2 comparison |
| Real-corpus smoke | Run the extractor over all ten admitted DOCX files after foundation verification | §§4,18,20 | synthetic tests alone cannot prove coverage of the inspected corpus |

## Synthetic/adversarial fixture requirements

Synthetic DOCX fixtures are generated entirely inside the test suite and contain only the minimum OOXML needed to exercise one contract at a time. At minimum they cover:

1. paragraph -> table -> paragraph ordering;
2. nested table content, `gridSpan`, and vertical merge metadata;
3. resolved and unresolved footnote references;
4. separate non-empty and empty header/footer parts;
5. complex field begin/instruction/separate/result/end;
6. hyperlink relationship metadata;
7. tabs, line breaks and page breaks;
8. drawing/legacy-object provenance and alternative text;
9. text-box visible text;
10. `mc:AlternateContent` with Choice/Fallback variants;
11. an intentionally unknown text-capable element/part that must fail;
12. deterministic repeat extraction;
13. input hash mismatch.

## Real-corpus acceptance behavior

A PR is not accepted merely because synthetic unit tests pass. CI must first run `scripts/verify_foundation.py`, then run the canonical tests, then extract all ten catalogued DOCX sources. If any real source exposes a possibly meaningful construct outside the supported universe, CI must fail and the correct response is to inspect/classify that structure and amend the specification/tests intentionally; it is not acceptable to add a catch-all ignore path.

Primary canonical records must remain source-near and reversible. A secondary TXT view, Szondi2 comparison, doctrine modeling, scoring, or interpretation is outside this test gate.

## Independence rule

Until independent Szondi3 canonical generation is complete and verified, these tests and implementation must not be tuned against Szondi2 exporter behavior, old `P######` addresses, old canonical TXT, or predecessor hash equality.

## Gate consequence

Passing this plan establishes only that the canonical extractor is ready for the next P0 verification steps: repeated clean regeneration, schema/unit/order/provenance checks, real-source spot arbitration, output-hash inventory, and only then `ORACLE_ONLY` predecessor comparison.
