# P1 Resolution Sweep

**Status:** ACTIVE P1 CLOSURE RECORD

## Purpose

This document tracks every P1 item that is still partial, source-underdetermined, deferred, or potentially out of scope before `P1_DETERMINISTIC_ENGINE_PASS` can be considered.

The governing evidence order is:

`SZONDI_PRIMARY -> POST-SZONDI SECONDARY (Deri -> Melon) -> external research only if internal admitted evidence is insufficient`

Secondary sources may clarify where to look or how later tradition understood a rule, but they do not override a clear Szondi-primary statement.

The current sweep is performed against the CI-generated canonical-access artifact for authoritative `main`, not against chat recollection.

## Closure statuses

- `RESOLVED_IMPLEMENTED` — source-authorized deterministic rule implemented and tested.
- `RESOLVED_FAIL_CLOSED` — source does not determine a unique executable rule; software preserves the ambiguity explicitly.
- `RESOLVED_OUTSIDE_P1` — material belongs to doctrine, executable interpretation, clinical integration, or another later layer rather than deterministic scoring.
- `BLOCKED_MISSING_EVIDENCE` — a specific source needed to resolve the item is not yet admitted/available.
- `ACTIVE_RESEARCH` — internal corpus sweep still in progress.

## Active items

### 1. Abbreviated Triebformel: relation between simple extreme fraction and broader symptom/root fraction

**Current status:** `ACTIVE_RESEARCH`

Primary findings so far:

- Lehrbuch defines Symptomfaktoren as factors showing constantly or almost constantly ambivalent/null reactions, and Wurzel-/Konduktorfaktoren as factors showing constantly or almost constantly positive/negative reactions (`SZ_LEHR_1972`, canonical units U003709-U003720).
- Lehrbuch defines TspG as the sum of null and ambivalent reactions and states that Symptomfaktoren carry the highest TspG while Wurzelfaktoren carry the lowest (`U003718-U003720`).
- Lehrbuch defines the Triebformel as a fraction with Symptomfaktoren in the numerator and Wurzelfaktoren in the denominator; the simple abbreviated form is distinguished from the three-line complete form (`U003734-U003739`).
- In the complete form, two or three factors with the greatest TspG occupy the first line, middle-strength factors the middle line, and weakest/root factors the last line; factors with TspG difference not greater than 2 are written on the same line (`U003738-U003739`).
- Lehrbuch Fall 11 prints a simple abbreviation `m/s` although the complete formula contains a broader lower line.
- Lehrbuch Fall 16 prints an abbreviation with one symptomatic extreme and tied low/root evidence; the canonical text layout alone is not sufficient to infer a universal tie algorithm.
- Lehrbuch Fall 18 (six profiles) places under the heading `Abgekürzte Triebformel` the two displayed fractions `k/s` and `kp/hs` (`U004525-U004530`), then prints the complete formula separately.
- For short series, Lehrbuch states that Symptomfaktoren, Wurzelfaktoren and the abbreviated Triebformel are constant from six profiles onward, and that these judgments must be used only after conversion to the ten-profile base through Tabelle 13 (`U003983-U003999`). Fall 18 has exactly six profiles.
- Schicksalsanalyse independently defines the Triebformel as a fraction whose numerator contains Symptomfaktoren and whose denominator contains Wurzelfaktoren and prints multi-factor formula examples (`SZ_SA_1948`, U000987-U001008).
- Triebpathologie II again defines the formula as a summary of ten or more profiles, with Symptomfaktoren in the numerator and never/almost-never discharged Wurzelfaktoren in the denominator, including reaction direction/frequency annotations (`SZ_TRIEBPATH_2`, canonical paragraph corresponding to source U000131 in body order).

Secondary corroboration:

- Deri describes the drive formula as the relationship between the most symptomatic factor(s) and least symptomatic/root factor(s), with middle factors on the middle row (`DERI_1949`, U000311-U000315).
- Deri explicitly warns that, in the 1949 formulation, there is no exact universal rule for the absolute number of factors to place on each of the three formula lines; placement is relative to the symptomatic-reaction index (`U000314`). This cannot override Szondi's later 1972 same-line rule but is relevant evidence against inventing an unstated selector.

**Current executable rule:** after PR #36, unique extreme factors can produce a unique simple fraction; ties remain candidates and fail closed when a unique formula would require an unproved tie rule.

**Working hypothesis, not yet executable doctrine:** Fall 18 may preserve two legitimate representational granularities — a leading/extreme pair (`k/s`) and a broader abbreviated symptom/root configuration (`kp/hs`) after short-series normalization. This is strongly suggested by the primary corpus but must be tested against the complete set of Szondi formula examples before universalization.

**Required closure:** build a corpus-wide matrix of Szondi-primary examples recording profile count, raw and ten-base TspG, simple abbreviation, broader abbreviation if printed, complete first/middle/last lines, and class/root designation. Accept a general rule only if the examples and explicit text jointly determine it.

### 2. Abbreviated Triebformel ties

**Current status:** `ACTIVE_RESEARCH`, executable behavior currently fail-closed.

Fall 16 demonstrates that more than one tied root may be represented, while another Lehrbuch example with equal minimal TspG does not justify the universal rule `emit every max/min combination`. PR #36 therefore removed that overgeneralization.

**Required closure:** corpus-wide comparison of formula examples for evidence of an additional selector such as Leitfaktor status, root-direction constancy, Triebklasse relation, Symptom/Wurzel reaction constancy, or another explicitly stated criterion. If no such rule exists, close as `RESOLVED_FAIL_CLOSED`.

### 3. Unterklasse sign for mixed Wurzelfaktor direction

**Current status:** `ACTIVE_RESEARCH`, executable behavior currently fail-closed.

Primary Lehrbuch findings:

- Unterklassen are defined by the positivity or negativity of the Wahlrichtung of the unsatisfied need/Wurzelfaktor (`SZ_LEHR_1972`, U003865-U003875).
- Szondi explains the positive-root case through constantly or almost constantly positive reactions and the negative-root case through negative reactions (`U003867-U003875`).
- Elsewhere he defines Wurzelfaktoren jointly through constantly or almost constantly positive and negative reactions (`U003713-U003717`).
- No universal numerical majority threshold for a genuinely mixed `+`/`-` Wurzelfaktor series has yet been found in the admitted Szondi-primary corpus.

Secondary witnesses:

- Deri states that each factor can be latent in plus or minus direction and describes 16 basic drive-class variations, but the passages located so far do not provide a numerical mixed-direction threshold.
- Melon states that the 16 subclasses depend on whether the positive or negative tendency of the factor dominates (`MELON_1975`, U001988-U001993), but this secondary wording does not itself define how dominance is calculated and cannot supply a rule absent from Szondi.

**Current executable rule:** assign `+` or `-` only for one-sided directional root evidence; mixed directional histories fail closed.

**Required closure:** continue searching Szondi examples and tables for an operational meaning of `fast ständig` or a demonstrated mixed-series assignment. If the corpus never maps mixed direction to a unique sign, close the mixed case as `RESOLVED_FAIL_CLOSED`, not by majority convention.

### 4. Complete Triebformel partition when the explicit TspG line rule admits multiple partitions

**Current status:** `ACTIVE_RESEARCH`, executable behavior currently fail-closed.

Lehrbuch supplies the explicit same-line rule: factors belong on the same formula line when their TspG difference is not greater than 2 (`SZ_LEHR_1972`, U003738-U003739). The engine correctly applies Tabelle 13 normalization for short-series decision values while preserving observed TspG for display.

Fall 11 and Fall 18 are reproduced after applying the source-required ten-profile conversion. Hypothetical rankings can still admit more than one mathematical three-line partition unless further source constraints are imposed.

**Required closure:** test every published Szondi-primary formula example against the current partition primitive. If all source examples are uniquely reproduced but no additional universal selector is stated, document the general ambiguous case as `RESOLVED_FAIL_CLOSED` rather than extrapolating from examples.

### 5. Quantenverrechnung

**Current status:** `RESOLVED_FAIL_CLOSED` — not executable as a completed method from the admitted Szondi description.

Lehrbuch (`SZ_LEHR_1972`, U003694-U003695) says that Deri, Achtnich, Ungricht and Moser attempted a simple quantitative computation for vocational guidance by summing positive and negative image choices independently of direction. Szondi explicitly states that, despite hundreds of applications, the calculation method had **not yet been completed**, declines a more exact exposition, and says the detailed publication must be awaited.

**Closure consequence:** Szondi3 must not manufacture a completed Quantenverrechnung algorithm from the brief conceptual summary. This is not unfinished P1 implementation debt; it is a source-defined incompleteness boundary. If a later admitted primary publication is added, this status may be reopened through governance.

### 6. Inkonstanzmethode

**Current status:** `BLOCKED_MISSING_EVIDENCE` for exact computation; descriptive claims are source-preserved but not executable as a complete algorithm.

Lehrbuch (`SZ_LEHR_1972`, U003696-U003702) states that G. Böszörményi developed the method under Szondi's direction in 1939-1940 and that the posthumous work appeared in **Szondiana I (1953)**. Szondi explicitly directs the reader there rather than reproducing the calculation technique. Lehrbuch describes the method's purpose and interpretation of high/low inconsistency values but does not provide enough calculation detail for independent implementation.

The current admitted repository corpus contains no `Szondiana I` volume or Böszörményi article.

**Exact missing evidence object:** G. Böszörményi's posthumous 1953 publication on the Inkonstanzmethode in *Szondiana I* (the calculation technique cited by Szondi).

**Closure consequence:** do not infer the algorithm from interpretive prose. External acquisition/search is justified only for this specifically named missing evidence object if the steward chooses to admit it.

### 7. Trieblinnaeus constancy criteria for short series

**Current status:** `ACTIVE_RESEARCH / boundary classification`.

Primary Lehrbuch supplies explicit empirical conditions for 3-8 profiles (`SZ_LEHR_1972`, U003965-U003999):

- at three and four profiles, stability of Symptomfaktoren/Wurzelfaktoren/abbreviated formula is conditional on specified repeated reactions;
- at five profiles, Szondi distinguishes sick cases from normals;
- from six profiles, Symptomfaktoren, Wurzelfaktoren, abbreviated formula and first leading class are stated to be constant;
- at seven profiles the second class becomes constant with Äqualität;
- at eight profiles the entire Trieblinnäus is stated to be constant;
- all these judgments require Tabelle 13 conversion to the ten-profile base.

**Required closure:** separate (a) deterministic ten-base normalization and observable reaction-pattern conditions from (b) Szondi's empirical claims of constancy and clinical-status-dependent applicability. Do not turn an empirical reliability statement into an arithmetic identity or silently require clinical diagnosis inside P1.

### 8. Rand-Mitte and verbal/association methods

**Current status:** candidate `RESOLVED_OUTSIDE_P1`.

Lehrbuch explicitly contrasts the qualitative methods, which require depth-psychological knowledge, combinatorial interpretation and Einfühlung, with the later quantitative methods (`SZ_LEHR_1972`, U003688-U003693). Rand-Mitte is presented as a qualitative interpretive method for relating Rand and Mitte dynamics; verbal/association methods require qualitative material and interpretation.

**Required closure:** document the exact routing to Primary Doctrine / Executable Interpretation in P2 rather than retaining them as deterministic-engine debt.

### 9. Dur-Moll and Sozialindex interpretation

**Current status:** numeric procedures `RESOLVED_IMPLEMENTED`; interpretation candidate `RESOLVED_OUTSIDE_P1`.

P1 contains the source-defined matrices and arithmetic. Sexual, social, forensic, diagnostic, hereditary, and clinical meanings remain downstream doctrine/interpretation and must not be smuggled into the arithmetic layer.

## Corpus sweep order

For each active item, search in this order:

1. `SZ_LEHR_1972` — Lehrbuch der experimentellen Triebdiagnostik.
2. `SZ_SA_1948` — Schicksalsanalyse.
3. `SZ_IA_1956_A` and `SZ_IA_1956_B` — Ich-Analyse.
4. `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` — Triebpathologie.
5. `SZ_THER_1963_A` and `SZ_THER_1963_B` — Schicksalsanalytische Therapie.
6. Deri as the first secondary witness.
7. Melon as the next secondary witness.
8. External research only for a specifically identified missing source or unresolved historical publication.

## Gate rule

`P1_DETERMINISTIC_ENGINE_PASS` must not be declared while an item is merely postponed because the internal corpus has not been searched sufficiently.

The gate does **not** require pretending that every historical/clinical question has a unique algorithm. It requires every P1-relevant uncertainty to have a durable, justified status: implemented, explicitly fail-closed because the source is underdetermined, outside P1, or blocked by a named missing evidence object.
