# SZONDI3 — P2B executable claim data contract

**Status:** ACTIVE DATA CONTRACT  
**Layer:** `EXECUTABLE_INTERPRETATION`  
**Date:** 2026-08-27

## 1. Purpose

This contract refines `docs/P2B_EXECUTABLE_INTERPRETATION_SPEC.md` into the stable information model for executable interpretation claims and their activation records.

The object model must make it mechanically difficult to lose the distinctions that matter epistemically:

`what was observed -> what deterministic fact was computed -> which doctrine authorizes interpretation -> under what trigger/context -> with what source strength -> what is explicitly not licensed`

Human-readable report prose is not part of this layer.

## 2. Identity

Every claim object requires:

- `schemaVersion` — contract version;
- `claimId` — stable non-recycled identity;
- `ruleVersion` — version of the executable formalization, independent of `claimId`;
- `status` — lifecycle/review status, not activation result.

Renaming a display label must not change identity.

A rule change that alters trigger semantics must increment `ruleVersion` and preserve an audit trail. A materially different interpretation should receive a new `claimId` rather than silently changing the old claim's meaning.

## 3. Authority and provenance fields

Required:

- `sourceLayer` — `SZONDI_PRIMARY` or an exact named later layer such as `DERI_1949` / `MELON_1975`;
- `doctrineIds` — non-empty set of stable P2A doctrine IDs;
- `sourceIds` — derivable/validated from the linked doctrines, retained explicitly for inspection;
- `canonicalAnchors` — recoverable canonical source addresses or a mechanically resolvable doctrine-to-anchor reference;
- `epistemicClass` — one of:
  - `SOURCE_ESTABLISHED_TRIGGER`
  - `IMPLEMENTATION_INFERRED_TRIGGER`
  - `POST_SZONDI_TRIGGER`
  - `UNRESOLVED_NO_RULE`
- `inferenceRationale` — required when `epistemicClass = IMPLEMENTATION_INFERRED_TRIGGER`;
- `reversalCondition` — required for implementation-inferred rules and recommended for historically calibrated rules.

Validation invariant:

> A claim cannot exist without doctrine provenance, and a doctrine reference cannot be replaced by a checkpoint, chat statement, test, or current code behavior.

## 4. Assertion semantics

Required:

- `assertionMode` — one of:
  - `DEFINITIONAL`
  - `CATEGORICAL`
  - `CONDITIONAL`
  - `PROBABLE`
  - `POSSIBLE`
  - `HYPOTHESIS`
  - `WARNING`
  - `LIMITATION`
- `sourceStrengthNote` — short source-near explanation of retained epistemic strength;
- `claim` — faithful clinician/source-oriented statement;
- `alternatives` — zero or more co-valid interpretations that must remain present when source polysemy is not resolved by context.

Mechanical rule:

> P2B may downgrade assertion strength when implementation context is incomplete; it may never upgrade it above the strongest linked doctrine authorization.

Examples:

- source `scheint` cannot become `CATEGORICAL`;
- source `kann` / possibility cannot become a deterministic diagnosis;
- an `Arbeitshypothese` remains `HYPOTHESIS` even when its trigger is structurally exact.

## 5. Trigger description

The schema separates **formal trigger structure** from human explanation.

The trigger object requires:

- `triggerKind`:
  - `EXACT_STRUCTURAL`
  - `CONDITIONAL_CONTEXTUAL`
  - `POLYSEMIC`
  - `LIMITATION_GUARD`
  - `COMPOSITE`
- `requiredFacts` — typed deterministic/context fact selectors;
- `conditions` — all required predicates, with conjunction/disjunction explicit;
- `exclusions` — conditions that suppress activation;
- `ambiguityPolicy` — behavior for non-unique or source-underresolved input;
- `contextRequirements` — named contextual facts that cannot be inferred from test data.

No condition may be implicit in prose only.

A trigger cannot read arbitrary free text from a clinical note unless a separately governed extraction layer converts it into an explicit typed fact with provenance.

## 6. Input fact references

P2B consumes **references to typed facts**, not recalculated P1 results.

A fact reference identifies:

- `factType`;
- `factId` or deterministic object address;
- `scope` — profile / series / foreground / background / test session / group;
- `calculationVersion` where relevant;
- `inputState` — `AVAILABLE`, `AMBIGUOUS`, `UNDEFINED`, `MISSING`.

Invariant:

> P2B does not repair, tie-break, normalize differently, or reinterpret a P1 fact. If the prerequisite fact is ambiguous, the claim handles that ambiguity locally.

## 7. Activation result

Evaluation of a claim yields an **activation record**, distinct from the claim definition.

Required conceptual fields:

- `claimId`;
- `ruleVersion`;
- `activationStatus`:
  - `ACTIVE`
  - `INACTIVE`
  - `UNRESOLVED_INPUT`
  - `BLOCKED_CONTEXT`
  - `BLOCKED_SOURCE_CONFLICT`
- `matchedFacts` — exact fact references that satisfied the trigger;
- `missingFacts` / `missingContext` where applicable;
- `activeAlternatives` — retained polysemic outputs;
- `antiInferences` — conclusions not licensed by this activation;
- `qualifications` — linked claim/doctrine qualifications that must accompany the result;
- `provenanceTrace` — enough information to recover claim -> doctrine -> canonical anchor.

Inactive claims do not belong in ordinary clinical output, but their evaluation may remain available for debugging/audit.

## 8. Anti-inference as first-class data

`antiInferences` must be structured and identifiable, not buried in prose.

Recommended form:

- `antiInferenceId` — stable identity;
- `prohibitedConclusion` — short controlled statement;
- `reasonDoctrineIds`;
- `scope` — when the prohibition applies;
- `severity` — `HARD_BLOCK` or `QUALIFICATION_REQUIRED`.

A `HARD_BLOCK` must prevent downstream integration/reporting from reconstructing the prohibited conclusion from the same evidence path.

## 9. Polysemy and alternatives

A claim may contain multiple alternatives when the source itself provides multiple interpretations and the current context does not select among them.

Each alternative should carry:

- `alternativeId`;
- `statement`;
- `assertionMode`;
- `requiredDiscriminator` if the source gives one;
- `doctrineIds`;
- optional `exclusions`.

Rules:

1. absence of a discriminator does not authorize choosing the first alternative;
2. downstream integration may preserve or contextualize alternatives but cannot silently collapse them into one;
3. ranking is allowed only when a source-grounded ranking/context rule is represented explicitly.

## 10. Source conflict / diachronic qualification

P2B must be able to represent two simultaneously valid source-attributed claims that differ.

Relevant fields may include:

- `conflictsWithClaimIds`;
- `qualifiedByClaimIds`;
- `relationType` — `CONTRADICTS`, `NARROWS`, `EXTENDS`, `DIACHRONIC_CHANGE`, `POST_SZONDI_ALTERNATIVE`, etc.;
- `resolutionPolicy` — normally `PRESERVE_BOTH` unless a separately reviewed project decision authorizes another handling.

Cross-source disagreement is expected knowledge structure, not an exception to hide.

## 11. Context boundary

Context must have provenance too.

A context fact should minimally carry:

- `contextType`;
- `value`;
- `source` — clinician-entered, administration fact, deterministic test metadata, etc.;
- `scope`;
- `timestamp/phase` if temporally relevant.

Sensitive client context must never be stored in repository fixtures except synthetic/de-identified authorized examples.

P2B must not infer missing age, diagnosis, detention status, developmental phase, family history, or other clinically consequential context from the test configuration itself unless a source-authorized rule explicitly defines that inference.

## 12. Historical calibration marker

For historically calibrated norms/thresholds whose contemporary validity is questioned by the source or project, claims require:

- `historicalCalibration: true`;
- `calibrationContext`;
- `contemporaryValidityStatus` — e.g. `UNVERIFIED`, `OUTDATED_POSSIBLE`, `REQUIRES_REVALIDATION`;
- `activationPolicy` — typically `DO_NOT_APPLY_AS_CONTEMPORARY_NORM` unless separate clinical evidence/governance authorizes it.

## 13. Sensitive-domain marker

To preserve source fidelity while controlling downstream risk, claim definitions should copy/derive domain flags from doctrine:

- `sexualContent`;
- `pathodiagnosticContent`;
- `criminologicalContent`;
- `hereditaryGeneticContent`;
- optional future domain flags.

These flags do not censor the claim. They determine review depth, downstream report policy, and adversarial test requirements.

## 14. Review and activation lifecycle

Claim-definition statuses:

- `DRAFT`
- `SOURCE_LINKED`
- `FORMALIZATION_REVIEWED`
- `CLINICIAN_REVIEWED`
- `APPROVED`
- `RETIRED`
- `SUPERSEDED`

Only `APPROVED` claims may enter production P2B evaluation.

A source-linked claim is not automatically approved merely because its doctrine is valid.

## 15. Validation invariants

The validator should reject a claim when:

1. `doctrineIds` is empty or references missing doctrine;
2. linked doctrines cross source layers while `sourceLayer` pretends they are one voice;
3. assertion strength exceeds source authorization;
4. `IMPLEMENTATION_INFERRED_TRIGGER` lacks rationale/reversal condition;
5. a contextual trigger omits required context declaration;
6. a polysemic doctrine is represented by one forced alternative without a discriminator;
7. a known anti-inference is omitted from a rule whose output could otherwise license the prohibited conclusion;
8. a high-risk historical calibration is applied as a contemporary norm without separate authorization;
9. trigger conditions are stored only in prose and cannot be audited;
10. a P2B rule recomputes or silently tie-breaks a P1 fact;
11. a post-Szondi rule is labelled `SZONDI_PRIMARY`;
12. provenance cannot reconstruct the canonical evidence path.

## 16. Implementation families

The executable catalogue may grow through narrowly scoped families such as:

### `STRUCTURAL_SEMANTICS`

- Symptomfaktor / Wurzelfaktor roles;
- Triebformel symptom/root semantics;
- Triebklasse versus Triebformel distinction.

### `METHOD_SCOPE_GUARD`

- TspQu not autonomous;
- `%Sy-Re` not sufficient diagnosis;
- Proporzmethoden partial;
- Dur-Moll not sole social valuation.

### `CLINICAL_OVERREACH_BLOCK`

- root-negative != automatic repression;
- Sozialindex <40% != criminal act;
- Testsyndrom != one-to-one diagnosis when the prerequisite object is available.

These are examples of useful low-inflation claim families, not an exhaustive roadmap or a statement of the current frontier.

## 17. Runtime relationship

The repository contains concrete claim schema/model code, validators, executable catalogues and runtime evaluation. Their current field names and implementation details are authoritative only insofar as they conform to this contract and its tests.

Volatile implementation state, current claim-number frontier and CI status belong to the live repository and `docs/PROJECT_STATE.md`, not to this data contract.

Breaking schema changes require explicit migration and compatibility verification under `docs/FOUNDATION_ARCHITECTURE.md` and `docs/DEVELOPMENT_GOVERNANCE.md`.

## Final invariant

> **Every P2B activation must be able to answer four questions mechanically: what fact activated it, which doctrine authorizes it, how strong the source claim is, and what the result does not license.**