# P2A Batch 006 — Schicksalsanalyse: Objektwahl und sexuelle Auswahl in der Tierwelt

**Batch:** `P2A-SA-006`  
**Source:** `SZ_SA_1948` — `SZONDI_PRIMARY`  
**Canonical range:** `BODY U000379-U000410`  
**Registry entries:** 28 (`DR_SZ_SA_1948_000175`–`DR_SZ_SA_1948_000202`)  
**Review state:** `SOURCE_VERIFIED`; clinician/steward review remains required before P2A gate closure.

## Scope

This source-order batch covers §7, `Die Frage der Objektwahl, der sexuellen Auswahl in der Tierwelt`. It ends at U000410, the continuation of the final sentence across a page header. U000411 begins the next true section, `Zwei Erscheinungsformen der genischen Bestrebungen`.

The batch preserves three distinct evidentiary layers rather than collapsing them:

1. Szondi's own `Hypothese des Libido-Genotropismus`;
2. the attributed historical Darwin/Plate/Lorenz animal-selection material used as argumentative context;
3. Szondi's proposed future animal experiment for deciding the genotropism question.

## Libido-Genotropismus

At U000382 Szondi explicitly calls the construct a `Hypothese`. The registry therefore preserves `HYPOTHESIS` strength rather than converting it into an assertion. The hypothesis states that equality of latent recessive genes in two `Konduktorpersonen` could exercise a previously unknown and unexplored `tropistische Wirkung`, manifested in reciprocal sexual attraction.

The later animal formulation remains restricted. At U000399 Szondi writes that the genotropism thesis may perhaps be valid for only `einen Teil der Tiere`; `vielleicht` and the restricted scope are retained. The associated formulation about `Bastard-Konduktoren` being drawn toward one another `in Liebe` is stored as the content of that thesis, not as independently demonstrated zoological fact.

## Darwin, Plate and Lorenz remain attributed

Darwin's thesis about female choice, his probability language concerning non-random mammalian pairing, Plate's much more restrictive assessment of the available observations, and Lorenz's work on `Schlüsselreize` / `angeborenes Schema` remain separate historical evidence/context. They are not silently promoted to original Szondian discoveries.

Particularly important limitations are preserved: Darwin says the attracting characters can rarely or never be established with certainty; Plate says only very few observations seem to demonstrate female choice; Szondi says he does not know whether later observations exist and that Lorenz's work supports the hereditary basis of choice without reaching the depth of the `Wahlzwang`.

## Proposed animal experiment

U000400-U000406 are represented as a source-proposed future research design, not completed evidence. Szondi says simple observation in nature/domestication cannot decide the question and proposes planned animal experiments. The registry preserves separately:

- production of conductors of known genes/genetic constructions in both sexes within one species;
- equal rearing conditions and balanced conductor/control populations;
- the empirical endpoint: whether heterozygotes of the same genes choose each other as love partners more often than genetically specified controls;
- the assumption that genotropic effect strength can vary by gene;
- developmental/phylogenetic variation in forms of sexual selection;
- the explicit future-oriented statement that such experiments would be desirable.

No proposed experimental criterion is converted into a P2B runtime trigger.

## `Annahme` versus `Hypothese`

The section uses both source terms. P2A already represented literal `Hypothese`; Batch 006 extends `assertionStrength` with `ASSUMPTION` so explicit `Annahme` statements at U000407-U000408 are not silently mapped either upward to `ASSERTION` or sideways to `HYPOTHESIS`.

The central `Annahme` at U000407 is preserved: in the object choice of the heterozygous individual, the latent-recessive gene / `verdrängte Erbelement` is effective. Separately, Szondi states categorically that efficacy of latent genes in phenotype formation in humans is `nicht zu bezweifeln`; that stronger sentence retains its own assertion force.

## Closing genotropism distinction

U000408 says latent genes are not `scheintot` but `wirksame vitale Kräfte im Konduktor` and describes Genotropismus as a step beyond ordinary latent-gene efficacy. The text distinguishes a manifestation approximating the genotypic form from another manifestation: `genotrope Wirkung`.

The sentence crosses the page boundary. Canonical U000409 is only the printed-page header. U000410 completes U000408: through genotropic action, the latent genes become `Richtungsfaktoren der triebhaften Bindungen der Menschen`. This continuation is registered explicitly rather than being lost at the mechanical page break.

## Historical terminology

Terms including `Bastard-Individuen`, `Bastard-Konduktoren`, `reinen homozygoten Variationen`, `narzißtisch-autotrop`, `anaklitisch-heterotrop`, `verdrängtes Erbelement` and the sexual-selection terminology are retained source-near. Their preservation is not contemporary endorsement.

## Original-PDF verification and visual arbitration

The admitted original `SCHICKSALSANALYSE- Szondi.pdf` was rendered and directly inspected for printed pp. 54–59 (scan pp. 58–63). Every registered doctrine has a verification witness in `doctrine/verification/P2A-SA-006.jsonl`.

Visual arbitration is material at U000387 and U000393 (carried headers inside canonical prose), U000404 (hyphenation/page transition), and especially U000408-U000410, where U000409 is page furniture between the two parts of one sentence.

## Evidence witness

Canonical extraction/review uses the independently green post-Batch-005 `main` witness:

- workflow run: `33016141516`;
- artifact: `9624591649` (`p0-canonical-access`);
- artifact digest: `sha256:f3dac52a518c63051d5ffd8ff6552f0a4835563f021ba45750f42da52d435a90`;
- source HEAD: `4fe67ed4329563b44131ffce41bdcb0d00626a13`.

## Coverage and unresolved state

All BODY units U000379-U000410 were reviewed in source order. Batch-specific coverage is recorded in `doctrine/coverage/SZ_SA_1948_BATCH_006.jsonl`.

No unresolved source-access ambiguity remains for the registered excerpts. The empirical truth of the historical zoological/genetic claims is not adjudicated in P2A. High-risk hereditary/genotropic/sexual assertions remain `SOURCE_VERIFIED`; no P2A gate is declared here.

## Batch boundary

The next source-order unit is U000411, `Zwei Erscheinungsformen der genischen Bestrebungen`. Batch 007 must begin there unless a later audit reopens an earlier unit.
