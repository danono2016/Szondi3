# P2A Batch 007 — Schicksalsanalyse: genische Erscheinungsformen und fünf Hauptformen des Genotropismus

**Batch:** `P2A-SA-007`  
**Source:** `SZ_SA_1948` — `SZONDI_PRIMARY`  
**Canonical range:** `BODY U000411-U000433`  
**Registry entries:** 24 (`DR_SZ_SA_1948_000203`–`DR_SZ_SA_1948_000226`)  
**Review state:** `SOURCE_VERIFIED`; clinician/steward review remains required before P2A gate closure.

## Scope

This source-order batch covers the section `Zwei Erscheinungsformen der genischen Bestrebungen` and the complete section `Die fünf Hauptformen des Genotropismus`. It ends at U000433. U000434 begins the next true section, `Die Gen-Quantitätstheorie und die multiple Allelie`.

The batch preserves the distinction between `genotypische Erscheinungsform` and `genotropische Erscheinungsform`, then registers all five principal forms of genotropism: Libido/Eroto-, Idealo-, Opero-, Morbo- and Thanatotropismus.

## Genotypische versus genotropische Erscheinungsform

U000412 defines the genotypic form as manifestation according to the inherited `Erbbild`. U000413 preserves the historical genetic dosage distinction used by Szondi: dominant genes can manifest in `Einzeldosis`, recessive genes require `Doppeldosis`; the text also states historically that `Erblehre` had until then recognized only the genotypic manifestation form.

U000414 defines the specifically Schicksalsanalyse `genotropische Erscheinungsform`: a gene present in `Einzeldosis` in a heterozygous individual reaches manifestation indirectly by driving choices of love object, friend, ideal, business partner and professional connection toward persons who are themselves hidden or manifest carriers of the same gene.

U000415 supplies the paradigmatic hereditary example: a hearing-intact descendant of deaf ancestors falls in love with another hearing-intact descendant of deaf ancestors. This remains Szondi's example; it is not translated into a modern genetic or partner-selection rule.

## Libido/Eroto-Genotropismus

U000417 defines `Libido-Genotropismus` / `Eroto-Genotropismus` as the genotropic effect of latent genes in determining mate choice. U000419 then gives the historical recessive-genetic mechanism used to justify this as a `genische Erscheinungsform`.

The epistemic distinction is preserved. Szondi explicitly writes `Wir nehmen an` for the thesis that genotypic manifestation of a recessive gene in descendants is always preceded by genotropic action of latent genes in the conductor parents; this remains `ASSUMPTION`. The subsequent sentence that the genotropic form always precedes the genotypic form is stored as the stronger assertion made by the text.

## Idealo-Genotropismus

U000420-U000421 define friend and ideal choice as another genotropic manifestation. `Idealo-Genotropismus` is represented source-near as the conductor choosing a genetically related (`genverwandt`) person as model or friend.

## Opero-Genotropismus

U000422-U000423 define `Opero-Genotropismus` as the manifestation of latent genes through occupational choice, by which the conductor forms ties to manifest homozygous carriers of the relevant gene.

The psychiatrist example crosses a page boundary and is preserved as one conceptual example through two canonical anchors, skipping the page-header furniture U000424. The original explicitly describes a person with an openly mentally ill parent or sibling who remains apparently healthy, becomes a psychiatrist and spends most of life in an `Irrenhaus unter Geisteskranken`; Szondi interprets this as opero-genotropic manifestation of latent genes conditioning the disposition to mental illness.

The historically sensitive vocational examples at U000425 are preserved without sanitization: `Feuerwehrmann` / `pyromanische Anlage`, `Kriminalist` / `kriminelle Anlage`, and `Friseur` / `homosexuelle Anlage`.

Equally importantly, U000426 is registered as an explicit anti-overgeneralization. Szondi says he does **not** claim that every firefighter is a latent pyromaniac, every criminalist a latent criminal, or every barber a latent homosexual. His positive statement is only that such occupations can give the individual a `Möglichkeit`, to live out the named `Triebansprüche` `in sozialer Weise`. P2A preserves both sides together.

## Morbotropismus

U000427 defines the fourth form, `Krankheitswahl` / `Morbotropismus`. U000428 is preserved as a research/problem question concerning why the same bodily damage can lead to different pathological consequences in different people.

U000429 contains the doctrinal answer: Szondi states that the latent genes inherent in the individual determine the form of illness that appears as a reaction to external damage. The same unit also presents the family-pattern observation that varied physical and psychic traumas can repeatedly evoke the same bodily or mental illness in particular families.

These are historical Szondian hereditary/pathodiagnostic claims. They are preserved at source strength and are not converted into contemporary medical causation or diagnostic behavior.

## Thanatotropismus

U000430-U000431 introduce the fifth form: `Todeswahl`, `Thanatotropismus`. The mechanical split between the two units is resolved by the original scan, which confirms a single continuous sentence.

U000432 states categorically that the disease by which a person dies is not left to chance. U000433 continues the sentence across the page boundary and assigns determination of death type / death-bringing illness to `familiäre Gene` carried throughout life.

The final sentence is intentionally weaker. Szondi writes that suicide as cause of death, together with the means and method by which one brings about death by one's own will, `scheint` to be the work of familial recessive genes. The registry therefore uses `SUSPICION_INDICATION`; it does not upgrade `scheint` to an assertion.

No suicide, death-selection, disease-selection, occupational or relationship inference is implemented in P2A.

## Original-PDF verification and visual arbitration

The admitted original `SCHICKSALSANALYSE- Szondi.pdf` was directly inspected for printed pp. 59–62 (scan pp. 63–66). Every registered doctrine has a witness in `doctrine/verification/P2A-SA-007.jsonl`.

Visual arbitration is material at:

- U000411, where canonical joins `dergenischen` while the original heading reads `der genischen`;
- U000418 and U000424, which are page-header furniture;
- U000423-U000425, where the psychiatrist example crosses U000424 page furniture;
- U000430-U000431, where the Thanatotropismus definition is mechanically split;
- U000432-U000433, where the death-selection sentence crosses printed pp. 61–62.

## Evidence witness

Canonical extraction/review uses the independently green post-Batch-006 `main` witness:

- workflow run: `33017069697`;
- artifact: `9624972741` (`p0-canonical-access`);
- artifact digest: `sha256:0703e0e9256bf21ab1fc8c7248e4ac0ad4bc65ea2715c5bf6594a5283308a687`;
- source HEAD: `a5371682c9c8e9d11fd0bd8289ad43e3c49993ec`.

## Coverage and unresolved state

All BODY units U000411-U000433 were reviewed in source order. Batch-specific coverage is recorded in `doctrine/coverage/SZ_SA_1948_BATCH_007.jsonl`.

No unresolved source-access ambiguity remains for registered excerpts. The historical empirical truth of the hereditary, pathodiagnostic, vocational and death-selection claims is not adjudicated in P2A. No P2A gate is declared here.

## Batch boundary

The next source-order unit is U000434, `Die Gen-Quantitätstheorie und die multiple Allelie`. Batch 008 must begin there unless a later audit reopens an earlier unit.
