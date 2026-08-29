# SZONDI3 — CLINICAL GROUNDING FOUNDATION

**Status:** ACTIVE CLINICAL ARCHITECTURE / SUCCESSION ANCHOR  
**Base main commit:** `d192c984eff9d753de4ee60955accec3d6252938`  
**Purpose:** establish the smallest durable P3/P4 foundation required for a source-grounded AI-assisted clinician report without creating a second epistemic system beside Szondi3.

## 1. Why this increment exists

Cabinet Alpha already proves the path:

`administration -> P1 deterministic calculation -> P2B approved findings -> structured clinical report`

The next clinical problem is not generic report generation. A general LLM can recount a series incorrectly, confuse doctrinal levels, import Szondi meanings from pretraining, or convert co-occurrence into a plausible causal story.

The project therefore needs one additional invariant before AI narrative generation:

> **No new Szondian clinical information may originate in the narrative model.**

The model may organize and express an already grounded clinical object. Szondi3 remains responsible for the clinical knowledge supplied to it.

## 2. Minimal architecture

The working clinical path is now:

`Administration -> P1 -> P2B -> P3 Clinical Evidence -> P4 Clinical Integration -> narrative model -> clinician working report -> manual therapist synthesis`

P3 and P4 are deliberately implemented as ordinary Python data structures. They are epistemic layers, not infrastructure products.

Explicitly **not** required for the first grounded vertical slice:

- graph database;
- RDF/OWL or a second ontology;
- vector database;
- generic RAG framework;
- rule-engine framework;
- separate narrative-packet service;
- extra CI workflow;
- second reporting system.

Complexity may be added only after a demonstrated clinical/software failure requires it.

## 3. P3 — Clinical Evidence

Module: `szondi3/clinical_evidence.py`

P3 consumes one existing `ClinicalProtocolEvaluation` and adds only information that downstream synthesis must not be allowed to recalculate or invent.

### 3.1 `FactorSeriesPattern`

For every factor `h s e hy k p d m`, P3 records:

- exact ordered P1 symbols including quantum marks;
- base reactions;
- one-based profile positions for positive, negative, null and ambivalent reactions;
- forced-null positions separately;
- profiles carrying quantum tension;
- total quantum units;
- actual longitudinal base-reaction transitions.

These are deterministic observations of the already scored series. They are not Szondian interpretations and do not move into P1 merely because they are deterministic summaries.

Their immediate purpose is to prevent a language model from recounting the protocol itself.

### 3.2 `GroundedFinding`

Every activated P2B finding receives a case-local evidence ID.

Examples:

- `EF_P01_IC_SZONDI_PRIMARY_000010`
- `EF_SERIES_IC_SZONDI_PRIMARY_000003`

The wrapper preserves the existing P2B finding, including doctrine IDs, source IDs, assertion mode, lifecycle status, source-strength note, sensitive-domain flags and anti-inferences.

### 3.3 `GroundingBoundary`

P3 makes downstream gaps explicit. Boundaries include:

- unresolved deterministic calculations;
- unresolved P2B input;
- missing P2B context;
- blocked source conflict/rule.

A later model must not use general knowledge to fill one of these boundaries.

## 4. P4 — Clinical Integration

Module: `szondi3/clinical_integration.py`

P4 organizes relations among P3 evidence without creating new doctrine or increasing certainty.

The first relation vocabulary is intentionally restricted to:

- `COEXISTENCE`
- `CONTRAST`
- `LONGITUDINAL_CHANGE`
- `QUALIFICATION`

There is deliberately no `CAUSES` relation in this first vocabulary.

The reason is clinical and epistemic: repeated co-occurrence or temporal succession in a Szondi series does not by itself license the narrative claim that one drive configuration caused another. Causal integration may be introduced only if a later source-grounded, reviewed rule demonstrates the exact authorization required.

### 4.1 Automatic integration

The only automatically generated P4 relation in the foundation is within-factor `LONGITUDINAL_CHANGE`, and only where the P3 pattern contains an actual base-reaction transition.

No cross-factor psychological synthesis is generated automatically.

### 4.2 Explicit relations

A future reviewed integration rule may add a typed `IntegrationRelation`, but every support ID must resolve to evidence present in the same P3 object. Orphan support fails closed.

## 5. Direct grounding contract for AI

`ClinicalIntegration.to_grounding_payload()` is the direct first contract for a future narrative model.

It contains:

- deterministic factor-series patterns;
- activated P2B findings;
- full P2B provenance and anti-inference constraints;
- explicit grounding boundaries;
- typed P4 relations.

There is intentionally no separate `NarrativePacket` subsystem. If multiple future consumers demonstrate a need for a separate transport abstraction, it can be extracted later without changing P3/P4 semantics.

The payload does **not** contain or create therapist synthesis. `TherapistSynthesis` in `clinical_report.py` remains `MANUAL_CLINICIAN_INPUT_ONLY`.

## 6. Current doctrinal bottleneck

The initial production P2B catalogue contains 12 approved claims and is structurally sound, but it is not yet rich enough for a serious grounded interpretation of a complete ten-profile clinical series.

In particular, Cabinet Alpha currently has useful structural/guard claims for the Ego vector and several series methods, while clinically important meanings involving `h`, `s`, `e`, `hy`, `d`, `m`, vector configurations and richer series relations are not yet broadly executable.

Therefore:

> **Do not connect a free narrative model and let it fill missing Szondian semantics from pretraining.**

The next clinical increment is a small, case-driven P2B expansion from already represented primary doctrine.

## 7. Fall40 development case

The Fall40 ten-profile series is the first intended adversarial development case for the grounded vertical slice.

It is used to discover exactly which executable primitives are missing and to test failures already observed in unconstrained LLM interpretation, especially:

- wrong counting of repeated/quantum reactions;
- confusion of factor/radical level with signed elementary function;
- replacement of Szondi terms by generic psychodynamic language;
- unsupported reversal of a factor meaning;
- causal stories manufactured from co-occurrence or sequence.

Fall40 narrative outputs are **not doctrine** and are not imported as executable truth. They are test evidence for what the controlled system must preserve or refuse.

## 8. Anti-dinosaur budget

Until the Fall40 grounded vertical slice has been demonstrated, the following budget is binding for this workstream:

1. only the two new runtime modules `clinical_evidence.py` and `clinical_integration.py` for P3/P4;
2. no new external runtime dependency;
3. no new database;
4. no second ontology or semantic type system unless a measured grounding failure demonstrates the need;
5. no additional CI workflow — use existing runtime tests;
6. no second report model;
7. no separate narrative-packet subsystem;
8. one narrative-model call is the default first experiment;
9. P2B grows from concrete clinical capability needs, not catalogue-size goals;
10. every new architectural component must answer a demonstrated failure that cannot be solved in an existing layer.

## 9. Validation requirements before AI is clinically trusted

The future grounded narrative step must demonstrate at least:

- **counting test:** deterministic P3 counts/patterns, not LLM recounting, determine the reported series facts;
- **provenance test:** every Szondian proposition in generated narrative maps to supplied P2B/P4 support IDs;
- **ablation test:** remove a relevant executable meaning and the corresponding clinical proposition disappears rather than being restored from model pretraining;
- **canary test:** a test-only controlled meaning supplied through the grounding object is followed by the model;
- **mutation test:** controlled change to supplied meaning changes the narrative predictably;
- **boundary test:** unresolved/missing support remains unresolved instead of being plausibly completed;
- **causality test:** `COEXISTENCE`/`LONGITUDINAL_CHANGE` input does not become an unsupported causal chain;
- **model-swap test:** replacing the narrative model may change wording and organization, but not the fundamental grounded clinical content.

## 10. Succession / recovery

A new chat taking over this work should:

1. read `docs/PROJECT_MISSION.md` and the normative foundation;
2. read this file before designing any new AI/RAG architecture;
3. verify current `main`, active PRs and CI independently;
4. inspect `szondi3/clinical_evidence.py`, `szondi3/clinical_integration.py` and `tests/test_clinical_grounding.py`;
5. preserve the anti-dinosaur budget unless a concrete failed test justifies changing it;
6. continue with the smallest Fall40-driven P2B tranche that can be supported directly by current primary doctrine;
7. never use an unconstrained LLM interpretation as authority for a missing P2B meaning.

If this workstream is interrupted mid-change, the repository branch/PR and tests, not chat history, define the recoverable state.

## 11. Completion criterion for this foundation increment

This foundation increment is complete when:

- P3 produces deterministic factor-series patterns, grounded P2B evidence identities and explicit boundaries;
- P4 validates typed relations and produces deterministic within-factor longitudinal relations;
- `ClinicalIntegration` serializes a direct provenance-rich grounding payload;
- `CAUSES` is absent from the initial P4 relation vocabulary;
- existing P0/P1/P2A/P2B/runtime tests remain green;
- new grounding tests are green;
- the work is merged through normal repository governance.

This does **not** declare complete clinical P3/P4 coverage or the P2B interpretation catalogue finished. It establishes the stable narrow foundation on which those capabilities can grow without replacing the project architecture.

## Final invariant

> **Szondi3 produces the authorized clinical knowledge. A narrative model may express that knowledge; it may not become an unrecorded second source of Szondian doctrine.**
