# Szondi3 AI Clinical Decision Register

Status: **INITIAL STRATEGY DECISIONS**

This register records the decisions that define the AI-clinical workstream. It is intentionally separate from the global project `DECISION_LOG.md` until the strategy is reviewed and intentionally integrated into main governance.

## AI-D-001 — The LLM is not a Szondian authority

**Decision:** The production language model is a synthesis layer only.

**Consequence:** scoring, doctrine, and executable interpretation must be supplied by Szondi3 before synthesis.

**Rejected alternative:** asking a general-purpose model to interpret the test using its own knowledge and then adding citations afterward.

---

## AI-D-002 — Production uses a closed-world evidence boundary

**Decision:** For Szondian semantics, only information contained in the versioned Clinical Evidence Packet is available to the production model.

**Consequence:** model memory is not accepted as evidence even when correct.

**Rejected alternative:** prompt-only instruction to "prefer project sources."

---

## AI-D-003 — Web access is disabled for production clinical synthesis

**Decision:** The clinical synthesis runtime has no web-search route.

**Consequence:** external web material cannot silently influence Szondian interpretation.

**Rejected alternative:** allowing web access but requesting that the model use it only when necessary.

---

## AI-D-004 — Executable claims mediate individualized interpretation

**Decision:** Canonical doctrinal text does not automatically authorize a person-level conclusion.

**Consequence:** case-specific Szondian assertions require an eligible P2B claim triggered by case facts.

**Rejected alternative:** direct RAG over canonical books followed by free LLM application to the case.

---

## AI-D-005 — Retrieval is identifier-first

**Decision:** Production canonical retrieval prefers explicit claim -> doctrine -> source-unit links before semantic search.

**Consequence:** retrieval follows already-established provenance paths and remains reproducible.

**Rejected alternative:** unrestricted vector similarity as the primary clinical evidence selector.

---

## AI-D-006 — Clinical Evidence Packet is the system boundary

**Decision:** A versioned immutable evidence packet is the only semantic input to production synthesis.

**Consequence:** the packet must include deterministic results, facts, active claims, canonical evidence, anti-inferences, unresolved states, coverage gaps, and explicit clinician context.

**Rejected alternative:** passing raw protocol + long system prompt directly to an LLM.

---

## AI-D-007 — Synthesis is proposition-first

**Decision:** The model first returns structured propositions with support references; prose rendering follows validation.

**Consequence:** provenance can be checked before fluent language hides unsupported inference.

**Rejected alternative:** validating only a finished free-text essay after generation.

---

## AI-D-008 — Validator has veto power

**Decision:** A generated draft is not a report until it passes provenance and anti-inference validation.

**Consequence:** unsupported propositions block release.

**Rejected alternative:** treating validation warnings as advisory while still showing the report.

---

## AI-D-009 — Coverage gaps are first-class output

**Decision:** Missing executable interpretation is represented explicitly as a coverage gap.

**Consequence:** reports may be incomplete by design; gaps feed future P2B development.

**Rejected alternative:** filling gaps with general Szondi knowledge to maintain report richness.

---

## AI-D-010 — Assertion strength cannot increase in prose

**Decision:** Synthesis must conserve or weaken, never strengthen, the assertion mode of its supporting claims.

**Consequence:** tendency cannot become certainty; local label cannot become global identity; insufficiency cannot become diagnosis.

**Rejected alternative:** allowing stylistic confidence to strengthen semantic claims.

---

## AI-D-011 — Anti-inferences are runtime data

**Decision:** Anti-inferences are carried through the complete pipeline and tested semantically.

**Consequence:** the system guards against prohibited meanings, not merely prohibited exact phrases.

**Rejected alternative:** storing anti-inferences only as documentation comments.

---

## AI-D-012 — Global corpus closure is not a prerequisite

**Decision:** Complete closure of `Schicksalsanalyse`, `Schicksalsanalytische Therapie`, and `Triebpathologie` is not required for this workstream.

**Consequence:** production eligibility is claim-local and evidence-local. Unsupported areas remain gaps.

**Rejected alternative:** blocking all AI-clinical progress until every primary corpus is globally closed.

---

## AI-D-013 — P1 stability is protected

**Decision:** The AI workstream does not rewrite stable P1 machinery unless a demonstrated defect or explicit dependency requires it.

**Consequence:** the first implementation seam is downstream of `ClinicalProtocolEvaluation`.

**Rejected alternative:** redesigning deterministic scoring merely to simplify LLM integration.

---

## AI-D-014 — Production and research modes are separate

**Decision:** Candidate doctrine discovery and candidate claim authoring occur in research/authoring mode, never in production synthesis.

**Consequence:** AI can assist project development without silently promoting its own proposals into clinical authority.

**Rejected alternative:** one universal agent that alternates implicitly between research and production.

---

## AI-D-015 — Versioning is part of provenance

**Decision:** Every report must retain the software revision, doctrine snapshot, P2B release, evidence-packet version/hash, synthesis contract version, model configuration, and validator version.

**Consequence:** reports remain auditable after the system evolves.

**Rejected alternative:** storing only the generated text and source bibliography.

---

## AI-D-016 — First code milestone contains no LLM

**Decision:** The first implementation increment builds schemas, evidence packet compilation, serialization, and integrity tests before adding model calls.

**Consequence:** evidence boundaries are testable independently from generative behavior.

**Rejected alternative:** prototype the chatbot first and retrofit structure later.

---

## AI-D-017 — Report richness follows evidence coverage

**Decision:** Clinical report richness is allowed to grow only as production-eligible executable interpretation coverage grows.

**Consequence:** a sparse but valid report is a successful intermediate product.

**Rejected alternative:** using generic language-model knowledge to make early reports appear complete.

---

## Open design questions

The following are deliberately not resolved by this baseline and require implementation evidence or steward review:

1. Exact schema names and Python module placement for the evidence packet.
2. Whether final semantic anti-inference checking requires a second constrained model pass in addition to deterministic rules.
3. Exact representation of canonical excerpt boundaries and source locations.
4. Whether clinician-supplied context is stored directly in the evidence packet or through a linked immutable context object.
5. Exact production model/provider abstraction and pinning strategy.
6. Exact clinician review threshold for `S7_CLINICIAN_REVIEW_READY`.
7. Whether a human-readable provenance appendix is always shown or only available on demand.

These questions do not weaken the core invariants above.
