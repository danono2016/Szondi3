# Szondi3 — current project state

**Status:** CURRENT OPERATIONAL STATE  
**Purpose:** concise mutable summary of the live clinical/software direction. Live Git, source evidence, executable code and CI outrank this file whenever they disagree.

## Active line

- repository: `danono2016/Szondi3`
- active semantic-audit branch: `work/p2b-semantic-coverage-audit-001`
- continuity baseline HEAD: `17dc86d7fc068133cde67d16bba3f0c6cea15bb0`
- continuity package branch: `work/documentary-continuity-002` (documentation only; based exactly on the baseline HEAD above)
- PR #144: OPEN / DRAFT / frozen historical clinical-acceptance baseline on `work/alpha1-executable-richness-001`; do not merge automatically
- PR #65: OPEN / DRAFT / older clinical integration umbrella; never merge automatically
- current executable P2B frontier: `IC_SZONDI_PRIMARY_000087`
- reserved historical P2B gaps remain `000022`, `000035`, `000036`
- IA-A HOLD doctrines remain `DR_SZ_IA_1956_A_000033`, `000042`, `000050` = `NOT_EXECUTABLE_YET`
- no current authorization exists for `IC_SZONDI_PRIMARY_000088`

The current continuity baseline is the merge of PR #165. It preserves the existing P2B frontier and incorporates the latest approved trigger-boundary repair for `IC_SZONDI_PRIMARY_000013`; it does not authorize a new claim identity.

## Closed remediation history since the older handoff

The following work is already closed and must be treated as current state, not as pending work:

1. **`000021` / `000081` lifecycle replacement.** `IC_SZONDI_PRIMARY_000021` remains a historical identity but is projected `SUPERSEDED`; `IC_SZONDI_PRIMARY_000081` is the guarded executable replacement route for the corresponding IA-B 53 relation. The ordinary Sch `+±` boundary remains quantum-sensitive and does not collapse base reaction with `Quantumspannung`.
2. **P2A materialization `000363`–`000366`.** Four source-adjudicated Lehrbuch doctrine records are materialized and CI-validated at P2A: exact `S -+!`, ordinary `P --`, ordinary `C 0-`, and the guard that Szondi's `hypomanische Reaktion (C 0-)` is not the psychiatric picture of Hypomanie or Manie. Their existence does not itself create executable P2B routes.
3. **`000013` trigger repair.** `IC_SZONDI_PRIMARY_000013` now requires ordinary Sch `+±` with `k q0` and `p q0`. Regression coverage validates overpressure exclusion and valid simultaneous coactivation with the doctrinally distinct `000063`, `000075`, and `000081` routes. PR #165 merged this repair into the active line.

These closures do not move the executable frontier beyond `IC_SZONDI_PRIMARY_000087`.

## Durable product orientation

Read in this order when entering the project for clinician-facing work:

1. `docs/PROJECT_MISSION.md`
2. `docs/CLINICAL_REPORTING_AND_AI_MANIFEST.md`
3. this `docs/PROJECT_STATE.md`
4. `docs/HANDOFF.md`
5. `docs/P2B_SEMANTIC_COVERAGE_AUDIT.md` and `docs/P2B_SEMANTIC_COVERAGE_MATRIX.md` when working on the current frontier
6. only the source/spec/code needed for the concrete task

The repository is the durable memory. Do not reconstruct current direction from old chat handoffs.

## Current engineering frontier — P2B semantic coverage audit

The immediate engineering problem is more precise than the original Alpha-0 report finding. The question is not only whether reviewed doctrine has an executable route, but whether the executable P2B layer carries enough of the source-authorized Szondian meaning to support clinically useful formulation without forcing AI to invent generic psychological bridges.

Current audit state:

- the structural first pass over `IC_SZONDI_PRIMARY_000001` through `000087` is complete;
- there are 84 present claim identities in that interval; historical holes `000022`, `000035`, `000036` remain reserved and unused;
- exact source adjudication and the reverse primary-doctrine -> P2B audit remain in progress;
- `IC_SZONDI_PRIMARY_000021` is historical and projected `SUPERSEDED`; `IC_SZONDI_PRIMARY_000081` is its current guarded executable replacement route for the corresponding IA-B 53 relation;
- for ordinary Sch `+±` with `k q0` and `p q0`, the doctrinally distinct routes `000013`, `000063`, `000075`, and `000081` may coactivate as validated by focused regression coverage; overpressure must not leak into those ordinary-only routes;
- the public P2B frontier remains `000087`; no `000088` is authorized by this audit state.

Four source-adjudicated Lehrbuch doctrine records are materialized and CI-validated at P2A:

- `DR_SZ_LEHR_1972_000363` — exact `S -+!` semantic reserve;
- `DR_SZ_LEHR_1972_000364` — exact ordinary `P --` semantic reserve;
- `DR_SZ_LEHR_1972_000365` — exact ordinary `C 0-` core semantic reserve;
- `DR_SZ_LEHR_1972_000366` — qualification that Szondi's `hypomanische Reaktion (C 0-)` is not the psychiatric picture of Hypomanie or Manie.

This P2A materialization slice is closed. These records do **not** create executable P2B routes. `S -+!`, `P --` and `C 0-` remain reverse-audit candidates until any future P2B implementation gate is explicitly authorized and closed under the applicable provenance, scope and trigger controls.

The current audit also preserves the distinction between semantic enrichment classes. In particular, the existing `-m/+k` route has a B1 semantic reserve already present in linked doctrine at the conceptual-mechanism level, while the broader `Sch +0` field remains B2 pending an explicitly reviewed additional support relation. No enrichment may outrun source, trigger or scope adjudication.

## Source and asset state

The current admitted documentary/visual inventory is:

- **10 DOCX textual sources**;
- **10 PDF visual-arbitration originals**;
- **48 stimulus WebP files**.

The two authentic Triebpathologie PDFs are admitted source assets. Any description of the current repository as having only eight PDFs is stale and refers only to the historical initial binary-admission checkpoint. See `docs/SOURCE_ASSET_MANIFEST.md` for the authoritative inventory and provenance witnesses.

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

PR #144 improved the reporting/AI contract and exposed a deeper bottleneck: some clinically important source-authorized meanings do not yet reach the report with sufficient executable semantic richness. PR #144 is now a frozen historical baseline, not the active engineering line. Do **not** solve the remaining bottleneck by widening AI freedom or by feeding non-executable P2A directly to AI.

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

The documentary-continuity package is the only authorized work before another semantic or product slice. This package must remain documentation-only, must not touch P1/P2A/P2B or `docs/manual/`, and must have green CI on its exact PR head before it is considered closed.

After this continuity package is approved and landed, resume the existing P2B semantic-coverage audit from the active line. Do **not** create `IC_SZONDI_PRIMARY_000088` merely because source reserve has been found or P2A doctrine has been materialized.

Do **not** change P1/scoring, widen quantum/base-symbol equivalence, migrate meaning across factor/vector/profile/series/foreground/complement scopes, feed non-executable P2A directly to AI, introduce support percentages, or expand unrelated product architecture while the semantic audit gate remains open.

When the audit resumes, continue only explicitly authorized source/scope/trigger work, with focused tests and green relevant CI on the exact branch SHA. Design the deterministic Interpretive Support Scoring Contract separately **before** implementing any support percentages or ranking heuristics.

After the report surface is clinically coherent, run a small number of real pseudonymized Alpha administrations and let those observations determine the next product slice.

## Working rule

> **Correct-but-incomplete is preferable to rich-but-invented. Clinical clarity is preferable to technical dump. Preserve Szondi; structure uncertainty; let AI formulate, never fabricate.**
