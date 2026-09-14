# P2B Semantic Coverage Audit

Status: **CLOSED**

Branch: `work/p2b-semantic-coverage-audit-001`

Frozen implementation baseline: `2dfbfccb4951b3042c26e2637d285fd7b598de50` (`work/alpha1-executable-richness-001`, PR #144).

Validated remediation checkpoint before this documentation alignment: `728b2267315998a4ad4cea2787215514aa67d2ef`. On that exact branch SHA, Foundation verification #1181, Runtime tests #538, and P2A doctrine registry #1240 all completed successfully from `push` events.

**Closure note:** the P2B semantic coverage audit is closed. This final status supersedes earlier in-document wording that described the audit, reverse pass, or implementation gate as still in progress. Those passages are retained only as historical record of how the audit was conducted; no further semantic-audit rounds are planned for `000063`-`000087`, and A/D items from the final screening are not to be reopened merely to deepen the audit.

## Purpose

This audit asks a different question from the earlier executability-closure work.

Earlier closure audits asked whether reviewed primary doctrine had an executable route, indirect coverage, a legitimate contextual/theoretical role, or a deliberate HOLD.

This audit asks additionally:

> **When Szondi3 does execute a meaning, does the executable layer carry enough of the source-authorized Szondian meaning to support a clinically useful formulation without forcing the AI to invent or fill gaps with generic psychology?**

The earlier closures are therefore not presumed wrong. They remain evidence about executability. This audit adds a semantic-sufficiency and reverse-coverage pass.

## Non-negotiable safeguards

The audit remains the governing process. Two explicitly authorized remediation slices have already been applied and validated; they are exceptions recorded below, not permission for uncontrolled implementation.

From this checkpoint forward:

- no P1/scoring change;
- no additional P2A mutation without explicit source adjudication, authorization, focused tests, and green relevant CI before the next slice;
- no additional P2B claim mutation without explicit trigger/source adjudication, authorization, focused tests, and green relevant CI before the next slice;
- no new P2B identity and specifically no automatic `IC_SZONDI_PRIMARY_000088` before the implementation gate is closed;
- no sourceExcerpt rewriting;
- no widening of quantum/base-symbol equivalence;
- no migration of meaning across factor/vector/profile/series/foreground/complement scopes;
- no AI use as a substitute for missing executable doctrine;
- no `manual` branch or `docs/manual/` change;
- no merge of PR #65, #143 or #144.

PR #144 remains the frozen clinical acceptance baseline. The current audit branch may contain only explicitly authorized, source-adjudicated remediation slices plus audit/documentation work.

## Validated remediation slices already applied

### `000021` / `000081` trigger overlap

The overlap was resolved without creating a new P2B identity and without rewriting the historical base catalogue.

- historical `IC_SZONDI_PRIMARY_000021` remains `APPROVED` in its historical segment;
- the current public catalogue projects `000021` as `SUPERSEDED`;
- `IC_SZONDI_PRIMARY_000081` remains the single executable route for this semantic relation;
- `000081` requires Sch +± plus `k.quantum_level == 0` and `p.quantum_level == 0`;
- overpressure at k or p therefore activates neither `000021` nor `000081` in current clinical execution;
- the public P2B frontier remains `IC_SZONDI_PRIMARY_000087`.

The initial CI attempt exposed stale tests that still expected `000021`. Those tests were corrected to require `000081` and all three exact supporting facts. The transferred remediation was then validated on the active branch by the three successful push workflows recorded above.

### P2A rematerialization for the control gaps

Four Lehrbuch doctrine objects were explicitly authorized, added, and validated through the P2A doctrine workflow, including canonical regeneration and exact source-excerpt validation:

- `DR_SZ_LEHR_1972_000363` — exact `S -+!` semantic reserve; new identity, with historical provenance noting retired `DR_SZ_LEHR_1972_000235` without reusing that retired ID;
- `DR_SZ_LEHR_1972_000364` — exact ordinary `P --` / Variation II semantic reserve;
- `DR_SZ_LEHR_1972_000365` — exact ordinary `C 0-` core semantic reserve;
- `DR_SZ_LEHR_1972_000366` — the C 0- terminological guard that Szondi's `hypomanische Reaktion` is not the psychiatric picture of `Hypomanie` or `Manie`, related by `QUALIFIES` to `000365`.

These P2A records do **not** create executable P2B routes. `S -+!`, `P --`, and `C 0-` therefore remain reverse-audit C candidates at the executable layer. No `000088` or later P2B identity has been created.

Operator counter-verification for the newly rematerialized P2A round remains a separate provenance-control requirement before those records can support a future P2B activation decision.

## CI slice discipline

A behavioral or doctrine slice is not considered complete because its diff appears correct. It is complete only after the relevant GitHub Actions workflows run on the exact active-branch SHA and are green. No new semantic/doctrine slice should be stacked on a red or unrun predecessor.

Direct push CI is now configured for `work/p2b-semantic-coverage-audit-001`, so Foundation verification, Runtime tests, and P2A doctrine registry can validate the branch without a temporary PR harness.

## Classification

Each current executable claim and each reverse-audited doctrine candidate will be classified as one of:

- **A — semantically sufficient:** current executable meaning carries the source-authorized content needed at its exact scope.
- **B1 — correct trigger, semantically thin:** the current trigger is correct and its already-linked doctrine supports a richer executable semantic packet without adding a new inference.
- **B2 — correct trigger, richer meaning requires additional doctrine relation/reconsultation:** no enrichment until that relation is explicitly reviewed.
- **C — executable coverage gap:** reviewed doctrine supports a person/profile/series-level meaning, deterministic facts can discriminate the condition, but no current executable route carries it.
- **D — legitimately non-executable/contextual:** theory, historical background, example-only material, missing discriminator, or content that cannot support independent person-level inference.

LIMITATION/GUARD claims are judged for boundary precision, not narrative richness.

**Trigger fidelity is a prerequisite to semantic classification.** If a current claim has a trigger-boundary defect or unresolved overlap, it is marked as blocked by trigger review rather than being forced into A/B1/B2/C/D. This keeps semantic richness from hiding an activation error.

## Two-direction audit

The audit must be completed in both directions:

1. **P2B -> doctrine/source:** review every current identity `000001` through `000087` for lifecycle/trigger fidelity, scope, semantic sufficiency, source modality and anti-inference completeness.
2. **Primary doctrine -> P2B:** review admitted primary doctrine for semantically important meanings that have deterministic discriminators but are not carried by the current executable layer.

No new executable implementation batch may begin from one direction alone.

## Current structural matrix

The current first-pass inventory is maintained in:

`docs/P2B_SEMANTIC_COVERAGE_MATRIX.md`

It inventories the full `000001`-`000087` interval, preserves historical holes `000022`, `000035`, `000036`, records trigger/scope/support/semantic boundaries, and records the resolved lifecycle state of `000021`/`000081`.

The matrix is the durable closure record for this audit. Its final `000062`-`000087` classifications and closure section supersede earlier candidate/continuation language retained elsewhere for history.

## First control reconsultation — `alpha1-test2`

Control morphology:

`h- s+! | e- hy- | k+ p0 | d0 m-`

Vectors:

`S -+! | P -- | Sch +0 | C 0-`

The control specimen is not the scope of the audit; it is the case that exposed the systemic defect.

### Source-confirmed semantic reserve not fully reaching the current report

The following are **audit findings, not P2B implementation authorizations**.

#### `S -+!`

Primary Lehrbuch, printed p. 92, explicitly describes the diagonal vector configuration `S - +` as `Sadismus mit Unterdrückung des Eros`, less often `Kultursadismus` / `Sadohumanismus`. With overpressure in `+s`, the text explicitly says `extremer Sadismus`. The Lehrbuch also contains the exact combined notation `S -+!` in the relevant coupling discussion.

P2A support is now materialized as `DR_SZ_LEHR_1972_000363`, with the retired pre-compaction identity recorded only as historical provenance. Current `alpha1-test2-v2` output still receives only the generic quantum-tension meaning for `s +!`; it does not receive this vector-level semantic content.

Audit class: **C candidate at P2B**, with exact q1 trigger design still requiring the P2B gate. The quantum claim itself must not be widened to carry this meaning.

#### `P --`

Primary Lehrbuch, printed p. 117, explicitly gives `P --` as `Innere Panik, Beklemmungen`, with `Immobilisierung` up to `Sich-tot-Stellen`. It explains the vector dynamically: `-hy` moral censorship blocks the discharge path of accumulated gross Kainic affects `-e`, so affective life freezes outwardly.

P2A support is now materialized as `DR_SZ_LEHR_1972_000364`. Current control output still has no executable vector-level `P --` finding.

Audit class: **C candidate at P2B**, exact ordinary q0/q0 only. No modern panic, catatonia, neurological, behavioral or biographical conclusion is authorized by this record alone.

#### `C 0-`

Primary Lehrbuch identifies foreground `C 0-` as Variation IV and describes the associated field through `Hypomanische Bindung`, `Sichlosreißen`, `Vereinsamung`, `Verwahrlosung`, `Sucht und Haltlosigkeit`. A later explicit methodological passage states that Szondi's `hypomanische Reaktion (C 0-)` does not coincide with the psychiatric picture of Hypomanie or Manie.

P2A support is now separated into `DR_SZ_LEHR_1972_000365` for the core and `DR_SZ_LEHR_1972_000366` for that diagnostic/terminological guard. Current control output still has no executable vector-level `C 0-` finding.

Audit class: **C candidate at P2B**, exact ordinary q0/q0 only. Any future executable packet must carry the `000366` qualification so the historical Szondian term cannot be promoted to a modern psychiatric diagnosis.

#### `Sch +0`

Primary Lehrbuch chapter XII names the unitendency `Sch +0` explicitly as `Totale Introjektion, Egoismus, Egozentrismus, Narzißmus, Habmachtsucht` (printed p. 148). Current P2B already carries `totale Introjektion`, `Einverleibung` and `Seinsmacht -> Habmacht`, but the clinician-facing executable meaning is markedly narrower than the primary semantic field.

Final audit class: **B2**. The richer wording requires an explicitly reviewed additional P2A/support relation before any future executable enrichment. No implementation is authorized by this classification.

#### `-m/+k`

Current P2B correctly carries `introjektive Identifizierung` and the distinction `Identifizierung != Identität`. Primary Ich-Analyse material develops introjective identification further through incorporation and object-in-Ego models, including the historical expression `psychischer Kannibalismus` in the relevant introjective conceptual field.

After reconsulting the doctrine record already linked to current claim `000038`, part of this reserve is more precisely classified: `DR_SZ_IA_1956_A_000046` itself contains `Aufrichtung des verlorenen Objektes im Ich` and calls introjective (+k) and inflative (+p) forms of identification narcissistic. The retained final classification is **B1 at the conceptual-mechanism level**, while the case-level assertion of an actual biographical loss remains forbidden. `psychischer Kannibalismus` is not retained as a separate closure-backlog item and would require fresh explicit authorization if ever reconsidered.

## Resolved systemic trigger-boundary finding — `000021` / `000081`

The structural matrix exposed a defect that was not merely semantic thinness.

Both identities link to `DR_SZ_IA_1956_B_000053` and carry the same core probabilistic Sch +± relation (`scheinen`; Angst rarer than the four preceding defense forms), but the historical `000021` trigger used Sch +± base symbols alone while `000081` also requires k/p quantum level 0.

The current public catalogue now resolves this conflict by projecting `000021` as `SUPERSEDED` while leaving its historical definition unchanged. Runtime lifecycle filtering excludes `SUPERSEDED` claims before trigger evaluation. `000081` is therefore the only executable route for this semantic relation, and its q0/q0 boundary prevents leakage into Überdruck.

Focused tests prove both direct-catalogue and clinical-protocol behavior, and the corrected Annahme tests now require the full support bundle of vector Sch base symbols plus k and p quantum facts. The exact active-branch remediation checkpoint passed Foundation, Runtime, and P2A workflows.

This trigger conflict is therefore **RESOLVED**. It is no longer a gate blocker. The P2B semantic coverage audit itself is now closed; no broader follow-on audit round remains open.

## Source-adjudicated checkpoint — `000055`–`000061`

The read-only source round reconsulted the primary Triebpathologie I and Ich-Analyse II evidence independently, used original-PDF arbitration wherever sign/quantum/configuration notation was decisive, then compared that evidence with the already-admitted P2A records and the current P2B triggers/packets. The final result is:

`000055 A / 000056 A / 000057 D/guard / 000058 D/guard / 000059 A / 000060 A / 000061 A`.

No trigger blocker was found and no P1, P2A, P2B catalogue/runtime, evaluator, reporting or AI remediation is authorized or required by this slice.

- `000055` — exact `s+!! / e+ ordinary`; linked doctrine `DR_SZ_TRIEBPATH_1_000002` + `DR_SZ_TRIEBPATH_1_000003`. Triebpathologie I supports Gewissen/Güte as the source-model protection/counterbalance to the intensely accumulated s tendency. The OCR of the `e=+` formula is defective, while visual inspection of the original PDF confirms **ordinary `e=+`**. Existing P2A already records this arbitration. The executable packet does not infer aggressive behavior, dangerousness, moral character or successful defense.
- `000056` — exact `s+!! / e0`; linked doctrine `DR_SZ_TRIEBPATH_1_000002` + `DR_SZ_TRIEBPATH_1_000004`. The source states `Aggressionsgefahr` without `ethischen Schutz` in its historical model. `e0` is not promoted into a global judgment about conscience, morality or self-control, and the packet does not infer violence or criminality. The separately discussed `e−` example remains a reverse-coverage question and does not widen this trigger.
- `000057` — D/guard; linked doctrine `DR_SZ_IA_1956_B_000015`. Defense has its functional origin in the Ego, but Ich-Analyse II explicitly distributes defensive routes through Ich-, Sexual-, Affekt- and Kontaktreaktionen. The limitation therefore prevents reducing defense to Sch and does not become a positive Sch finding.
- `000058` — D/guard; linked doctrine `DR_SZ_IA_1956_B_000017`. Ich-Analyse II distinguishes five projective forms/modes; `p−` alone cannot identify which form is present and in particular cannot be equated automatically with `totale Projektion`.
- `000059` — exact ordinary `Sch 0+`; linked doctrine `DR_SZ_IA_1956_B_000018`. Source-authorized meaning is `totale Inflation` / unifunctional defense at the exact ordinary configuration. No quantum/Überdruck extension, psychosis, modern diagnosis or invented content is licensed.
- `000060` — exact ordinary `Sch ±+`; linked doctrine `DR_SZ_IA_1956_B_000018`. Source-authorized meaning is `Zwangsdeflation`, including Inflation held back by Zwang. The historical term is not translated into OCD or modern obsessive-compulsive symptomatology, and quantum/Überdruck neighbors remain outside the trigger.
- `000061` — exact ordinary `Sch −+`; linked doctrine `DR_SZ_IA_1956_B_000018`. Source-authorized meaning is `Hemmung / Inhibition / negierte Inflation`; the individual content of the negated Inflation remains undetermined and quantum/Überdruck neighbors remain excluded.

**Negative-neighborhood result:** `000055` does not import its meaning into s+!, s+!!!, e0/e− or quantum-marked e+; `000056` does not turn e0 into a global conscience/morality verdict; `000057` remains a cross-zone methodological guard; `000058` does not select a projection form from p− alone; and `000059`–`000061` remain exact ordinary Sch configurations without quantum/Überdruck or neighboring-tuple expansion.

This checkpoint is documentation-only. No `IC_SZONDI_PRIMARY_000088` is created, the public frontier remains `IC_SZONDI_PRIMARY_000087`, and `manual` / `docs/manual/` remain untouched.

## Important architectural observation

The P2B release digest serializes the current claim definitions. Therefore, changing an existing claim's text, support doctrine, guard, trigger or lifecycle projection is provenance-significant; it is not a cosmetic edit.

For that reason this audit will not assume that "richer report" means "rewrite the existing claim text". The implementation design will be selected only after the full matrix shows which meanings are A/B1/B2/C/D. A separate versioned executable semantic projection may prove safer than mutating stable activation claims; the `000021` supersession is a narrowly authorized lifecycle projection, not blanket authorization for future rewrites.

## Final closure state

**P2B semantic coverage audit = CLOSED.** The compact final screening found no new blocker in `000063`-`000087`; the A/D results in that interval are closed and are not scheduled for deeper audit. The executable frontier remains stable at `IC_SZONDI_PRIMARY_000087`.

The retained backlog is exactly:

- `000009` — **B1**;
- `000038` — **B1**;
- `000062` — **B2**;
- reverse coverage **C** — exact `S -+!`, ordinary `P --`, ordinary `C 0-`.

This backlog is not an obligation to implement all items. Any future work is selected by demonstrated clinical value and cost/risk, not by numeric order. This closure authorizes no P1, P2A, P2B runtime/catalogue, evaluator, reporting or AI mutation; creates no `000088`; and does not alter `manual` or `docs/manual/`.
