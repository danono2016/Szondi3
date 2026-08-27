# SZONDI3 — Engine provenance / gap audit

**Status:** WORKING TRANSITION AUDIT — not a new gate  
**Date:** 2026-08-27  
**Purpose:** identify what still blocks completion of the test engine without restarting source reading or inflating P2A.

## Governing rule

This audit is deliberately small. It is not a new ontology and not a replacement for canonical evidence, doctrine registry, P1 verification or P2A coverage.

Classification vocabulary:

- `SOURCE-ESTABLISHED` — deterministic behavior is directly authorized by admitted primary evidence, including approved visual arbitration where required;
- `IMPLEMENTATION-INFERRED` — executable representation is a project inference constrained by source doctrine and explicitly labelled as such;
- `POST-SZONDI` — later-author material may clarify or corroborate but does not become Szondi-primary authority;
- `UNRESOLVED` — the admitted evidence does not determine a unique behavior; software must fail closed or leave the method unimplemented.

## Deterministic engine status

| Area | Current epistemic status | Runtime status | Remaining action |
|---|---|---|---|
| 48 stimuli, series, positions, factor mapping, presentation order | `SOURCE-ESTABLISHED` | implemented + tested | none |
| VGP foreground administration | `SOURCE-ESTABLISHED` | implemented + tested | none |
| EKP/background complement and forced `ø` distinction | `SOURCE-ESTABLISHED` | implemented + tested | none |
| factor-count reaction table and quantum marks | `SOURCE-ESTABLISHED` | implemented + tested | none |
| S/P/Sch/C vector and profile construction | `SOURCE-ESTABLISHED` | implemented + tested | none |
| repeated series and Tabelle 13 normalization | `SOURCE-ESTABLISHED` | implemented + tested | none |
| Tendenzspannungsquotient and `%Sy-Re` arithmetic | `SOURCE-ESTABLISHED` | implemented + tested | interpretation remains downstream; neither index is sufficient alone |
| factorial TspG | `SOURCE-ESTABLISHED` | implemented + tested | none |
| vectorial TspD and lower-TspG directional index | `SOURCE-ESTABLISHED` | implemented + tested | none |
| Gefahr/Ventil threshold | `SOURCE-ESTABLISHED` | implemented + tested | none |
| Triventil / Quadriventil structure | `SOURCE-ESTABLISHED` after D-015 visual arbitration | implemented + tested | none; `U003912` blocker closed as `3–4` |
| Haupttriebklasse | `SOURCE-ESTABLISHED` | implemented + tested with co-leading ties preserved | none |
| Unterklasse with one-sided root direction | `SOURCE-ESTABLISHED` | implemented + tested | none |
| Unterklasse with genuinely mixed `+/-` root direction | `UNRESOLVED` | fail-closed | do not invent majority threshold |
| complete Triebformel line constitution | `SOURCE-ESTABLISHED` constraints | implemented + tested | non-unique mathematical partitions remain locally `UNRESOLVED` / fail-closed |
| simple abbreviated Triebformel | `SOURCE-ESTABLISHED` | implemented + tested | tied extrema remain locally `UNRESOLVED` / fail-closed |
| extended abbreviated Triebformel (`kp/hs` type) | `IMPLEMENTATION-INFERRED, strongly source-constrained` under D-014; Fall 18 form itself is `SOURCE-ESTABLISHED` | implemented + regression-tested | no active `kp/hs` research blocker |
| Dur-Moll arithmetic | `SOURCE-ESTABLISHED` with approved visual table arbitration | implemented + tested | psychological/social interpretation belongs P2B |
| Sozialindex arithmetic | `SOURCE-ESTABLISHED` with approved visual table arbitration | implemented + tested | interpretation belongs P2B; `<40%` must not be converted into a criminal-act inference |
| Quantenverrechnung | `UNRESOLVED` by Szondi's own incompleteness statement | intentionally not completed | no action unless stronger admitted evidence appears |
| Böszörményi Inkonstanzmethode | `UNRESOLVED — missing identified primary publication` | intentionally not reconstructed | reopen only if the identified source is admitted |
| Rand-Mitte / verbal-association qualitative procedures | source-described, but not deterministic P1 arithmetic | routed downstream | formalize only where P2B can state explicit triggers/limits without pretending full clinical judgment is arithmetic |

## Post-Szondi status

No currently accepted deterministic engine rule needs Deri or Mélon to override Szondi-primary evidence.

Deri and Mélon remain useful as separate `POST-SZONDI` witnesses for clarification, systematization and comparison. They may inform cross-source retrieval and later interpretation, but any post-Szondian extension must retain author/layer identity and cannot silently become `SOURCE-ESTABLISHED` Szondi behavior.

## P2A readiness relevant to the engine

### Lehrbuch

`SZ_LEHR_1972` is source-order read and P2A-covered to EOF. The compact registry contains 166 retained standalone doctrines. No Lehrbuch numeric blocker remains active.

### Ich-Analyse

On PR #52:

- `SZ_IA_1956_A` is P2A-covered to EOF and has a compact critical registry;
- `SZ_IA_1956_B` has been read to EOF at book level but source-order canonical P2A extraction has not yet started at the current continuation checkpoint;
- this branch must not edit IA source-local coverage/registry artifacts.

Therefore a formal cross-source relation index should wait until the referenced IA doctrine IDs are stable on `main`. This is a concurrency/provenance constraint, not a reason to resume Lehrbuch reading.

## Doctrine already pointing toward P2B

The deterministic engine is no longer the main gap. The next substantive gap is the **Executable Interpretation** layer. High-value doctrine already available or source-locally prepared includes:

1. Triebformel as the relation of symptom to unsatisfied/failed drive satisfaction;
2. Symptomfaktor versus Wurzel-/Konduktorfaktor semantics;
3. the prohibition against equating a negative root reaction automatically with repression;
4. the possibility that a positive root reaction also represents an unsatisfied need;
5. the distinction between formal indices/partial methods and total interpretation;
6. Dur-Moll and Sozialindex safeguards;
7. Testsyndrom as process rather than one-to-one clinical diagnosis;
8. Ego/Sch doctrine from Ich-Analyse A — elementary Ego functions, Egodiastole/Egosystole, Partizipation/Projektion, Introjektion, Negation, Integration/Desintegration — once the source-local doctrine is integrated through normal P2A governance.

These are **P2B candidates**, not yet runtime triggers. Their existence does not authorize deterministic clinical conclusions before a P2B specification defines inputs, conditions, ambiguity behavior and provenance links.

## Current blockers by layer

### P1 deterministic engine

**No active Lehrbuch calculation blocker.** D-014 restored the approved `kp/hs` representation; D-015 closed the Triventil OCR ambiguity. Existing intentional fail-closed cases remain source boundaries, not unfinished coding debt.

### P2A

The main integration dependency is unfinished source-local P2A for `SZ_IA_1956_B` and, at corpus scale, the remaining source partitions required by the P2A architecture. Do not manufacture a P2A PASS merely because Lehrbuch is complete.

### P2B

No authoritative executable-interpretation specification exists yet. Per development governance, specification must precede or accompany P2B implementation.

## Next safe development sequence

1. keep the deterministic engine under regression verification; do not reopen resolved Lehrbuch arithmetic;
2. allow the IA writer to continue `SZ_IA_1956_B` source-local P2A without cross-branch edits;
3. after stable source-local IDs exist on `main`, create only the small transversal concept/relation index needed for retrieval;
4. draft the P2B executable-interpretation specification with explicit doctrine/source links, triggers, context requirements, uncertainty and fail-closed behavior;
5. implement P2B incrementally from the highest-confidence, most structurally constrained doctrines rather than attempting a monolithic interpretation engine;
6. preserve all deterministic/clinical distinctions and never upgrade a possibility, hypothesis, empirical tendency or polysemic reading into a categorical runtime conclusion.

## Audit conclusion

The practical bottleneck has moved.

> **P1 arithmetic/formal classification is not the current problem. The next real engineering problem is provenance-controlled executable interpretation.**

The correct response is not more open-ended Lehrbuch extraction. It is to finish the minimum source-local P2A dependencies, connect them compactly, then specify P2B before adding interpretive runtime behavior.
