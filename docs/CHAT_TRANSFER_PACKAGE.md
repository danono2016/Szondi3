# SZONDI3 — CANONICAL CHAT TRANSFER PACKAGE

Status: **MANDATORY SUCCESSOR ENTRY POINT**  
Repository: `danono2016/Szondi3`  
Prepared on: 2026-08-29  
Verified `main` baseline at preparation: `d192c984eff9d753de4ee60955accec3d6252938`  
Verified strategy branch at preparation: `work/ai-clinical-provenance-strategy-001@259bf6a17bb867b71071e102ad647136adc33b01`  
Open draft PR at preparation: **#65 — Build minimal provenance-constrained clinical evidence packet**  
PR #65 status at preparation: **OPEN / DRAFT / MERGEABLE / NOT MERGED**  
Verification at preparation: **all five PR workflows green** on `259bf6a...`.

---

## 0. Why this file exists

This document is the mandatory transfer package for any future chat that continues Szondi3, especially the AI-clinical strategy.

It exists because a capable language model can still damage the project by:

- trusting remembered Szondi knowledge instead of repository evidence;
- reconstructing doctrine from generic psychology;
- importing design ideas from abandoned Szondi1/Szondi2 attempts;
- treating historical PRs or old reports as current authority;
- inventing P2B meaning to make a report richer;
- building large frameworks before one real case demonstrates a need;
- silently changing scoring, source hierarchy, assertion strength or anti-inference boundaries;
- declaring gates or readiness that the repository has not formally declared.

A successor chat must therefore treat this file as an **operational safety boundary**, not as background reading.

The central rule is:

> **AI-ul nu are voie să „știe Szondi”. AI-ul are voie doar să formuleze ceea ce Szondi3 îi demonstrează și îi furnizează explicit.**

And the engineering corollary is:

> **Build only as much architecture as is required to make the next clinically meaningful behavior correct and demonstrable.**

If a future chat disagrees with these rules, it must stop and ask the user before changing the strategy.

---

# PART I — MANDATORY TAKEOVER PROTOCOL

## 1. Successor chat: first actions are READ ONLY

A new chat receives no write authority merely because it has this package.

Before any repository write it MUST independently re-check:

1. `refs/heads/main`;
2. `refs/heads/work/ai-clinical-provenance-strategy-001` if that branch still exists;
3. PR #65 state, base SHA, head SHA, draft/merge state;
4. current PR/check-run status for the actual head;
5. whether newer commits or PRs have superseded any state recorded here.

The hashes in this package are a verified checkpoint, **not permission to assume the repository has not changed**.

### TAKEOVER CHECK-IN O0 — repository identity

Before writing, a successor must be able to state explicitly:

```text
O0_REPOSITORY_CHECK
main_sha = <freshly verified>
strategy_branch_sha = <freshly verified or branch absent>
pr_65_state = <freshly verified>
ci_head = <freshly verified>
ci_result = <freshly verified>
main_changed_since_transfer = YES|NO
```

If `main` changed from `d192c984eff9d753de4ee60955accec3d6252938`, STOP and inspect the new main before any write.

Do not force-reset, restore or replay anything merely to reproduce this checkpoint.

---

## 2. Mandatory reading order after O0

Read these files before changing the AI-clinical architecture:

1. `docs/CHAT_TRANSFER_PACKAGE.md` — this file;
2. `docs/AI_CLINICAL_STRATEGY_INDEX.md`;
3. `docs/AI_CLINICAL_MANIFEST.md`;
4. `docs/AI_CLINICAL_ROADMAP.md`;
5. `docs/AI_CLINICAL_RUNTIME_CONTRACT.md`;
6. `docs/AI_CLINICAL_ARCHITECTURE.md` only as target/background, not as a mandate to build every abstraction;
7. `docs/AI_CLINICAL_VALIDATION_PLAN.md` only as a test inventory, not as a mandate for exhaustive machinery;
8. `docs/AI_CLINICAL_DECISION_REGISTER.md`;
9. `docs/PROJECT_CONSTITUTION.md`;
10. `docs/DOCTRINAL_FIDELITY_POLICY.md`;
11. `docs/DEVELOPMENT_GOVERNANCE.md`;
12. `config/source_catalog.json`;
13. `config/evidence_lock.json`;
14. `szondi3/interpretation_catalogue.py`;
15. `szondi3/clinical_protocol.py`;
16. `szondi3/clinical_report.py`;
17. `szondi3/clinical_evidence_packet.py`;
18. `szondi3/clinical_synthesis.py`;
19. `szondi3/clinical_ai_preview.py`;
20. `tests/test_clinical_evidence_packet.py`.

The successor should read the actual current files, not rely only on this summary.

---

# PART II — AUTHORITY AND EPISTEMIC ORTHODOXY

## 3. Governing hierarchy

The semantic hierarchy is:

```text
PRIMARY EVIDENCE
    -> DOCTRINE
        -> EXECUTABLE INTERPRETATION
            -> SOFTWARE BEHAVIOR
                -> AI SYNTHESIS
```

No downstream layer may silently rewrite an upstream layer.

### Authority rules

- Original `SZONDI_PRIMARY` evidence is supreme for Szondian doctrine.
- Canonical derivatives are access/provenance aids, not superior doctrine.
- Paired admitted PDFs arbitrate signs, tables, formulas, OCR and layout where relevant.
- Doctrine Registry and Executable Interpretation remain structurally separate.
- Deri/Mélon/post-Szondian material remains separate from `SZONDI_PRIMARY`.
- Tests, CI and code enforce or witness claims; they do not create doctrine.
- Identity/hash correctness does not prove textual or semantic correctness.
- Uncertainty must be preserved and resolved at the lowest affected layer.

### Language fidelity rule

Do not modernize or sanitize Szondi-primary vocabulary merely because it is historically uncomfortable or clinically old-fashioned.

Source-supported hereditary/genetic/genotropic/transgenerational/family, sexual, pathological, criminological and historically anachronistic terminology remains valid primary-language material.

Client communication may later be adapted by a clinician. Repository doctrine must not be politically or stylistically rewritten.

### Historical-person metadata exclusion

Historical metadata about photographed persons is excluded from runtime scoring, doctrine, executable interpretation and generated reports.

---

## 4. Binding corpus rule

The user has explicitly ruled that:

> **Schicksalsanalyse, Therapie și Triebpathologie nu trebuie să parcurgă vreo închidere globală.**

Therefore:

- global closure of these corpora is NOT a prerequisite for AI-clinical production work;
- claim-local evidence sufficiency controls whether a specific claim may be used;
- no successor may reintroduce a global-corpus-closure requirement unless the user explicitly changes this policy.

---

## 5. Legacy contamination rule

Szondi1, Szondi2, old AI reports, old branches and historical PRs may be used as **failure evidence or comparison oracles only**.

They are NOT:

- source truth;
- doctrinal authority;
- implementation templates;
- architecture authority;
- scoring authority;
- automatic restoration targets.

Especially important:

- PRs #61–#64 were historically merged but are not on the verified current `main` baseline.
- A real ref reset/rollback occurred.
- The durable reason for that reset is UNKNOWN.
- **Do not restore PRs #61–#64 automatically.**

Old experiments may tell us **what to test**, never **what to believe**.

---

# PART III — CURRENT REPOSITORY STATE AT TRANSFER

## 6. Accepted formal gates

Accepted durable project gates:

- `P0_SOURCES_PASS`
- `P1_DETERMINISTIC_ENGINE_PASS`

Do NOT infer later formal gates from the existence of code.

At transfer time there is no formal repository declaration of:

- `P2A_PRIMARY_DOCTRINE_PASS`
- `P2B_EXECUTABLE_INTERPRETATION_PASS`
- P3 PASS
- P4 PASS

The project may contain mature downstream code without a formal gate declaration. Preserve that distinction.

---

## 7. Source inventory / canonical boundary

`config/source_catalog.json` currently describes 10 logical sources:

- 8 `SZONDI_PRIMARY`;
- `DERI_1949`;
- `MELON_1975`.

Repository evidence also includes:

- 10 DOCX source files under `sources/text`;
- 8 paired PDF visual arbiters under `sources/originals`;
- 48 WebP stimuli under `assets/stimuli`.

No paired PDF exists for Triebpathologie in the admitted source set; this is a known visual-arbitration limitation.

`config/evidence_lock.json` machine-locks admitted evidence identities.

---

## 8. Current P2A snapshot relevant to AI work

The last integrated Lehrbuch + Ich-Analyse snapshot contains 269 doctrine objects:

- Lehrbuch: 166;
- Ich-Analyse I: 51;
- Ich-Analyse II: 52.

High-value transversal concepts include:

- p/k Egodiastole/Egosystole;
- four elementary Ego functions;
- Negation vs Verdrängung;
- Ich-Bild vs Ich-Mechanismus;
- defense origin vs site;
- Intronegation/Zwang;
- Projektion/Deprojektion;
- Inflation/Deflation;
- Integration/Desintegration;
- Vorder-Ich/Hinter-Ich/complement.

No doctrine object automatically becomes an executable person-specific P2B rule.

---

## 9. Current approved P2B tranche

`szondi3/interpretation_catalogue.py` contains 12 initial `APPROVED` source-linked claims.

They cover:

1. negative Wurzelfaktor != automatic Verdrängung;
2. constantly positive Wurzelfaktor can still reflect unsatisfied need;
3. TspQu is not autonomous;
4. %Sy-Re/TspQu are insufficient alone for clinical diagnosis;
5. Dur–Moll alone cannot ground social valuation;
6. Sozialindex <40% does not authorize criminal/antisocial-act inference;
7. `-p` = Projektion with Einssein/Gleichsein/Partizipationsdrang;
8. `+p` = Inflation with Verdoppelung/Vollkommenheit/Allessein;
9. `+k` = Introjektion with Einverleibung/Inbesitznahme/Alleshaben;
10. `-k` = Negation family; Verdrängung is subordinate, not automatic;
11. `Sch ±±` may be testologically called `integriertes Ich`, but does not prove achieved global/existential/spiritual integration;
12. `Sch 00` may be testologically called `Desintegration`, but an isolated profile is not a global/permanent verdict and requires Vorder-/Hinter-Ich dialectic.

No successor may add new production claims merely because a source passage looks suggestive.

New claims require the existing evidence/lifecycle/human-review path.

---

# PART IV — WHY THE AI STRATEGY EXISTS

## 10. The observed failure

The project demonstrated a structural problem: a general ChatGPT can produce fluent Szondian-looking reports while bypassing Szondi3.

The Fall 40 experiment made this empirical rather than theoretical:

- same verified series;
- five independent AI reports;
- high convergence among those reports;
- significant divergence from Szondi's configuration-first reading;
- repeated generic-psychology substitutions;
- LLM counting instability;
- factor-first interpretation where Szondi uses vector Gestalts;
- causal narratives generated from mere co-occurrence;
- modernization of Szondi vocabulary;
- rare but interpretively important configurations underweighted.

Therefore the project objective is not "make the model smarter about Szondi".

It is:

> **make it structurally impossible for model knowledge to replace project evidence.**

---

## 11. Fall 40 contamination boundary

Fall 40 is now used as a **regression specimen**, not as hidden doctrine.

The runtime implementation contains no `if Fall40` rule and no case-specific clinical interpretation.

The Fall 40 regression fixes deterministic morphology such as:

- 6 tensioned `h+` profiles;
- 7 tensioned `m-` profiles, quantum total 8;
- `P`: `--` x6, `0-` x2, `-0` x2;
- `Sch`: `-±` x1, `-+` x1, `++` x2, `+±` x5, `±±` x1;
- `C +-` x10;
- `S +0` x9 and `+-` x1;
- real `0` remains distinct from forced `ø`.

The published Fall 40 interpretation is not converted automatically into universal executable rules.

Use Fall 40 to test the architecture, not to bend the architecture around the case.

---

# PART V — CURRENT EXECUTABLE AI VERTICAL SLICE

## 12. Current path

At transfer time the branch implements this real path:

```text
ClinicalProtocolEvaluation
    -> ClinicalReport
        -> ClinicalEvidencePacket
            -> OpenAI preview request
                -> SynthesisProposition
                    -> deterministic local validation
```

The intended full conceptual chain remains:

```text
raw/recorded input
  -> P1 deterministic scoring
  -> formal facts
  -> P2B executable interpretation
  -> exact canonical doctrine support
  -> ClinicalEvidencePacket
  -> constrained AI wording
  -> provenance / anti-inference validation
  -> clinician-facing report
```

The current code does NOT yet claim production report release.

---

## 13. `szondi3/clinical_evidence_packet.py`

This module is the finite closed-world handoff to a future narrative model.

Current responsibilities:

- deterministic whole-series factor morphology;
- exact factor symbols and base symbols;
- positive/negative/null/ambivalent/forced-null counts;
- tensioned profiles and quantum totals;
- vector configurations as Gestalts, not only decomposed factors;
- exact vector configuration frequencies;
- existing calculations/findings/uncertainties from `ClinicalReport`;
- exact `support_fact_ids` for active findings;
- exact deterministic doctrine lookup by `doctrine_id`;
- `SOURCE_VERIFIED` canonical excerpts;
- source anchors including canonical units, PDF paths and printed pages;
- fail-closed behavior for missing/unverified doctrine or provenance mismatch.

It does NOT:

- score;
- create doctrine;
- create P2B claims;
- perform semantic search;
- use RAG/vector search;
- use web;
- invoke an LLM;
- include manual therapist synthesis.

Current packet schema version: **2**.

---

## 14. Provenance preservation

A concrete defect was repaired on this branch: the fact that activated a P2B claim used to be lost downstream.

The branch now preserves:

```text
Fact
  -> ActivationRecord.matched_facts
  -> ClinicianFinding.support_fact_ids
  -> ReportFinding.support_fact_ids
  -> ClinicalEvidencePacket
```

A successor must not remove this chain for convenience.

---

## 15. Anti-inference preservation

Another concrete provenance loss was repaired: anti-inference IDs previously degraded to prose only.

The branch now preserves both:

- anti-inference ID, e.g. `AI_SZONDI_000011`;
- prohibited-conclusion text.

This reaches the report and synthesis gate.

Do not collapse anti-inferences back into free text only.

---

## 16. `szondi3/clinical_synthesis.py`

This is deliberately a small deterministic support-envelope validator.

A `SynthesisProposition` must cite:

- `proposition_id`;
- `scope` (`PROFILE` or `SERIES`);
- `profile_number` where applicable;
- proposition text;
- complete `support_claim_ids`;
- complete `support_fact_ids`;
- complete `support_doctrine_ids`;
- complete `anti_inference_ids_applied`.

The validator fails closed if:

- the claim is not active in that exact scope/profile;
- the fact bundle does not exactly match the finding;
- the doctrine bundle does not exactly match the finding;
- canonical evidence is absent;
- an active anti-inference ID is omitted or altered.

Important limitation:

> Correct support IDs do NOT prove that the natural-language proposition is semantically faithful.

Do not falsely claim that this validator solves semantic entailment or paraphrase equivalence.

---

## 17. `szondi3/clinical_ai_preview.py`

This module adds one deliberately narrow provider path.

It is NOT a general provider framework.

Current properties:

- direct OpenAI Responses API call;
- no SDK dependency added;
- default preview model identifier currently `gpt-5.6-sol`;
- `tools: []`;
- `store: false`;
- strict Structured Outputs / JSON Schema;
- `ClinicalEvidencePacket` is the only Szondian evidence boundary;
- prompt explicitly forbids general/pretrained/remembered/web Szondi knowledge from extending the packet;
- API key is supplied by caller only and is not stored in repository code;
- provider response is parsed locally;
- output is not exposed as `PreviewSynthesisResult` unless it passes the local synthesis validator;
- HTTP/provider error bodies are not echoed into exceptions, reducing accidental case-data leakage into logs.

This path is **PREVIEW ONLY**.

No live provider call has yet been executed as part of this branch verification.

CI uses synthetic provider responses only.

---

## 18. Fall 40 exact support-envelope regression

For profile 10, the currently APPROVED `Sch ±±` proposition is required to preserve the exact bundle:

```text
claim:
IC_SZONDI_PRIMARY_000011

activating fact:
foreground_profile_10:vector:Sch:base_symbols

canonical doctrine:
DR_SZ_IA_1956_A_000051
DR_SZ_IA_1956_B_000009

anti-inference:
AI_SZONDI_000011
```

Tests require rejection if:

- the claim is moved to profile 9;
- part of doctrine support is dropped;
- the anti-inference guard is omitted;
- real zero is collapsed into forced `ø`.

This test is a regression against observed AI failure, not a special runtime rule for Fall 40.

---

# PART VI — LEAN ARCHITECTURE / ANTI-DINOSAUR LAW

## 19. Normative constraint from Szondi1/Szondi2 experience

The project must not collapse under code volume, recursive audit, speculative schemas or governance bureaucracy.

Therefore the AI strategy follows **minimum viable epistemic architecture**.

Preferred development sequence:

```text
one real case
  -> smallest packet
  -> smallest exact resolver
  -> constrained synthesis
  -> smallest effective validator
  -> clinician inspection
  -> only then generalize
```

### Before creating any new abstraction, ask

1. Which concrete clinical/provenance failure does this prevent?
2. Can an existing layer prevent it more simply?
3. Can the current vertical slice exercise it immediately?
4. What existing or future complexity does this let us delete or avoid?

If the answers are weak, **do not build it yet**.

### Stop rule

If two consecutive increments mostly add infrastructure, documentation, audits or validation machinery without adding a new end-to-end clinical capability, STOP and simplify.

### Explicitly not to build merely because it sounds architectural

- universal agent framework;
- general RAG platform;
- vector database;
- multiple provider adapters;
- large proposition ontology;
- semantic second-model validator;
- new governance document for every milestone;
- duplicate registries;
- broad P1 refactor for elegance;
- exhaustive test matrices disconnected from observed failure modes.

---

# PART VII — ORTHODOXY CHECK-INS

These check-ins are mandatory moments of self-audit. They are intentionally small and tied to concrete risk.

## O0 — takeover check

Already defined above.

A successor may not write before completing O0.

---

## O1 — pre-write check

Immediately before every repository write in this AI branch:

```text
O1_PREWRITE_CHECK
fresh_main_sha = <verified now>
current_working_branch_sha = <verified now>
write_target = <exact file/path>
concrete_failure_or_capability = <one sentence>
new_doctrine_created = NO unless separately authorized
new_P2B_claim_created = NO unless separate lifecycle/review task
restores_PR61_64 = NO
```

If `main` changed, inspect first. Do not write from stale assumptions.

---

## O2 — semantic-authority check

Before adding any person-specific meaning to code, packet, prompt or report:

```text
O2_SEMANTIC_AUTHORITY
person_specific_statement = <statement>
active_executable_claim = <claim id or NONE>
claim_status = <must be production-admissible for production>
activating_fact = <fact id>
canonical_doctrine = <doctrine ids>
anti_inferences = <ids>
assertion_mode = <mode>
```

If `active_executable_claim = NONE`, the AI must not fill the gap from doctrine, web, model memory or plausible psychodynamics.

Correct result: **coverage gap**, not improvisation.

---

## O3 — provider-call check

Before a live AI preview:

```text
O3_PROVIDER_PREVIEW
mode = PREVIEW_ONLY
packet_only_szondian_evidence = YES
tools = []
store = false
structured_output = YES
api_key_in_repo = NO
web_retrieval = NO
model_may_rescore = NO
model_may_create_new_claims = NO
local_validation_required = YES
```

If any answer differs, STOP.

---

## O4 — post-model check

After any live model response:

1. retain/inspect the raw structured response in the controlled experiment context;
2. run local deterministic proposition validation;
3. separate rejected propositions from accepted propositions;
4. inspect whether accepted propositions nevertheless violate assertion strength or anti-inference semantics in prose;
5. classify observed failures before changing architecture;
6. do not turn the preview directly into a production report.

Required checkpoint record:

```text
O4_MODEL_RESULT
model = <exact model id returned>
response_id = <id>
raw_proposition_count = <n>
locally_validated_count = <n>
rejected_count = <n>
semantic_overreach_observed = YES|NO
new_failure_mode_observed = <description or NONE>
```

---

## O5 — architecture-expansion check

Before adding a new validator, schema, abstraction, provider interface, retrieval mechanism or CI layer:

```text
O5_COMPLEXITY_JUSTIFICATION
observed_failure = <specific failure from a real case/test>
existing_simpler_fix = <yes/no + explanation>
new_component_exercised_by_current_case = YES|NO
what_it_replaces_or_avoids = <specific complexity>
```

If there is no observed failure and no current case exercise, **do not build it**.

---

## O6 — P2B expansion check

P2B must expand only through observed coverage gaps:

```text
case gap
  -> canonical source support located
  -> narrow candidate claim
  -> source/lifecycle review
  -> clinician review where required
  -> APPROVED or rejected
  -> rerun case
```

Never:

```text
case gap -> LLM explanation -> production prose
```

Do not require global closure of Schicksalsanalyse/Therapie/Triebpathologie.

---

## O7 — PR readiness / merge check

PR #65 must remain draft unless the user explicitly authorizes moving toward merge.

Before marking any AI-clinical PR ready or merging:

- re-check actual `main`;
- re-check actual head;
- require all relevant CI green on that exact head;
- inspect real diff, not only PR prose;
- confirm no unreviewed clinical claim was added;
- confirm no hidden provider credential exists;
- confirm preview code is not accidentally presented as production release;
- confirm no formal P2A/P2B/P3/P4 gate is being declared without its own authorized gate process;
- if a live preview has been run, review the observed failure modes first;
- require explicit user authorization for readiness/merge if the branch is still being developed interactively.

---

# PART VIII — STOP CONDITIONS

## 20. Hard STOP conditions for any successor chat

STOP and reconcile before writing if any of the following occurs:

- current `main` differs from the last verified baseline and has not been inspected;
- the strategy branch head differs and the new commits have not been read;
- PR #65 was merged/closed/rebased unexpectedly;
- someone proposes restoring PR #61–#64 merely because they were once merged;
- a proposed report statement has no active executable claim;
- a model is asked to score or repair P1 output;
- a model is given unrestricted repository/web/source search for production interpretation;
- canonical doctrine is being used directly as person-specific inference without P2B authorization;
- a candidate claim is being promoted without lifecycle/source review;
- a high-consequence statement is being softened, modernized or strengthened beyond source support;
- zero/forced-zero or vector Gestalt distinctions are being collapsed;
- a new architecture layer has no concrete observed failure to justify it;
- two successive increments are infrastructure-only;
- CI is red and work continues as if green;
- a successor wants to declare a formal gate merely because tests pass;
- a live preview is treated as a production report;
- a semantic validator is claimed to prove more than it actually validates.

---

# PART IX — NEXT SAFE WORK

## 21. Exact next meaningful experiment

At transfer time, the next clinically meaningful step is **not more infrastructure**.

It is one controlled live preview:

```text
Fall 40 or another already-built ClinicalProtocolEvaluation
  -> ClinicalEvidencePacket
  -> run_openai_preview(...)
  -> structured propositions
  -> local deterministic validation
  -> clinician inspection
  -> failure classification
```

A live call requires an explicitly supplied OpenAI API credential in a controlled environment.

Rules:

- do not commit the credential;
- do not add it to source code;
- do not add a new secrets-management framework merely for the first preview;
- do not run the live call inside ordinary CI;
- do not change architecture before seeing the actual model behavior unless a concrete defect is discovered first.

If no live credential/environment is available, the correct action is to STOP at the validated preview boundary rather than invent new machinery.

---

## 22. What to inspect in the first live preview

Do not judge only whether the prose sounds good.

Inspect:

- does the model restrict itself to active findings?
- does it preserve PROFILE vs SERIES scope?
- does it copy exact fact/doctrine/anti-inference bundles?
- does it subtly upgrade CONDITIONAL to categorical language?
- does it turn testological labels into person-level truths?
- does it import generic psychodynamic causality between independent claims?
- does it modernize or dilute Szondi terminology?
- does it use canonical excerpts to create new case meaning not authorized by P2B?
- does it conceal coverage gaps by writing broad generic prose?
- does it omit important limitations while technically carrying their IDs?

Those observed failures determine the next code change.

---

## 23. Expected likely next branches of work after a live preview

Only if evidenced by the preview:

- tighten deterministic support validation;
- add a narrow semantic guard for one demonstrated failure mode;
- enrich P2B for a real coverage gap;
- improve exact canonical support presentation;
- adjust prompt contract minimally;
- add one regression example reproducing the observed failure.

Do not generalize from one failure into a universal framework unless repeated cases justify the abstraction.

---

# PART X — STATE OF PR #65 AT TRANSFER

## 24. PR #65 contents and status

At the verified transfer checkpoint:

- PR: #65;
- branch: `work/ai-clinical-provenance-strategy-001`;
- head: `259bf6a17bb867b71071e102ad647136adc33b01`;
- base: `main@d192c984eff9d753de4ee60955accec3d6252938`;
- state: OPEN;
- draft: YES;
- merged: NO;
- mergeable: YES;
- all five workflows on the verified head: SUCCESS.

The five workflows were:

- Runtime tests;
- P0 source inspection;
- Foundation verification;
- P2A doctrine registry;
- P0 canonical access.

Do not claim future CI is green without checking the actual current head.

---

# PART XI — FILE-LEVEL MAP FOR SUCCESSORS

## 25. Files that matter immediately

### Governance / strategy

- `docs/AI_CLINICAL_STRATEGY_INDEX.md`
- `docs/AI_CLINICAL_MANIFEST.md`
- `docs/AI_CLINICAL_ROADMAP.md`
- `docs/AI_CLINICAL_RUNTIME_CONTRACT.md`
- `docs/AI_CLINICAL_DECISION_REGISTER.md`

The architecture and validation-plan docs contain useful target material but may be more expansive than the current lean implementation. Do not implement their speculative machinery automatically.

### Existing clinical pipeline

- `szondi3/clinical_protocol.py`
- `szondi3/clinical_interpretation.py`
- `szondi3/clinical_report.py`
- `szondi3/interpretation_catalogue.py`

### New AI-clinical vertical slice

- `szondi3/clinical_evidence_packet.py`
- `szondi3/clinical_synthesis.py`
- `szondi3/clinical_ai_preview.py`
- `tests/test_clinical_evidence_packet.py`

### Canonical doctrine

- `doctrine/registry/*.jsonl`
- `config/source_catalog.json`
- `config/evidence_lock.json`

---

# PART XII — WHAT A SUCCESSOR MUST NEVER CLAIM

## 26. Forbidden status statements unless newly verified

A future chat must not say any of the following merely from this package:

- "main is still d192c984";
- "PR #65 is still draft";
- "CI is green";
- "the branch is still 259bf6a";
- "no one merged anything";
- "P2A is complete";
- "P2B is formally passed";
- "the AI pipeline is production ready";
- "the semantic validator guarantees faithful prose";
- "Fall 40 proves a universal Szondi rule";
- "the five old AI reports are canonical";
- "Szondi1/Szondi2 can be reused because they already solved the problem".

All time-sensitive repository-state statements require fresh verification.

---

# PART XIII — SUCCESSOR ORTHODOXY CERTIFICATE

## 27. Minimal certificate before substantial continuation

A successor chat should explicitly produce the following short certificate to the user or in its working notes before substantial new work:

```text
SZONDI3_AI_ORTHODOXY_CHECK

Repository state re-verified: YES
Current main inspected: YES
Current branch/PR inspected: YES
Current CI inspected: YES
Transfer package read: YES
Manifest + lean roadmap read: YES
P1 remains deterministic and outside LLM: YES
P2B remains sole person-specific semantic authority: YES
Canonical doctrine is support, not automatic person-level inference: YES
Web/model memory excluded from Szondian production semantics: YES
Old Szondi1/Szondi2/old AI reports treated only as failure/oracle evidence: YES
PR61-64 automatic restoration: NO
Global closure requirement for Schicksalsanalyse/Therapie/Triebpathologie: NO
New architecture justified by observed failure: YES|NO (if NO, do not build)
Next concrete clinical capability: <one sentence>
```

If a successor cannot fill this truthfully, it is not ready to modify the AI strategy.

---

# PART XIV — FINAL NORTH STAR

## 28. The one sentence that must survive every handoff

> **The AI is allowed to write beautifully; it is not allowed to invent what Szondi3 has not authorized.**

Richness must come from expanding the evidence/claim coverage faithfully, not from increasing model freedom.

Correct-but-incomplete is an acceptable intermediate product.

Fluent-but-unsupported is a project failure.

And if a future chat must choose between a smaller faithful implementation and a grander speculative one, choose the smaller faithful implementation.
