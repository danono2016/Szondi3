# SZONDI3 — P2B Executable Interpretation Specification

**Status:** DRAFT SPECIFICATION — NO P2B GATE DECLARED  
**Layer:** `EXECUTABLE_INTERPRETATION`  
**Date:** 2026-08-27

## 1. Purpose

P2B converts selected, already represented doctrine into **activatable interpretive claims** without rewriting the doctrine and without pretending that every Szondian statement is safely mechanizable.

The authority path is:

`canonical source -> P2A doctrine -> P2B executable claim -> clinical evidence -> integration -> report`

P2B is therefore not a second doctrine registry and not a free-form rules engine. Its job is to state exactly **when software is allowed to surface a source-grounded interpretation, with what strength, alternatives and limits**.

## 2. Non-negotiable invariants

1. Every executable claim must link to one or more stable doctrine IDs and, through them, to canonical source anchors.
2. P2B may narrow an activation condition; it may not strengthen the source assertion.
3. `Hypothese`, `Arbeitshypothese`, `Annahme`, `scheint`, `zumeist`, probability, possibility and similar qualifiers remain visible in executable output.
4. A single factor/reaction/profile feature may not be converted into a diagnosis unless admitted doctrine explicitly authorizes that exact inference under the satisfied conditions.
5. Polysemic Szondian configurations remain polysemic. Software must preserve alternatives rather than select one merely for convenience.
6. Contradictory or developmentally different source claims remain separately attributable. P2B does not harmonize them silently.
7. Szondi-primary and post-Szondian claims remain separate executable layers.
8. An anti-inference/limitation is first-class executable knowledge, not an editorial footnote.
9. Missing context, ambiguous deterministic input or non-unique prerequisite calculation fails closed at the affected claim.
10. P2B never modifies deterministic P1 outputs to make an interpretation easier to activate.

## 3. Inputs

A P2B evaluation may consume only explicit typed inputs:

### 3.1 Deterministic test facts

Examples:

- factor reactions and quantum levels;
- vector/profile reactions;
- ordered profile series;
- TspG / TspD;
- normalized latency status/class structure;
- Haupttriebklasse / source-safe Unterklasse evidence;
- simple or extended abbreviated Triebformel where available;
- complete Triebformel where uniquely constituted;
- Dur-Moll / Sozialindex numeric outputs;
- foreground/background distinction.

### 3.2 Context facts

Only context explicitly supplied by the clinical workflow may be used. Examples may later include age/developmental context, foreground versus experimental complement, series length, repeated-test phase, or other source-required conditions.

No client-identifying data belongs in repository fixtures.

### 3.3 Doctrine references

Every rule instance must name the P2A doctrine IDs it operationalizes. A rule may not cite a checkpoint summary as its sole doctrinal authority.

## 4. Output object

An executable interpretation claim should minimally contain:

- stable `claimId`;
- `sourceLayer`: `SZONDI_PRIMARY` or named post-Szondian layer;
- linked `doctrineIds`;
- exact typed `trigger` description;
- `activationStatus`: `ACTIVE`, `INACTIVE`, `UNRESOLVED_INPUT`, or `BLOCKED_CONTEXT`;
- `assertionMode`: categorical / conditional / probable / possible / hypothesis / warning / limitation;
- faithful source-near `claim`;
- optional `alternatives` for polysemic configurations;
- `requiredContext` and missing-context explanation;
- `antiInferences` — conclusions explicitly not licensed;
- `conflictsOrQualifications` — linked doctrine/claim IDs that qualify or contradict it;
- provenance payload sufficient to recover canonical `U######` context;
- implementation version / rule version.

Human-facing wording belongs to later reporting layers. P2B output should remain clinician/source-oriented and provenance-rich.

## 5. Trigger semantics

### 5.1 Exact structural trigger

Use when doctrine associates a clearly defined formal configuration with an interpretation or limit and all required deterministic inputs are available.

The trigger must state the full condition; no hidden default or implied conjunction is allowed.

### 5.2 Conditional/contextual trigger

Use when the same test configuration changes meaning by context, series, foreground/background status, developmental phase, or another explicitly required condition.

If the context is missing, return `BLOCKED_CONTEXT`; do not choose the most common interpretation.

### 5.3 Polysemic trigger

If Szondi gives multiple `Deutungsmöglichkeiten`, activation returns an alternative set. P2B may rank alternatives only if a source-grounded contextual discriminator is also satisfied.

Absent such a discriminator, alternatives remain co-present and downstream integration must preserve the uncertainty.

### 5.4 Limitation / anti-inference trigger

A rule may activate only to prohibit an overclaim. Examples of already established candidates include:

- a negative Wurzelfaktor reaction does not automatically mean repression;
- a positive Wurzelfaktor can also represent an unsatisfied need;
- `p` alone does not authorize a homosexuality diagnosis;
- Dur-Moll is a partial method and must not be used alone for social valuation;
- Sozialindex below 40% does not authorize an inference of a criminal act;
- Testsyndrom is not one-to-one equivalent to a clinical diagnosis;
- experimental `Sch ±±` does not by itself prove transcendence/spiritual achievement.

These rules are clinically important because they constrain downstream certainty.

## 6. Epistemic status of executable rules

Every P2B rule must be labelled independently of its doctrine source:

- `SOURCE-ESTABLISHED_TRIGGER` — source doctrine states both the relevant condition and inference sufficiently explicitly to operationalize;
- `IMPLEMENTATION-INFERRED_TRIGGER` — trigger formalization is a project inference constrained by doctrine; rationale and reversal condition are required;
- `POST-SZONDI_TRIGGER` — derived from Deri/Mélon or another admitted later layer and never presented as Szondi-primary;
- `UNRESOLVED_NO_RULE` — doctrine is important but cannot yet be safely activated by software.

A doctrinally true statement is not automatically an executable rule.

## 7. Failure and ambiguity behavior

P2B fails closed locally rather than globally.

Examples:

- non-unique complete Triebformel -> claims requiring a unique complete formula are `UNRESOLVED_INPUT`;
- tied simple abbreviated extrema -> claims requiring a unique simple abbreviation are `UNRESOLVED_INPUT`;
- mixed root direction -> claims requiring a signed Unterklasse are blocked, while unrelated claims may still activate;
- missing clinical/contextual discriminator for a polysemic Sch image -> return alternatives or `BLOCKED_CONTEXT`;
- doctrine conflict -> surface both qualified claims with provenance; do not synthesize a third rule inside P2B.

## 8. Cross-source discipline

Cross-source retrieval may place multiple doctrines beside one another, but P2B rule identity remains source-aware.

A later author may:

- clarify Szondi;
- propose a selector Szondi did not state;
- introduce terminology or thresholds;
- narrow or broaden interpretation.

Such a rule is marked `POST-SZONDI_TRIGGER`. It is not merged into a Szondi-primary trigger merely because it is useful or clinically familiar.

## 9. Candidate first implementation tranche

P2B should begin with high-confidence **structural semantics and safeguards**, not with a large catalogue of diagnoses.

Recommended first tranche after the required P2A doctrine IDs are stable:

1. Triebformel symptom/root semantic output;
2. Wurzelfaktor sign anti-inference safeguards;
3. method-scope safeguards for TspQu, `%Sy-Re`, Dur-Moll and Sozialindex;
4. Testsyndrom-versus-clinical-diagnosis limitation;
5. selected Sch/Ego structural interpretations from integrated Ich-Analyse doctrine where triggers and alternatives can be stated explicitly;
6. explicit polysemy handling for Sch configurations before adding any deterministic-looking clinical labels.

This tranche is intentionally biased toward preventing false certainty while establishing the P2B data model and provenance path.

## 10. Test requirements

For every rule:

1. positive fixture satisfying the full trigger;
2. nearest negative fixture that must not activate;
3. missing-context fixture where relevant;
4. ambiguity fixture where relevant;
5. assertion-strength test ensuring epistemic qualifier is preserved;
6. provenance test linking to stable doctrine/source anchors;
7. anti-overreach test for any diagnosis/pathology-sensitive interpretation;
8. post-Szondi separation test when a later-author claim exists.

Regression output is not authority; source/doctrine review remains decisive.

## 11. P2B gate requirements

`P2B_EXECUTABLE_INTERPRETATION_PASS` may be considered only when:

- the P2A doctrine dependencies of implemented claims are stable and valid;
- executable claim schema and validator exist;
- every claim has recoverable doctrine/source provenance;
- assertion strength is mechanically preserved;
- ambiguity and missing context fail closed;
- polysemy is representable without forced choice;
- source layers remain separate;
- clinically consequential anti-inferences are tested;
- clinician review has examined representative high-risk claims;
- no claim depends on hidden chat memory or an unrecorded interpretation convention.

## 12. Relationship to current work

P1 deterministic calculation is accepted and has no active Lehrbuch numeric blocker after D-015. `kp/hs` is governed by D-014.

P2A is still being completed source-locally across the corpus. In particular, IA-A is ready source-locally on PR #52 while IA-B P2A remains to be populated. Therefore this document specifies P2B behavior **without declaring P2B started or authorized for production implementation**.

## Final invariant

> **P2B may make doctrine executable only by making its conditions, uncertainty and provenance more explicit — never by making the doctrine stronger, simpler or more deterministic than the source permits.**
