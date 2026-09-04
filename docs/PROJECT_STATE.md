# Szondi3 — current project state

**Status:** CURRENT OPERATIONAL STATE

This file is the only mutable project-state summary. It is not a chat handoff. Live repository state, source evidence, executable code and CI outrank this summary whenever they disagree.

## Active line

- repository: `danono2016/Szondi3`
- clinical branch: `work/ai-clinical-provenance-strategy-001`
- PR #65: OPEN / DRAFT / NOT MERGED; integration umbrella, not an automatic release gate
- current executable catalogue frontier: `IC_SZONDI_PRIMARY_000085`

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

The live catalogue extends through `IC_SZONDI_PRIMARY_000085`.

`000079` preserves the source boundary around Sublimationsart: the kind of Ego defense may constrain a source-authorized reading, but Szondi explicitly presents the relevant table as incomplete; the software must not manufacture a complete sublimation taxonomy or infer profession, talent or vocation from an isolated Sch formula.

`000080` preserves the boundary between Charakter and Schicksal: character is a part of fate impressed into the Ego through introjection, not the whole fate of the person. Wahl/Projektion and Einprägung/Introjektion remain distinct levels.

`000081` preserves Szondi's probabilistic comparison for Annahme, Sch +±: the source says these defenses `scheinen` to have more success against Triebgefahren because Angst is rarer than with the four immediately preceding forms, Sch ±+, -0, ±± and ±-. The executable relation is restricted to the exact ordinary Sch +± configuration and must not be turned into a person-level anxiety measurement, a mental-health conclusion or a claim of globally superior defense efficacy.

`000082` and `000083` execute the two source-explicit Kontaktlosigkeit C 00 special cases from Ich-Analyse II p.359: C 00 with Sch ±± (Integration) and C 00 with Sch +± (Introjektion der Verlassenheit). Both require the exact ordinary C/Sch conjunction and block promotion of the source imagery into invented biography.

`000084` executes only the categorical core of the source relation `stets unsicher, problematisch`: ordinary Sch 00, +0 or +- together with the source-listed C configurations. Sch ++ remains excluded because Szondi qualifies that form only with `teils auch`.

`000085` is a method boundary for Charakterbildung: Szondi explicitly rejects a unifunctional, purely introjective account. Introjektion remains the Einprägung function, but Projektion, Inflation and Negation also participate. Runtime therefore blocks reduction of character to +k/Introjektion or to one isolated Ich-Funktion.

## Technical state

The public interpretation contract preserves distinct `unresolved`, `blocked_context`, `production_mode` and `suppressed` state while retaining current catalogue routing.

Global P2B provenance verification evaluates the same complete executable catalogue imported by runtime, now through `IC_SZONDI_PRIMARY_000085`. Reserved historical claim gaps (`000022`, `000035`, `000036`) are treated as explicit gaps, not silently renumbered or re-created.

The audited clinical-release manifest hashes the same complete executable P2B catalogue used by runtime, now through `IC_SZONDI_PRIMARY_000085`. This prevents a release identity from remaining unchanged when later executable catalogue extensions are active.

A golden administered-protocol regression traverses actual recorded card choices through administration -> P1 scoring -> profile series -> P2B findings -> clinical report -> canonical evidence packet -> audited release. It also checks deterministic repeated release output and keeps experimental complement material in its separate scope.

`executionStatus` in the current primary-doctrine schema is not an implementation-completion field: its vocabulary contains only `NOT_ASSESSED` and `NOT_EXECUTABLE_YET`. Therefore executable status must currently be established from the live P2B catalogue and its provenance tests, not inferred from that optional registry field.

At the `000085` executable checkpoint, runtime had previously passed the full repository test suite. After traceability alignment changes, CI must be read from the current branch HEAD before declaring the checkpoint green.

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

Technical development may continue. Clinical development may continue in source order beyond the current `000085` frontier when an explicit primary-source relation can be represented without semantic inflation. Use the existing cycle:

`source -> doctrine -> executable condition/guard where justified -> tests -> pipeline verification`

Correct-but-incomplete remains preferable to rich-but-invented.