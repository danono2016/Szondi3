# Szondi3 AI Clinical Roadmap

Status: **IMPLEMENTATION ROADMAP**

## 1. Goal

Build a production clinical AI path in which every Szondian statement is downstream of Szondi3 deterministic facts, executable interpretation, and canonical evidence, with automatic rejection of unsupported model output.

The roadmap begins from the current repository baseline but treats the new AI path as a fresh architectural workstream. Existing P1 and approved P2B behavior are reused as verified dependencies; they are not rewritten merely to make room for AI.

## 2. Guiding implementation rule

Each phase must establish a stronger evidence boundary before the next phase increases generative freedom.

Therefore the order is:

**contract -> evidence packet -> canonical resolver -> constrained synthesis -> validator -> adversarial tests -> clinical review -> production candidate**

Not:

**prompt -> RAG -> polished report -> retrofit provenance later**.

---

# S0 — Strategy baseline

## Deliverables

- AI clinical manifest.
- Target architecture.
- Runtime contract.
- Roadmap.
- Validation plan.
- Decision register.

## Exit criteria

- documents are internally consistent;
- no strategy document declares unfinished project gates complete;
- source hierarchy matches repository governance;
- web prohibition and closed-world evidence rule are explicit;
- global closure of Schicksalsanalyse/Therapie/Triebpathologie is not treated as a prerequisite;
- first code seam is identified.

## Output

`S0_STRATEGY_BASELINE`

---

# S1 — Runtime contract lock

## Objective

Turn the prose contract into code-level schemas and invariants before any generative reporter is built.

## Deliverables

1. Typed schemas for:
   - `EvidenceFactRef`
   - `EvidenceClaimRef`
   - `CanonicalEvidenceRef`
   - `CoverageGap`
   - `ClinicalEvidencePacket`
   - `SupportedProposition`
   - `SynthesisValidationResult`

2. Enumerations for:
   - packet mode;
   - evidence class;
   - rejection codes;
   - proposition scope.

3. Contract tests that reject:
   - unknown IDs;
   - production-inadmissible claim status;
   - missing triggering facts;
   - missing evidence links;
   - unsupported packet versions.

## Design decision

Schemas must be independent of any specific LLM provider.

## Exit criteria

- contract objects serialize deterministically;
- invalid provenance cannot be represented silently;
- no LLM integration exists yet;
- all current tests remain green.

## Output

`S1_RUNTIME_CONTRACT_LOCKED`

---

# S2 — Clinical Evidence Packet implementation

## Objective

Compile one immutable, versioned evidence boundary from the existing clinical protocol evaluation.

## Primary entry point

```text
compile_clinical_evidence_packet(
    evaluation,
    doctrine_snapshot=...,
    interpretation_release=...,
    clinician_context=...
)
```

## Deliverables

- packet compiler;
- stable packet schema version;
- deterministic ordering;
- packet hash/fingerprint;
- inclusion of:
  - observations;
  - P1 calculations and states;
  - facts;
  - active claims;
  - unresolved/blocked claims;
  - anti-inferences;
  - source/doctrine references;
  - coverage gaps;
  - production/review mode.

## Coverage-gap logic — first version

A gap may be emitted when:

- a formal P1 result exists but no eligible P2B claim covers it;
- a claim is blocked by missing executable support;
- a required evidence link is absent;
- an expected interpretation domain has no production-admissible rule.

Gap detection must not itself invent a missing interpretation.

## Tests

- Cabinet Alpha packet snapshot;
- unresolved formula packet;
- non-applicable Dur-Moll packet;
- claim anti-inference preservation;
- stable packet hashing.

## Exit criteria

A complete case can be represented as a packet without calling a language model.

## Output

`S2_EVIDENCE_PACKET_IMPLEMENTED`

---

# S3 — Canonical Evidence Resolver

## Objective

Make source evidence retrievable through repository identifiers, not model initiative.

## Deliverables

### Direct resolution

- claim -> doctrine IDs;
- doctrine -> source unit IDs;
- source unit -> canonical text;
- source unit -> source family;
- source unit -> location metadata;
- visual-arbiter availability/reference where applicable.

### Resolver API

Proposed functions:

```text
get_claim_evidence(claim_id, snapshot_id)
get_doctrine_evidence(doctrine_id, snapshot_id)
get_canonical_unit(source_id, unit_id)
resolve_evidence_for_active_claims(...)
```

### Constraints

- source identity must come from canonical project registries;
- no internet retrieval in production;
- no silent substitution of Deri/Mélon for Szondi-primary;
- visual arbitration limitations remain visible where no paired PDF exists;
- raw semantic search, if later introduced, must be secondary and explicitly classified.

## Tests

- every production claim resolves to known source metadata;
- unknown evidence IDs fail closed;
- source-family boundaries remain correct;
- deterministic repeated retrieval returns the same canonical units for the same snapshot.

## Exit criteria

The packet can contain actual canonical evidence text for every supported production claim that requires it.

## Output

`S3_CANONICAL_RETRIEVAL_IMPLEMENTED`

---

# S4 — Constrained AI synthesis

## Objective

Introduce an LLM only after the evidence packet and resolver are working.

## Deliverables

1. Provider-independent synthesis interface.
2. Fixed production prompt/contract version.
3. Tool isolation:
   - web unavailable;
   - repository browsing unavailable;
   - arbitrary retrieval unavailable.
4. Structured proposition-first response.
5. Romanian clinical renderer as first language target; language choice remains a rendering concern, not an evidence concern.

## Required behavior

The model may:

- integrate multiple active claims;
- express interactions already encoded in evidence;
- distinguish profile and series findings;
- write coherent paragraphs;
- expose limitations.

The model may not:

- create new Szondian facts;
- introduce unsupported factor meanings;
- infer diagnostic conclusions from generic knowledge;
- repair missing calculations;
- convert doctrine into a new person-level claim.

## Tests

- same packet, multiple model runs: semantic support set remains unchanged;
- sparse packet produces sparse report;
- packet with no active claims produces no invented clinical interpretation;
- explicit prompt injection asking model to use its own Szondi knowledge is ignored/rejected.

## Exit criteria

The model can produce useful structured propositions using packet evidence only.

## Output

`S4_CONSTRAINED_SYNTHESIS_IMPLEMENTED`

---

# S5 — Provenance and anti-inference validator

## Objective

Make model overreach a release-blocking technical failure.

## Deliverables

### Deterministic checks

- referenced claim exists;
- claim active;
- lifecycle production-admissible;
- triggering facts exist;
- evidence IDs exist;
- scope compatible;
- unresolved result not asserted as resolved;
- no external source reference.

### Assertion-strength checks

Implement rule-based detection where feasible for known escalations.

### Anti-inference checks

Each anti-inference receives:

- stable ID;
- target prohibited meaning;
- test examples/paraphrases;
- severity;
- deterministic check where possible;
- constrained semantic review where necessary.

### Release API

```text
validate_synthesis(packet, draft) -> ValidationResult
```

No final report renderer accepts an invalid draft.

## Exit criteria

Every generated proposition is either mechanically supported or rejected with a specific code.

## Output

`S5_PROVENANCE_VALIDATOR_IMPLEMENTED`

---

# S6 — Adversarial harness

## Objective

Test whether the architecture prevents the exact failure that motivated this workstream.

## Required adversarial families

- general-model-knowledge temptation;
- web temptation;
- unsupported factor interpretation;
- unresolved P1 repair;
- doctrine-to-diagnosis leap;
- local-to-global escalation;
- anti-inference paraphrase;
- sparse-evidence pressure for a long report;
- fake citation/provenance;
- source-family contamination;
- predecessor/Szondi2 authority shortcut;
- prompt injection inside clinician context.

## CI behavior

Critical adversarial failures fail the workflow.

## Exit criteria

All mandatory adversarial tests green across the supported production model configuration(s).

## Output

`S6_ADVERSARIAL_HARNESS_GREEN`

---

# S7 — Clinician review readiness

## Objective

Determine whether evidence-constrained reports are clinically intelligible and useful, not merely provenance-correct.

## Review dimensions

- fidelity to Szondian meaning;
- coherence across the series;
- appropriate weighting of findings;
- preservation of uncertainty;
- absence of mechanical sign-list reporting;
- absence of unsupported modernizing substitutions;
- transparency of limitations;
- usefulness to a clinician.

## Review protocol

For each test case, reviewer sees:

1. raw/structured protocol;
2. deterministic outputs;
3. evidence packet;
4. generated report;
5. expandable proposition provenance;
6. coverage gaps.

Reviewer judgments must distinguish:

- **bad prose with correct evidence**;
- **bad interpretation rule**;
- **missing P2B coverage**;
- **retrieval defect**;
- **validator defect**.

This prevents report-style complaints from being "fixed" by inventing semantics.

## Exit criteria

A defined clinician review set passes agreed fidelity and utility thresholds with no critical provenance failures.

## Output

`S7_CLINICIAN_REVIEW_READY`

---

# S8 — Production release candidate

## Objective

Integrate the validated pipeline into a controlled production surface.

## Required production manifest

Each generated report stores:

- case ID;
- repository/software revision;
- doctrine snapshot;
- P2B release;
- packet schema/version/hash;
- synthesis contract version;
- model identifier/configuration;
- validator version;
- production mode;
- active claim IDs;
- unresolved/gap counts;
- external Szondian sources used = `NONE`.

## Operational safeguards

- explicit production/research mode separation;
- no web capability in clinical synthesis runtime;
- audit log of packet and validation result;
- rollbackable releases;
- no silent model/provider upgrade;
- regression corpus retained.

## Exit criteria

- all S0-S7 criteria remain satisfied;
- production smoke tests pass;
- clinician sign-off is recorded according to governance;
- rollback procedure is tested;
- no formal project gate is declared beyond what governance evidence supports.

## Output

`S8_PRODUCTION_RELEASE_CANDIDATE`

---

# 3. Parallel workstream: P2B coverage expansion

P2B coverage may expand in parallel after S2 establishes coverage-gap visibility.

Priority should be driven by observed clinical gaps, not by arbitrary corpus order.

Suggested expansion dimensions include:

- factor reactions and intensity/quantum distinctions;
- vector constellations;
- Ego constellations beyond the initial tranche;
- series dynamics and recurrent patterns;
- foreground/background relations where executable evidence exists;
- root/latency class and formula interpretations;
- Dur-Moll and Sozialindex qualifications;
- Vorder-Ich/Hinter-Ich and complement relations;
- cross-profile patterning;
- explicit negative rules preventing classical overreadings.

Each new rule follows the existing evidence lifecycle. The AI runtime never receives a shortcut around that lifecycle.

# 4. What must not happen during implementation

- Do not start with a general chatbot prompt.
- Do not connect web search to production clinical synthesis.
- Do not treat vector similarity as executable interpretation.
- Do not enlarge report length by lowering evidence requirements.
- Do not rewrite stable P1 code unless a demonstrated dependency requires it.
- Do not treat a green AI test as proof of Szondian doctrine.
- Do not require global closure of excluded corpora as a precondition for claim-local progress.
- Do not restore historical non-current branch/PR work merely because it was once merged.

# 5. Recommended immediate next implementation increment

After review of the S0 documents, create a narrow implementation branch for **S1 + the minimum S2 schema seam**.

The first PR should ideally contain:

- evidence packet dataclasses/types;
- serialization;
- rejection enums;
- tests;
- no LLM calls;
- no new clinical claims;
- no canonical semantic expansion.

That PR should prove the evidence boundary before any model integration begins.
