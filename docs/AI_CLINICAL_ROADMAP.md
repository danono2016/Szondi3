# Szondi3 AI Clinical Roadmap

Status: **LEAN IMPLEMENTATION ROADMAP**

## 1. Goal

Build the smallest production path in which AI-generated Szondian clinical prose is constrained by Szondi3 deterministic facts, executable interpretation, and canonical evidence.

The roadmap deliberately avoids building a complete platform in advance.

The governing implementation rule is:

> **one concrete case -> smallest necessary evidence boundary -> constrained synthesis -> validation -> clinician inspection -> only then generalize**

Existing stable P1 and approved P2B behavior are dependencies. They are not redesigned merely to make the AI architecture look cleaner.

---

## 2. Complexity discipline

This roadmap is not a sequence of bureaucratic gates. It is a sequence of increasingly useful clinical capabilities.

A new abstraction, registry, schema, audit, validator stage, workflow, or document is added only when it is required by:

- a concrete failing clinical case;
- a demonstrated provenance/safety defect;
- repeated working code that clearly needs consolidation;
- an explicit repository-governance requirement.

### Stop rule

If two consecutive milestones mainly add infrastructure, documentation, validation machinery, or audits without producing a new end-to-end clinical capability, stop architectural expansion and simplify.

### Preferred engineering behaviors

- extend existing objects before creating parallel hierarchies;
- add one data structure before designing a family of data structures;
- add one test for one meaningful failure mode;
- keep experimental code local until repetition justifies abstraction;
- delete unused structure early;
- do not audit an audit unless new evidence or contradiction requires it.

---

# S0 — Strategy baseline

Already established on the strategy branch:

- manifest;
- architecture;
- runtime contract;
- roadmap;
- validation plan;
- decision register.

This is sufficient strategy documentation for now. No additional governance document should be created unless a concrete need appears.

**Output:** `S0_STRATEGY_BASELINE`

---

# S1 — First evidence packet vertical slice

## Objective

Take **one existing concrete case** (Cabinet Alpha is acceptable) and represent exactly what Szondi3 already knows about it in one minimal evidence object.

Do not design a generalized framework first.

## Minimum implementation

Start with the smallest representation that can carry:

- case/profile identity;
- P1 observations/results actually needed by the case;
- active P2B claims;
- claim provenance already available (`claim_id`, doctrine/source IDs);
- anti-inferences;
- unresolved states;
- production/review mode.

A single `ClinicalEvidencePacket` plus the minimum nested values is preferable to a speculative hierarchy of packet interfaces and registries.

## Required test

For the chosen case:

1. run existing clinical evaluation;
2. compile packet;
3. serialize packet deterministically;
4. inspect packet manually;
5. verify that no information came from an LLM or the web.

## Exit criterion

One real/synthetic case can be converted from existing Szondi3 clinical evaluation into an understandable, deterministic evidence packet.

**Output:** `S1_FIRST_PACKET_WORKS`

---

# S2 — Canonical evidence for that same case

## Objective

Resolve the active claims in the S1 packet to their actual admitted canonical evidence.

Do not build a broad semantic-search subsystem yet.

## Minimum implementation

Use identifier-first resolution:

`active claim -> doctrine/source references -> canonical unit text`

Implement only the retrieval calls required by the first case.

Required properties:

- deterministic resolution;
- source-family identity preserved;
- unknown IDs fail visibly;
- no internet retrieval;
- visual-arbitration limitations remain visible when relevant.

## Exit criterion

The first packet contains the actual canonical evidence needed to support its active production claims.

**Output:** `S2_FIRST_CANONICAL_PACKET_WORKS`

---

# S3 — First constrained AI report

## Objective

Generate the first clinician-readable report from the S2 packet while denying the model any independent Szondian evidence path.

## Runtime constraints

The model receives:

- the evidence packet;
- a compact synthesis instruction;
- no web tool;
- no repository browser;
- no arbitrary source search.

The first version does **not** need a provider abstraction framework. One pinned provider/model path is sufficient to prove the behavior.

## Output shape

Prefer a small structured response containing:

- supported propositions;
- support IDs for each proposition;
- limitations/coverage gaps;
- rendered clinical prose.

If proposition-first output proves unnecessarily complicated for the first slice, use the smallest structured form that still permits support checking. Generalize later.

## Required adversarial checks

For the same case, explicitly ask the model to:

- use what it already knows about Szondi;
- make the report longer than the evidence supports;
- repair an unresolved calculation;
- derive a diagnosis from a local sign.

Expected behavior: it does not comply with unsupported semantic requests.

## Exit criterion

The first complete report is generated from Szondi3 evidence only and is clinically readable, even if sparse.

**Output:** `S3_FIRST_CONSTRAINED_REPORT`

---

# S4 — Smallest effective validator

## Objective

Block the concrete overreach observed in S3 tests.

Do not attempt a universal natural-language theorem prover.

## Start with deterministic checks

Check only what can already be verified reliably:

- referenced claim exists;
- claim was active for the case;
- claim is production-admissible when in production mode;
- support IDs exist in the packet;
- unresolved P1 results are not presented as resolved;
- external/web sources are absent;
- required anti-inferences remain attached.

Add semantic/paraphrase validation only when an actual test demonstrates that deterministic validation is insufficient.

## Exit criterion

A deliberately unsupported or malformed first-case report is rejected with a clear reason, while the valid report passes.

**Output:** `S4_MINIMUM_VALIDATOR_WORKS`

---

# S5 — Expand through cases, not frameworks

## Objective

Add a small set of clinically different cases and let their failures determine the next code.

Suggested early cases:

1. Cabinet Alpha / broad initial-claim activation;
2. sparse evidence case;
3. unresolved P1 case;
4. case exposing a meaningful P2B coverage gap;
5. case stressing an anti-inference.

For each new case:

`run -> inspect gap/failure -> smallest correction -> regression test`

Possible outcomes are deliberately different:

- fix packet representation;
- add one resolver capability;
- strengthen one validator rule;
- identify a P2B coverage gap;
- improve prose instruction;
- conclude that no code change is needed.

## Exit criterion

Several distinct cases traverse the same small pipeline without requiring case-specific hacks.

Only now should repeated code be refactored into broader abstractions.

**Output:** `S5_MULTI_CASE_VERTICAL_SLICE`

---

# S6 — Clinician review loop

## Objective

Determine whether the constrained reports are useful, not merely technically traceable.

The clinician should be able to inspect:

- deterministic results;
- active claims;
- canonical support;
- report;
- limitations/coverage gaps.

Feedback must be classified before code changes:

- prose problem;
- wrong/missing executable interpretation;
- retrieval problem;
- provenance/validation problem;
- missing clinician context.

This prevents a stylistic complaint from triggering a new architecture layer or an unsupported doctrine change.

## Exit criterion

A small clinician-reviewed set produces reports judged both source-faithful and practically readable, with no critical provenance failures.

**Output:** `S6_CLINICIAN_REVIEWED_SLICE`

---

# S7 — Targeted hardening

## Objective

Harden only the weaknesses revealed by S1-S6.

Possible work, only if evidence requires it:

- stronger packet versioning;
- provider abstraction;
- richer provenance rendering;
- additional anti-inference checks;
- more canonical resolver coverage;
- additional CI adversarial tests;
- performance/caching.

None of these is mandatory merely because it appeared in the original architecture sketch.

## Exit criterion

Known high-consequence failures have regression protection and the code remains understandable enough to modify without broad collateral work.

**Output:** `S7_TARGETED_HARDENING`

---

# S8 — Production candidate

## Objective

Expose the small validated pipeline through a controlled clinical surface.

Minimum retained provenance:

- software revision;
- evidence packet version/identity;
- doctrine/P2B release identifiers actually used;
- model identifier/configuration;
- validator version if a separate validator exists;
- active claim IDs;
- unresolved/gap summary;
- external Szondian sources used = `NONE`.

Operational requirements:

- explicit production/research separation;
- web unavailable to clinical synthesis;
- rollback possible;
- model upgrade not silent;
- regression cases retained.

## Exit criterion

The production candidate can run the clinician-reviewed cases end to end and fail closed on known adversarial cases without depending on undocumented model knowledge.

**Output:** `S8_PRODUCTION_CANDIDATE`

---

## 3. P2B coverage expansion

P2B may grow in parallel, but the priority comes from observed coverage gaps in actual cases rather than an obligation to formalize an entire corpus in advance.

A coverage-gap workflow should be simple:

`case gap -> locate canonical support -> propose narrow executable claim -> review -> approve/reject -> rerun case`

No global closure of `Schicksalsanalyse`, `Schicksalsanalytische Therapie`, or `Triebpathologie` is required for this workstream.

---

## 4. Things explicitly not to build yet

Until a failing case requires them, do not build:

- a universal agent framework;
- a general-purpose RAG platform;
- multiple LLM-provider adapters;
- a large ontology of report propositions;
- a second semantic-validator model;
- a new governance layer for every milestone;
- duplicated registries for data already represented canonically;
- broad P1 refactors;
- exhaustive test matrices disconnected from observed failures.

---

## 5. Immediate next increment

The next implementation branch should contain only what is required for **S1_FIRST_PACKET_WORKS**.

Ideal scope:

- one minimal `ClinicalEvidencePacket` representation;
- one compiler from existing `ClinicalProtocolEvaluation`;
- one Cabinet Alpha packet test;
- deterministic serialization if needed for inspection/reproducibility;
- no LLM;
- no new P2B claims;
- no new canonical-search framework;
- no new audit document.

The question at the end of that PR is not "Is the architecture complete?"

It is:

> **Can we now see, in one small object, exactly what Szondi3 is entitled to tell an AI about one case?**
