# Szondi3 — current project state

This file is the short continuation checkpoint. The full handoff, forensic audit,
severity assessment, source-authority rule, unresolved risks, and ordered next
steps are in:

`docs/CHAT_TRANSFER_PACKAGE.md`

Always read that file first and then verify current Git HEAD, open PRs, and CI.
Do not reconstruct project state from chat memory.

## Verified audit baseline

- repository: `danono2016/Szondi3`
- clinical line: `work/ai-clinical-provenance-strategy-001`
- forensic-audit baseline: `92befe8cc3a47af5f5c30d0ce56dc2d9b778b949`
- baseline includes PR #92 source-authority policy
- executable catalogue reaches `IC_SZONDI_PRIMARY_000055`
- PR #65 remains the open/draft umbrella PR toward `main` at the audit baseline

The docs-only transfer package itself may advance the branch after this baseline;
therefore never treat the SHA above as a substitute for checking the live ref.

## Authority chain

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE P2B -> SOFTWARE FINDINGS -> AI SYNTHESIS`

Original authentic PDF and clinician-created ABBYY DOCX replica have equal primary
documentary rank when concordant. On conflict, the original PDF is supreme. See
`docs/SOURCE_AUTHORITY_POLICY.md`.

## Current clinical boundary

P1 remains deterministic and separate from interpretation. P2B is source-linked,
production-gated, and fail-closed. AI synthesis remains preview-only.

Claim `000055` is live as the first exact sign-specific Rand–Mitte slice:
`s+!!` together with ordinary `e+`, with strict anti-inference guards. Do not
extend it by analogy to neighboring quantum/sign configurations.

## Audit result that changes priority

The 2026-09-02 forensic audit found no reason to rewrite P1 or restart the project.
The main current defect is upstream reproducibility:

- all 10 authentic PDFs are now documentary-authority sources;
- only 8 PDFs are repository-locked in the current evidence lock;
- `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` remain `pdfPath: null` pending binary lock;
- the current P0 canonical workflow still expects exactly 8 repository PDFs.

Under `docs/VALIDATION_AND_RECOVERY.md`, `P0_SOURCES_PASS` requires all authorized
PDF binaries to be present and identity-verified. Therefore P0 should be treated as
**administratively reopened** until the two Triebpathologie PDFs are locked and P0
passes 10/10.

This is a reproducibility/control-plane issue, not a finding that P1 or current P2B
clinical semantics are corrupted.

## Immediate next actions

Do not add new clinical doctrine before closing the first three items:

1. binary-admit and identity-lock both Triebpathologie original PDFs;
2. update source catalog, evidence lock, and P0 PDF expectation from 8 to 10, then
   run Foundation + Runtime + P0 source + P0 canonical + P2A to full green;
3. make P0 source/canonical workflows run directly on the clinical branch rather
   than depending incidentally on open PR #65 toward `main`.

After that:
4. enable GitHub required checks/branch protection on `main` and the clinical branch
   if repository settings permit;
5. decide the role/fate of oversized draft PR #65;
6. resume source-grounded Rand–Mitte, with `s+!! / e0` as the natural next candidate
   from the same primary context as 000055, unless a better primary rule is found.

## Important residual non-blockers

- ClinicalReport lacks a complete build/release manifest for retrospective production audit.
- E.K.P. findings can reach ClinicalReport but are not yet carried into the AI evidence packet.
- AI validation verifies the exact support envelope, not semantic fidelity of generated prose;
  therefore AI must not become autonomous production output yet.
- `_capture()` still treats any P1 `ValueError` as clinical `UNRESOLVED`; a domain-specific
  fail-closed exception would be cleaner later.
- `tmp-do-not-use` is an obsolete/accidental branch and must not be used as a work base.
- PR #50 contains unmerged Schicksalsanalyse research and is a research witness only.
- `work/p2b-multiple-triebgefahren-001` should be preserved but not merged automatically;
  claim ID 000054 is already occupied in live.

## Working style

Do not reopen another general audit after this package unless a concrete new
contradiction appears. Do not add RAG, vector DB, ontology, second LLM validator,
alternate scoring paths, or invented aggregate interpretation scores.

Ask the clinician only for genuine doctrinal/clinical decisions that change meaning.
Handle ordinary programming, tests, routing, CI, and source-provenance mechanics
autonomously.

> Correct-but-incomplete beats rich-but-invented.
