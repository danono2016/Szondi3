# Szondi3 AI Clinical Strategy — Entry Point

Status: **STRATEGY BASELINE — NOT A PRODUCTION GATE**  
Branch baseline: `main@d192c984eff9d753de4ee60955accec3d6252938`  
Strategy branch: `work/ai-clinical-provenance-strategy-001`

## Purpose

This branch defines the architecture required for an AI-assisted Szondi clinical report to be a product of **Szondi3**, rather than a product of a general-purpose language model using remembered, inferred, or web-retrieved Szondi material.

The core problem is simple: a language model asked to "score and interpret a Szondi series" can bypass the project, reconstruct generic Szondi knowledge from model memory or the web, and produce prose that is not traceable to the canonical Szondi3 evidence chain.

The solution is therefore architectural, not prompt-only.

The target invariant is:

> **No clinical Szondi statement may be released unless Szondi3 can show the deterministic facts, executable interpretation, canonical evidence, provenance, and admissible assertion strength that support it.**

The language model is the final synthesis layer. It is not the scoring engine, not the doctrinal authority, and not an unrestricted interpreter.

## Reading order

1. `AI_CLINICAL_MANIFEST.md` — governing principles and non-negotiable invariants.
2. `AI_CLINICAL_ARCHITECTURE.md` — target component architecture and data flow.
3. `AI_CLINICAL_RUNTIME_CONTRACT.md` — exact runtime permissions and prohibitions for the AI synthesis layer.
4. `AI_CLINICAL_ROADMAP.md` — staged implementation plan from strategy baseline to production release.
5. `AI_CLINICAL_VALIDATION_PLAN.md` — adversarial tests, metrics, release gates, and failure criteria.

## Governing hierarchy

This strategy remains subordinate to the repository's existing constitutional and doctrinal governance.

The semantic hierarchy remains:

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE INTERPRETATION -> SOFTWARE BEHAVIOR -> AI SYNTHESIS`

AI synthesis is deliberately placed **after** software behavior. It may communicate already-authorized interpretation; it may not create new Szondian authority.

## What this branch changes

At strategy-baseline stage, this branch changes **documentation only**.

It does not:

- alter P0 evidence;
- alter P1 scoring;
- alter existing P2A doctrine objects;
- alter approved P2B claims;
- restore commits or PRs that are not on current `main`;
- declare P2A, P2B, P3, or P4 complete;
- authorize an AI-generated therapist synthesis.

## Scope decision: corpus closure

Global closure of `Schicksalsanalyse`, `Schicksalsanalytische Therapie`, or `Triebpathologie` is **not a prerequisite** for this AI-clinical strategy.

The relevant requirement is claim-local evidence sufficiency: any statement released by the clinical AI must be supported by the specific executable claims and canonical evidence admitted for that statement.

A corpus may remain globally unfinished while a narrowly evidenced claim is production-eligible.

## Target runtime pipeline

```text
recorded choices / scored input
          |
          v
P1 deterministic Szondi3 engine
          |
          v
formal case facts
          |
          v
P2B executable interpretation
          |
          v
canonical evidence retrieval
          |
          v
Clinical Evidence Packet
          |
          v
constrained AI synthesis
          |
          v
provenance + anti-inference validation
          |
          v
clinician-facing report
```

No production path may bypass this pipeline.

## Definition of "AI working correctly"

The AI is working correctly when it can produce a coherent clinical report **without using its own Szondi knowledge as evidence**.

Correctness therefore requires all of the following:

- 0% LLM-derived scoring;
- 0 unsupported individualized Szondian assertions;
- 0 web-derived Szondian interpretation in production;
- 0 silent repair of `UNRESOLVED` P1/P2B states;
- 100% provenance for clinical Szondian assertions;
- preservation of assertion strength and anti-inferences;
- explicit coverage gaps instead of improvised completeness.

## Strategy status model

The strategy uses the following stages:

- `S0_STRATEGY_BASELINE`
- `S1_RUNTIME_CONTRACT_LOCKED`
- `S2_EVIDENCE_PACKET_IMPLEMENTED`
- `S3_CANONICAL_RETRIEVAL_IMPLEMENTED`
- `S4_CONSTRAINED_SYNTHESIS_IMPLEMENTED`
- `S5_PROVENANCE_VALIDATOR_IMPLEMENTED`
- `S6_ADVERSARIAL_HARNESS_GREEN`
- `S7_CLINICIAN_REVIEW_READY`
- `S8_PRODUCTION_RELEASE_CANDIDATE`

No later stage may be inferred merely from the presence of code. Each stage has explicit exit criteria in the roadmap.

## First implementation objective

The first code objective after this documentation baseline is **not** to add more report prose and not to add unrestricted RAG.

It is to define and implement a versioned **Clinical Evidence Packet** that can be produced deterministically from the existing `ClinicalProtocolEvaluation` plus linked executable interpretation and canonical evidence.

That packet becomes the only admissible knowledge boundary for the production AI synthesis layer.
