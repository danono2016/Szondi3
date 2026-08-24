# SZONDI3 — CANONICAL ACCESS SPECIFICATION

**Status:** AUTHORITATIVE P0 SPECIFICATION  
**Applies to:** admitted DOCX documentary sources in `sources/text/`

## 1. Purpose

The canonical access layer exists to make admitted documentary sources deterministically addressable, searchable and citable. It is an access/provenance derivative, not a doctrinal authority and not a correction of the source.

The source hierarchy remains:

`original documentary source -> canonical access derivative -> doctrine registry -> executable interpretation`

A canonical derivative may never silently modernize, correct, translate, simplify or reconcile source text.

## 2. Clean-restart rule

Szondi3 does not copy or adapt the Szondi2 exporter, verifier, canonical TXT files or P###### addressing scheme as implementation authority.

The old Szondi2 canonical hashes may be consulted only after Szondi3 independently generates and verifies its own output. Equality is evidence of reproducibility; difference triggers investigation and does not automatically make either side correct.

## 3. Inputs

Only source files explicitly admitted in `docs/SOURCE_ASSET_MANIFEST.md` may enter canonical extraction.

Before extraction, the input file identity must be checked against the admitted source catalog. Unknown DOCX files are rejected rather than included opportunistically.

The extractor must never read PDFs as textual authority. PDFs are a separate visual-arbitration channel for OCR-sensitive typography, signs, formulas, tables and layout when available.

## 4. Inspection before extraction

Before the first canonical extractor is finalized, Szondi3 must inspect the real OOXML structure of all ten admitted DOCX files.

The inspection must inventory at minimum:
- package parts under `word/`;
- main body paragraphs and tables;
- footnotes and endnotes;
- headers and footers;
- comments;
- text runs;
- tabs and explicit line/page breaks;
- symbols represented outside ordinary `w:t` text;
- field instructions/results;
- mathematical content;
- drawings/pictures/alternate content capable of carrying or replacing textual information;
- hyperlinks/bookmarks where they affect addressability;
- any unexpected text-bearing XML part.

No content class may be silently ignored merely because an earlier exporter did not handle it.

## 5. Canonical streams

Canonical access distinguishes source streams rather than flattening everything into one text:

- `BODY` — main document body, including table content in document order;
- `FOOTNOTE` — footnote text;
- `ENDNOTE` — endnote text;
- `HEADER` — header text;
- `FOOTER` — footer text;
- `COMMENT` — comment text when present;
- `AUXILIARY` — any other admitted text-bearing stream discovered by inspection and explicitly supported.

`BODY`, `FOOTNOTE` and `ENDNOTE` are doctrinal-access candidates. Header/footer/comment/auxiliary streams remain separately labeled and may not be silently merged into doctrine.

## 6. Structural preservation

Document order must be deterministic.

Paragraphs and table structures remain distinguishable. A table must not be reduced to an unmarked sequence of words. Row and cell boundaries must be represented explicitly in machine-readable output.

Explicit source tabs and line breaks must remain distinguishable from ordinary spaces. Mechanical OOXML packaging boundaries may be normalized only when they do not alter visible/source semantics.

The extractor must preserve Unicode characters as decoded from the admitted DOCX. It must not perform spelling correction, typographic modernization, language normalization, German orthography modernization or psychological terminology substitution.

## 7. Source units and identifiers

Szondi3 defines its own canonical unit identifiers.

A unit identifier is source-local, deterministic and zero-padded:

`U000001`, `U000002`, ...

Units are assigned in deterministic order within each labeled stream and never reused for a different unit in the same immutable source version.

A citation address consists at minimum of:

`sourceId + stream + unitId`

Example:

`SZ_LEHR_1972:BODY:U001842`

Machine-readable units also retain structural path/kind information so that a paragraph, table row/cell, note or other structure is not confused with another kind.

The old Szondi2 `P######` identifiers remain comparison witnesses only and are not inherited as Szondi3 source identity.

## 8. Machine-readable canonical output

The primary canonical derivative is structured data, not a plain-text blob.

Each source produces a deterministic JSONL or equivalently strict record stream containing at minimum:
- canonical schema version;
- `sourceId`;
- input source filename;
- input SHA-256;
- stream;
- unitId;
- structural kind;
- structural path or coordinates where applicable;
- source text;
- explicit table cells/coordinates where applicable;
- note/comment identifier where applicable.

A human-readable TXT rendering may be generated secondarily from the structured canonical records, but the TXT renderer may not become the primary source of structural truth.

## 9. Fail-closed requirements

Canonical extraction fails rather than approximates when:
- an admitted input is missing or its identity differs;
- required OOXML is malformed;
- a text-bearing source part is discovered but not classified;
- a source construct capable of materially changing visible text is unsupported;
- a note/comment reference cannot be resolved when resolution is required;
- unit identifiers duplicate or ordering is nondeterministic;
- output cannot be regenerated byte-for-byte from identical inputs, extractor version and environment assumptions.

Warnings may document non-material features, but they may not substitute for failure on possible text loss.

## 10. Visual arbitration

When canonical DOCX text is ambiguous for a sign, reaction formula, mathematical symbol, table, diagram, ordering or layout-sensitive statement, the paired original PDF is the visual arbiter if available.

Visual arbitration must be recorded as an explicit provenance event. PDF inspection does not silently rewrite the immutable DOCX-derived canonical record; corrections/annotations, if later authorized, live in a separate reviewed layer linked to both representations.

For `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`, no paired predecessor PDF is presently admitted. Any visual ambiguity there remains explicitly unresolved unless a new authorized original is later admitted.

## 11. Verification

P0 canonical verification requires:
- deterministic regeneration on repeated runs;
- source identity verification;
- schema validation;
- unit uniqueness and ordering validation;
- explicit inventory of extracted and non-doctrinal streams;
- tests for paragraph, table, note, symbol and break handling based on synthetic DOCX fixtures;
- inspection of all real admitted DOCX package structures;
- no silently unhandled text-bearing constructs.

Only after these pass may the new canonical output be compared with Szondi2 canonical hashes or text as `ORACLE_ONLY` evidence.

## 12. Repository policy

CI for this layer is read-only. It may inspect, extract, verify and upload artifacts for review, but it may not automatically commit generated canonical derivatives or state files.

Generated artifacts become repository content only after an explicit architectural decision and verification procedure.

## Final invariant

> **Canonical access must lose as little source information as technically possible, must label every transformation it makes, and must never convert extraction convenience into doctrinal meaning.**
