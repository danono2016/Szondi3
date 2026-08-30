# Szondi3 AI Clinical Manifest

Status: **NORMATIVE STRATEGY DOCUMENT**

## 1. Mission

The purpose of the Szondi3 AI clinical layer is to transform verified Szondi3 outputs into coherent clinician-facing language without allowing a general-purpose language model to become an independent source of scoring, doctrine, interpretation, or diagnosis.

The system must remain epistemically anchored in the repository.

The governing proposition is:

> **The AI may formulate what Szondi3 supports; it may not support what Szondi3 merely allows it to formulate.**

A second governing proposition protects the project from a different failure mode:

> **Build only as much architecture as is required to make the next clinically meaningful behavior correct and demonstrable.**

## 2. Non-negotiable hierarchy

All production clinical interpretation must respect:

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE INTERPRETATION -> SOFTWARE BEHAVIOR -> AI SYNTHESIS`

The hierarchy is directional. A lower layer may not silently create authority for an upper layer.

Therefore:

- software tests cannot establish Szondian doctrine;
- a doctrine passage cannot automatically become an individualized clinical claim;
- an LLM inference cannot become executable interpretation merely because it is plausible;
- polished prose cannot strengthen weak or qualified source support.

## 3. Role separation

### 3.1 P1 deterministic engine

P1 answers: **What formally resulted from the recorded test data?**

P1 owns scoring, reactions, vectors, series calculations, formulas, indices, deterministic classifications, and fail-closed ambiguity.

**Invariant:** no production scoring may be generated, repaired, or guessed by an LLM.

### 3.2 P2A doctrine layer

P2A answers: **What does the admitted Szondian evidence establish or qualify?**

Doctrine remains source-linked, provenance-preserving, and distinct from executable case interpretation.

### 3.3 P2B executable interpretation

P2B answers: **Which individualized or series-level conclusions are authorized when specified facts are present?**

P2B is the only layer permitted to turn case facts into production-eligible Szondian assertions.

### 3.4 Canonical evidence retrieval

Retrieval answers: **What exact canonical evidence supports the claims activated in this case?**

Retrieval supplies evidence. It does not invent clinical rules.

### 3.5 AI synthesis

AI synthesis answers: **How can the authorized findings be integrated into coherent clinical prose?**

The AI may organize, connect, prioritize, and phrase evidence-backed findings, while preserving their assertion strength and limitations.

It may not introduce unsupported Szondian content from model memory, external literature, or the web.

### 3.6 Provenance validator

The validator answers: **Did the generated report exceed what the case evidence authorizes?**

The validator has veto power. A report that fails provenance or anti-inference checks is not released.

## 4. Production invariants

The following are release-blocking invariants.

### I-01 — No LLM scoring

All formal scoring and deterministic calculations originate in Szondi3 code.

### I-02 — No unsupported individualized claim

Every individualized Szondian statement must map to at least one production-admissible executable claim and its triggering case facts.

### I-03 — No web-derived Szondian interpretation

The production clinical synthesis runtime has no web-search capability and no unrestricted external retrieval capability.

### I-04 — No silent repair

`UNRESOLVED`, ambiguity, source conflict, missing context, and non-applicability remain visible. The AI may explain them; it may not resolve them without admitted evidence and an executable rule.

### I-05 — Claim-local provenance

Every clinical assertion must retain machine-readable links to its `claim_id`, relevant `doctrine_ids`, `source_ids`, and triggering facts.

### I-06 — Assertion-strength conservation

The prose must not become more certain, global, diagnostic, causal, or permanent than the executable claim allows.

### I-07 — Anti-inference enforcement

Explicit prohibited conclusions travel with the claim through retrieval, synthesis, validation, and rendering.

### I-08 — Coverage gaps remain gaps

When Szondi3 does not yet authorize an interpretation, the runtime records a coverage gap rather than using generic model knowledge to fill it.

### I-09 — Source-family separation

`SZONDI_PRIMARY`, Deri, Mélon, and other admitted post-Szondian sources remain distinguishable. Secondary interpretation may not be silently presented as Szondi-primary doctrine.

### I-10 — No hidden knowledge path

The production synthesis layer must be reproducible from the supplied evidence packet. If a sentence cannot be explained from that packet, it is presumptively inadmissible.

### I-11 — Historical lexical fidelity

Clinician-facing Szondi reports must preserve source-authorized historical Szondian terminology, including wording that is archaic, severe, baroque, pathologizing, or inconsistent with contemporary clinical idiom.

The synthesis layer must not replace source-authorized Szondian terms with euphemisms, contemporary psychological constructs, or semantically softened paraphrases merely to make the report sound more modern, neutral, or socially acceptable.

When Romanian translation risks importing a foreign contemporary theory or weakening the original concept, the original German term should remain visible alongside the Romanian rendering.

Lexical fidelity does not expand semantic permission. A historical term may appear in the clinician-facing report only when the active P2B claim authorizes that term or meaning in the case and scope at hand. Contextual, conditional, diagnostic, biographical, or stronger branches remain prohibited unless separately authorized.

When a historical Szondian term resembles a contemporary diagnosis or concept, preserve and delimit its historical/testological Szondian status rather than silently modernizing, euphemizing, or deleting it.

## 5. Production versus research

### PRODUCTION mode

Permitted:

- deterministic P1 outputs;
- production-admissible P2B claims;
- linked canonical evidence;
- explicit clinician-supplied context;
- conservative synthesis of the above.

Forbidden:

- web search for Szondian meaning;
- unrestricted model-memory interpretation;
- candidate doctrine;
- non-approved executable claims;
- model-generated diagnostic repair;
- fabricated citations or provenance.

### RESEARCH / AUTHORING mode

May assist in:

- finding candidate canonical passages;
- proposing candidate doctrine relations;
- drafting candidate executable claims;
- identifying coverage gaps;
- comparing possible formalizations.

But all such outputs remain visibly non-production until they pass the project lifecycle and required human review.

## 6. RAG is subordinate, not authoritative

The project does not define its clinical AI as "RAG over Szondi books."

Raw retrieval can produce semantically plausible but unauthorized inference. Therefore retrieval must be constrained by the executable interpretation layer whenever the case assertion is individualized.

Preferred path:

`case facts -> executable claim -> doctrine/source links -> canonical retrieval -> synthesis`

Not:

`case -> semantic search over books -> LLM interpretation`

Unrestricted semantic retrieval may be useful in research mode, but it is not sufficient evidence architecture for production clinical interpretation.

## 7. Global corpus closure is not required

This strategy does not require complete closure of `Schicksalsanalyse`, `Schicksalsanalytische Therapie`, or `Triebpathologie` before clinically useful work may proceed.

The production criterion is narrower and stricter:

> A released statement must have sufficient admitted evidence and executable authorization for that statement.

Global corpus incompleteness is therefore not a license for improvisation, but neither is it a blanket blocker on already-supported claims.

## 8. The desired failure mode

When the system knows less, it must say less.

A shorter report with explicit coverage gaps is superior to a richer report contaminated by unsupported general knowledge.

The correct behavior under insufficient evidence is one of:

- omit the unsupported interpretation;
- state the unresolved condition;
- state the coverage gap;
- request explicit clinician context if the executable claim requires it.

The correct behavior is never to manufacture completeness.

## 9. Clinician role

The system assists clinical reasoning but does not erase clinician authorship.

The project should preserve distinct fields for:

- machine-derived observations;
- deterministic calculations;
- executable Szondian findings;
- uncertainty and limitations;
- AI-generated synthesis constrained by evidence;
- explicit clinician-authored synthesis or commentary.

A therapist-level conclusion must never be falsely represented as mechanically entailed by the test when the underlying evidence does not establish it.

## 10. Lean architecture is a validity requirement

Szondi3 must also defend against architectural overgrowth.

The project has failed if it becomes so elaborate that maintaining governance, schemas, audits, registries, validators, and abstractions consumes the work that should produce clinically demonstrable behavior.

Therefore:

- prefer a working vertical slice over a complete framework;
- prefer one concrete type over a hierarchy of speculative abstractions;
- prefer extending an existing document over creating another governance document;
- prefer one test tied to a real failure mode over many tests that merely restate implementation detail;
- prefer deletion and simplification when a layer no longer pays for its complexity;
- do not create an audit solely because a previous audit exists;
- do not add infrastructure that cannot yet be exercised by a concrete case unless it closes a demonstrated critical risk;
- generalize only after repetition appears in working code;
- protect stable P1/P2B components from redesign for architectural elegance.

### Complexity trigger

Any proposed new layer must answer:

1. **Which concrete failure does this prevent?**
2. **Can an existing layer prevent it with less machinery?**
3. **Can the new layer be exercised by the current vertical slice?**
4. **What would we delete or avoid because this layer exists?**

If these questions do not have strong answers, the default decision is **do not build it yet**.

### Progress stop rule

If two consecutive milestones mainly add infrastructure, documentation, audit machinery, or abstractions without producing a new end-to-end clinical capability, the next milestone is simplification or a clinician-visible vertical slice, not more architecture.

## 11. Success criterion

The strategy succeeds when an adversarial evaluator can deliberately tempt the model with facts it likely knows from general training and the system still refuses to use that knowledge unless Szondi3 supplies admissible evidence.

But epistemic safety alone is not sufficient. The implementation must also remain understandable, testable, and small enough that a clinician-facing capability can advance continuously.

The ultimate product test is not "Does the model know Szondi?"

It is:

> **Can the model produce a useful Szondi report while being prevented from acting as an independent Szondi authority — without requiring an architecture so heavy that the report never reaches the clinician?**
