# Executable Richness Worklog

Status: focused Alpha-1 development branch.

Purpose: close the gap between the richness already present in admitted Szondi doctrine and the thin executable material currently reaching clinician-facing AI.

Hard boundaries:
- no P1/scoring changes;
- no `manual` branch or `docs/manual/` changes;
- no unsupported doctrine creation;
- no AI invention of missing Szondian meaning;
- no automatic merge;
- preserve source epistemic strength and exact scope;
- preserve anti-Mosaikspiel constraints;
- keep P2B frontier discipline explicit rather than silently bypassing it.

Immediate acceptance specimen: `alpha1-test2`, foreground profile `h- s+! | e- hy- | k+ p0 | d0 m-`, vectors `S -+! | P -- | Sch +0 | C 0-`.

## Implemented in this branch

- The ordinary clinician report now shows every active case-specific deterministic meaning before and independently of AI, with a direct `Sursa și justificarea` drill-down.
- The Alpha AI contract is now explicitly governed by **semantic expansion without doctrinal expansion**.
- AI receives exact per-profile morphology: factor symbols, quantum levels, forced-null flags and vector symbols. This allows wording such as `s +!` instead of generic phrases such as “factorul marcat”.
- AI may provide zero to two explicitly hypothetical micro-examples, but they must be visibly marked as illustrative and remain inside the already-authorized meaning.
- The Alpha AI output scope is restricted to foreground `PROFILE` and `SERIES`. `EXPERIMENTAL_COMPLEMENT` is excluded from both schema and runtime validation; E.K.P. remains a separate testological surface.
- Existing anti-Mosaikspiel validation remains in force: independent deterministic fact bundles cannot be joined merely because they coexist in one profile.

## Acceptance-specimen coverage audit

The current executable layer already supplies useful material for `+k`, the quantum tension at `s +!`, the exact `-m/+k` introjective-identification relation, and ordinary `Sch +0` / `totale Introjektion`. Those meanings can now reach AI with their exact profile morphology and can be expanded semantically without changing their doctrinal scope.

The exact specimen configurations `S -+!`, `P --` and `C 0-` do **not** currently have corresponding executable P2B meanings adequate to support the richer vector-level reading desired for this case. This branch does not bypass that gap by sending non-executable P2A material directly to AI and does not create a new P2B claim. The public executable frontier remains `IC_SZONDI_PRIMARY_000087`.

Next acceptance step: verify the changed contract and clinician surface under the full test/CI suite, then evaluate one real Alpha AI rendering of `alpha1-test2`. Any remaining semantic thinness must be classified explicitly as either a wording problem or an executable-coverage problem before further development.
