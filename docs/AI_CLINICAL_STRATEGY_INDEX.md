# Szondi3 AI Clinical Strategy — Entry Point

Status: **ACTIVE EXECUTABLE STRATEGY — NOT A FORMAL PRODUCTION GATE**  
Verified baseline `main`: `d192c984eff9d753de4ee60955accec3d6252938`  
Strategy branch: `work/ai-clinical-provenance-strategy-001`  
Current transfer authority: `docs/CHAT_TRANSFER_PACKAGE.md`

## Mandatory successor rule

Any new chat continuing this strategy MUST read `docs/CHAT_TRANSFER_PACKAGE.md` first and independently re-verify current `main`, working branch, PR and CI state before writing.

The transfer package contains the mandatory orthodoxy check-ins (`O0`–`O7`), STOP conditions, current executable state and exact next safe experiment.

If this index and the transfer package ever disagree about current repository state, the successor must re-read the actual repository and repair the stale document rather than choosing the more convenient version.

## Purpose

This strategy exists so an AI-assisted Szondi clinical report is a product of **Szondi3**, not a product of a general-purpose model using remembered, inferred or web-retrieved Szondi material.

The governing invariant is:

> **No person-specific Szondian statement may be released unless Szondi3 can show the deterministic fact, active executable interpretation, canonical evidence, assertion boundary and anti-inference support that authorize it.**

The language model is the final synthesis layer. It is not the scoring engine, doctrinal authority or unrestricted interpreter.

A second governing invariant is equally important:

> **Build only as much architecture as is required to make the next clinically meaningful behavior correct and demonstrable.**

## Governing hierarchy

```text
PRIMARY EVIDENCE
  -> DOCTRINE
    -> EXECUTABLE INTERPRETATION
      -> SOFTWARE BEHAVIOR
        -> AI SYNTHESIS
```

AI synthesis is downstream of software behavior. It may phrase already-authorized meaning; it may not create new Szondian authority.

## Required reading after the transfer package

1. `AI_CLINICAL_MANIFEST.md`
2. `AI_CLINICAL_ROADMAP.md`
3. `AI_CLINICAL_RUNTIME_CONTRACT.md`
4. `AI_CLINICAL_DECISION_REGISTER.md`
5. `AI_CLINICAL_ARCHITECTURE.md` — target/background only; do not implement speculative machinery automatically
6. `AI_CLINICAL_VALIDATION_PLAN.md` — test inventory only; do not build exhaustive validation without a concrete failure

Then inspect the actual current code named in `CHAT_TRANSFER_PACKAGE.md`.

## Current executable vertical slice

The strategy branch now implements:

```text
ClinicalProtocolEvaluation
  -> ClinicalReport
    -> ClinicalEvidencePacket
      -> OpenAI preview request
        -> SynthesisProposition
          -> deterministic local validation
```

Key runtime files:

- `szondi3/clinical_evidence_packet.py`
- `szondi3/clinical_synthesis.py`
- `szondi3/clinical_ai_preview.py`
- `tests/test_clinical_evidence_packet.py`

The branch also preserves exact activating fact IDs and anti-inference IDs through the existing clinical report path.

## Current guarantees

The executable slice now enforces, mechanically:

- no LLM scoring;
- exact case-fact provenance for cited active claims;
- exact canonical doctrine bundle for cited claims;
- exact PROFILE/SERIES scope;
- required anti-inference ID transport;
- deterministic doctrine lookup by identity, not similarity;
- real `0` distinct from forced `ø`;
- tool-less preview request (`tools: []`);
- provider storage disabled (`store: false`);
- structured provider output;
- local validation before provider output is exposed downstream.

It does **not** yet prove semantic faithfulness of arbitrary natural-language prose. Do not claim otherwise.

## Current production boundary

The OpenAI path is **preview-only**.

No live model call was executed as part of the verified branch checkpoint recorded in the transfer package. CI uses synthetic provider responses only.

A live preview requires a caller-supplied credential in a controlled environment. Credentials must not be committed or embedded in source code.

## Current P2B boundary

Twelve initial source-linked claims are `APPROVED` in `szondi3/interpretation_catalogue.py`.

Production synthesis may use only production-admissible active claims. Canonical doctrine passages do not independently authorize new case-level conclusions.

A clinically relevant fact without an executable claim is a **coverage gap**, not an invitation for the model to improvise from doctrine or generic psychology.

## Corpus closure rule

Global closure of `Schicksalsanalyse`, `Schicksalsanalytische Therapie` or `Triebpathologie` is **not** required for this strategy.

Claim-local evidence sufficiency controls production eligibility.

## Fall 40 role

Fall 40 is a regression specimen chosen because five unconstrained AI reports exposed concrete failure modes.

It is not runtime doctrine, not a hard-coded case and not permission to universalize Szondi's published case-specific interpretation.

Its role is to test that deterministic morphology, vector Gestalts, exact support bundles and anti-inference guards survive the pipeline before AI wording.

## Legacy rule

Szondi1, Szondi2, old AI reports and historical PRs may be used to discover failure modes or as comparison oracles only.

They are not authority.

Do not automatically restore PRs #61–#64.

## Lean roadmap status

The strategy deliberately moved away from a framework-first roadmap.

The working sequence is:

```text
one real case
  -> smallest evidence packet
  -> exact canonical support
  -> constrained synthesis
  -> smallest effective validator
  -> clinician inspection
  -> expand only through observed failures / coverage gaps
```

The useful vertical slice through structured provider preview now exists.

The next meaningful step is therefore **a controlled live preview and inspection of actual model behavior**, not another layer of speculative infrastructure.

## Before adding any new architecture

Use the `O5_COMPLEXITY_JUSTIFICATION` check in `CHAT_TRANSFER_PACKAGE.md`.

No new validator, provider abstraction, RAG layer, ontology, retrieval platform, CI workflow or governance layer should be built unless a concrete observed failure or explicit repository requirement justifies it.

## Formal gate warning

The presence of working P2B/AI-clinical code does not automatically declare formal project gates.

At the recorded transfer checkpoint, durable formal gates remain:

- `P0_SOURCES_PASS`
- `P1_DETERMINISTIC_ENGINE_PASS`

Do not invent `P2A_PRIMARY_DOCTRINE_PASS`, `P2B_EXECUTABLE_INTERPRETATION_PASS`, P3 or P4 declarations.

## North star

> **The AI is allowed to write beautifully; it is not allowed to invent what Szondi3 has not authorized.**

Correct-but-incomplete is acceptable.

Fluent-but-unsupported is failure.
