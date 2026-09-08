# Szondi3 — current project state

**Status:** CURRENT OPERATIONAL STATE

This file is the only mutable project-state summary. It is not a chat handoff. Live repository state, source evidence, executable code and CI outrank this summary whenever they disagree.

## Active line

- repository: `danono2016/Szondi3`
- clinical branch: `work/ai-clinical-provenance-strategy-001`
- PR #65: OPEN / DRAFT / NOT MERGED; integration umbrella, not an automatic release gate
- current executable catalogue frontier: `IC_SZONDI_PRIMARY_000087`
- stabilization implementation HEAD: `8764198d889ecdb7b544cb36f59e0a28f94ae96e`

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

The live catalogue extends through `IC_SZONDI_PRIMARY_000087`.

`000079` preserves the source boundary around Sublimationsart: the kind of Ego defense may constrain a source-authorized reading, but Szondi explicitly presents the relevant table as incomplete; the software must not manufacture a complete sublimation taxonomy or infer profession, talent or vocation from an isolated Sch formula.

`000080` preserves the boundary between Charakter and Schicksal: character is a part of fate impressed into the Ego through introjection, not the whole fate of the person. Wahl/Projektion and Einprägung/Introjektion remain distinct levels.

`000081` preserves Szondi's probabilistic comparison for Annahme, Sch +±: the source says these defenses `scheinen` to have more success against Triebgefahren because Angst is rarer than with the four immediately preceding forms, Sch ±+, -0, ±± and ±-. The executable relation is restricted to the exact ordinary Sch +± configuration and must not be turned into a person-level anxiety measurement, a mental-health conclusion or a claim of globally superior defense efficacy.

`000082` and `000083` execute the two source-explicit Kontaktlosigkeit C 00 special cases from Ich-Analyse II p.359: C 00 with Sch ±± (Integration) and C 00 with Sch +± (Introjektion der Verlassenheit). Both require the exact ordinary C/Sch conjunction and block promotion of the source imagery into invented biography.

`000084` executes only the categorical core of the source relation `stets unsicher, problematisch`: ordinary Sch 00, +0 or +- together with the source-listed C configurations. Sch ++ remains excluded because Szondi qualifies that form only with `teils auch`.

`000085` is a method boundary for Charakterbildung: Szondi explicitly rejects a unifunctional, purely introjective account. Introjektion remains the Einprägung function, but Projektion, Inflation and Negation also participate. Runtime therefore blocks reduction of character to +k/Introjektion or to one isolated Ich-Funktion.

`000086` executes the source-explicit Affekt relation from Ich-Analyse II p.359: ordinary Sch 00, ±0, +0, -0 or 0+ occurs `oft` with an ethical dilemma e±, a moral dilemma hy±, or the double ethical-moral dilemma P ±±. Runtime represents the source's `oder` exactly as e± OR hy± across the ordinary P signatures; it does not require both factors to be ambivalent and does not extend the rule to Überdruck.

`000087` is a general non-determinism limitation grounded in `DR_SZ_IA_1956_A_000038`, Ich-Analyse I pp.105–106. A familiär angelegte Triebdialektik is not rendered as fixed personal fate: Szondi explicitly allows `persönliche, bewußte Stellungnahme` to alter the drive dialectic and Schicksal, and the following source context defines `Umkehrung` as `Dominanzwechsel` rather than alteration of `Ursubstanz`. Runtime therefore blocks inevitable-fate, fixed-biography and modern-genetic overreadings while preserving the historical doctrine's own limits.

## Technical state

The public interpretation contract preserves distinct `unresolved`, `blocked_context`, `production_mode` and `suppressed` state while retaining current catalogue routing.

Global P2B provenance verification evaluates the same complete executable catalogue imported by runtime through `IC_SZONDI_PRIMARY_000087`. Reserved historical claim gaps (`000022`, `000035`, `000036`) remain explicit historical gaps and are not silently renumbered or re-created.

The audited clinical-release manifest hashes the same complete executable P2B catalogue used by runtime through `IC_SZONDI_PRIMARY_000087`.

The audited release boundary is now bound to the verified local checkout identity. The caller-supplied `git_commit_sha` is only an assertion: it must equal the clean local Git `HEAD`; tracked modifications and untracked doctrine-registry records fail closed. In GitHub Actions, `GITHUB_SHA` is an additional trusted assertion and must equal the checked-out `HEAD`. A syntactically valid but different caller SHA is rejected, so the manifest cannot silently name a different commit from the checkout that produced its doctrine/P2B/evidence digests.

The P2B catalogue has one explicit current executable/public frontier: `szondi3.interpretation_catalogue_fate_modifiability` through `IC_SZONDI_PRIMARY_000087`. `szondi3.interpretation_catalogue` remains importable only as the historical internal predecessor segment through `000070` and is explicitly marked non-current; runtime and release imports are regression-tested against the live frontier.

Complement administration now applies one shared series-choice invariant at both `complete_complement()` and deserialized-protocol validation boundaries. A complement series must be exactly two distinct relative-sympathetic plus two distinct relative-unsympathetic cards partitioning the four VGP remainders; malformed `3+1` and duplicate constructions fail immediately.

A focused runtime regression for `000087` traverses `evaluate_clinical_protocol(..., production=True)` and verifies its limitation mode, doctrine link, source-bounded wording, support fact, anti-inference and hereditary/genetic sensitive-domain marking. A golden administered-protocol regression separately traverses actual recorded card choices through administration -> P1 scoring -> profile series -> P2B findings -> clinical report -> canonical evidence packet -> audited release.

`executionStatus` in the current primary-doctrine schema is not an implementation-completion field: its vocabulary contains only `NOT_ASSESSED` and `NOT_EXECUTABLE_YET`. Executability is therefore established from the live P2B catalogue, source/provenance audit records and tests, not inferred from that optional registry field.

## Closed doctrine frontiers

`SZ_IA_1956_B` is audited through `DR_SZ_IA_1956_B_000060`. Doctrines `000047`-`000052` remain non-executable at this stage because they concern theoretical Geist/Glaube claims, dream interpretation, historical hereditary theory, or a historically harmful criminological-sexual generalization that does not authorize a person-level software inference. Doctrines `000053`, `000054` and `000056`-`000060` were already represented by existing executable claims. `000055` was the remaining concrete coverage gap and is represented by `IC_SZONDI_PRIMARY_000086`.

Both Triebpathologie registries are source-order audited through their current frontiers. In `SZ_TRIEBPATH_1`, doctrines `000002`-`000004` are represented by the exact Rand-Mitte claims `000055` and `000056`; doctrine `000001` remains intentionally `NOT_EXECUTABLE_YET` because the registry does not authorize promotion of one `+!!` example into a generic overpressure-danger rule. In `SZ_TRIEBPATH_2`, doctrine `000001` is represented by `000031`, doctrine `000002` by `000052`, and doctrine `000003` by `000053`.

`SZ_IA_1956_A` is now retrospectively executability-audited through `DR_SZ_IA_1956_A_000051`; the record-by-record closure is `docs/SZ_IA_1956_A_EXECUTABILITY_CLOSURE.md`. The closure found 9 directly executable doctrines (`000038`, `000040`, `000043`, `000045`-`000049`, `000051`), 10 already covered indirectly, 29 contextual/theoretical doctrines without independent person-level inference authority, and 3 deliberate `NOT_EXECUTABLE_YET` items (`000033`, `000042`, `000050`). It found no `EXECUTABLE_GAP` and no unresolved source arbitration, so this frontier does not authorize `000088`.

The closure also repairs the procedural defect around `000087`: `DR_SZ_IA_1956_A_000038` itself was already `SOURCE_VERIFIED`, with batch-010 source-order coverage and printed-page arbitration predating promotion. `IC_SZONDI_PRIMARY_000087` remains doctrinally and software-valid. The missing step was the repository-level closure of the whole IA-A `000001`–`000051` frontier before that promotion, not a defect in doctrine `000038` or claim `000087`.

The IA-A HOLDs are unchanged: `DR_SZ_IA_1956_A_000033`, `000042` and `000050` remain `NOT_EXECUTABLE_YET` until source-faithful runtime discriminators exist and a fresh audit authorizes promotion. They do not authorize `IC_SZONDI_PRIMARY_000088`.

## Verification state

The stabilization implementation HEAD `8764198d889ecdb7b544cb36f59e0a28f94ae96e` has fresh green CI. All eight workflow runs reported for that exact branch HEAD completed successfully, including Runtime tests, P2A doctrine registry, P0 canonical access, P0 source inspection and Foundation verification. The Runtime suite completed `390` tests with `OK`, including the new release-identity, catalogue-frontier, complement-invariant and golden end-to-end regressions.

This state-sync document is a non-executable follow-up commit. Live branch HEAD and CI remain authoritative over any SHA written inside this mutable summary; the documentation commit itself must also remain green before the checkpoint is accepted.

## Development rule

Do not reconstruct project state from old chat-transfer documents or conversational checkpoints. Git history preserves that history.

For a new task:

1. verify live branch HEAD, `main`, PR #65 and CI;
2. read only the stable policy/specification documents relevant to the task;
3. inspect the current code and doctrine records directly;
4. make the smallest source-grounded change that solves the concrete problem;
5. run focused tests and the repository verification suite;
6. stop for clinician input only when a genuine doctrinal/clinical ambiguity changes meaning.

## Immediate next action

Do not create `IC_SZONDI_PRIMARY_000088` from the closed IA-A frontier. `DR_SZ_IA_1956_A_000033`, `000042` and `000050` remain HOLD / `NOT_EXECUTABLE_YET` until source-faithful runtime discriminators exist and a fresh audit authorizes promotion. No current IA-A doctrine is an executable gap.

The four stabilization/readiness findings authorized for repair are now implemented in code/tests and reflected in this state summary. Do not begin new clinical-content or feature development until the clinician explicitly confirms the development-ready checkpoint.

Use the existing cycle:

`source -> doctrine -> executable condition/guard where justified -> tests -> pipeline verification`

Correct-but-incomplete remains preferable to rich-but-invented.