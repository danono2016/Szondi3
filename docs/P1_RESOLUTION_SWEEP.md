# P1 Resolution Sweep

**Status:** CLOSED P1 CLOSURE RECORD  
**Closure date:** 2026-08-26  
**Gate:** `P1_DETERMINISTIC_ENGINE_PASS`

## Purpose

This record closes the P1 source-resolution sweep without converting historical uncertainty into invented software behavior.

The governing evidence order remains:

`SZONDI_PRIMARY -> POST-SZONDI SECONDARY (Deri -> Melon) -> external research only when the admitted corpus is insufficient and a specific missing source has been identified`

Original Szondi evidence remains superior to canonical derivatives, tests, CI and later authors. Later witnesses may corroborate or locate a problem; they do not create a Szondi-primary rule.

## Closure statuses

- `RESOLVED_IMPLEMENTED` — a source-authorized deterministic rule is implemented and tested.
- `RESOLVED_FAIL_CLOSED` — the admitted evidence does not determine a unique executable rule; software preserves that limit instead of inventing one.
- `RESOLVED_OUTSIDE_P1` — the material belongs to doctrine, clinical/executable interpretation or another downstream layer rather than deterministic scoring.

No item remains `ACTIVE_RESEARCH` or `BLOCKED_MISSING_EVIDENCE` for purposes of the P1 gate.

## Final item dispositions

### 1. Abbreviated Triebformel: simple extreme fraction versus broader symptom/root fraction

**Final status:** `RESOLVED_FAIL_CLOSED` for a universal broader-selector rule; simple unique-extrema core is `RESOLVED_IMPLEMENTED`.

Primary evidence establishes:

- Symptomfaktoren carry the greatest TspG and Wurzelfaktoren the lowest (`SZ_LEHR_1972`, U003709-U003720).
- The Triebformel is a symptom/root fraction, distinct from the complete three-line form (`U003734-U003739`).
- Fall 11 prints `m/s`.
- Fall 18 prints both `k/s` and `kp/hs` under `Abgekürzte Triebformel` (`U004525-U004530`).
- Schicksalsanalyse independently contains multi-factor Triebformel examples (`SZ_SA_1948`, U000987-U001008).

The corpus therefore proves that a broader multi-factor abbreviation is authentic Szondi material, but it does not supply a universal deterministic selector that derives every such form from TspG alone. Szondi3 preserves the printed cases as evidence and does not manufacture the missing selector.

Executable consequence: unique maximal/minimal TspG extrema may yield the source-safe simple fraction; the broader `kp/hs` type remains non-generalized until stronger admitted evidence determines a universal procedure.

### 2. Abbreviated Triebformel ties

**Final status:** `RESOLVED_FAIL_CLOSED`.

Fall 16 prints more than one tied root fraction, while another Lehrbuch example with equal minimal TspG does not establish the universal rule `emit every max/min combination`. PR #36 removed that overgeneralization.

The engine retains tie candidates but refuses to claim a unique authoritative abbreviation when an additional source rule would be required. The P1 closure adds an integration-level negative test for this refusal path.

### 3. Unterklasse sign for a mixed Wurzelfaktor direction

**Final status:** `RESOLVED_FAIL_CLOSED`.

Lehrbuch defines positive/negative Unterklasse through the Wahlrichtung of the unsatisfied Wurzelfaktor (`SZ_LEHR_1972`, U003865-U003875) and gives constant/almost-constant positive and negative root cases. The admitted Szondi-primary corpus does not provide a universal numerical majority threshold for a genuinely mixed `+`/`-` root history.

Deri does not provide such a threshold, and Mélon's later wording that one tendency "dominates" does not define a source-authorized calculation.

Executable consequence: one-sided directional evidence resolves `+` or `-`; mixed directional evidence remains explicit and fails closed. No 5/3, percentage or other majority convention is invented.

### 4. Complete Triebformel when the explicit line rule permits more than one mathematical partition

**Final status:** `RESOLVED_FAIL_CLOSED` for genuinely non-unique cases; published golden examples already reproduced are `RESOLVED_IMPLEMENTED`.

Lehrbuch supplies the explicit same-line rule that factors whose TspG difference is not greater than 2 may occupy the same line (`SZ_LEHR_1972`, U003738-U003739). Short-series decisions use Tabelle 13 normalization while printed/display TspG remains the observed value.

Fall 11 and, after correction in PR #32, Fall 18 are source-reproduced. A hypothetical ranking may still permit multiple three-line partitions under the stated numeric rule. No additional universal selector was established from the admitted primary corpus.

Executable consequence: return a complete formula only where the source-defined constraints yield a unique partition; otherwise preserve the candidates/ambiguity and fail closed.

### 5. Quantenverrechnung

**Final status:** `RESOLVED_FAIL_CLOSED`.

Lehrbuch (`SZ_LEHR_1972`, U003694-U003695) states that the quantitative method attempted by Deri, Achtnich, Ungricht and Moser had not yet been completed and explicitly declines a more exact exposition pending later publication.

This is a source-defined incompleteness boundary, not unfinished Szondi3 coding debt. No completed Quantenverrechnung algorithm may be inferred from the summary.

### 6. Inkonstanzmethode

**Final status:** `RESOLVED_FAIL_CLOSED — REOPENABLE_ON_SOURCE_ADMISSION`.

Lehrbuch (`SZ_LEHR_1972`, U003696-U003702) identifies G. Böszörményi's method, says it was developed under Szondi's direction, and directs the reader to the posthumous publication in *Szondiana I* (1953) instead of reproducing the exact calculation technique.

The admitted Szondi3 evidence boundary does not contain that article. The exact missing object is:

G. Böszörményi, `Bestimmung der faktoriellen Schwankungen im Szondi-Test: Die Inkonstanzmethode`, *Szondiana I* (1953), pp. 199-210.

Deri and later/tertiary witnesses corroborate that repeated-series factorial changes, polarity reversals and constancy are relevant objects, but they do not authorize reconstruction of Böszörményi's exact numerical procedure. AI-generated formulas or thresholds encountered during research are therefore excluded.

This does not block P1: within the current admitted evidence boundary there is no source-complete deterministic algorithm to implement. If the Böszörményi source is later admitted through governance, this item may be reopened and implemented as a new source-authorized deterministic increment.

### 7. Trieblinnaeus constancy claims for short series

**Final status:** deterministic normalization `RESOLVED_IMPLEMENTED`; empirical/clinical constancy claims `RESOLVED_OUTSIDE_P1`.

Lehrbuch (`SZ_LEHR_1972`, U003965-U003999) gives empirical statements for 3-8 profile series, including clinical-status-dependent claims, while requiring Tabelle 13 conversion to the ten-profile basis.

P1 implements the deterministic part it needs: ordered series, the minimum profile boundary for Trieblinnaeus evaluation, and exact Tabelle 13 conversion. Claims that a construct is empirically "constant" at a given series length, especially where Szondi distinguishes sick from normal subjects, are not arithmetic identities and are not silently converted into P1 scoring rules.

They remain available for faithful primary-doctrine representation and later executable interpretation where appropriate.

### 8. Rand-Mitte and verbal/association methods

**Final status:** `RESOLVED_OUTSIDE_P1`.

Lehrbuch explicitly presents these among qualitative methods requiring depth-psychological knowledge, combinatorial interpretation and/or verbal associative material (`SZ_LEHR_1972`, U003688-U003693). They are not unfinished deterministic scoring primitives.

They route to the Primary Doctrine Registry and, only where safely formalizable later, the Executable Interpretation layer.

### 9. Dur-Moll and Sozialindex interpretation

**Final status:** numeric procedures `RESOLVED_IMPLEMENTED`; psychological/clinical interpretation `RESOLVED_OUTSIDE_P1`.

PR #33 implements the visually arbitrated Dur-Moll matrix and arithmetic. PR #34 implements the visually arbitrated Sozialindex matrix and arithmetic. Sexual, social, forensic, diagnostic, hereditary and clinical meanings are deliberately excluded from P1 and belong downstream.

## P1 deterministic coverage already integrated on `main`

The accepted P1 sequence is represented by PRs #14-#36 and includes:

1. 48-card stimulus identity, source mapping and presentation order;
2. VGP foreground choice recording and EKP/background recording;
3. complete factor-count reaction table and forced-null `ø` handling;
4. formal S/P/Sch/C profile construction;
5. repeated profile series and Tabelle 13 normalization;
6. Tendenzspannungsquotient, symptom percentage, factorial TspG and vectorial TspD;
7. latency proportions, Gefahr/Ventil structure, Haupttriebklasse and strict source-supported Unterklasse;
8. normalized/complete/abbreviated Triebformel primitives with explicit ambiguity preservation;
9. numeric Dur-Moll and Sozialindex procedures.

Every implemented rule is kept below the clinical-interpretation boundary.

## Gate conclusion

The resolution sweep found no remaining P1-relevant uncertainty that requires an invented rule or an unbounded research wait.

All identified items are now durably one of:

- implemented and tested;
- explicitly fail-closed because admitted evidence is underdetermined/incomplete;
- explicitly routed outside P1.

Therefore there is no semantic blocker to `P1_DETERMINISTIC_ENGINE_PASS` once the closure PR containing this record and the final negative gate test is merged with green CI. The exact merge and post-merge CI witnesses are to be recorded in the final gate checkpoint before P1 is declared durably complete.
