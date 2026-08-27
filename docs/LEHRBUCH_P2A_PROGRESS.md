# SZ_LEHR_1972 — P2A completion checkpoint

**Branch:** `work/p2a-lehr-full-read-001`  
**Source:** `SZ_LEHR_1972`  
**Policy:** `READ EVERYTHING -> ACCOUNT FOR EVERYTHING -> STORE ONLY CRITICAL DOCTRINE`

## Current durable state

- Full book source-order read: **complete to EOF**.
- P2A canonical BODY coverage: **complete U000584-U008416 (EOF)**.
- Next source-order unit: **none — source-order coverage complete**.
- Original over-granular objects `000001-000257`: audited and compacted from **257 to 72 retained standalone doctrines**; retired IDs remain reserved.
- Post-compaction selective objects: `DR_SZ_LEHR_1972_000258-000351` (**94** objects).
- Current retained standalone Lehrbuch doctrine count: **166**.
- Final substantive exposition ends before the bibliography/index tail; `U006133-U008416` is the Sachregister and is coverage-only.
- Lehrbuch calculation blockers: **none active**. The former `U003912` Triventil OCR blocker is resolved by D-015 / `docs/TRIVENTIL_VISUAL_ARBITRATION.md`.
- `kp/hs`: **RESOLVED** by D-014 / `docs/KP_HS_RESOLUTION.md`; it is not an active research target.

## Final selective batches

- `P2A-LEHR-034` — Fall 18 `k/s` + `kp/hs` preserved as project-critical worked evidence.
- `P2A-LEHR-035` — Dur-Moll and Sozialindex calculation cores + interpretation safeguards.
- `P2A-LEHR-036` — factorial association boundary, how the test functions, structural/statistical/genetic validation conditions.
- `P2A-LEHR-037` — application survey accounted; interpretable-choice validity and Testsyndrom≠clinical diagnosis retained.
- `P2A-LEHR-038` — appendices/EES/prognosis/Ich-stage/parallel-series material accounted; expertise/reliability restriction retained.
- `P2A-LEHR-039` — final bibliography and Sachregister accounted to EOF with no doctrine inflation.

## Formula/calculation core now indexed

1. Triebformel originates from the explicit symptom-versus-underbliebene-Triebbefriedigung question.
2. Symptomfaktoren are constant/almost-constant ambivalent/null reactions; Wurzelfaktoren are constant/almost-constant positive/negative reactions representing unsatisfied needs/Konduktornatur.
3. Negative root reaction is **not** synonymous with repression; it may mean Verzicht/Anpassung, and a constant positive reaction can also mark an unsatisfied need.
4. Factorial `TspG = count(ambivalent) + count(null)` in the profile series.
5. Symptom factors occupy the highest TspG region; root factors the lowest.
6. Triebformel is a fraction: symptom factors numerator, root factors denominator.
7. Abbreviated form is for quick orientation; complete form has top symptom line, middle submanifest/sublatent line and bottom root line.
8. In the complete formula, factors whose TspG difference is not greater than 2 are written on the same line.
9. Operational order: first Triebklasse, then Triebformel; together they support Trieblinnäus placement.
10. `TspD = larger factor TspG - smaller factor TspG`; the lower-TspG factor is carried as the directional index and is treated as dynamically stronger/latent.
11. Largest TspD determines current Haupttriebklasse; largest latency = danger, smallest = vent/outlet, but all four proportions matter.
12. For ten-series values, 5-10 = danger and 0-4 = vent.
13. If all four normalized Latenzgrößen are below 5, the visually arbitrated Lehrbuch rule is: highest-minus-lowest spread `3–4` = Triventilklasse; spread `0–2` = Quadriventilklasse.
14. Short-series values must be normalized through Tabelle 13 to the ten-series basis before using ten-series thresholds/formula numbers.
15. Minimum three profiles are required for use of Trieblinnäus parts; stability increases by profile count, with whole Trieblinnäus stated constant at eight profiles in the cited Schafir scheme.
16. TspQu = Σ null / Σ ambivalent; it must never be interpreted alone.
17. `%Sy-Re = (Σ null + Σ ambivalent) * 100 / Σ all factorial reactions`; it is likewise insufficient for clinical diagnosis by itself.
18. Trieblinnäus lookup proceeds from class to abbreviated formula (horizontal) and complete formula (vertical); complete formulas in Trieblinnäus tables omit the middle theme factors as a table representation convention.
19. Fall 18 canonically prints both `k/s` and `kp/hs` under `Abgekürzte Triebformel`; `Vollständige Triebformel` begins only afterward. Under D-014, the extended abbreviated representation is implemented as the strongly source-constrained symptomatic-line/root-line projection with the median line omitted; this project rule is explicitly classified as implementation-inferred rather than as verbatim universal Szondi wording.
20. Wurzelfaktoren are explicitly also called `Konduktorfaktoren`; Szondi's original genetic validation compared formula roots with genealogical findings.

## Later calculation/interpretation safeguards

- Proporzmethoden are partial, not total interpretations; the vectorial method supersedes the earlier factorial Dur-Moll computation.
- Dur-Moll uses 8 or 10 profiles; each quantum `!` counts as one unit on the D/M side of the corresponding vector image.
- Dur-Moll must not be used alone for social valuation; Szondi requires synoptic reading with Sozialindex.
- Sozialindex uses vector reactions and adds all quantum tensions to the socially negative side.
- A Sozialindex below 40% does **not** permit inference of a criminal act; Szondi limits it to `asoziales Verhalten`.
- Proportion-method calibrations are empirical and historically contingent; Szondi explicitly says their contemporary validity would need re-examination.
- Testsyndrom is a process syndrome, not a one-to-one clinical diagnosis.
- Group statistical significance requires comparison with a regionally/culturally appropriate reference population; Szondi questions broad statistical validity when such data are absent.
- EES/psychotherapy indication/prognosis appendix methods are explicitly expertise-sensitive and should not be mechanized as general scoring procedures.

## Resolved former calculation blocker — Triventil

`U003912` contains a source-near/OCR corruption (`3^1`) in the approved canonical text. The approved paired Lehrbuch PDF was consulted solely as visual arbiter. PDF page 287 (1-based), printed page 283, unambiguously reads **`3–4`**.

Status: **SOURCE-ESTABLISHED / RESOLVED**. See D-015 and `docs/TRIVENTIL_VISUAL_ARBITRATION.md`.

The existing implementation was already behaviorally correct because its all-Ventil `spread >= 3` condition can only mean spreads 3 or 4 when every normalized value is in `0..4`.

## `kp/hs` final status

At source-example level, Fall 18 establishes `k/s` and `kp/hs` under **Abgekürzte Triebformel**, followed only afterward by **Vollständige Triebformel**.

Project status: **RESOLVED**, not an active research question. D-014 / `docs/KP_HS_RESOLUTION.md` defines the extended abbreviated representation as:

`extended abbreviated formula = symptomatic line / root line, median line omitted`

No separate neighbour/distance/fixed-cardinality expansion selector is used. Ambiguity in a non-unique underlying complete-formula partition remains local and fail-closed; simple-form extrema ties remain a separate issue.

## Next project action

1. keep Lehrbuch source-order P2A closed; do not resume open-ended extraction;
2. integrate the independent compact Ich-Analyse contribution when its source-local PR is ready, without editing IA source-local artifacts here;
3. build only the small cross-source concept/relation index required for retrieval after referenced doctrine IDs are stable on `main`;
4. maintain a compact engine-provenance/gap audit separating `SOURCE-ESTABLISHED`, `IMPLEMENTATION-INFERRED`, `POST-SZONDI` and `UNRESOLVED`;
5. use that audit to qualify the transition toward P2B executable interpretation rather than reopening resolved Lehrbuch calculation questions.

## Final invariant

**Lehrbuch P2A source-order coverage is complete. The registry is a compact doctrinal map, not a duplicate manual. No Lehrbuch numeric blocker remains active.**
