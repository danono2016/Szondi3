# Clinical composition — prior-art reconciliation

**Status:** RESEARCH NOTE / CORRECTION TO ARCHITECTURAL HISTORY  
**Date:** 2026-09-15  
**Companion to:** `docs/CLINICAL_REPORT_COMPOSITION_REVERSE_ENGINEERING.md`  
**Runtime effect:** none

## 1. Why this note exists

After the first statement-level reverse-engineering pass, the earlier project artifact `SZONDI_CLINICAL_VOICE_AND_REPORT_SPEC_v1_3.md` was re-read in full enough to compare its composition contract with the current V3/V4 implementation.

This changes the historical diagnosis in an important way:

> The project did **not** discover the need for authorized composition only now. The v1.3 voice/report specification had already stated the essential composition logic explicitly. The implementation failed to compile that logic into a first-class deterministic representation between P2B and the writer.

Therefore the current research task is not to invent a new theory of composition. It is to determine whether the already-specified composition contract can be made machine-readable, minimal and source-faithful without becoming an ad-hoc ontology.

This note records that correction so future work does not repeat the mistake of treating the idea as new.

---

## 2. What v1.3 already specified

### 2.1 Four composition levels

Section 12 of v1.3 explicitly distinguished:

#### Level 0 — coexistence

Two findings occur in the same profile without an authorized relation.

Allowed:
- both may appear in the report.

Forbidden:
- saying one produces, explains or regulates the other merely because they coexist.

#### Level 1 — same support bundle

Two formulations describe the same deterministic configuration/fact.

Allowed:
- combine them in one section to avoid repetition.

This is the level that the current `ClinicalReportPlan` implements most directly through exact support-fact grouping and `SAME_FACT_BUNDLE` units.

#### Level 2 — explicit doctrinal bridge

Admitted doctrine/executable interpretation explicitly relates two reactions/configurations.

Allowed:
- describe exactly that relation, preserving source force and limits.

This is the crucial level that current report planning does **not** expose as an explicit typed dependency between otherwise separate meanings.

#### Level 3 — integration with clinician context

The clinician supplies explicit external case data.

Allowed:
- use that data as a separately-provenanced clinical context.

Forbidden:
- back-project clinician context into the test and call it Szondian evidence.

### 2.2 The governing rule was already explicit

v1.3 stated the rule:

> **Coexistence is not causality.**

It also used a rich-profile example to show that an elegant causal chain is epistemically invalid if the intermediate bridges are not authorized.

This is the same problem later encountered in V3/V4 under the name anti-Mosaikspiel.

### 2.3 v1.3 already distinguished modes of synthesis

Section 13 described at least four outcomes:

1. **structural synthesis** — say where support is richest, without converting support density into a personality claim;
2. **synthesis through an authorized bridge** — e.g. a source-authorized relation such as `C -- + Sch ++`;
3. **convergent interview questions** — when a bridge is absent, turn the possible connection into something to investigate rather than a conclusion;
4. **valid null synthesis** — explicitly say that no authorized global synthesis exists when the active meanings cannot legally be joined.

The last point is particularly important: failure to create a global mechanism is sometimes the correct clinical report output, not a failure of the writer.

---

## 3. v1.3 already contained the reference-case writing logic

The same artifact included clinician-facing formulations for the exact kinds of material now used in the reference case.

For ordinary `Sch ++`, it already proposed the explanatory structure:

- appropriation / making things one's own;
- Ego expansion toward a more encompassing form;
- the Szondian name `Introinflation`;
- the open question of whether the Ego can set a limit when reality requires it;
- no conclusion that the capacity for limitation succeeds or fails.

It also included:

- a contrast between appropriation and expansion;
- hypothetical micro-scenes;
- a bifurcation around successful/unsuccessful limitation;
- concrete interview questions;
- separate formulations for `+k`, `+p`, `-m/+k`, and `C -- + Sch ++`.

For `C -- + Sch ++`, v1.3 explicitly treated the contact/Introinflation relation as an authorized bridge rather than a writer-created inference.

Thus the desired clinical voice and the core anti-Mosaik composition rule were already conceptually aligned before V3/V4.

---

## 4. What the current implementation compiled — and what it lost

### 4.1 P2B

P2B activates source-authorized person/profile meanings. Several clinically important relations are already represented as composite executable claims, including the reference routes:

- `000038` — ordinary `-m/+k` / introjective identification;
- `000042` — ordinary `Sch ++` / Introinflation;
- `000073` — ordinary `Sch ++` / Persona-Deflation route;
- `000078` — ordinary `C -- + Sch 0+/++` / contact blockage with narcissistic Ego-protection relation.

This means the source bridge often already exists **inside P2B**, rather than needing discovery by the writer.

### 4.2 `ClinicalReportPlan`

The plan compiles a narrower rule:

> same scope/profile + exact same support-fact set -> one narrative unit.

This safely implements much of v1.3 Level 1.

It does **not** currently expose, as a machine-readable relation:

- that an atomic `+k` meaning is a constituent/explanatory input to the already-authorized `Sch ++` Introinflation relation;
- that `+p` is another constituent/explanatory input;
- that `000073` extends the same exact configuration with a Persona/Deflation relation;
- that independent nuclei are `NO_BRIDGE` rather than merely different unit IDs;
- the difference between multi-nucleus editorial summary and multi-nucleus person-level semantic synthesis.

### 4.3 V3

V3 made the plan unit the visible writing unit.

Result:

- strong provenance;
- weak clinical integration;
- repeated mini-reports.

It implemented safety more faithfully than composition.

### 4.4 V4

V4 improved global report organization but retained:

> every visible text atom -> exactly one report-plan `unit_id`.

This allows global ordering and adjacency but not general semantic composition across units.

Therefore V4 solved the **layout problem** more than the **composition problem**.

The contradiction was structural:

- ask the model to write one global clinical report;
- prevent a text atom from using more than one unit unless the needed composition already happened inside that unit.

---

## 5. Revised architectural diagnosis

The most precise diagnosis is now:

> **The missing layer is not a newly invented “meaning graph”. It is a deterministic compiler of the v1.3 composition contract over the live P2B meanings.**

In other words:

```text
P2B active meanings
    +
v1.3 composition semantics
    ↓
compiled relation/dependency metadata
    ↓
clinical nuclei / report map
    ↓
AI wording
```

This is materially safer than starting from a blank-slate ontology because:

- the composition levels already have a normative product history;
- P2B already contains many of the actual source bridges;
- anti-Mosaikspiel is already an invariant;
- the current task becomes compilation and representation, not doctrinal invention.

---

## 6. Minimal candidate contract after this correction

A universal graph is **not** justified yet.

The smallest machine-readable contract worth testing is closer to:

### `CompiledClinicalRelation`

```text
relation_id
relation_level:
  COEXISTENCE_ONLY
  SAME_SUPPORT_BUNDLE
  EXPLICIT_DOCTRINAL_BRIDGE
  CLINICIAN_CONTEXT_BRIDGE
member_meaning_ids
bridge_claim_ids
support_fact_ids
support_doctrine_ids
scope
source_strength
forbidden_inferences
```

### `ClinicalNucleus`

```text
nucleus_id
member_meaning_ids
relation_ids
authorized_statements
open_bifurcations
forbidden_inferences
hard_terms
```

### Narrative/propositional role

This must be separate from the semantic relation level:

```text
SEMANTIC_ASSERTION
EDITORIAL_META_SUMMARY
HYPOTHETICAL_INSTANTIATION
INTERVIEW_QUESTION
BOUNDARY
```

The distinction matters because a sentence may list several independent nuclei as a report map without claiming that they form one person-level mechanism.

---

## 7. Mapping v1.3 to the reference-case anatomy

| v1.3 concept | Reference-case example | Current representation | Gap |
|---|---|---|---|
| Level 0: coexistence only | `N-REF-01` vs `N-REF-02`; `N-REF-01` vs `N-REF-03` except where a specific composite claim already links exact inputs | different plan units + prompt prohibition | no explicit `NO_BRIDGE`/coexistence relation object |
| Level 1: same support bundle | `000042` + `000073` share ordinary Sch++ support and can be grouped locally where exact fact support matches | `ClinicalReportPlan.SAME_FACT_BUNDLE` | largely compiled already |
| Level 2: explicit doctrinal bridge | `+k/+p -> Sch++ Introinflation`; `C-- + Sch++ -> narcissistic Ego protection` | composite P2B claims exist, but writer sees plan units rather than explicit constituent/dependency topology | missing typed link from atomic explanations to composite claim |
| Level 3: clinician context | future case history / interview material | clinician integration kept separately | must never be silently merged into test evidence |
| structural synthesis | “these are the richest authorized areas” | writer can phrase it | needs deterministic support-density/ranking only if explicitly contracted; no invented dominance |
| bridge synthesis | `C-- + Sch++` | executable relation exists | writer should consume relation, not rediscover it |
| convergent question | ask whether independently documented movements connect in real life | prompt/voice behavior | should be an explicit narrative role, not semantic bridge |
| null synthesis | rich profile, no legal bridge | allowed in v1.3 benchmark | must remain first-class output, not a failure state |

---

## 8. Benchmark prior art and Gate-1 implications

The internal artifact `SZONDI_CLINICAL_REPORT_BENCHMARK_2026-09-14.md` had already tested 16 scenario families against v1.2/v1.3, including:

- atomic `+k` and `+p`;
- `-m/+k`;
- `Sch ++`;
- `C -- + Sch ++`;
- severe/hard-term cases;
- **C6: a rich profile with multiple bundles and no doctrinal bridges**;
- a ten-profile series;
- VGP/ThKP/E.K.P.

Its architectural conclusion was already:

> the writing guide remains a wording layer; for series and E.K.P. especially, the Report Plan must precompile authorized relations and the writer must not calculate doctrine from raw profiles.

The benchmark is useful prior art, but it is **not proof** of the current architecture:

- it was generative/internal;
- it did not prove that the live runtime compiled v1.3 semantics correctly;
- its style scores are not clinical validation;
- it cannot replace present source/P2B/proposition-level analysis.

It should guide Gate-1 control selection, not close Gate 1.

---

## 9. Revised Gate-1 question

The question is no longer:

> “Can we invent a graph that explains the good report?”

It is:

> **“Can the existing v1.3 composition levels be compiled from current P2B/support data into a small recurring relation/dependency type system that explains good reports without encoding the prose by hand?”**

This is a substantially more falsifiable and lower-risk problem.

### Evidence that would support continuation

Across divergent control cases:

- the same small relation levels recur;
- explicit doctrinal bridges can be pointed to in P2B/source support;
- `NO_BRIDGE` cases yield useful null synthesis rather than writer invention;
- source modality/quantum conditions survive compilation;
- editorial meta-summary remains distinguishable from semantic synthesis;
- a deterministic nucleus dump is clinically intelligible before AI.

### Kill conditions

Stop if:

- relation metadata merely restates the desired final prose;
- every case requires bespoke composition types;
- Level 2 bridges cannot be recovered reliably from executable/source support;
- editorial vs semantic assertions cannot be separated operationally;
- quantum/series/complement conditions cause uncontrolled combinatorial complexity;
- the AI still has to invent the clinically decisive bridge.

---

## 10. Gate-1 control families to materialize next

The prior benchmark suggests three deliberately different stress families. They still need exact deterministic case materialization before anatomy begins.

### Control A — rich, no bridge

Purpose:
- test v1.3 Level 0 and valid null synthesis;
- prove that the system can remain clinically readable without inventing a central mechanism.

Selection rule:
- several active P2B meanings;
- at least two support bundles;
- no executable Level-2 bridge among the main bundles.

### Control B — different explicit bridge

Purpose:
- test whether the composition compiler generalizes beyond the reference Sch++/contact material.

Selection rule:
- use an exact P2B vector/interfactor/intervector relation not already serving as N-REF-01/02/03;
- preserve ordinary/quantum conditions exactly.

### Control C — intensity / hard historical vocabulary

Purpose:
- test that composition does not erase quantum, source strength or severe historical terminology.

Candidate family:
- an exact overpressure/intensity route such as the source-bounded `s+!! + e0` path (`000056`) or a similarly precise hard-term route.

Selection must be made from the actual runtime/P2B trigger, not from a hand-invented profile.

---

## 11. Decision

**Continue research. Do not implement the composition subsystem yet.**

The first reference anatomy and the v1.3 reconciliation point in the same direction, but the historical correction is essential:

> The conceptual grammar was already present. The engineering failure was that we implemented report units and writer protocols without compiling that grammar into the data structure between P2B and prose.

The next work is cross-case Gate-1 materialization and anatomy. No user live-testing is required for this phase.
