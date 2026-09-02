# Szondi3 — current project state

This file is the short continuation checkpoint. The full handoff and forensic-audit history are in `docs/CHAT_TRANSFER_PACKAGE.md`.

Always read the handoff first, then verify current Git HEAD, open PRs and CI. Do not reconstruct project state from chat memory. Historical SHA/count statements in older checkpoint documents remain historical witnesses and must not override this current checkpoint or the live repository.

## Current verified line

- repository: `danono2016/Szondi3`
- clinical line: `work/ai-clinical-provenance-strategy-001`
- forensic-audit baseline: `92befe8cc3a47af5f5c30d0ce56dc2d9b778b949`
- P0 10/10 recovery verification checkpoint: `061c172afb67b848d58295851ea22165ccbc1df5`
- Rand–Mitte `s+!! / e0` verification checkpoint: `90b5bcc54ee1cec2ccc25271ab22bc621e9db63a`
- technical finishing verification checkpoint: `3637f1c56c90fd36a6378d8e20e40d317a5a932c`
- executable catalogue currently reaches `IC_SZONDI_PRIMARY_000056`
- clinical development after that frontier was explicitly resumed by clinician decision on 2026-09-02
- PR #65: OPEN / DRAFT / NOT MERGED; role explicitly set to **clinical integration umbrella**, not release gate

Never treat a checkpoint SHA above as a substitute for checking the live ref; documentation or later work may advance the branch.

## Authority chain

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE P2B -> SOFTWARE FINDINGS -> AI SYNTHESIS`

Original authentic PDF and clinician-created ABBYY DOCX replica have equal primary documentary rank when concordant. On conflict, the original PDF is supreme. See `docs/SOURCE_AUTHORITY_POLICY.md`.

## Permanent clinician-report voice directive

`docs/DOCTRINAL_FIDELITY_POLICY.md` and `docs/PROJECT_CONSTITUTION.md` now make the reporting requirement explicit and authoritative.

The clinician-facing report must speak from inside Szondi's conceptual system. It must preserve, when source-authorized, not only concepts and diagnostic content but also Szondi's terminology, degree of assertion, directness, density, categorical contrasts, dramatic tension and baroque clinical atmosphere. It must not be automatically softened, euphemized, politically corrected, morally sanitized or translated into generic contemporary psychological prose.

The primary corpus is both doctrinal authority and stylistic reference for the clinician-facing report. Contemporary critique or softened communication may exist only as a separate labeled downstream layer.

AI is constrained on doctrinal/evidential truth but is not to domesticate Szondi's language. Stylistic fidelity never authorizes invention: the source remains the ceiling.

> **Constrain AI on doctrinal truth; do not domesticate Szondi's language.**

## P0 reproducibility boundary — RESTORED 10/10

The audit blocker `10 authorized PDFs / 8 repository-locked PDFs` is closed.

Both authentic Triebpathologie originals are repository-locked:

- `sources/originals/Szondi Triebpathologie 1. Teil.pdf` — Git blob `de905f28eb96b9da40bd4f6ce7e1cc852c94fe88`;
- `sources/originals/Szondi Triebpathologie 2. Teil.pdf` — Git blob `0ed487efd94788c13651032479b2278eabde49f5`.

Current machine boundary: 10 DOCX sources, 10 original/admitted PDF binaries and 48 stimulus WebP binaries. `config/source_catalog.json` carries both Triebpathologie `pdfPath` values; `config/evidence_lock.json` identity-locks all 10 PDFs; P0 canonical validation expects exactly 10 unique PDF paths.

## CI governance

P0 source inspection and P0 canonical access run directly on both `main` and `work/ai-clinical-provenance-strategy-001`; they no longer depend on PR #65 merely to execute on the clinical line.

At technical finishing checkpoint `3637f1c...` all five verification workflows completed successfully:

- Foundation verification — run `33573153763` — `success`;
- Runtime tests — run `33573153789` — `success`;
- P0 source inspection — run `33573153768` — `success`;
- P2A doctrine registry — run `33573153736` — `success`;
- P0 canonical access — run `33573153755` — `success`.

Repository governance is now actively enforced by two GitHub branch rulesets:

- `Szondi3 main protection` — ruleset `22055760`, active, targeting only `main`; blocks deletion and force-push, requires pull-request integration with zero mandatory human approvals, requires the branch to be up to date, and requires exactly these five GitHub Actions checks: `verify-foundation`, `unittest`, `inspect-docx`, `canonical-access`, `doctrine-registry`.
- `Szondi3 clinical branch protection` — ruleset `22056039`, active, targeting only `work/ai-clinical-provenance-strategy-001`; blocks deletion and force-push while deliberately allowing ordinary direct fast-forward updates so the existing clinical workflow can continue and CI can run after each push.

Both rulesets have an empty bypass list. The earlier governance gap is therefore closed.

PR #65 is intentionally retained OPEN/DRAFT as an integration umbrella. Its accumulated size is not treated as a release gate, and it must not be merged automatically merely because CI is green.

## Historical eight-PDF wording

Older documents such as `docs/PROJECT_CHECKPOINT.md`, `docs/SOURCE_ASSET_MANIFEST.md` and `docs/ASSET_ADMISSION_VERIFICATION.md` contain accurate statements about the earlier initial transfer, when only eight PDF binaries were repository-admitted. Those statements are historical witnesses, not current inventory assertions.

For current documentary authority and repository lock state, `docs/SOURCE_AUTHORITY_POLICY.md`, `config/source_catalog.json`, `config/evidence_lock.json` and this file supersede any reading of those historical eight-PDF counts as present state.

## Current clinical frontier — development resumed after 000056

P1 remains deterministic and separate from interpretation. P2B is source-linked, production-gated and fail-closed. AI synthesis remains preview-only.

Two exact sign-specific Rand–Mitte slices are live from the same primary Triebpathologie I passage:

- `IC_SZONDI_PRIMARY_000055`: exact `s+!!` together with ordinary `e+`; Szondi describes the e-side through Gutmachung/Gewissensschutz.
- `IC_SZONDI_PRIMARY_000056`: exact `s+!!` together with `e0`; Szondi's first example calls the configuration `Aggressionsgefahr` without `ethischen Schutz`.

The prior hold on opening further clinical relations has been explicitly lifted by clinician decision on 2026-09-02. This authorization permits continued source-grounded clinical development; it does not authorize analogical widening of existing claims or invention of missing doctrine.

The next clinical increment must be selected from the admitted corpus by evidential strength and clinical value, not merely by numerical adjacency or by mechanically extending the `s/e` examples. Each new increment must preserve exact source meaning, executable conditions, unsupported-inference boundaries, and the permanent clinician-report voice directive above.

Existing limitations attached to the current Rand–Mitte slices must be interpreted as guards against conclusions unsupported by their source/configuration, never as a license to sanitize explicit Szondian terminology or diagnostic force. Any such limitation that appears to suppress an explicit source meaning must be reviewed against the primary source before being carried forward as precedent.

## Technical finishing completed

### Audited build/release identity

`szondi3/clinical_release.py` provides an audited deterministic release envelope around an already-built evidence packet. Its manifest records:

- full Git commit SHA;
- doctrine snapshot identity and doctrine-registry SHA-256;
- P2B release identity and P2B-catalogue SHA-256;
- evidence-packet SHA-256;
- synthesis contract version;
- synthesis model identity.

The manifest explicitly records `PREVIEW_ONLY_MANUAL_CLINICIAN_RELEASE` and `autonomous_ai_release = false`. The manifest adds traceability only; it grants no new clinical authority.

### E.K.P. evidence transport

Administered experimental-complement material can now be carried into an `AdministeredClinicalEvidencePacket` together with its exact complement-specific findings, canonical doctrine, formal factor symbols and complement facts.

The separation invariant is preserved:

- foreground profiles remain the repeated free-reaction series;
- E.K.P. remains `EXPERIMENTAL_COMPLEMENT` scope tied to its administered test number;
- E.K.P. is never silently promoted to a foreground profile;
- the deterministic synthesis validator can validate an explicitly complement-scoped proposition only against the exact active complement finding/support bundle.

The OpenAI preview structured-output schema remains intentionally narrower (`PROFILE` / `SERIES`). Therefore E.K.P. is present in the closed-world evidence packet but model-authored E.K.P.-scoped prose is not automatically released or promoted. This is a fail-closed safety boundary, not missing evidence transport.

### P1 unresolved/error boundary

`P1UnresolvedError` now marks expected source-defined deterministic fail-closed states. The clinical orchestrator `_capture()` catches only this typed exception.

Consequently:

- legitimate P1 ambiguity can still appear as clinical `UNRESOLVED`;
- a generic accidental `ValueError` is no longer masked as clinical ambiguity;
- `TypeError` and other programming errors continue to surface normally.

This removes the earlier broad-`ValueError` masking risk without changing P1 scoring or source-defined rules.

## Remaining deliberate boundaries, not unfinished repairs

- AI validation proves the exact support envelope, not semantic fidelity of arbitrary generated prose. Autonomous AI clinical release therefore remains disabled by design.
- `tmp-do-not-use` remains obsolete and must not be used as a work base.
- PR #50 remains an unmerged Schicksalsanalyse research witness only.
- `work/p2b-multiple-triebgefahren-001` remains preserved but must not be merged automatically; claim ID `000054` is already occupied in live.

## Immediate next action

Clinical development is now authorized to continue. First verify live HEAD and CI, then select the next source-grounded clinical increment from the admitted corpus by clinical value and evidential strength. Do not reopen a general audit and do not mechanically extend the current Rand–Mitte examples by analogy.

The next increment should be developed end-to-end: primary passage and visual arbitration where needed -> doctrine -> executable conditions -> unsupported-inference boundaries -> clinician-facing Szondian wording -> tests -> pipeline verification.

## Working style

Do not reopen another general audit unless a concrete new contradiction appears. Do not add RAG, vector DB, ontology, second LLM validator, alternate scoring paths or invented aggregate interpretation scores.

Ask the clinician only for genuine doctrinal/clinical decisions that change meaning. Handle ordinary programming, tests, routing, CI and source-provenance mechanics autonomously.

> Correct-but-incomplete beats rich-but-invented.
