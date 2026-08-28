# SZONDI3 — P1 DETERMINISTIC ENGINE VERIFICATION

**Gate:** `P1_DETERMINISTIC_ENGINE_PASS`  
**Record date:** 2026-08-26  
**Gate state:** `PASS`  
**Semantic closure witness:** PR #37 merged to `main` as `5e4d02782d7165dbcea7828ca055a2415b72d262`  
**Durable gate-finalization witness:** PR #38 merged to `main` as `0cfe097f10c445044fcc60f561d60aae3e299dd2`

> **POST-GATE SUPERSESSION — 2026-08-27:** the gate remains valid, but residual limitation 1 below is superseded by Decision Log `D-014` / `docs/KP_HS_RESOLUTION.md`: `kp/hs` is now conceptually resolved, with the extended abbreviated representation implemented as the strongly source-constrained outer-line projection. The later Lehrbuch Triventil OCR blocker is also resolved by `D-015` / `docs/TRIVENTIL_VISUAL_ARBITRATION.md`. The remaining fail-closed boundaries are unchanged.

## Scope

P1 reconstructs source-authorized deterministic administration, scoring and formal classification procedures from the admitted evidence boundary. It contains no clinical interpretation.

The gate is judged against `docs/RESTART_ROADMAP.md` and `docs/VALIDATION_AND_RECOVERY.md`: a PASS states acceptance evidence and known residual limitations. Passing CI alone is not semantic authority.

## Acceptance evidence by roadmap item

### 1. Stimulus identity and series presentation — PASS

PR #14 implemented all 48 immutable stimulus identities, six source-defined series, eight positions/factors per series and the 1-4 / 5-8 presentation rows from primary Szondi evidence. P0 had already verified the mapping directly against Lehrbuch 1972 Tabelle 19.

### 2. Administration protocol — PASS

PR #15 implemented the formal foreground choice protocol: exactly two sympathetic and two unsympathetic selections per series, with four remaining cards, across all six series.

### 3. VGP selection/recording — PASS

PR #15 records the complete 12 sympathetic + 12 unsympathetic foreground protocol with validation against duplicates, cross-series cards and incomplete series coverage.

### 4. EKP/background procedure — PASS

PR #15 implemented complement selection from the remaining four cards under both source-described instruction directions. PR #18 implemented EKP factor reactions and PR #19 corrected the forced-null notation to Szondi's crossed zero `ø`.

### 5. Factor counts and reactions — PASS

PR #16 implemented all 28 rows of Lehrbuch Tabelle 3, including `0`, `+`, `-`, `±` and quantum intensity marks. Invalid count pairs fail closed.

### 6. Vectors/profiles and quantum intensities — PASS

PR #17 constructs the formal vector order `S(h,s)`, `P(e,hy)`, `Sch(k,p)`, `C(d,m)` without interpretation. Quantum levels remain explicit in factor reactions and are used only where a later source-defined numeric procedure requires them.

### 7. Complements and repeated series — PASS

PRs #18-#20 cover complement reactions, forced-null distinction, ordered profile series, the ten-profile ceiling and exact Tabelle 13 conversion for 3-9 profile series.

### 8. Formal indices/classifications — PASS

PRs #21-#36 implement the source-supported deterministic core:

- exact Tendenzspannungsquotient and symptom percentage;
- factorial TspG;
- vectorial TspD;
- latency proportions and Gefahr/Ventil thresholds;
- Triventil/Quadriventil quantitative structure;
- Haupttriebklasse with co-leading ties preserved;
- Wurzelfaktor direction evidence and strict unambiguous Unterklasse;
- normalized Triebformel tensions and complete-formula partitions;
- corrected short-series Triebformel semantics;
- abbreviated-formula unique-extrema core with tie ambiguity preserved;
- Dur-Moll arithmetic;
- Sozialindex arithmetic.

Post-gate D-014 adds the extended abbreviated representation without changing the source-safe simple/tie behavior. D-015 confirms the already-implemented Triventil 3–4 boundary by approved-source visual arbitration.

### 9. Remaining source-authorized deterministic procedures — PASS WITH EXPLICIT SOURCE BOUNDARIES

PR #37 closed `docs/P1_RESOLUTION_SWEEP.md`. Every identified residual item is durably classified as `RESOLVED_IMPLEMENTED`, `RESOLVED_FAIL_CLOSED`, or `RESOLVED_OUTSIDE_P1`. There is no remaining `ACTIVE_RESEARCH` or gate-blocking missing-evidence item.

## Adversarial / negative-validation evidence

P1 tests refusal behavior as well as successful outputs. In particular:

- forced `ø` cannot silently enter free-reaction series measures;
- denominator-zero TspQu remains undefined instead of inventing infinity;
- equal TspD/Haupttriebklasse cases do not receive arbitrary tie-breaks;
- mixed Wurzelfaktor direction does not receive an invented majority sign;
- non-unique complete Triebformel partitions fail closed;
- abbreviated Triebformel ties remain candidates rather than becoming a universal all-combinations rule;
- PR #37 added an integration-level test proving that the authoritative unique abbreviated-formula entry point refuses tied extrema.

## Known residual limitations

These are explicit source/scope boundaries, not hidden P1 debt. Later decisions supersede individual items where stated:

1. **SUPERSEDED by D-014:** Fall 18's authentic broader abbreviated formula `kp/hs` was preserved at P1 closure but not generalized then. Current project status: `kp/hs` RESOLVED; see `docs/KP_HS_RESOLUTION.md`.
2. Mixed-direction Unterklasse remains unresolved unless source evidence is one-sided enough to authorize `+` or `-`.
3. Hypothetical complete-formula rankings that remain mathematically non-unique under the source rule fail closed.
4. Szondi describes Quantenverrechnung as incomplete; no finished algorithm is invented.
5. Exact Böszörményi Inkonstanzmethode computation is not recoverable from the currently admitted corpus; it may be reopened if the identified original publication is later admitted through governance.
6. Empirical/clinical short-series constancy statements are not converted into arithmetic identities.
7. Rand-Mitte, association/verbal methods and clinical meanings of Dur-Moll/Sozialindex route downstream.

## CI witnesses for semantic closure

PR #37 head `909a7fe762f5dd6c30f9e1e2dc86da104282a6a7` passed all three repository workflows before merge.

After PR #37 merged as `5e4d02782d7165dbcea7828ca055a2415b72d262`, `main` passed:

- Foundation verification — run `32939562736` — `success`;
- P0 source inspection — run `32939562733` — `success`;
- P0 canonical access — run `32939562754` — `success`.

The canonical-access workflow includes the integrated Python test suite, including the final fail-closed abbreviated-formula test.

## CI witnesses for durable gate finalization

PR #38 recorded the P1 PASS in the verification record, project checkpoint, transfer package and decision log, then merged as `0cfe097f10c445044fcc60f561d60aae3e299dd2`.

Post-merge `main` CI on that gate-finalization SHA passed:

- Foundation verification — run `32941382584` — `success`;
- P0 source inspection — run `32941382567` — `success`;
- P0 canonical access — run `32941382560` — `success`.

Thus the gate is both semantically closed and durably present on `main` under green integrated verification.

## Gate decision

The deterministic layer satisfies the P1 roadmap while preserving every identified source-underdetermined boundary explicitly.

> **`P1_DETERMINISTIC_ENGINE_PASS`**

This PASS may be reopened if newly admitted evidence invalidates an executable assumption. Reopening is governed by `docs/VALIDATION_AND_RECOVERY.md`.

The next roadmap phase is `P2A — Primary Doctrine Registry`, but this gate record does **not** authorize or begin P2A. The P1 closure mission stops after this PASS and its continuity checkpoint are merged and verified on `main`.
