# P2A Batch 003 — Schicksalsanalyse: Physiologie der latenten rezessiven Gene

**Batch:** `P2A-SA-003`  
**Source:** `SZ_SA_1948` — `SZONDI_PRIMARY`  
**Canonical range:** `BODY U000230-U000295`  
**Registry entries:** 53 (`DR_SZ_SA_1948_000075`–`DR_SZ_SA_1948_000127`)  
**Review state:** `SOURCE_VERIFIED`; clinician review remains required for high-risk entries before P2A gate closure.

## Scope

This source-order batch opens Chapter II, *Physiologie der latenten rezessiven Gene*, and follows the chapter from the historical genetic scaffold through Szondi's specifically schicksalsanalytische construction of `Genotropismus` and `Genverwandtschaft`.

The batch deliberately distinguishes two layers that occur consecutively in the source. First, Szondi summarizes the genetics he takes over from Johannsen, Bateson, Morgan, de Vries, Goldschmidt and the contemporary hereditary literature: `Gen`, `Allele`, homo-/heterozygosity, `Genotypus`, `Phänotypus`, dominant/recessive inheritance, gene quantity, reaction chains and `Determinationsstoffe`. These claims are preserved as historical source content and as the conceptual framework Szondi adopts; they are not silently recast as original Szondian discoveries or as contemporary genetic endorsement.

Second, the text moves into Szondi's own Schicksalsanalyse-specific doctrine. The registry preserves, without modernization or sanitization:

- `primordialer Genkampf` / `Ahnenkampf`;
- the formulation of each gene as representative of an `Ahnenanspruch` seeking restoration of an earlier state;
- the claim that weaker hereditary demands are `verdrängt` yet continue dynamically in latency;
- the distinction between manifestation in `Einzeldosis` and `Doppel-` / `Volldosis`;
- the distinction between weakened `genotypisch` and `genotropisch` action of latent genes;
- the `Arbeitshypothese` that latent recessive genes direct the person's `Wahlhandlungen`;
- the two explicitly stated principles of Schicksalsanalyse in this section;
- the statement that the `Gentheorie der Objektwahl` rests on the genobiological process called `Genotropismus`;
- the explicit definition of `Genotropismus` as a force mediated by identical or related genetic factors in two people's `Genbestände`;
- the description of Genotropismus and the drive theory founded on it as `genpsychologisch`;
- the definition of `Genverwandtschaft`;
- the explicit limitation that the concrete `Anlagematerial` of genotropically acting genes can, at the time of writing, be established only approximately and only through especially careful, large-scale `Familienforschung`.

No P2B trigger, protocol-match rule, anti-inference rule or runtime behavior is introduced.

## Assertion-strength discipline

Historical and theoretical certainty markers are preserved rather than normalized upward. The source's `wahrscheinlich` and `möglicherweise` in the genetic discussion remain probability/possibility statements. The split sentence U000276-U000277 remains governed by `Die Schicksalsanalyse nimmt an`. The central genotropic mechanism at U000282 remains explicitly an `Arbeitshypothese`. The first principle at U000286-U000287 remains a `theoretische Annahme`. Source examples involving deafness, hereditary disease and partner/profession choice are represented as examples or possibilities and are not converted into executable individual-level inference rules.

The completion sweep also recovered U000295 as a doctrine entry (`DR_SZ_SA_1948_000127`) because omitting it would preserve the theory while dropping Szondi's own evidentiary limitation. Its `heute nur annähernd` boundary is therefore part of the primary doctrine record.

## Historical terminology and source-level content

The source contains terminology and examples that are historically dated or offensive by current usage, including `Bastarde`, `Schwachsinn`, `Neger`, `Mulatten`, `Taubstummheit` and `Geisteskrankheit`. These are not silently rewritten out of the source model. Where a term is required for the registered proposition it is retained and flagged; where it occurs only in a historical illustration, the illustration is preserved in coverage/context without unnecessarily promoting it to a separate doctrine.

This preservation is descriptive and provenance-faithful. It does not amount to contemporary scientific or ethical endorsement.

## Original-PDF verification and visual arbitration

The original `SCHICKSALSANALYSE- Szondi.pdf` scan was directly inspected for printed pp. 36–43 (scan pp. 40–47). All 53 registered doctrines in this batch have an original-PDF visual verification witness in `doctrine/verification/P2A-SA-003.jsonl`.

The canonical derivative remains the deterministic address witness, but several units require the original scan for typography, formulae or sentence continuity:

1. U000262 contains the corrupted canonical phrase `au/ genotype Weise`; the original reads the intended `auf genotypische Weise` context.
2. U000264 contains materially corrupted genetic formula typography. No doctrine is anchored to the damaged formula string.
3. U000267 is a page/sentence continuation inside the genetic example; the original establishes continuity.
4. U000277 begins with a stray apostrophe after the page split; the original confirms the continuation from U000276.
5. U000291 ends at the page boundary with `Seeli-`.
6. U000292 begins with a carried page header plus the continuation of `Seelischen`; the original establishes the intact sentence and page transition.

A separate source-level ambiguity is preserved at U000282. The original itself reads `Bei gemischterbigen Personen, d.h. bei homozygot-rezessiven Individuen`, which is internally inconsistent terminology. This is not silently corrected to a presumed intended reading. `DR_SZ_SA_1948_000115` and `000116` anchor only the unambiguous preceding statements about genotropic and attenuated genotypic action. The contradictory example wording remains explicitly unresolved at source level.

## Evidence witness

Canonical extraction/review uses the independently green post-Batch-002 `main` witness:

- workflow run: `33003278826`;
- artifact: `9619492223` (`p0-canonical-access`);
- artifact digest: `sha256:372f3a18d254e1901064efd8d877f90dbf72a7356ea5e229137db66d79936803`;
- source HEAD: `9248c42e70675173be10c64eba02e4c63cfb3a1f`.

## Unresolved / pending review

No source-access ambiguity remains for the exact excerpts that were registered. The U000282 wording conflict described above remains an explicit source-level ambiguity rather than being resolved by editorial conjecture.

High-risk hereditary/genetic and pathodiagnostic assertions remain `SOURCE_VERIFIED`; clinician/steward acceptance is not fabricated. Historical genetics is represented as historical source doctrine/framework, not as a contemporary scientific correction layer. No statement in this batch declares `P2A_PRIMARY_DOCTRINE_PASS`.

## Batch boundary

The next source-order unit is U000296, the subsection heading `Die Wirkung der latenten, rezessiven Gene`. Batch 004 must begin there unless a later audit reopens an earlier unit.
