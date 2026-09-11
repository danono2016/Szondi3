# Szondi3 — current project state

**Status:** CURRENT OPERATIONAL STATE  
**Purpose:** concise mutable summary of the live clinical/software direction. Live Git, source evidence, executable code and CI outrank this file whenever they disagree.

## Active line

- repository: `danono2016/Szondi3`
- active semantic-audit branch: `work/p2b-semantic-coverage-audit-001`
- last independently verified pre-continuity checkpoint: `37a03a77e44f36980c03b139ed618315d209b4d8`
- exact-checkpoint CI: Foundation verification `#1183` = SUCCESS; Runtime tests `#540` = SUCCESS; P2A doctrine registry `#1242` = SUCCESS
- PR #144: OPEN / DRAFT / frozen clinical acceptance baseline on `work/alpha1-executable-richness-001`; do not merge automatically
- PR #65: OPEN / DRAFT / older clinical integration umbrella; never merge automatically
- current executable P2B frontier: `IC_SZONDI_PRIMARY_000087`
- reserved historical P2B gaps remain `000022`, `000035`, `000036`
- IA-A HOLD doctrines remain `DR_SZ_IA_1956_A_000033`, `000042`, `000050` = `NOT_EXECUTABLE_YET`
- no current authorization exists for `IC_SZONDI_PRIMARY_000088`

The `37a03a77...` checkpoint is a clean descendant of the previously validated `728b226...` checkpoint. The intervening continuation aligned the semantic-coverage audit and matrix with already authorized lifecycle/P2A remediation state; it did not open a new P2B frontier.

## Durable product orientation

Read in this order when entering the project for clinician-facing work:

1. `docs/PROJECT_MISSION.md`
2. `docs/CLINICAL_REPORTING_AND_AI_MANIFEST.md`
3. this `docs/PROJECT_STATE.md`
4. `docs/P2B_SEMANTIC_COVERAGE_AUDIT.md` and `docs/P2B_SEMANTIC_COVERAGE_MATRIX.md` when working on the current frontier
5. only the source/spec/code needed for the concrete task

The repository is the durable memory. Do not reconstruct current direction from old chat handoffs.

## Current engineering frontier — P2B semantic coverage audit

The immediate engineering problem is now more precise than the original Alpha-0 report finding. The question is not only whether reviewed doctrine has an executable route, but whether the executable P2B layer carries enough of the source-authorized Szondian meaning to support clinically useful formulation without forcing AI to invent generic psychological bridges.

Current audit state:

- the structural first pass over `IC_SZONDI_PRIMARY_000001` through `000087` is complete;
- there are 84 present claim identities in that interval; historical holes `000022`, `000035`, `000036` remain reserved and unused;
- exact source adjudication and the reverse primary-doctrine -> P2B audit remain in progress;
- `IC_SZONDI_PRIMARY_000021` remains a historical identity but is projected `SUPERSEDED` in the current public catalogue;
- `IC_SZONDI_PRIMARY_000081` is the sole current executable route for the corresponding Sch `+±` relation and requires ordinary `q0/q0`; quantum overpressure therefore does not leak into that route;
- the public P2B frontier remains `000087`; no `000088` is authorized by this audit state.

Four source-adjudicated Lehrbuch doctrine records have been rematerialized and CI-validated at P2A:

- `DR_SZ_LEHR_1972_000363` — exact `S -+!` semantic reserve;
- `DR_SZ_LEHR_1972_000364` — exact ordinary `P --` semantic reserve;
- `DR_SZ_LEHR_1972_000365` — exact ordinary `C 0-` core semantic reserve;
- `DR_SZ_LEHR_1972_000366` — qualification that Szondi's `hypomanische Reaktion (C 0-)` is not the psychiatric picture of Hypomanie or Manie.

These P2A records do **not** create executable P2B routes. `S -+!`, `P --` and `C 0-` remain reverse-audit C candidates until the P2B implementation gate is explicitly closed. Operator counter-verification for this newly rematerialized P2A round remains a separate provenance-control requirement before a future P2B activation decision.

The current audit also preserves the distinction between semantic enrichment classes. In particular, the existing `-m/+k` route has a B1 semantic reserve already present in linked doctrine at the conceptual-mechanism level, while the broader `Sch +0` field remains B2 pending an explicitly reviewed additional support relation. No enrichment may outrun source, trigger or scope adjudication.

## Current product checkpoint

The owner has explicitly moved the project from foundation-first expansion into **clinical Alpha product validation**.

The local browser product already supports the complete first clinical loop:

`new pseudonymous assessment -> visual administration -> deterministic calculation -> current Szondi profile -> authorized interpretation -> exact source drill-down -> clinician integration -> working report -> immutable pseudonymous archive snapshot`

The normal launcher is:

```bash
python -m szondi3
```

The product is loopback/local-first. The current SQLite archive is pseudonymous and unencrypted; it is not a patient-record system. Manual clinician free text is intentionally not persisted by the baseline archive.

Historical archive browsing is read-only and snapshot-based. Opening a historical case does not rerun P1/P2B/doctrine under the current checkout.

## Alpha-0 finding that changes the direction

The first real end-to-end Alpha-0 working report demonstrated that the deterministic/provenance foundation works, but the clinician-facing report is **not yet acceptable as a clinical Szondi interpretation**.

The problem is not primarily missing infrastructure. The report currently exposes too much internal machinery and too little coherent clinical formulation.

Observed defects include:

- mixed Romanian/English/German language;
- untranslated or insufficiently translated German terminology;
- internal IDs/statuses/hashes in the clinical reading flow;
- a large volume of method safeguards presented alongside case findings;
- atomic P2B findings printed in sequence, risking a software form of `Mosaikspiel`;
- source-authorized Szondian language sometimes neutralized/euphemized;
- insufficiently visible AI clinical formulation;
- uncertainty expressed as verbose hedging rather than structured interpretive indetermination.

PR #144 improved the reporting/AI contract and exposed a deeper bottleneck: some clinically important source-authorized meanings do not yet reach the report with sufficient executable semantic richness. Therefore **do not solve this by widening AI freedom or by feeding non-executable P2A directly to AI**. The current engineering priority is to finish the semantic-sufficiency audit and admit only source-, scope- and trigger-proven P2B remediation before further report enrichment.

## Normative reporting and AI direction

`docs/CLINICAL_REPORTING_AND_AI_MANIFEST.md` is authoritative for clinician-facing reporting, AI synthesis/wording, interpretive selection/ranking and uncertainty presentation.

Core invariants:

- preserve Szondi's direct, baroque, historically uncomfortable terminology when source-authorized;
- do not euphemize or modernize away concepts such as `totaler Narzißmus`, `Macht-Ich`, `Allessein`, `Alleshaben`, `Wahn`, `Destruktion`, historical sexual/pathological/genotropic language, etc.;
- do not dramatize beyond the source either; preserve `kann`, `scheint`, `wir nehmen an`, probability/suspicion language exactly at the source's epistemic strength;
- main clinical prose is Romanian;
- important German terms remain visible but must be immediately and clearly translated/explained for a clinician who knows no German;
- German quotations must have complete Romanian translations;
- internal software English, claim IDs, doctrine IDs, hashes and runtime statuses belong in source/audit surfaces, not normal clinical prose;
- general method safeguards are not patient findings;
- AI may formulate and explain only authorized material; it may not create doctrine, activate claims, invent correlations, invent biography or diagnosis;
- AI may not mechanically concatenate valid atomic findings into a whole-person narrative;
- AI must produce actual clinical wording and, when useful, explicit directions of clinical exploration;
- clinician judgment remains final.

## Precise indetermination / interpretive predominance

The intended future model is **structured indetermination**, not verbal fog.

When several source-authorized interpretations genuinely compete at the same interpretive level, the deterministic program may eventually assign a **relative interpretive support weight**. AI then expresses the supplied ranking; AI never generates or modifies the number.

Do not call these values statistical probabilities unless future empirical calibration justifies that term.

No percentages are currently authorized merely by this design decision.

Before percentages appear in production, a separate versioned deterministic **Interpretive Support Scoring Contract** must define evidence dimensions, weighting, contradictory evidence, normalization, same-level interpretive families, scope boundaries, missing-data behavior, rounding and regression tests, and it must receive explicit clinician approval.

Current provisional product gates, to be treated as configurable alpha hypotheses rather than doctrine:

- single dominant reading: top support about `>=65%` with margin about `>=20` percentage points;
- otherwise, when a second reading remains materially supported (initially around `>=25%`), show both with approximate relative support;
- when leading readings are close (roughly `<=10–15` points apart) or none is meaningfully dominant, state structured indetermination rather than forcing a synthesis;
- display approximate/coarsely rounded percentages if/when authorized, never spurious precision.

Only interpretations belonging to an explicit same-level competition family may be normalized together. A factor meaning, a vector configuration and an interfactor relation must not be forced into one artificial 100% competition.

Testological support and clinician-assessed clinical concordance, if later implemented, remain separate quantities. Clinical fit must never retroactively change the deterministic Szondian support score.

## Stable epistemic architecture

The authority chain remains:

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE P2B -> SOFTWARE FINDINGS -> INTERPRETIVE SUPPORT/RANKING -> AI WORDING -> CLINICIAN JUDGMENT`

No downstream layer may rewrite upstream evidence or doctrine.

P1 remains deterministic and separate from interpretation.

Base reaction, quantum/intensity and forced null remain distinct. Forced null in complement is not an observed real zero.

Factor/vector/profile/series/foreground/complement/longitudinal scopes must never be silently migrated into one another.

Historical/pathognostic terminology is not automatically a modern DSM/ICD diagnosis.

Original PDF remains documentary arbiter when OCR/DOCX conflicts on signs, formulas, tables, layout or typography. `sourceExcerpt` remains literal canonical evidence; PDF/visual repairs belong in explicit arbitration notes.

Source conflict is preserved, not silently harmonized. The known TspQu/%Sy-Re threshold conflict remains a conflict:

- Triebpathologie II p.474: `TspQu < 1` and `% Sy.-R. > 50`
- Lehrbuch pp.287–288: `TspQu < 1` and `% Sy-Re > 30`

## AI boundary

AI is closed-world for Szondi interpretation.

It may:

- translate;
- explain;
- compose authorized meanings into readable Romanian;
- preserve Szondi's rhetorical force;
- express deterministic interpretive predominance supplied by software;
- propose clearly marked clinical exploration directions inside the authorized meaning ceiling.

It may not:

- recalculate the protocol;
- create doctrine;
- invent percentages;
- infer unsupported relations;
- invent patient biography;
- invent modern diagnoses;
- use general model knowledge to fill doctrinal gaps;
- resolve source conflicts by stylistic preference;
- hide missing support behind fluent prose.

Fail closed when the authorized chain is insufficient.

## Product/report surface target

The ordinary clinician-facing report should separate:

1. **Raport clinic** — profile/series structure, case-specific Szondian meaning, coherent clinical formulation, relevant exploration directions, clinician synthesis;
2. **Surse / De ce apare?** — doctrine, exact source, full Romanian translation, page/provenance;
3. **Audit tehnic** — IDs, hashes, release/runtime metadata.

Nothing important is discarded. Technical detail is moved out of the ordinary clinical reading flow.

For important interpretations, the intended presentation pattern is:

- **În termenii lui Szondi** — faithful/direct formulation;
- **Formulare clinică** — clear Romanian clinical language without semantic dilution;
- **De explorat clinic** — a small number of testable directions/questions where useful;
- **Limită relevantă** — only where a likely modern overreading materially needs to be blocked.

## Immediate next action

Do **not** create `IC_SZONDI_PRIMARY_000088` merely because source reserve has been found or P2A doctrine has been materialized.

Do **not** change P1/scoring, widen quantum/base-symbol equivalence, migrate meaning across factor/vector/profile/series/foreground/complement scopes, feed non-executable P2A directly to AI, introduce support percentages, or expand unrelated product architecture while the semantic audit gate remains open.

The immediate development sequence is:

1. continue exact canonical source reconsultation for the current `000001`-`000087` matrix;
2. continue the reverse primary-doctrine -> P2B audit source by source;
3. complete operator counter-verification where required for the newly rematerialized P2A round;
4. make trigger discriminators and anti-inference boundaries explicit for B1/B2/C candidates;
5. admit only explicitly authorized remediation slices, with focused tests and green relevant CI on the exact branch SHA;
6. only after the semantic implementation gate is closed, return to clinician-facing report enrichment using the now-sufficient executable material.

Design the deterministic Interpretive Support Scoring Contract separately **before** implementing any support percentages or ranking heuristics.

After the report surface is clinically coherent, run a small number of real pseudonymized Alpha administrations and let those observations determine the next product slice.

## Working rule

> **Correct-but-incomplete is preferable to rich-but-invented. Clinical clarity is preferable to technical dump. Preserve Szondi; structure uncertainty; let AI formulate, never fabricate.**
