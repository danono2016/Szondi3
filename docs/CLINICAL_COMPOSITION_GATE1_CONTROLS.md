# Clinical composition Gate 1 — divergent control cases

**Status:** GATE-1 CROSS-CASE RESEARCH  
**Date:** 2026-09-15  
**Companion documents:**
- `docs/CLINICAL_REPORT_COMPOSITION_REVERSE_ENGINEERING.md`
- `docs/CLINICAL_COMPOSITION_PRIOR_ART_RECONCILIATION.md`

**Runtime effect:** none. The companion regression file `tests/test_clinical_composition_gate1_controls.py` only freezes the evidence shapes used here.

---

## 1. Purpose

The reference case alone could not establish whether the proposed composition layer was reusable or merely a post-hoc description of one good report.

Gate 1 therefore requires deliberately divergent controls that test three different failure modes:

1. **coexistence without a legal bridge** — can the report remain useful without inventing a whole-person synthesis?
2. **a different explicit doctrinal bridge** — can the same composition grammar handle a relation unrelated to the reference Introinflation/contact case?
3. **an exact quantum-sensitive hard-term relation** — can the composition grammar preserve intensity, historical terminology and anti-inference boundaries?

The three controls below are not hand-invented prose specimens. Their P2B evidence shapes are now materialized against the production evaluator in `tests/test_clinical_composition_gate1_controls.py`, and the current PR CI passes them.

---

# 2. Control A — multiple independent nuclei, no cross-vector bridge

## 2.1 Exact profile

```text
h+ s0 e0 hy0 k0 p0 d+ m-
```

Vectors:

```text
S +0 | P 00 | Sch 00 | C +-
```

## 2.2 Runtime-frozen active meanings used by this control

The Gate-1 regression requires these three active non-limitation findings:

| Claim | Exact support | Meaning ceiling |
|---|---|---|
| `IC_SZONDI_PRIMARY_000017` | `S +0` | `Unitendenz / Dominanz der Personenliebe`; vector organization, not global personality dominance |
| `IC_SZONDI_PRIMARY_000012` | `Sch 00` | testological `Desintegration`; not proof of global/permanent personal disintegration |
| `IC_SZONDI_PRIMARY_000020` | `C +-` | simultaneous `Sich-Frei-Machen/Abtrennung` and `Auf-Suche-Gehen`; no automatic biography/pathology |

The regression also inspects every active non-limitation finding in this profile and requires that **no finding span more than one of the three target vector domains `S`, `Sch`, `C`**.

This gives us an executable specimen of v1.3 **Level 0 — coexistence only**.

## 2.3 What a report may say

A safe report map can say, in substance:

> În acest profil apar trei direcții distincte de lectură: S +0 organizează vectorul sexual ca Dominanz der Personenliebe; Sch 00 este denumit testologic Desintegration; iar C +- descrie simultan desprinderea și pornirea în căutare la nivel contactual. În materialul executabil actual nu există o relație care să autorizeze transformarea acestor trei sensuri într-un singur mecanism clinic.

This is a **valid null synthesis**. It is not a poor report and not a writer failure.

It may then ask separate questions appropriate to each meaning, for example:

- what forms of personal attachment/love are clinically relevant, without presupposing that `S +0` describes the whole person;
- whether any clinically observed experience corresponds to the testological `Sch 00` label, without converting it into a modern diagnosis;
- what concrete episodes, if any, involve separation/disengagement together with searching for new contact, without assuming a loss or substitution history.

## 2.4 What a report may not say

Examples of forbidden bridges:

> `Sch 00` makes the person leave relationships and search for new ones.

> The dominance of personal love is destabilized by Ego disintegration and therefore produces contact seeking.

> All three vectors show one underlying abandonment mechanism.

None of these relations is supplied by the current executable findings.

## 2.5 Gate-1 lesson

A clinically coherent report does **not** require a fabricated central mechanism. The architecture needs a first-class representation of:

```text
COEXISTENCE_ONLY
```

plus an explicit ability to produce:

```text
NULL_SYNTHESIS
```

when no Level-2 bridge exists.

This control is important because a writer optimized only for fluency would be strongly tempted to turn the three vivid meanings into a story.

---

# 3. Control B — explicit doctrinal bridge with probabilistic source force

## 3.1 Exact profile

```text
h0 s0 e± hy0 k+ p0 d0 m0
```

Vectors:

```text
S 00 | P ±0 | Sch +0 | C 00
```

This profile is directly materialized from the existing `000086` production regression shape.

## 3.2 The bridge

`IC_SZONDI_PRIMARY_000086` is active.

The runtime regression now additionally freezes that:

- assertion mode is `PROBABLE`;
- doctrine is `DR_SZ_IA_1956_B_000055`;
- source-strength text preserves `oft`;
- its support spans exactly the `P` and `Sch` vector domains;
- `AI_SZONDI_000086` remains attached.

The primary source was rechecked in _Ich-Analyse II_, printed p. 359. Szondi states that five ordinary Ego-defense forms — including `Sch +0` — go **`oft`** with ethical `e±`, moral `hy±`, or double ethical-moral `P ±±` dilemmas.

This is an executable specimen of v1.3 **Level 2 — explicit doctrinal bridge**.

## 3.3 Why this case is structurally different from the reference case

The reference Sch++ material contains a named structural configuration (`Introinflation`) and a Persona/Deflation route.

Control B instead gives a **frequent association** across two vector domains:

```text
ordinary P dilemma signature
        +
authorized ordinary Sch defense form
        ↓
source relation: "oft"
```

The composition engine must therefore carry not only membership but **source modality**.

A bridge is not simply `TRUE/FALSE`.

## 3.4 Safe report formulation

A faithful formulation can say:

> În combinația prezentă, forma de apărare Sch +0 se află în una dintre relațiile pentru care Szondi spune că apar „adesea” (`oft`) împreună cu dileme etice, aici prin e±. Relația este una frecvențială în modelul sursei: configurația nu dovedește că persoana trăiește factual o dilemă morală sau etică.

If `Sch +0` is separately explained through its own active meaning, that explanation may be placed next to the bridge, but the report must not silently convert the association into causality.

## 3.5 Forbidden upgrades

Not authorized:

> Total introjection is caused by an ethical conflict.

> The person is currently in an ethical dilemma.

> The person is guilty, immoral, indecisive or anxious.

> Because e± is present, Sch +0 must have developed as a defense against that concrete conflict.

The source says `oft`, not invariant causal production.

## 3.6 Gate-1 lesson

A reusable relation object needs, at minimum:

```text
relation_level = EXPLICIT_DOCTRINAL_BRIDGE
source_modality = PROBABLE / "oft"
members = [P signature, Sch form]
anti_inferences = [...]
```

If modality is stripped away, the composition layer would create exactly the certainty inflation the project is designed to prevent.

---

# 4. Control C — exact quantum-sensitive historical relation

## 4.1 Exact profile

```text
h0 s+!! e0 hy0 k0 p0 d0 m0
```

Vectors:

```text
S 0+!! | P 00 | Sch 00 | C 00
```

The relevant relation is not triggered by the vector label alone. It depends on the exact factor/quantum configuration:

```text
s = +!!
e = 0 ordinary
```

## 4.2 Runtime-frozen meaning

`IC_SZONDI_PRIMARY_000056` is active and the Gate-1 regression freezes:

- assertion mode `CONDITIONAL`;
- doctrine IDs `DR_SZ_TRIEBPATH_1_000002` and `DR_SZ_TRIEBPATH_1_000004`;
- the historical source term `Aggressionsgefahr` remains present;
- `AI_SZONDI_000056` remains attached;
- support contains exactly:
  - `s.base_symbol`;
  - `s.quantum_level`;
  - `e.base_symbol`;
  - `e.quantum_level`.

A neighboring `s+! / e0` specimen is explicitly required **not** to activate `000056`.

The primary PDF was rechecked. In _Triebpathologie I_, Szondi's example gives maximal accumulation of aggressive claims at `s=+!!` with `e=0` and then states historically that this person lives in an `Aggressionsgefahr` without an `ethischen Schutz` against it. The current executable claim intentionally keeps that wording inside the source model and blocks person-level behavioral promotion.

## 4.3 Safe report formulation

A faithful report can say:

> În modelul istoric al lui Szondi, configurația exactă s+!! cu e0 este descrisă drept `Aggressionsgefahr` fără `ethischen Schutz`. Termenul trebuie păstrat în forța lui istorică, dar formula nu dovedește că persoana este agresivă, violentă, criminală ori lipsită global de conștiință morală.

The report can turn the unresolved clinical part into an interview question, for example:

> Există situații în care apare o tensiune agresivă foarte intensă și, dacă da, ce o limitează sau o transformă în fapt?

The question must remain exploratory; the test does not supply the episode or its outcome.

## 4.4 Forbidden generalization

Not authorized:

- treating `s+!` or `s+!!!` as equivalent to the exact `s+!!` route;
- dropping `e0` from the trigger;
- translating `Aggressionsgefahr` into proven dangerousness;
- concluding absence of conscience/morality/self-control;
- concluding actual violent discharge;
- converting the historical construct into a contemporary sadism diagnosis.

## 4.5 Gate-1 lesson

A composition/bridge object must carry **trigger precision**, not only semantic labels:

```text
member = s+
quantum = exactly 2
co-condition = e0 ordinary
```

A generic edge such as `s+ -> aggression` would be a serious regression from current P2B precision.

---

# 5. Cross-case comparison

The reference specimen plus Controls A–C now give four deliberately different composition shapes.

| Specimen | Main shape | Required composition semantics | Main failure if absent |
|---|---|---|---|
| Reference `h- s+ e+ hy0 k+ p+ d- m-` | atomic meanings feeding already-composite Sch++ and contact/identification routes | constituent-to-composite dependency; same-trigger extension; explicit no-bridge across nuclei | V3 fragmentation or V4 pseudo-synthesis |
| Control A `h+ s0 e0 hy0 k0 p0 d+ m-` | three independent vector meanings | `COEXISTENCE_ONLY` + `NULL_SYNTHESIS` | fluent Mosaikspiel story |
| Control B `h0 s0 e± hy0 k+ p0 d0 m0` | P/Sch explicit association | `EXPLICIT_DOCTRINAL_BRIDGE` + source modality `oft` | causality/certainty inflation |
| Control C `h0 s+!! e0 hy0 k0 p0 d0 m0` | exact quantum-sensitive interfactor relation | exact trigger/quantum preservation + hard-term boundary | loss of quantum precision or dramatization |

A small set of recurring principles explains all four without encoding their final prose:

1. **COEXISTENCE_ONLY / NO_BRIDGE**
2. **SAME_SUPPORT_BUNDLE**
3. **EXPLICIT_DOCTRINAL_BRIDGE**
4. **CONSTITUENT_EXPLAINS_COMPOSITE**
5. **SAME_TRIGGER_EXTENDS_MEANING**
6. **SOURCE_MODALITY_IS_BINDING**
7. **TRIGGER_PRECISION_IS_BINDING**
8. **EDITORIAL_META_SUMMARY != SEMANTIC_SYNTHESIS**
9. **NULL_SYNTHESIS is a valid output**

The last three are not separate Szondian doctrines. They are compiler/reporting invariants needed to preserve the doctrine already admitted upstream.

---

# 6. Gate-1 verdict

## Result

**GATE 1 PASSES for the foreground single-profile research slice.**

This is deliberately narrower than saying the whole Szondi reporting problem is solved.

The pass is justified because:

- four different specimens are now explainable with a small recurring composition vocabulary;
- the vocabulary is derived from the already-existing v1.3 contract and live P2B, not invented to mimic one report;
- the no-bridge control produces a useful null synthesis instead of requiring invented integration;
- the different-bridge control forces preservation of probabilistic source modality;
- the hard-term control forces exact quantum/trigger preservation;
- the reference-report audit was allowed to reject attractive prose rather than bend the model to fit it.

## What Gate 1 does not pass

Not yet covered:

- SERIES-level composition;
- Triebformel / Linnäus composition;
- E.K.P. / complement relations;
- clinician-context Level 3 integration;
- longitudinal comparison;
- a semantic natural-language validator.

Those are later slices and must not be silently inferred from this result.

---

# 7. Gate-2 authorization

The next step may now be a **minimal deterministic contract/prototype for foreground single-profile composition**, with the following restrictions:

1. no AI writer change yet;
2. no V5;
3. no P2B semantic mutation;
4. no new claim identity;
5. no automatic discovery of doctrine;
6. relations are compiled only from already-active findings/support metadata and an explicit reviewed mapping of relation/dependency type;
7. unknown relationships default to `COEXISTENCE_ONLY`, never to synthesis;
8. `NULL_SYNTHESIS` remains first-class;
9. source modality, quantum and anti-inferences must survive losslessly;
10. the prototype must emit a deterministic human-readable nucleus dump before any AI consumes it.

Gate 2 should fail if the prototype needs case-specific prose rules or if it cannot reproduce the four Gate-1 evidence shapes without semantic loss.
