# SZONDI3 — P0 REAL-SOURCE VISUAL ARBITRATION REPORT

**Status:** `PASS — REAL_SOURCE_VISUAL_SPOT_ARBITRATION`  
**Phase:** `P0 — Constitution + Sources`  
**Change class:** `SOURCE_ACCESS / VERIFICATION`  
**P0 overall gate:** `IN_PROGRESS` — **`P0_SOURCES_PASS` is NOT declared**

## 1. Purpose

This report records the required real-source DOCX/canonical-to-PDF visual spot arbitration after independent Szondi3 canonical generation.

The purpose is not to make PDF text a replacement canonical source and not to rewrite source-derived canonical records. The paired admitted PDF is used only as the visual arbiter when layout, signs, profiles, diagrams, figures, reaction notation or OCR-sensitive typography carry meaning that the DOCX-derived canonical stream cannot safely express as plain text.

This verification was performed before any Szondi2 canonical/output comparison. No Szondi2 exporter, canonical TXT or predecessor runtime implementation was consulted.

## 2. Verified inputs

Authoritative repository state used for this arbitration:

- `main` commit: `9e263171e4de4be46df78caa9208e2b433fdf0bc`
- canonical workflow run: `32795960486` — `SUCCESS`
- canonical artifact: `p0-canonical-access`, artifact ID `9544839103`
- visual source artifact: `p0-visual-arbitration-sources`, artifact ID `9544842560`
- visual artifact digest: `sha256:71cfc33815ec0c113ae201de6a76d31a323c4689909a250bbbe738d23d4bffae`
- canonical identity manifest SHA-256: `4629e5730f298043cfd42c541d0d319fecb6da45ec6cb9f8b5a807e91dc59479`

The visual artifact contains the same eight admitted PDF binaries already locked by `config/evidence_lock.json`; it is transport only and is not a new evidence layer.

## 3. Method

The spot arbitration was deliberately stratified rather than random:

1. read the independently generated canonical records and their `visualArbitrationRequired` markers;
2. cover every source that has an admitted paired PDF — six `SZONDI_PRIMARY` works plus Deri and Mélon;
3. select source-near constructs where visual meaning is materially plausible: pedigree, Szondi profile, personality schema, ego-function graph, experimental existence scale, chromatin image/diagram, topological diagram and vector/reaction notation;
4. include one layout-sensitive table whose row/cell structure is canonically represented but whose reaction symbols are typography-sensitive;
5. locate the corresponding passage in the admitted PDF using nearby source text;
6. render the relevant original PDF page and inspect the visual page directly;
7. classify the relationship between canonical text/structure and the original visual evidence.

Text extraction was used only to locate pages. The visual judgment was made from rendered PDF pages, not from OCR or `pdftotext` output.

No canonical JSONL record was modified by this procedure.

## 4. Arbitration observations

| Source | Canonical address(es) | PDF page index / printed page | Visual construct | Arbitration result |
|---|---|---|---|---|
| `SZ_SA_1948` | `BODY:U000609–U000611`, `BODY:U000614–U000617` | PDF 93 / printed 89 | `Stammbaum 1` and `Stammbaum 2` | **PDF_REQUIRED.** The diagrams carry kinship topology, sex/individual markers, numbering and affected-status relationships that are not reconstructible from the empty visual units alone. The surrounding prose is useful but does not replace the pedigree. The PDF confirms the visual marker and also shows that stray source-near symbols beside `Stammbaum 1` are not a substitute for the diagram. |
| `SZ_LEHR_1972` | `BODY:U001097–U001102` | PDF 60 / printed 60 | `Abb. 8. Triebprofil eines Zwangsneurotikers` plus beginning of `Tabelle 3` | **PDF_REQUIRED + TABLE_VISUAL_ARBITRATION.** Exact profile geometry and factor/reaction positions are visual. The table is structurally preserved as rows/cells, but several OCR/source-near reaction glyphs in the DOCX-derived text are degraded. The PDF visibly resolves signs such as plus/minus/null and quantum-pressure notation. Canonical structure is retained; visual typography remains authoritative for the symbols. |
| `SZ_IA_1956_A` | `BODY:U001946–U001950` | PDF 137 / printed 136 | Freud personality decomposition schema | **PDF_REQUIRED + TEXT_AMBIGUITY_RESOLVED.** The diagram contains spatial relations and labels (`ES`, `ICH`, `ÜBER-ICH`, conscious/unconscious regions) not encoded by the empty visual unit. The paired PDF resolves the source-near caption `Abb. j.` as `Abb. 5.` and `Ges. Sehr.` as `Ges. Schr.`. |
| `SZ_IA_1956_B` | `BODY:U001977–U001981` | PDF 185 / printed 443 | `Abb. 17` — Negations-/Destruktionswahn and ego functions | **PDF_REQUIRED + TEXT_AMBIGUITY_RESOLVED.** Bar heights, percentages, rank order and reaction strings are visually meaningful. The PDF resolves `n= 41:180= 22.7’Z»` as `n = 41:180 = 22,7%` and the distorted caption as `Abb. 17. Negations- bzw. Destruktionswahn und Ich-Funktionen`. |
| `SZ_THER_1963_A` | `BODY:U001138–U001147` | PDF 115–116 / printed 115–116 | experimental existence scales, including `Abb. 9` | **PDF_REQUIRED + TEXT_AMBIGUITY_RESOLVED.** The A/B/C panels and occupied grid squares encode the result and cannot be recovered from caption text alone. The PDF resolves `Existen^skala` to `Existenzskala`. The narrative interpretation corresponds to the visible grid patterns. |
| `SZ_THER_1963_B` | `BODY:U000127–U000135` | PDF 21 / printed 285 | female sex-chromatin micrograph and morphology diagram (`Abb. 14–15`) | **PDF_REQUIRED + TEXT_AMBIGUITY_RESOLVED.** The micrograph and four morphology forms are inherently visual. The PDF resolves the heavily degraded source-near heading beginning `Cbromosornengescblechi :$` as `Chromosomengeschlecht` with the female-sign notation and visibly distinguishes the labelled morphology types. |
| `DERI_1949` | `BODY:U000828–U000832` | PDF 189 / printed 170 | `Fig. 8. Topological Representation of the Personality` | **PDF_REQUIRED, TEXTUAL LEGEND CONFIRMED.** Canonical prose correctly retains the caption and the legend that A–F are needs and K is the self/environment boundary. The PDF is still required to preserve the spatial topology of those regions. No source-near caption correction was required in this sample. |
| `MELON_1975` | `BODY:U000716–U000725` | PDF 58 / printed 50 | unitendential contact-vector reaction diagrams | **PDF_REQUIRED + TEXT_AMBIGUITY_RESOLVED.** The circular diagrams contain reaction notation that is not represented by the empty visual units; surrounding prose supplies interpretation but not the complete visual formula. The PDF also resolves `unitend&ntielles` to `unitendantielles`. |

## 5. What the spot arbitration establishes

The sampled visual markers are not false formalities. The paired originals demonstrate three distinct cases that the canonical-access design must preserve:

1. **material visual information not expressible by the surrounding canonical prose** — pedigrees, profiles, grids, topology, micrographs and reaction diagrams;
2. **correct structural extraction with visually sensitive symbol content** — especially `SZ_LEHR_1972` table/profile notation;
3. **source-near DOCX/OCR transcription distortions resolved by the paired original PDF** — including figure numbering, percent signs, captions and typography-sensitive words.

No sampled case revealed a canonical unit-order/provenance failure or an extractor traversal defect. The extractor behaved as designed: it preserved source-near DOCX text, preserved visual-object identity and failed to pretend that an image had been translated into prose.

The discrepancies listed above are therefore **visual arbitration findings, not permission to silently normalize the canonical derivative**.

## 6. Provenance rule for resolved ambiguities

For every ambiguity identified above:

- the immutable admitted DOCX remains the source from which the canonical record was generated;
- the admitted paired PDF is the visual arbitration witness;
- the canonical JSONL is not rewritten in place;
- this reviewed report records the resolution and links it to both the canonical address and PDF page;
- downstream doctrinal work must not quote a visibly corrupted source-near token as if it had been confirmed by the original when this report provides the visual resolution.

This keeps the distinction required by `docs/CANONICAL_ACCESS_SPEC.md`: source evidence, generated derivative and reviewed visual-arbitration event remain separate.

## 7. Residual limitation: Triebpathologie

`SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` have no paired admitted PDF in `config/source_catalog.json`.

Their canonical streams contain many `visualArbitrationRequired` records, but no authorized paired original currently exists to arbitrate them. Those visual ambiguities remain explicitly **UNRESOLVED_NO_PAIRED_PDF**. They must not be guessed from context and must not be backfilled from an unadmitted web copy or predecessor-generated derivative.

This limitation is carried forward to final P0 acceptance.

## 8. Gate result

The repository requirement for **real-source DOCX/PDF visual spot arbitration** is satisfied for the eight admitted DOCX/PDF pairs:

`REAL_SOURCE_VISUAL_SPOT_ARBITRATION = PASS`

This PASS means that the arbitration mechanism was exercised on every paired source and on multiple classes of visually meaningful material, and that concrete ambiguities were resolved with explicit provenance.

It does **not** mean that every visual object in the corpus has been manually interpreted, and it does not remove the unresolved Triebpathologie limitation.

`P0_SOURCES_PASS` remains **NOT DECLARED**.

## 9. Next safe P0 work

Per `docs/PROJECT_CHECKPOINT.md`, after independent canonical generation and real-source visual spot arbitration, the next permitted source task is:

1. inspect Szondi2 canonical witness hashes/text strictly as `ORACLE_ONLY` comparison evidence;
2. compare it against the independently generated Szondi3 canonical derivative;
3. classify every observed difference as source-version difference, serialization difference, structural-preservation improvement, omission/regression, access/OCR difference or unresolved cause;
4. never make equality with Szondi2 a target;
5. after predecessor comparison, independently revalidate the 48-card series/position/factor mapping from authorized primary source evidence;
6. only then evaluate the complete `P0_SOURCES_PASS` gate.

P1 administration/scoring and clinical interpretation remain prohibited until that explicit gate is declared.
