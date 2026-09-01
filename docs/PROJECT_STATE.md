# Szondi3 — current project state

This file is the short continuation checkpoint. The full handoff and forensic-audit history are in `docs/CHAT_TRANSFER_PACKAGE.md`.

Always read the handoff first, then verify current Git HEAD, open PRs and CI. Do not reconstruct project state from chat memory. Historical SHA/count statements in older checkpoint documents remain historical witnesses and must not override this current checkpoint or the live repository.

## Current verified line

- repository: `danono2016/Szondi3`
- clinical line: `work/ai-clinical-provenance-strategy-001`
- forensic-audit baseline: `92befe8cc3a47af5f5c30d0ce56dc2d9b778b949`
- P0 10/10 recovery verification checkpoint: `061c172afb67b848d58295851ea22165ccbc1df5`
- Rand–Mitte `s+!! / e0` verification checkpoint: `90b5bcc54ee1cec2ccc25271ab22bc621e9db63a`
- executable catalogue reaches `IC_SZONDI_PRIMARY_000056`
- PR #65: OPEN / DRAFT / NOT MERGED; role explicitly set to **clinical integration umbrella**, not release gate

Never treat a checkpoint SHA above as a substitute for checking the live ref; documentation or later clinical work may advance the branch.

## Authority chain

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE P2B -> SOFTWARE FINDINGS -> AI SYNTHESIS`

Original authentic PDF and clinician-created ABBYY DOCX replica have equal primary documentary rank when concordant. On conflict, the original PDF is supreme. See `docs/SOURCE_AUTHORITY_POLICY.md`.

## P0 reproducibility boundary — RESTORED 10/10

The audit blocker `10 authorized PDFs / 8 repository-locked PDFs` is closed.

Both authentic Triebpathologie originals are repository-locked:

- `sources/originals/Szondi Triebpathologie 1. Teil.pdf` — Git blob `de905f28eb96b9da40bd4f6ce7e1cc852c94fe88`;
- `sources/originals/Szondi Triebpathologie 2. Teil.pdf` — Git blob `0ed487efd94788c13651032479b2278eabde49f5`.

Current machine boundary: 10 DOCX sources, 10 original/admitted PDF binaries and 48 stimulus WebP binaries. `config/source_catalog.json` carries both Triebpathologie `pdfPath` values; `config/evidence_lock.json` identity-locks all 10 PDFs; P0 canonical validation expects exactly 10 unique PDF paths.

At checkpoint `061c172a...` all five recovery workflows were green, establishing `P0_SOURCES_PASS` for the 10/10 source set.

## CI governance

P0 source inspection and P0 canonical access run directly on both `main` and `work/ai-clinical-provenance-strategy-001`; they no longer depend on PR #65 merely to execute on the clinical line.

GitHub branch protection / required status checks remain unset on `main` and the clinical branch. The available repository connector can inspect protection but does not expose a mutation action for enabling it, so this remains a manual GitHub-settings task rather than a code blocker.

PR #65 is intentionally retained OPEN/DRAFT as an integration umbrella. Its accumulated size is not treated as a release gate, and it must not be merged automatically merely because CI is green.

## Historical eight-PDF wording

Older documents such as `docs/PROJECT_CHECKPOINT.md`, `docs/SOURCE_ASSET_MANIFEST.md` and `docs/ASSET_ADMISSION_VERIFICATION.md` contain accurate statements about the earlier initial transfer, when only eight PDF binaries were repository-admitted. Those statements are historical witnesses, not current inventory assertions.

For current documentary authority and repository lock state, `docs/SOURCE_AUTHORITY_POLICY.md`, `config/source_catalog.json`, `config/evidence_lock.json` and this file supersede any reading of those historical eight-PDF counts as present state.

## Current clinical boundary

P1 remains deterministic and separate from interpretation. P2B is source-linked, production-gated and fail-closed. AI synthesis remains preview-only.

Two exact sign-specific Rand–Mitte slices are now live from the same primary Triebpathologie I passage:

- `IC_SZONDI_PRIMARY_000055`: exact `s+!!` together with ordinary `e+`; Szondi describes the e-side through Gutmachung/Gewissensschutz.
- `IC_SZONDI_PRIMARY_000056`: exact `s+!!` together with `e0`; Szondi's first example calls the configuration an historical/testological `Aggressionsgefahr` without `ethischen Schutz`.

For `000056`, `e0` is not generalized into a universal meaning of absent conscience or morality, and `Aggressionsgefahr` is not translated into factual aggression, violence, dangerousness, criminality or prediction. Both claims remain exact profile-level source relations and do not extend to neighboring quantum/sign configurations by analogy.

The exact supporting doctrine for the new slice is `DR_SZ_TRIEBPATH_1_000004`; the older `DR_SZ_TRIEBPATH_1_000003` provenance metadata was also refreshed to point to the now repository-locked original PDF.

At checkpoint `90b5bcc...` all five workflows completed successfully:

- Foundation verification — run `33571664321` — `success`;
- Runtime tests — run `33571664290` — `success`;
- P0 source inspection — run `33571664283` — `success`;
- P2A doctrine registry — run `33571664295` — `success`;
- P0 canonical access — run `33571664326` — `success`.

## Immediate next action

Continue source-grounded Rand–Mitte research from the primary corpus without widening `000055` or `000056`. The next candidate should be chosen by explicit source support, not by completing a reaction matrix by analogy.

For every new relation the sequence remains:

`primary source -> doctrine -> executable P2B -> exact trigger/guards -> focused tests -> Runtime/Foundation/P2A verification`

If source review reveals a genuine doctrinal ambiguity that changes clinical meaning, stop for clinician decision; ordinary implementation details remain technical work.

## Important residual non-blockers

- ClinicalReport lacks a complete build/release manifest for retrospective production audit.
- E.K.P. findings can reach ClinicalReport but are not yet carried into the AI evidence packet.
- AI validation verifies the exact support envelope, not semantic fidelity of generated prose; therefore AI must not become autonomous production output yet.
- `_capture()` still treats any P1 `ValueError` as clinical `UNRESOLVED`; a domain-specific fail-closed exception would be cleaner later.
- `tmp-do-not-use` is an obsolete/accidental branch and must not be used as a work base.
- PR #50 contains unmerged Schicksalsanalyse research and is a research witness only.
- `work/p2b-multiple-triebgefahren-001` should be preserved but not merged automatically; claim ID `000054` is already occupied in live.

## Working style

Do not reopen another general audit unless a concrete new contradiction appears. Do not add RAG, vector DB, ontology, second LLM validator, alternate scoring paths or invented aggregate interpretation scores.

Ask the clinician only for genuine doctrinal/clinical decisions that change meaning. Handle ordinary programming, tests, routing, CI and source-provenance mechanics autonomously.

> Correct-but-incomplete beats rich-but-invented.
