# SZ_LEHR_1972 — P2A progress checkpoint

**Branch:** `work/p2a-lehr-full-read-001`  
**Source:** `SZ_LEHR_1972`  
**Policy:** `READ EVERYTHING -> ACCOUNT FOR EVERYTHING -> STORE ONLY CRITICAL DOCTRINE`

## Current durable state

- Full book source-order read: **complete to EOF**.
- P2A canonical BODY coverage: **U000584-U004535**.
- Next source-order unit: **U004536**.
- Original over-granular objects `000001-000257`: audited and compacted from **257 to 72 retained standalone doctrines**; retired IDs remain reserved.
- Post-compaction selective objects added: `DR_SZ_LEHR_1972_000258-000333` (**76** objects).
- Current retained standalone Lehrbuch doctrine count: **148**.

## Recent selective batches

- `P2A-LEHR-023` — P/e/hy foundations.
- `P2A-LEHR-024` — selected P-vector interpretations.
- `P2A-LEHR-025` — Sch/k/p foundations.
- `P2A-LEHR-026` — selected Sch Ich-Bilder and Integration.
- `P2A-LEHR-027` — Sch close + Kontakttrieb/d/m foundations.
- `P2A-LEHR-028` — profile-interpretation Leitsätze + method classification + Rand-Mitte foundations.
- `P2A-LEHR-029` — Rand-Mitte cases accounted for; Komplementmethode/ThKP/EKP/Wahlzwang core retained.
- `P2A-LEHR-030` — remaining complement cases and quantitative-method prelude accounted for; Linnäus origin of Triebformel retained.
- `P2A-LEHR-031` — formula-critical TspG, Symptom-/Wurzelfaktor, abbreviated/complete Triebformel and TspD rules.
- `P2A-LEHR-032` — Triebklasse, danger/ventil thresholds, short-series rules and Tabelle 13 conversion principle.
- `P2A-LEHR-033` — TspQu, %Sy-Re and Trieblinnäus lookup conventions.
- `P2A-LEHR-034` — class catalogues and Falls 14-18 accounted for; Fall 18 `k/s` + `kp/hs` preserved as project-critical worked evidence.

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
13. Short-series values must be normalized through Tabelle 13 to the ten-series basis before using ten-series thresholds/formula numbers.
14. Minimum three profiles are required for use of Trieblinnäus parts; stability increases by profile count, with whole Trieblinnäus stated constant at eight profiles in the cited Schafir scheme.
15. TspQu = Σ null / Σ ambivalent; it must never be interpreted alone.
16. `%Sy-Re = (Σ null + Σ ambivalent) * 100 / Σ all factorial reactions`; it is likewise insufficient for clinical diagnosis by itself.
17. Trieblinnäus lookup proceeds from class to abbreviated formula (horizontal) and complete formula (vertical); complete formulas in Trieblinnäus tables omit the middle theme factors as a table representation convention.
18. Fall 18 canonically prints both `k/s` and `kp/hs` under `Abgekürzte Triebformel`; `Vollständige Triebformel` begins only afterward. No universal broadened-abbreviation selector has been inferred.

## Remaining explicit unresolved calculation item

- `U003912` renders the exact Triventil max-min spread as OCR-corrupted `3^1`. The source partition and worked examples strongly constrain the intended rule, but P2A keeps the exact threshold unresolved until visual arbitration rather than backfilling it from current code/tests.

## Selection discipline

Do **not** resume sentence-granular extraction. Worked cases, repeated clinical catalogues, chapter exposition and tables already recoverable from canonical anchors normally stay in coverage only. Create a doctrine object only when omission would lose a distinct rule, definition, interpretive constraint, exception, epistemic limit, calculation principle, contradiction or rare high-consequence claim relevant to faithful future interpretation.

## Immediate continuation

Resume at `BODY U004536`. Fall 18 notation has now been reached and durably represented. Continue source-order selectively toward the remaining interpretation methods (especially Dur-Moll and Sozialindex) and any later calculation/interpretation constraints, while avoiding reproduction of class/case catalogues.
