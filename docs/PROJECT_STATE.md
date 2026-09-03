# Szondi3 — current project state

**Status:** CURRENT OPERATIONAL STATE

This file is the only mutable project-state summary. It is not a chat handoff. Live repository state, source evidence, executable code and CI outrank this summary whenever they disagree.

## Active line

- repository: `danono2016/Szondi3`
- clinical branch: `work/ai-clinical-provenance-strategy-001`
- PR #65: OPEN / DRAFT / NOT MERGED; integration umbrella, not an automatic release gate
- current executable catalogue frontier: `IC_SZONDI_PRIMARY_000080`

## Authority chain

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE P2B -> SOFTWARE FINDINGS -> AI SYNTHESIS / WORDING`

No downstream layer may rewrite upstream evidence or doctrine.

P0 remains 10 admitted DOCX + 10 original/admitted PDFs + 48 stimulus WebP. The original PDF is the documentary arbiter when OCR/DOCX conflicts on signs, formulas, tables, layout or typography. See `docs/SOURCE_AUTHORITY_POLICY.md`.

## Stable boundaries

- P1 remains deterministic and separate from interpretation.
- Doctrine and executable formalization remain separate layers.
- AI synthesis remains closed-world, preview-only and deterministically gated; autonomous clinical release remains disabled.
- No vector DB/RAG, alternate P1 scoring path, hidden case-specific rules or second LLM validator.
- Fall 40 is a regression specimen, not runtime doctrine.
- Clinician-facing wording preserves source-authorized Szondian terminology, diagnostic force and rhetorical character; stylistic fidelity never authorizes invention.

## Current executable frontier

The live catalogue extends through `IC_SZONDI_PRIMARY_000080`.

`000079` preserves the source boundary around Sublimationsart: the kind of Ego defense may constrain a source-authorized reading, but Szondi explicitly presents the relevant table as incomplete; the software must not manufacture a complete sublimation taxonomy or infer profession, talent or vocation from an isolated Sch formula.

`000080` preserves the boundary between Charakter and Schicksal: character is a part of fate impressed into the Ego through introjection, not the whole fate of the person. Wahl/Projektion and Einprägung/Introjektion remain distinct levels.

## Technical state

The regression introduced in `clinical_interpretation.py` by commit `06a152c` was repaired by `f9d183798d39c53aee1fed28790da4a9812665f3` (`Restore clinical interpretation contract compatibility`). The public interpretation contract again preserves distinct `unresolved`, `blocked_context` and `production_mode` state while retaining current catalogue routing.

At that repair checkpoint the full runtime suite ran 366 tests successfully, and all five repository verification workflows completed successfully.

## Development rule

Do not reconstruct project state from old chat-transfer documents or conversational checkpoints. Git history already preserves that history.

For a new task:

1. verify live branch HEAD, `main`, PR #65 and CI;
2. read only the stable policy/specification documents relevant to the task;
3. inspect the current code and doctrine records directly;
4. make the smallest source-grounded change that solves the concrete problem;
5. run focused tests and the repository verification suite;
6. stop for clinician input only when a genuine doctrinal/clinical ambiguity changes meaning.

## Immediate next action

Technical development may continue. Clinical development may continue in source order beyond the current `000080` frontier when an explicit primary-source relation can be represented without semantic inflation. Use the existing cycle:

`source -> doctrine -> executable condition/guard where justified -> tests -> pipeline verification`

Correct-but-incomplete remains preferable to rich-but-invented.
