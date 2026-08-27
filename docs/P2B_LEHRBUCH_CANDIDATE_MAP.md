# SZONDI3 — Lehrbuch P2B candidate map

**Status:** PLANNING / PROVENANCE MAP — NO EXECUTABLE RULES CREATED  
**Layer transition:** `P2A -> P2B`  
**Source scope:** `SZ_LEHR_1972` only  
**Date:** 2026-08-27

## Purpose

This document identifies the smallest high-confidence set of Lehrbuch doctrines that can later seed P2B without turning the doctrine registry into runtime code and without waiting for unrelated corpus work.

It does **not** declare P2B started, does not create trigger objects, and does not authorize clinical diagnosis. The governing specification remains `docs/P2B_EXECUTABLE_INTERPRETATION_SPEC.md`.

Candidate status vocabulary:

- `READY_STRUCTURAL` — current P1 facts are sufficient to state the trigger deterministically; later implementation still requires P2B schema/validator and review.
- `READY_LIMITATION` — current facts can activate an anti-inference or scope limitation without choosing a clinical interpretation.
- `BLOCKED_PREREQUISITE` — doctrine is suitable for P2B but the required deterministic/context input is not yet available.
- `DEFER_CONTEXT_HIGH_RISK` — source claim is real but should not enter the first tranche because it requires sensitive context, historical calibration, or clinically risky discrimination.
- `NON_CLIENT_METHOD_GUARD` — methodological constraint relevant to validation/research rather than ordinary individual interpretation.

## A. First-tranche structural semantics

### A1. Triebformel symptom/root syntax and meaning

**Doctrine:** `DR_SZ_LEHR_1972_000316`, `DR_SZ_LEHR_1972_000318`  
**Status:** `READY_STRUCTURAL`

P2B-safe content:

- Triebformel is a symptom/root fraction: Symptomfaktoren in the numerator, Wurzelfaktoren in the denominator.
- Its declared interpretive question is the relation between symptom and underbliebene / unsatisfied drive satisfaction.

Deterministic prerequisite already exists:

- source-safe simple/extended abbreviated formula when uniquely available;
- complete formula when uniquely constituted.

Safe activation sketch:

- when a formula object is available, surface the numerator/denominator roles and the symptom-versus-unsatisfied-drive relation;
- do not convert factor membership itself into a diagnosis.

Required anti-inferences:

- formula semantics are not one-to-one diagnosis;
- local formula ambiguity propagates as `UNRESOLVED_INPUT`.

### A2. Symptomfaktor semantics

**Doctrine:** `DR_SZ_LEHR_1972_000312`  
**Status:** `READY_STRUCTURAL`

P2B-safe content:

- Symptomfaktoren arise from constant/almost-constant ambivalent or null reactions;
- they describe the Erscheinungsbild side and do not by themselves establish the unconscious causal process.

Deterministic prerequisite:

- series reactions / formula factor role.

This is a strong first-tranche claim because it adds source semantics while simultaneously preventing causal overreach.

### A3. Wurzel-/Konduktorfaktor semantics with sign safeguards

**Doctrine:** `DR_SZ_LEHR_1972_000313`  
**Status:** `READY_STRUCTURAL` + `READY_LIMITATION`

P2B-safe content:

- Wurzel-/Konduktorfaktoren represent unsatisfied needs / Konduktornatur in Szondi's model;
- a negative root reaction does **not** automatically mean Verdrängung; Szondi explicitly allows Verzicht or Anpassung;
- a constant positive root reaction may also represent an unsatisfied need without repression.

Deterministic prerequisite:

- root-factor identity and, where sign-specific wording is used, source-safe root direction evidence.

Required behavior:

- if root direction is mixed/unresolved, do not manufacture a sign-specific interpretation;
- the anti-repression limitation remains valid and should be surfaced when relevant.

### A4. Triebklasse versus Triebformel roles

**Doctrine:** `DR_SZ_LEHR_1972_000319`, `DR_SZ_LEHR_1972_000330`  
**Status:** `READY_STRUCTURAL`

P2B-safe content:

- Triebklasse and Triebformel are distinct and complementary;
- class primarily locates the danger/root side, while formula additionally exposes symptom factors as vents / Notausgänge in Szondi's terminology;
- both are dynamic rather than immutable person labels.

Deterministic prerequisite:

- Haupttriebklasse and formula outputs already exist in P1.

Do not collapse these into a single diagnostic label.

## B. First-tranche anti-inference and scope guards

### B1. TspQu is not autonomous behavioral inference

**Doctrine:** `DR_SZ_LEHR_1972_000328`  
**Status:** `READY_LIMITATION`

Trigger prerequisite already exists: calculated TspQu.

Required P2B guard:

- never infer behavior from TspQu alone;
- profile reactions remain required context.

No numerical reinterpretation is needed; this is a pure anti-overreach rule.

### B2. `%Sy-Re` is not sufficient for clinical diagnosis

**Doctrine:** `DR_SZ_LEHR_1972_000329`  
**Status:** `READY_LIMITATION`

Trigger prerequisite already exists: `%Sy-Re` and TspQu.

Required P2B guard:

- `%Sy-Re` must be considered with TspQu;
- neither is sufficient for clinical diagnosis.

The historical approximate 20–30% normal range should **not** be the first executable claim because calibration/generalizability review is a separate issue.

### B3. Gefahr/Ventil class is dynamic, not a fixed clinical label

**Doctrine:** `DR_SZ_LEHR_1972_000326`  
**Status:** `READY_LIMITATION`

Trigger prerequisite already exists: danger/ventil class structure.

Required guard:

- class membership is phase-dependent in Szondi's model and can reflect pre- versus post-discharge state;
- the same clinical form may occur in danger or vent state;
- do not render danger/ventil class as a stable diagnosis of the person.

### B4. Proportion methods are partial, not total interpretation

**Doctrine:** `DR_SZ_LEHR_1972_000334`  
**Status:** `READY_LIMITATION`

Trigger prerequisite:

- any Dur-Moll or Sozialindex output.

Required guard:

- proportion methods deliver partial data, not Gesamtpersönlichkeit / Gesamtschicksal.

This should be attached at the method/result level, not hidden in report prose.

### B5. Dur-Moll must not determine social value alone

**Doctrine:** `DR_SZ_LEHR_1972_000337`  
**Status:** `READY_LIMITATION`

Trigger prerequisite already exists: Dur-Moll output.

Required guard:

- Dur-Moll alone may not be used for social valuation;
- if a later social interpretation is attempted, the source requires synoptic consideration with Sozialindex.

### B6. Sozialindex below 40% does not license criminal-act inference

**Doctrine:** `DR_SZ_LEHR_1972_000340`  
**Status:** `READY_LIMITATION`; positive historical interpretation deferred

Trigger prerequisite already exists: Sozialindex.

First-tranche implementation should encode only the robust prohibition:

- `Sozialindex < 40%` does **not** authorize inference of a criminal/antisocial act.

The source's positive phrase `asoziales Verhalten` is historically/pathodiagnostically consequential and should be preserved in doctrine, but not automatically surfaced as a categorical modern client label in the first P2B tranche. Any later activation must preserve the source's uncertainty around the 40–50% normal zone and remain clinician-facing/provenance-rich.

### B7. Trieblinnäus result is one possible Schicksalsform

**Doctrine:** `DR_SZ_LEHR_1972_000332`  
**Status:** `READY_LIMITATION`

Trigger prerequisite:

- any future Trieblinnäus lookup output.

Required guard:

- the table is incomplete;
- the resulting diagnosis/classification is only one possible Schicksalsform, not an exhaustive or absolute verdict.

Current runtime does not yet expose a full table lookup object, so this guard becomes executable together with that output surface.

### B8. Testsyndrom is a process syndrome, not a clinical diagnosis

**Doctrine:** `DR_SZ_LEHR_1972_000350`  
**Status:** `BLOCKED_PREREQUISITE`, but priority-high

Required guard once Testsyndrom is represented:

- a Testsyndrom characterizes a process, not a one-to-one clinical diagnosis;
- the same syndrome may occur under different clinical diagnoses.

Do not build a profile/syndrome -> diagnosis dictionary.

### B9. EES / indication / prognosis methods are expertise-sensitive

**Doctrine:** `DR_SZ_LEHR_1972_000351`  
**Status:** `BLOCKED_PREREQUISITE` + `READY_LIMITATION`

The methods are not currently deterministic P1 procedures.

Required project guard:

- do not mechanize them as ordinary scoring merely because they appear in the manual;
- any future implementation requires explicit expertise/reliability governance and clinician review.

## C. Important doctrines deliberately deferred from first P2B tranche

### C1. Haupttriebklasse as "most dangerous" dynamic drive

**Doctrine:** `DR_SZ_LEHR_1972_000321`, qualified by `000322`  
**Status:** `DEFER_CONTEXT_HIGH_RISK`

The source association is explicit, but wording around `gefährlichste Trieb` is clinically and historically loaded. A future rule must preserve that this is a Szondian dynamic construct, use all four latency proportions rather than the maximum alone, and avoid translating it into present-day dangerousness/risk-to-others.

### C2. Historical Dur-Moll calibration

**Doctrine:** `DR_SZ_LEHR_1972_000336`  
**Status:** `DEFER_CONTEXT_HIGH_RISK`

Szondi himself says present validity would need renewed investigation. Therefore the historical approximately 2:1 male Dur:Moll calibration must not become a silent contemporary normative threshold.

### C3. Delinquent / Hintergänger Sozialindex scenario

**Doctrine:** `DR_SZ_LEHR_1972_000341`  
**Status:** `BLOCKED_PREREQUISITE` + `DEFER_CONTEXT_HIGH_RISK`

Requires the specific detention/delinquency context, ThKP/Hintergänger and Rand-Mitte procedures. The source claim is explicitly possibility-level. It is inappropriate for early mechanization.

### C4. Genetic validation of Wurzelfaktoren

**Doctrine:** `DR_SZ_LEHR_1972_000347`, `DR_SZ_LEHR_1972_000348`  
**Status:** `DEFER_CONTEXT_HIGH_RISK`

These are authentic Szondi-primary hereditary/genetic doctrines and must remain intact in P2A. They are not required for the first individual test-interpretation tranche and must not be silently translated into contemporary genetic claims.

### C5. Group statistical significance

**Doctrine:** `DR_SZ_LEHR_1972_000346`  
**Status:** `NON_CLIENT_METHOD_GUARD`

This belongs to group research/validation: do not declare a factor/vector frequency significant without an appropriate comparison population. It should inform analytics/research modules rather than ordinary individual P2B output.

### C6. Interpretability of choice acts

**Doctrine:** `DR_SZ_LEHR_1972_000349`  
**Status:** `NON_CLIENT_METHOD_GUARD`

The source requires calm observation, comparison and superlative choice for psychologically interpretable Wahlhandlungen. This is best treated as an administration/validity constraint and should not be converted into post-hoc personality interpretation.

## D. Triventil correction propagated to P2A

`DR_SZ_LEHR_1972_000325` formerly carried the unresolved OCR state for U003912. After D-015 approved-source visual arbitration, the doctrine/coverage/verification records now state the source-established rule:

- all four normalized Latenzgrößen < 5;
- max-min spread `3–4` -> Triventilklasse;
- spread `0–2` -> Quadriventilklasse.

This is a P1 deterministic fact, not a P2B interpretation candidate. The correction is recorded here only so P2B planning does not inherit the former unresolved flag.

## E. First implementation order after P2B authorization

When P2B implementation is authorized and its P2A dependencies are accepted, the safest order is:

1. data model + provenance + activation status only;
2. formula symptom/root structural semantics (`000312`, `000313`, `000316`, `000318`);
3. TspQu / `%Sy-Re` scope guards (`000328`, `000329`);
4. dynamic class guard (`000326`);
5. Dur-Moll / proportion scope guards (`000334`, `000337`);
6. Sozialindex criminality anti-inference (`000340`);
7. only afterward add higher-risk/contextual interpretations;
8. integrate Ich-Analyse Sch/Ego candidates only after their source-local IDs are stable through normal P2A integration.

## Final rule

> **The first P2B increment should make false certainty harder, not make diagnosis easier.**
>
> Start with structural meaning, provenance, and anti-inference. Add contextual clinical meanings only when their required inputs and discriminators are explicit and source-grounded.
