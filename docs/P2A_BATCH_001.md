# P2A Batch 001 — Schicksalsanalyse foundational doctrine

**Batch:** `P2A-SA-001`  
**Source:** `SZ_SA_1948` — `SZONDI_PRIMARY`  
**Canonical range:** `BODY U000132-U000177`  
**Registry entries:** 39  
**Review state:** `SOURCE_VERIFIED`; original-PDF verification basis is recorded separately; clinician review remains required for high-risk entries before P2A gate closure.

## Scope

This batch begins source-order population of the Primary Doctrine Registry from Szondi's *Schicksalsanalyse*. It covers the foundational definition of Schicksalsanalyse, its relation to genealogy and depth psychology, the familial unconscious, latent/recessive genes, the three-layer model of the unconscious, choice in love/friendship/profession/illness/death, hereditary fate possibilities, `lenkbarer Fatalismus`, `Ahnenstrom`, latent pathological dispositions in so-called normal individuals, and the Mörder–Metzger–Chirurg example.

No executable trigger, protocol match rule, anti-inference or P2B behavior is introduced.

## Fidelity-sensitive content preserved

The batch deliberately retains rather than modernizes or metaphorizes:

- `Ahnenansprüche`, `familiäres Unbewußtes`, `familiäres Erbgut`;
- `latente, rezessive Gene`, `Erbfaktoren`, `Erbgut`, `Genotypen`;
- the claim that hidden hereditary elements guide fate-forming choice;
- the claim that familial drive conflicts originate at fertilization / `Amphimixis`;
- `Lebensplan`, `erbgemäße Determination`, `Schicksalsmöglichkeiten`;
- `lenkbarer Fatalismus` and `Ahnenstrom`;
- `krankhafte Triebanlagen`, `Konduktoren`, `triebkranke Ahnen`;
- the dose-language `Volldosis` / `Einzel-Dosis`;
- the historically sensitive Mörder–Metzger–Chirurg and `sadistisches Erbgut` formulation.

These are represented as Szondi-primary doctrine, not as contemporary scientific endorsement.

## Assertion-strength discipline

Two passages are explicitly prevented from certainty inflation:

- U000139 calls the identification of the latent recessive genes as the `Ureinwohner` of the familial unconscious an `Arbeitshypothese`; the registry records `SUSPICION_INDICATION`.
- U000139 says `nimmt ... an` when assigning latent genes a fate-guiding function; that claim is likewise recorded below categorical assertion strength.

Other categorical formulations retain their categorical Szondian force rather than being softened because they are scientifically disputed today.

## Exclusions / no-entry accounting

Every unit in U000132-U000177 is accounted for in `doctrine/coverage/SZ_SA_1948.jsonl`. Units that produce no entry are limited to structural transitions, publication history, reception commentary, rhetorical framing, or critic quotations that must not be promoted into Szondi's own doctrine.

In particular, U000162-U000163 report criticisms of genobiological determinism/predestination; they are preserved as source context but are not registered as Szondi-primary propositions.

## Original-PDF verification and visual arbitration

No claim in this batch required typography, a formula, a table, a symbol or page layout to resolve its doctrinal meaning. Therefore there was no *meaning-changing visual arbitration*.

Separately, after direct access to the original scan became available, the complete relevant printed-page span was reviewed against the scan rather than relying solely on the canonical derivative. High-risk hereditary/genetic, sexual, pathodiagnostic and criminological formulations were text-checked directly in the original page images; lower-risk definitional/contextual records received direct page-context confirmation.

The verification basis for every doctrine record is made durable in `doctrine/verification/P2A-SA-001.jsonl`, distinguishing:

- `ORIGINAL_PDF_TEXT_VISUALLY_VERIFIED` — the registered formulation was checked directly against the original page image;
- `ORIGINAL_PDF_PAGE_CONTEXT_VERIFIED` — the original page and surrounding context were visually inspected and found consistent with the canonical extraction.

This witness strengthens provenance but does not itself establish doctrinal truth, scientific validity or clinical acceptance. The original evidence remains superior to the derivative, while CI/validators remain mechanical witnesses only.

## Unresolved items

None at the source-access level for this batch.

Human/clinician review is still required before gate acceptance for the high-risk hereditary/genetic, pathodiagnostic and criminological entries. That pending review is not disguised as `ACCEPTED`.

## Validation intent

The registry records are deterministic JSONL ordered by `doctrineId` within each committed batch file. The coverage ledger records the exact reviewed range, source artifact witness, created doctrine IDs, no-entry units, visual-arbitration state and unresolved state. The original-PDF verification ledger records the actual verification basis per doctrine record.

The canonical witness is the last independently green P0 canonical-access artifact: workflow run `32943656679`, artifact `9597442817`, digest `sha256:eaff1bc0b4169b265dcdd90f6bd4df5a1993cf284a014eda41b8a8a0ded4ca0a`, generated from `main` at `27443fb4e5bece509497654d79a976a880dc1d56`.

This batch does not declare `P2A_PRIMARY_DOCTRINE_PASS`.
