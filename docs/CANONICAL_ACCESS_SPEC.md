# SZONDI3 — CANONICAL ACCESS SPECIFICATION

**Status:** AUTHORITATIVE P0 SPECIFICATION  
**Applies to:** admitted DOCX documentary sources in `sources/text/`

## 1. Purpose

The canonical access layer exists to make admitted documentary sources deterministically addressable, searchable and citable. It is an access/provenance derivative, not a doctrinal authority and not a correction of the source.

The source hierarchy remains:

`original documentary source -> canonical access derivative -> deterministic/formal use -> doctrine registry -> executable interpretation`

A canonical derivative may never silently modernize, correct, translate, simplify or reconcile source text.

## 2. Clean-restart rule

Szondi3 does not copy or adapt the Szondi2 exporter, verifier, canonical TXT files or `P######` addressing scheme as implementation authority.

The old Szondi2 canonical hashes may be consulted only after Szondi3 independently generates and verifies its own output. Equality is evidence of reproducibility; difference triggers investigation and does not automatically make either side correct.

## 3. Inputs

Only source files explicitly admitted in `docs/SOURCE_ASSET_MANIFEST.md` and `config/source_catalog.json` may enter canonical extraction.

Before extraction, input identity must be checked against the admitted source catalog/evidence lock. Unknown DOCX files are rejected rather than included opportunistically.

The extractor must never read PDFs as substitute textual authority. PDFs are a separate visual-arbitration channel for OCR-sensitive typography, signs, formulas, tables and layout when available.

## 4. Inspection-before-extraction gate

Before the first canonical extractor is accepted, Szondi3 must inspect the real OOXML structure of all ten admitted DOCX files.

That gate has now been executed successfully. The verified witness is `docs/P0_SOURCE_INSPECTION_REPORT.md`; workflow run `32763754908` produced artifact digest `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`.

The inspection established that the corpus contains substantial tables, footnote references, fields, drawings/legacy pictures and very large numbers of header/footer story parts. Therefore neither a `document.xml`-only parser nor a paragraph-only text dump is acceptable.

Future extractor changes must preserve structural-inspection coverage. If new admitted source versions introduce previously unseen potentially meaningful constructs, the extractor returns to specification/review before silently accepting them.

## 5. OOXML part classification registry

Every `word/*.xml` part encountered must be assigned deterministically to one of:

- `SUPPORTED_DOCTRINAL_CANDIDATE` — body/notes or other explicitly approved text-bearing content;
- `SUPPORTED_NON_DOCTRINAL` — headers, footers, comments or metadata-like story content preserved separately;
- `SUPPORTED_STRUCTURAL` — styles/settings/numbering/relationships needed to interpret supported content but not emitted as prose;
- `SUPPORTED_VISUAL_REFERENCE` — drawings/pictures/objects preserved as explicit visual references;
- `IGNORABLE_PROVEN_NON_TEXTUAL` — a construct explicitly reviewed and documented as non-content-bearing for this corpus/version;
- `UNSUPPORTED_POSSIBLY_MEANINGFUL` — extraction failure.

There is no implicit “other = ignore” branch.

The extractor/verifier must be able to emit an inventory of encountered part names and relevant element/tag classes so a new source structure is visible during review.

## 6. Canonical streams

Canonical access distinguishes source streams rather than flattening everything into one text:

- `BODY` — main document body, including paragraph/table structures in document order;
- `FOOTNOTE` — footnote text keyed to source note identity;
- `ENDNOTE` — endnote text keyed to source note identity;
- `HEADER` — header text, preserved by story-part identity;
- `FOOTER` — footer text, preserved by story-part identity;
- `COMMENT` — comment text when present;
- `AUXILIARY` — any other explicitly supported text-bearing stream discovered by inspection.

`BODY`, `FOOTNOTE` and `ENDNOTE` are doctrinal-access candidates. Header/footer/comment/auxiliary streams remain separately labeled and may not be silently merged into doctrine.

## 7. Body traversal and structural preservation

Traversal order must follow OOXML document order deterministically.

Body paragraphs and tables remain distinguishable. A table is represented hierarchically: table identity -> row -> cell -> contained blocks/runs. It must not be reduced to an unmarked sequence of words. Merged cells, cell coordinates/order and nested content must be represented or explicitly rejected if unsupported.

Paragraph boundaries are canonical structure, not merely whitespace. Explicit source tabs, line breaks and page breaks remain distinguishable from ordinary spaces/newlines when represented in OOXML.

Mechanical run fragmentation may be normalized only where concatenation is demonstrably equivalent to displayed text. The extractor must not insert spaces merely because OOXML split one word into multiple runs.

Unicode is preserved as decoded from the admitted DOCX. No spelling correction, typographic modernization, language normalization, German orthography modernization or psychological terminology substitution is permitted.

## 8. Notes and references

Footnotes/endnotes are emitted as separate canonical units retaining their source note identifier. Body references retain links to that note identity.

Reference order and note-body order are both preserved. A reference that cannot be resolved to the relevant note part is a failure unless it is one of the explicitly recognized OOXML separator/continuation-note constructs.

The canonical layer must never inline a note into body prose in a way that destroys the distinction between authored body text and note text.

## 9. Headers and footers

The structural inspection found hundreds of header/footer parts in several sources. They may contain page numbers, running titles, repeated publication text, images or other layout artifacts.

Canonical extraction therefore preserves each header/footer story part independently with its part identity and extracted visible content/reference inventory.

**No destructive deduplication is permitted in the primary canonical records.** A secondary search/view layer may later collapse byte/text-identical repetitions, but it must retain links to every original story-part occurrence and may not become the primary provenance record.

Empty header/footer parts remain structurally inventoried even if they produce no text unit.

## 10. Fields and displayed text

OOXML fields are not ordinary prose. The extractor must distinguish:

- field instruction/code;
- field result/displayed content;
- field boundaries/state.

Displayed field result may be emitted in its structural context when it forms visible source content. Field instruction text must not be concatenated into prose by default.

Common navigational/layout fields such as page numbering or table-of-contents machinery require an explicit classification rule. Unknown field instructions with possible semantic effect cause failure or a reviewed unsupported marker.

## 11. Hyperlinks, bookmarks and identifiers

Hyperlink visible text remains source text. Relationship targets are metadata attached to the relevant structural unit; they are not silently injected into prose.

Bookmarks are preserved when needed for stable linking/navigation but do not themselves become doctrinal text.

Source-native identifiers (note IDs, relationship IDs, bookmark names) may be stored as provenance attributes but are not assumed globally stable across source versions.

## 12. Drawings, pictures, objects and alternate content

The verified corpus contains many drawings/legacy pictures. Canonical text does not pretend to translate visual content into prose.

For every visual/object construct encountered in a doctrinal candidate stream, canonical records must preserve at minimum:

- containing structural unit;
- relationship/object identity where available;
- object kind;
- source order position;
- any explicit textual alternative/title/description exposed by OOXML;
- a `VISUAL_ARBITRATION_REQUIRED` marker when visual content may carry meaning not represented in text.

Text boxes, embedded objects, alternate-content branches or graphic text capable of carrying visible text must be parsed explicitly or fail closed. An image placeholder with no provenance is insufficient.

## 13. Source units and identifiers

Szondi3 defines its own canonical unit identifiers.

A unit identifier is source-local, deterministic and zero-padded:

`U000001`, `U000002`, ...

Units are assigned deterministically within each labeled stream according to the accepted traversal algorithm and never reused for a different unit in the same immutable source version/schema.

A citation address consists at minimum of:

`sourceId + stream + unitId`

Example:

`SZ_LEHR_1972:BODY:U001842`

Machine-readable units also retain structural kind/path/coordinates so paragraphs, tables, cells, notes and visual references cannot be confused.

The old Szondi2 `P######` identifiers remain comparison witnesses only and are not inherited as Szondi3 source identity.

## 14. Machine-readable canonical output

The primary canonical derivative is structured data, not a plain-text blob.

Each source produces a deterministic JSONL (or an equivalently strict versioned record stream selected before implementation) containing at minimum:

- canonical schema version;
- extractor version/identity;
- `sourceId` and doctrinal layer;
- input source filename and SHA-256;
- stream;
- unitId;
- structural kind;
- structural path/coordinates;
- source text where applicable;
- explicit table coordinates where applicable;
- note/comment/source-native identifier where applicable;
- field/visual-reference metadata where applicable;
- explicit unresolved/visual-arbitration flags.

A human-readable TXT rendering may be generated secondarily from structured canonical records, but the TXT renderer may not become the primary source of structural truth.

## 15. Canonical serialization

When byte-identical determinism is claimed, serialization rules must be fixed before acceptance:

- UTF-8 encoding;
- one declared newline convention;
- deterministic object key/order policy;
- deterministic record order;
- no timestamps, random IDs, host paths or environment-specific metadata in hashed canonical content;
- final-newline policy;
- stable escaping/Unicode policy.

Operational build metadata may be stored separately from the hashed semantic canonical stream.

## 16. Fail-closed requirements

Canonical extraction fails rather than approximates when:

- an admitted input is missing or its identity differs;
- required OOXML is malformed;
- a text-bearing/possibly meaningful source part is discovered but unclassified;
- a visible-text construct is unsupported;
- a note/comment reference cannot be resolved where resolution is required;
- a table structure cannot be represented without structural loss;
- a field/alternate-content/text-box construct could alter displayed meaning but is unsupported;
- unit identifiers duplicate or ordering is nondeterministic;
- output cannot be regenerated byte-for-byte from identical inputs, extractor version and declared environment assumptions.

Warnings may document proven non-material features, but they may not substitute for failure on possible information loss.

## 17. Visual arbitration

When canonical DOCX text is ambiguous for a sign, reaction formula, mathematical symbol, table, diagram, ordering or layout-sensitive statement, the paired original PDF is the visual arbiter if available.

Visual arbitration is recorded as an explicit provenance event. PDF inspection does not silently rewrite immutable DOCX-derived canonical records; corrections/annotations, if authorized later, live in a separate reviewed layer linked to both representations.

For `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2`, no paired predecessor PDF is presently admitted. Any visual ambiguity there remains explicitly unresolved unless a new authorized original is later admitted.

## 18. Verification requirements

P0 canonical verification requires:

- foundation/evidence-lock verification first;
- deterministic regeneration on repeated clean runs;
- schema validation;
- unit uniqueness/order validation;
- explicit inventory of extracted, non-doctrinal, structural, visual and ignored-proven-nontextual constructs;
- tests for body paragraphs, tables, nested structure, notes, tabs/breaks, fields, hyperlinks, header/footer stories, drawings/visual markers and unknown-construct failure;
- source-derived real-corpus spot checks in addition to synthetic fixtures;
- no silently unhandled possibly meaningful constructs;
- output content hashes recorded after independent generation.

Only after these pass may the new canonical output be compared with Szondi2 canonical hashes or text as `ORACLE_ONLY` evidence.

A difference from Szondi2 is not itself failure. The difference must be classified: source-version difference, serialization difference, structural-preservation improvement, omission/regression, OCR/access difference or unresolved cause.

## 19. Repository policy

CI for this layer is read-only. It may inspect, extract, verify and upload artifacts for review, but it may not automatically commit generated canonical derivatives or state files.

Generated artifacts become repository content only after an explicit architectural decision and verification procedure.

## 20. Acceptance boundary

The extractor implementation is not accepted merely because it runs on all ten documents. Acceptance requires proving that its supported universe matches this specification and the inspected corpus, and that anything outside that universe is surfaced rather than dropped.

The canonical layer should be boring, strict and reversible: it preserves access and provenance; it does not interpret psychology.

## Final invariant

> **Canonical access must lose as little source information as technically possible, must label every transformation it makes, and must never convert extraction convenience into doctrinal meaning.**
