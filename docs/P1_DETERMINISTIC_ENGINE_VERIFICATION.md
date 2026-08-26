# SZONDI3 — P1 DETERMINISTIC ENGINE VERIFICATION

**Gate:** `P1_DETERMINISTIC_ENGINE_PASS`  
**Record date:** 2026-08-26  
**Current gate state in this closure PR:** `IN_PROGRESS`  
**Pass condition remaining:** merge this closure PR with green CI, then record exact merge/post-merge witnesses in the final checkpoint.

## Scope

P1 reconstructs source-authorized deterministic administration, scoring and formal classification procedures from the admitted evidence boundary. It does not contain clinical interpretation.

The gate is judged against `docs/RESTART_ROADMAP.md` and the reliability rule in `docs/VALIDATION_AND_RECOVERY.md`: a PASS must state its acceptance evidence and known residual limitations. Passing CI alone is not semantic authority.

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

### 9. Remaining source-authorized deterministic procedures — PASS WITH EXPLICIT SOURCE BOUNDARIES

`docs/P1_RESOLUTION_SWEEP.md` performs the final closure sweep. Every identified residual item is durably classified as either:

- `RESOLVED_IMPLEMENTED`;
- `RESOLVED_FAIL_CLOSED` because admitted evidence does not determine a unique/completed algorithm;
- `RESOLVED_OUTSIDE_P1` because the material is qualitative, doctrinal or clinical rather than deterministic scoring.

There is no remaining unbounded `ACTIVE_RESEARCH` item and no missing source that must be invented around to make P1 pass.

## Adversarial / negative-validation evidence

P1 explicitly tests refusal behavior, not only successful outputs. Examples include:

- forced `ø` cannot silently enter free-reaction series measures;
- denominator-zero TspQu remains undefined instead of inventing infinity;
- equal TspD/Haupttriebklasse cases do not receive arbitrary tie-breaks;
- mixed Wurzelfaktor direction does not receive an invented majority sign;
- non-unique complete Triebformel partitions fail closed;
- abbreviated Triebformel ties are candidates rather than a universal all-combinations rule;
- this closure PR adds an integration-level test that the authoritative unique abbreviated-formula entry point actually refuses tied extrema.

## Known residual limitations

These are recorded limitations, not hidden P1 debt:

1. Fall 18's authentic broader abbreviated formula `kp/hs` is preserved as source evidence but is not generalized into an unsupported universal selector.
2. Mixed-direction Unterklasse remains unresolved unless source evidence is one-sided enough to authorize `+` or `-`.
3. Hypothetical complete-formula rankings that remain mathematically non-unique under the source rule fail closed.
4. Szondi describes Quantenverrechnung as incomplete; no finished algorithm is invented.
5. Exact Böszörményi Inkonstanzmethode computation is not recoverable from the currently admitted corpus; it may be reopened only if its identified original publication is admitted later.
6. Empirical/clinical short-series constancy statements are not converted into arithmetic identities.
7. Rand-Mitte, association/verbal methods and clinical meanings of Dur-Moll/Sozialindex route downstream.

These limits preserve the project's authority boundary rather than weakening it.

## Gate decision procedure

The semantic review represented by this document and `P1_RESOLUTION_SWEEP.md` finds the deterministic layer sufficient for P1 closure.

The gate remains `IN_PROGRESS` while this branch is unmerged. It becomes eligible for an explicit durable `PASS` only after:

1. the closure PR is merged to `main`;
2. PR CI is green;
3. post-merge `main` CI is green;
4. the exact merge SHA and workflow run witnesses are recorded in the project checkpoint/transfer package through the normal PR process.

No P2A work is authorized by this candidate record. The current mission stops after the final P1 PASS checkpoint is merged and verified.
