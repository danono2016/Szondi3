# Szondi3 AI Clinical Runtime Contract

Status: **PROPOSED NORMATIVE RUNTIME CONTRACT**

## 1. Purpose

This contract defines what a production clinical language model may receive, what it may do, what it must preserve, and what causes automatic rejection of its output.

The purpose is not to encourage good model behavior. The purpose is to make unacceptable behavior structurally detectable and release-blocking.

## 2. Allowed inputs

The production synthesizer may receive only:

1. a versioned `ClinicalEvidencePacket`;
2. a fixed synthesis instruction set identified by version;
3. explicit clinician-provided contextual information that has been separately admitted into the packet;
4. formatting preferences that do not alter semantic authority.

The production synthesizer must not receive direct unrestricted access to:

- the public web;
- arbitrary external documents;
- general Szondi web searches;
- arbitrary repository browsing;
- model-selected source discovery;
- unclassified candidate doctrine;
- historical predecessor outputs treated as authority.

## 3. Permitted transformations

The model may:

- reorder supported findings for readability;
- combine compatible findings into coherent paragraphs;
- explain relationships already represented in the evidence packet;
- make explicit contrasts represented by claims or anti-inferences;
- summarize deterministic calculations without changing them;
- state uncertainty, non-applicability, source limitations, and coverage gaps;
- preserve Szondian terminology while writing natural clinician-facing language;
- distinguish profile-level from series-level findings;
- distinguish source-established content from implementation-constrained or qualified content when the packet encodes that distinction.

## 4. Forbidden transformations

The model must not:

- score photographs, factors, vectors, profiles, or series;
- infer a missing deterministic result;
- reinterpret an `UNRESOLVED` result as if resolved;
- invent an executable rule from a doctrinal paragraph;
- infer person-level meaning from a source passage when no active P2B claim authorizes that inference;
- use generic model knowledge to extend the evidence packet;
- add a diagnosis, trait, prognosis, causal claim, criminality inference, sexuality inference, hereditary/genetic inference, or therapeutic conclusion unless specifically authorized by active claims;
- convert a local/profile statement into a global/person statement without explicit authorization;
- convert a tendency into certainty;
- convert a qualified or negative assertion into a positive diagnosis;
- omit an anti-inference when omission would make the surrounding prose misleading;
- fabricate citations, doctrine IDs, source IDs, or evidence IDs;
- cite a source not present in the packet;
- conceal known coverage gaps by using generic prose.

## 5. Closed-world rule

Production synthesis operates under a **closed-world evidence assumption**:

> For Szondian interpretation, what is not present in the packet is unavailable to the model, even if the base model happens to know it.

The model may use ordinary linguistic knowledge to write Romanian or another requested language. It may use ordinary grammar and discourse skills. It may not use hidden Szondi knowledge as semantic evidence.

## 6. Proposition-first output

The first model output should be machine-readable propositions rather than unconstrained final prose.

Required fields:

```text
proposition_id
scope
profile_number | null
text
support_claim_ids[]
support_fact_ids[]
support_evidence_ids[]
assertion_mode
anti_inference_ids_applied[]
```

Optional fields:

```text
relation_to_previous
coverage_gap_reference
uncertainty_reference
```

Only validated propositions may be rendered into final prose.

## 7. Support rule

Every Szondian proposition about the case must satisfy:

```text
exists active claim
AND
claim is production-admissible
AND
claim's trigger is satisfied by packet facts
AND
referenced canonical evidence exists
AND
proposition does not exceed assertion mode
AND
anti-inferences are respected
```

If any term is false, the proposition is invalid.

## 8. Assertion-strength rules

The validator and prompt contract should recognize at least these prohibited escalations:

- `may / can / is compatible with` -> `is`;
- `testological label` -> `global personality fact`;
- `profile-local` -> `permanent person characteristic`;
- `requires contextual confrontation` -> `diagnosis established`;
- `not sufficient alone` -> `sufficient in this case`;
- `one possible meaning` -> `exclusive meaning`;
- `source-qualified relation` -> `unqualified causal relation`.

When in doubt, the synthesis must choose the weaker supported formulation.

## 9. Anti-inference transport

Anti-inferences are first-class runtime data.

They must remain attached to the claim through:

```text
catalogue -> evaluation -> evidence packet -> synthesis -> validator -> report
```

The model may not merely avoid the exact forbidden phrase. It must avoid semantically equivalent prohibited conclusions.

Because semantic equivalence can be difficult to validate deterministically, high-risk anti-inferences should be tested with explicit adversarial examples and, where needed, a second constrained review pass.

## 10. Coverage-gap behavior

If a clinically relevant formal fact has no executable interpretation, the system should create a coverage-gap record.

Production prose may say, for example:

- that the current executable corpus does not yet support a further interpretation of that result;
- that a calculation is available but not yet connected to an approved clinical claim;
- that additional clinician context would be required if a defined claim is blocked on context.

It must not replace the missing interpretation with textbook-style generalities.

## 11. Web rule

Production clinical interpretation must run with web access disabled.

If future product requirements add web access to the surrounding application, the clinical synthesis component must still be isolated so that external web content cannot enter the Szondian evidence packet or support case-level Szondian propositions.

Any future exception requires an explicit governance decision and a new source-class policy. No exception is implicit.

## 12. Clinician context

Clinician-provided context may enter the packet only as clearly marked external case context.

It must never be relabeled as Szondi-primary evidence.

Claims that require context must declare the required context fields explicitly. Missing context produces `BLOCKED_CONTEXT`, not model guesswork.

## 13. Therapist synthesis

The existing distinction between machine-produced findings and clinician-authored synthesis should be preserved.

If the product later permits AI assistance in drafting therapist synthesis, that function must be separately labeled and must not claim that its higher-order clinical integration is mechanically entailed by the Szondi test.

## 14. Release rejection codes

Minimum rejection taxonomy:

- `R_UNSUPPORTED_PROPOSITION`
- `R_UNKNOWN_CLAIM`
- `R_INACTIVE_CLAIM`
- `R_NONPRODUCTION_CLAIM`
- `R_UNKNOWN_EVIDENCE`
- `R_ASSERTION_ESCALATION`
- `R_ANTI_INFERENCE_VIOLATION`
- `R_UNRESOLVED_REPAIR`
- `R_EXTERNAL_SOURCE_CONTAMINATION`
- `R_SCOPE_ESCALATION`
- `R_DIAGNOSTIC_OVERREACH`

A final report is releasable only when no rejection remains.

## 15. Prompting is not the security boundary

The system prompt should repeat these rules, but compliance cannot depend on prompt wording alone.

The actual security boundary is the combination of:

- restricted model inputs;
- restricted tool access;
- structured proposition output;
- deterministic provenance checks;
- anti-inference checks;
- explicit release gate.

## 16. Reproducibility

Every final report should retain an internal manifest containing:

```text
case identifier
Szondi3 revision
P1 engine revision
doctrine snapshot
P2B release
evidence packet hash
synthesis contract version
model identifier
validator version
production mode
external Szondian sources used: NONE
```

The report may render a simplified form to the clinician, but the full manifest should remain auditable.
