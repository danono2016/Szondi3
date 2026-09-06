# Szondi3 AI Clinical Architecture

Status: **TARGET ARCHITECTURE**

## 1. Architectural objective

The clinical AI path must make it impossible for a language model to substitute generic knowledge for Szondi3 evidence without that substitution becoming detectable and release-blocking.

The architecture therefore treats the language model as a constrained renderer over a versioned evidence object.

## 2. End-to-end flow

```text
INPUT
  |
  v
[1] Recorded Test Data
  |
  v
[2] P1 Deterministic Engine
  |
  v
[3] Case Fact Graph
  |
  v
[4] P2B Executable Interpretation
  |
  v
[5] Canonical Evidence Resolver
  |
  v
[6] Clinical Evidence Packet Compiler
  |
  v
[7] Constrained AI Synthesizer
  |
  v
[8] Provenance / Anti-Inference Validator
  |
  +---- FAIL ---> regenerate / redact / expose unresolved state
  |
  v
[9] Clinician-Facing Renderer
```

Production execution must never jump from input directly to step 7.

## 3. Component responsibilities

### 3.1 Recorded Test Data

Accepts structured test selections or already-valid structured profile input.

Responsibilities:

- preserve raw recorded choices when available;
- validate input shape;
- preserve profile ordering;
- distinguish foreground/background or other formally defined protocol positions when applicable.

It does not interpret.

### 3.2 P1 Deterministic Engine

Existing Szondi3 deterministic machinery remains the single scoring authority.

Output includes:

- factor reactions;
- vector reactions;
- profile-level formal facts;
- series indices;
- tension measures;
- class/subclass/root-direction results;
- complete/abbreviated formula states;
- Dur-Moll and Sozialindex where applicable;
- explicit `UNRESOLVED` and `NOT_APPLICABLE` states.

No LLM is called here.

### 3.3 Case Fact Graph

A normalized machine-readable layer translating P1 outputs into facts that can trigger executable interpretation.

Each fact should contain at minimum:

```text
fact_id
scope
profile_number | null
predicate
value
origin_function
origin_result
status
```

The fact layer must preserve exact provenance back to P1 outputs.

### 3.4 P2B Executable Interpretation

Evaluates only explicit executable claims against case facts.

Each evaluated claim should expose:

```text
claim_id
activation_status
triggering_fact_ids
missing_fact_ids
required_context
assertion_mode
lifecycle_status
doctrine_ids
source_ids
anti_inferences
sensitive_domains
```

Production permits only claims whose lifecycle status is admitted for production.

### 3.5 Canonical Evidence Resolver

This component resolves evidence for already-selected claims.

Primary retrieval sequence:

1. `claim_id` -> linked `doctrine_ids`;
2. `doctrine_id` -> linked canonical source units;
3. source units -> canonical text and, when required/available, visual arbiter metadata;
4. supplemental in-corpus retrieval only when explicitly allowed by contract.

The resolver should prefer direct identifier traversal over semantic search.

Semantic search may assist when an identifier link is incomplete, but any resulting evidence must remain classified and must not silently create a new executable inference.

### 3.6 Clinical Evidence Packet Compiler

This is the central boundary object between Szondi3 and the language model.

The packet must be immutable for one synthesis attempt, versioned, serializable, and reproducible.

Proposed top-level schema:

```text
ClinicalEvidencePacket
  packet_version
  case_id
  generated_at
  engine_revision
  doctrine_snapshot_id
  interpretation_release_id
  production_mode

  observations[]
  deterministic_results[]
  facts[]
  active_claims[]
  unresolved_claims[]
  blocked_claims[]
  canonical_evidence[]
  anti_inferences[]
  coverage_gaps[]
  clinician_context[]
  synthesis_constraints
```

#### Active claim record

```text
claim_id
scope
profile_number | null
statement
assertion_mode
lifecycle_status
triggering_fact_ids[]
doctrine_ids[]
source_ids[]
canonical_evidence_ids[]
anti_inference_ids[]
sensitive_domains[]
```

#### Canonical evidence record

```text
evidence_id
source_family
source_id
canonical_unit_id
text
location
visual_arbiter_available
visual_arbiter_reference | null
evidence_class
```

#### Coverage gap record

```text
gap_id
scope
observed_fact_ids[]
description
reason
candidate_research_query | null
production_effect
```

Coverage gaps are data, not errors to hide.

### 3.7 Constrained AI Synthesizer

The synthesizer receives only:

- the Clinical Evidence Packet;
- a fixed production synthesis contract;
- optional explicit clinician-provided context admitted into the packet.

It must not receive:

- unrestricted web tools;
- arbitrary repository browsing;
- general source discovery tools;
- a prompt inviting free Szondi interpretation.

The synthesizer should produce structured output first, prose second.

Proposed internal output:

```text
ClinicalSynthesisDraft
  sections[]
    section_id
    heading
    propositions[]
      proposition_id
      text
      support_claim_ids[]
      support_fact_ids[]
      support_evidence_ids[]
      assertion_mode
      anti_inference_ids_applied[]
```

A renderer may later turn this into fluent prose.

### 3.8 Provenance / Anti-Inference Validator

The validator is deterministic wherever possible.

For every proposition it must verify:

- all referenced claims exist in the packet;
- claims are active in this case;
- production lifecycle is admissible;
- required facts actually triggered the claim;
- evidence identifiers exist;
- assertion strength has not been increased;
- prohibited conclusions are absent;
- unresolved facts have not been converted into positive assertions;
- no external source identifier appears.

The validator returns:

```text
VALID
INVALID_UNSUPPORTED_PROPOSITION
INVALID_ASSERTION_ESCALATION
INVALID_ANTI_INFERENCE_VIOLATION
INVALID_SOURCE_PROVENANCE
INVALID_UNRESOLVED_REPAIR
```

Invalid drafts are not rendered as final reports.

### 3.9 Clinician-Facing Renderer

The renderer consumes only validated synthesis plus deterministic report data.

It may show:

- concise clinical prose;
- structured calculations;
- explicit limitations;
- optional provenance expansion;
- clinician-authored synthesis field.

The user-facing surface may hide machine identifiers by default, but the identifiers must remain inspectable.

## 4. Two runtime modes

### 4.1 Production

Hard restrictions:

- no web;
- no unrestricted retrieval;
- approved executable claims only;
- packet-bound synthesis;
- validator mandatory;
- coverage gaps preserved.

### 4.2 Research / Authoring

May use broader canonical retrieval and AI assistance to propose:

- candidate doctrine links;
- candidate P2B claims;
- missing relations;
- likely coverage gaps.

Research output must never masquerade as production output.

## 5. Why direct RAG is insufficient

A vector search over the canonical books may retrieve a relevant paragraph, but the model can still perform an unauthorized individualized inference.

Example failure pattern:

```text
profile fact -> semantic search -> doctrinal paragraph -> LLM concludes person-level meaning
```

The safe pattern is:

```text
profile fact -> executable claim -> linked doctrine -> linked evidence -> LLM phrases authorized meaning
```

RAG remains useful as an evidence-access mechanism, not as the authority that decides what the case means.

## 6. Provenance granularity

Provenance should be maintained at proposition level rather than only report level.

A report-level bibliography proves only that sources were available. It does not prove that a particular sentence was authorized.

Therefore each proposition should remain traceable to:

`case fact -> executable claim -> doctrine -> canonical source unit`.

## 7. Versioning requirements

Every generated report must record at minimum:

- Szondi3 commit/release identifier;
- P1 engine revision;
- doctrine snapshot identifier;
- P2B interpretation release identifier;
- evidence packet schema version;
- synthesis contract version;
- validator version;
- production/research mode.

A report should therefore be reproducible even after the project evolves.

## 8. Failure philosophy

The architecture deliberately prefers false negatives over unsupported clinical positives.

When evidence is insufficient:

- preserve uncertainty;
- reduce prose;
- emit a coverage gap;
- require later P2B work.

The architecture must never reward the model for sounding complete.

## 9. First code seam

The recommended first implementation seam is between the existing `ClinicalProtocolEvaluation` / structured clinical report and the future AI layer.

Implement:

```text
compile_clinical_evidence_packet(evaluation, ...)
```

before implementing any generative report writer.

This establishes a hard evidence boundary first and minimizes the blast radius to existing P1/P2B behavior.
