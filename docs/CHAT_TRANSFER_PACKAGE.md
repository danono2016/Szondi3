# SZONDI3 — CANONICAL CHAT TRANSFER PACKAGE

Status: **MANDATORY SUCCESSOR ENTRY POINT**  
Repository: `danono2016/Szondi3`  
Prepared on: 2026-08-29; refreshed 2026-08-30  
Verified `main` baseline: `d192c984eff9d753de4ee60955accec3d6252938`  
Verified strategy branch checkpoint: `work/ai-clinical-provenance-strategy-001@60c61aebbbb07b35917af6513c25da62dbd95c7f`  
Open draft PR: **#65 — Build minimal provenance-constrained clinical evidence packet**  
PR #65 status: **OPEN / DRAFT / MERGEABLE / NOT MERGED**  
Verification at refreshed checkpoint: **all five PR workflows green** on `60c61ae...`.

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

# PART III — CURRENT REPOSITORY STATE AT REFRESH

## 6. Accepted formal gates

Accepted durable project gates:

- `P0_SOURCES_PASS`
- `P1_DETERMINISTIC_ENGINE_PASS`

Do NOT infer later formal gates from the existence of code or green CI.

At the refreshed checkpoint there is no formal repository declaration of:

- `P2A_PRIMARY_DOCTRINE_PASS`
- `P2B_EXECUTABLE_INTERPRETATION_PASS`
- P3 PASS
- P4 PASS

---

## 7. Current approved P2B tranche

`szondi3/interpretation_catalogue.py` contains **18 APPROVED source-linked claims**.

Claims 000001–000012 preserve the original limitation/ego nucleus. Recent claims driven by observed Fall 40 coverage gaps are:

- `000013`: exact `Sch +±`, with Szondi's average alternative `Annahme der Weiblichkeit` / `Annahme der Verlassenheit`; no branch selection or stronger pathodiagnostic/biographical inference;
- `000014`: one Triebprofil is only one Schicksals-/Existenzmöglichkeit; 8–10 profile series context;
- `000015`: Haupttriebklasse via maximal TspD as current Triebgefahr locus, interpreted with all four Latenzproportionen and phase dynamics;
- `000016`: exact serial `Sh+`, with +h as current affirmation of Eros-/Liebes-/Bindungsbedürfnis; no automatic homosexuality/travestism/gender/passivity inference;
- `000017`: exact PROFILE `S +0` as Unitendenz / Dominanz der Personenliebe; the `Mit Überdruck` branch is not imported from base symbols;
- `000018`: exact PROFILE `S +−` as diagonale Spaltung Variation I, linking bejahte Personenliebe (+h) with Passivität/Hingabe (−s); stronger sex-specific/pathodiagnostic branches remain blocked.

`Sh− = repression/sublimation` was explicitly NOT implemented because primary-source work showed that `−h` cannot be reduced to that meaning and depends on constellation/context.

No `000019` claim has been approved or added at this checkpoint.

---

## 8. Current P2A additions relevant to Fall 40

Recent SOURCE_VERIFIED Lehrbuch doctrines include:

- `DR_SZ_LEHR_1972_000352`: exact `Sch +±`;
- `DR_SZ_LEHR_1972_000353`: exact `S +0`, with PDF visual arbitration separating base meaning from `Mit Überdruck` extension;
- `DR_SZ_LEHR_1972_000354`: exact `S +−`, with sex-specific/Überdruck extensions kept contextual;
- `DR_SZ_LEHR_1972_000355`: established Symptomfaktoren in the numerator of Triebformel indicate possible Triebventile/Notausgänge and contribute to differentiae specificae;
- `DR_SZ_LEHR_1972_000356`: records an internal Lehrbuch tension: U003738 says the first complete-formula line contains two or three Symptomfaktoren, while canonical Fall 11 U003754–U003756 has `m` alone as Symptomfaktor in the complete formula. The `2–3` phrase is therefore not promoted to a universal executable cardinality constraint.

The Lehrbuch snapshot count at this checkpoint is 171 doctrine objects.

---

# PART IV — CURRENT EXECUTABLE AI VERTICAL SLICE

## 9. Current path

```text
ClinicalProtocolEvaluation
    -> ClinicalReport
        -> ClinicalEvidencePacket
            -> OpenAI preview request
                -> SynthesisProposition
                    -> deterministic local validation
```

The model remains a wording layer. P1 scoring/morphology and P2B person-specific meaning remain outside the model.

`ClinicalEvidencePacket` is a finite closed-world handoff and includes deterministic morphology, vector configuration frequencies, active findings, exact fact support, SOURCE_VERIFIED doctrine objects, anti-inference IDs and uncertainties. It does not score, create doctrine, create claims, use semantic retrieval/RAG/web, or include manual therapist synthesis.

`clinical_synthesis.py` validates the exact support envelope: active claim in exact PROFILE/SERIES scope, activating facts, doctrine bundle and anti-inference IDs. Correct IDs do not prove arbitrary prose is semantically faithful; O4 clinician inspection remains required after live previews.

---

# PART V — FALL 40 CURRENT REGRESSION STATE

## 10. Deterministic morphology and serial state

Fall 40 remains a regression specimen, never runtime doctrine.

Current locked facts include:

- TspG: `h=0, s=9, e=2, hy=2, k=1, p=7, d=0, m=0`;
- TspD: `S=9, P=0, Sch=6, C=0`;
- Haupttriebklasse: `Sh`;
- strict subclass: `Sh+`;
- `Sch +±`: profiles 4,5,6,8,9;
- `S +0`: profiles 1,2,3,4,5,6,8,9,10;
- `S +−`: profile 7;
- real `0` remains distinct from forced `ø`.

Nine PROFILE findings for `S +0` do NOT authorize a SERIES/global conclusion such as a dominant sexual pattern.

---

## 11. Controlled live-preview evidence through v5

Four controlled Fall 40 live previews have now been run outside repository CI; raw responses remain diagnostic artifacts only and are not committed or released as clinical reports.

The latest v5 preview used head `403ecf2d49779590bfe9704fbea0264e5e9fd9f4` and returned:

```text
model = gpt-5.6-sol
raw_proposition_count = 36
locally_validated_count = 36
rejected_count = 0
semantic_overreach_observed = NO
new_failure_mode_observed = NONE
```

It preserved exact scope and guards for `Sh+`, nine `S +0` PROFILE findings and one `S +−` PROFILE finding. It did NOT promote `S +0` recurrence to SERIES meaning and did NOT import homosexuality/bisexuality/travestism/gender identity, Triebzielinversion, Masochismus, preregenital-abnormal sexuality, global passivity or unsupported diagnosis.

Observed effect remains:

```text
EXACTLY_SCOPED_ENRICHMENT
```

The remaining gap is not model failure but serial integration beyond enumeration.

---

# PART VI — TRIEBFORMEL PRE-SEMANTIC WORK

## 12. Why Triebformel is the current next route

After v5, the next source-grounded integration route is Triebformel, not naive recurrence counting.

Existing doctrine states:

- Symptomfaktoren occupy the high TspG zone; Wurzelfaktoren the low TspG zone;
- Triebformel is a multi-line fraction with symptom factors in the numerator and roots in the denominator;
- Triebformel relates symptom to underbliebene Triebbefriedigung;
- Triebklasse is determined first, then Triebformel; class gives genus proximum, formula differentiae specificae;
- established symptom factors in the numerator are possible Triebventile/Notausgänge.

### Internal cardinality contradiction

Do NOT enforce `2–3 Symptomfaktoren` universally. The general sentence at U003738 conflicts with Fall 11, where `m` is explicitly alone as Symptomfaktor in the complete formula. This contradiction is recorded in `DR_SZ_LEHR_1972_000356` and must remain unresolved unless a primary-source reconciliation is found.

---

## 13. `formula_role_consensus` is P1 only

`szondi3/formula.py` now exposes `formula_role_consensus(series)`.

It does **not** choose among ambiguous complete Triebformel partitions and does not attach clinical meaning. It intersects factor roles across every partition already admitted by the non-contradicted source-compatible P1 rules.

For Fall 40:

```text
complete_formula = UNRESOLVED (multiple admissible partitions)
candidate_count = 3
invariant symptomatic = s
invariant roots = h, d, m
variable roles = e, hy, k, p
```

The full formula remains unresolved. The consensus is partial formal truth only.

Szondi does not explicitly define a "consensus across ambiguous formula partitions" method. Any future P2B trigger using this fact must therefore be `IMPLEMENTATION_INFERRED_TRIGGER`, with explicit rationale and reversal condition, and must never masquerade as a source-established trigger.

---

# PART VII — NEXT SAFE DECISION

## 14. Candidate only: no approved claim yet

The next possible executable increment is a narrow SERIES claim that would use an invariant Symptomfaktor only to preserve Szondi's source meaning "possible Triebventil/Notausgang" while the complete formula remains unresolved.

This claim is NOT yet implemented or approved at this checkpoint. It requires explicit clinician review because the trigger is implementation-inferred.

If reviewed, the claim must:

- cite the formal consensus fact, not choose a complete formula;
- preserve `complete_formula = UNRESOLVED`;
- be weaker than a categorical behavioral statement;
- state only possible Triebventil/Notausgang in Triebformel terminology;
- forbid diagnosis, healthy/adaptive-coping judgment, global personality inference, specific sadistic/aggressive/sexual behavior from factor `s`, and any role assignment to variable factors;
- include a reversal condition if future source evidence supplies a real disambiguating partition rule or changes the candidate set.

Do not implement this merely because doctrine 355 exists. P2B remains the sole semantic gate.

---

# PART VIII — LEAN ARCHITECTURE / ANTI-DINOSAUR LAW

## 15. Normative constraint

Preferred sequence remains:

```text
observed case gap
  -> canonical primary evidence
  -> smallest deterministic fact already justified by P1
  -> narrow reviewed P2B claim
  -> exact regression
  -> controlled preview
  -> clinician inspection
```

Do NOT build a universal agent framework, RAG platform, vector database, provider abstraction layer, semantic second-model validator, ontology/graph system, new CI workflow or broad P1 refactor without a concrete observed failure that cannot be solved more simply.

---

# PART IX — MANDATORY ORTHODOXY CHECKS

## 16. O0–O7 condensed

Before repository writes: re-check main, branch, PR and CI. If main changed, inspect before writing.

Before person-specific semantics:

```text
O2_SEMANTIC_AUTHORITY
person_specific_statement = <statement>
active_executable_claim = <claim id or NONE>
claim_status = <production-admissible if production>
activating_fact = <fact id>
canonical_doctrine = <ids>
anti_inferences = <ids>
assertion_mode = <mode>
```

If claim = NONE, correct output is coverage gap, not model improvisation.

Before live preview: packet-only Szondian evidence, `tools=[]`, `store=false`, structured output, no repo credential, no rescoring, local validation required.

After live preview: inspect raw response, exact support validation, assertion strength and anti-inference semantics before changing architecture.

Before new architecture: identify a concrete observed failure and prove no simpler existing-layer fix suffices.

P2B expansion must follow:

```text
case gap -> canonical source -> narrow candidate -> review -> approve/reject -> rerun
```

Never:

```text
case gap -> LLM explanation -> production prose
```

PR #65 remains draft unless explicitly authorized otherwise.

---

# PART X — HARD STOP CONDITIONS

STOP and reconcile if:

- main/branch/PR changed unexpectedly;
- CI is red;
- source and executable rule contradict and no lower-layer reconciliation exists;
- someone proposes restoring PR61–64 automatically;
- a person-specific statement lacks an active P2B claim;
- the LLM is asked to score/repair P1;
- doctrine is converted directly into person-level meaning;
- a model is given unrestricted web/repository/source search for runtime interpretation;
- a source-qualified statement is strengthened or modernized;
- a new layer lacks a concrete observed failure;
- a live preview is treated as production report;
- a formal downstream gate is declared from green tests alone.

---

# PART XI — CURRENT CHECKPOINT

## 17. Repository state at this refresh

```text
main = d192c984eff9d753de4ee60955accec3d6252938
strategy_branch = 60c61aebbbb07b35917af6513c25da62dbd95c7f
PR = #65 OPEN / DRAFT / NOT MERGED
approved_P2B_claims = 18
Lehrbuch_doctrine_count = 171
```

All five workflows on `60c61ae...` passed:

- Runtime tests;
- Foundation verification;
- P0 source inspection;
- P2A doctrine registry, including exact doctrine anchor/excerpt validation;
- P0 canonical access.

This is a workflow-success checkpoint only, not a formal P2A/P2B/P3/P4 gate declaration.

---

# FINAL NORTH STAR

> **The AI is allowed to write beautifully; it is not allowed to invent what Szondi3 has not authorized.**

Richness must come from faithful evidence/claim coverage, not increased model freedom.

Correct-but-incomplete remains acceptable.

Fluent-but-unsupported remains a project failure.
