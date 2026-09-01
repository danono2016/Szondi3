# Szondi3 — current project state

This file is the default continuation checkpoint for future development sessions.
It is intentionally short. Git history, tests, doctrine registries, and source
artifacts remain the authorities for detail; they should not be duplicated into
large chat handoffs.

Always verify the current Git HEAD and open PRs before writing. The commit named
below is a stabilization baseline, not a substitute for checking the live ref.

## Goal

Build a clinically useful Szondi implementation that preserves deterministic P1
calculation, source-linked P2B interpretation, explicit epistemic limits, and a
bounded narrative/report layer without unnecessary procedural or runtime overhead.

## Current architecture

`administration -> scoring/profile/series (P1) -> clinical facts -> P2B claims -> clinical protocol -> report/evidence packet -> bounded synthesis`

Cross-cutting authorities:
- canonical source corpus;
- doctrine registry;
- automated tests and fail-closed guards.

The authority chain remains:

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE P2B -> SOFTWARE FINDINGS -> AI SYNTHESIS`

## Current working line

- clinical development line: `work/ai-clinical-provenance-strategy-001`
- stabilization baseline after PR #89: `c206d2f7e1c330998be9e099907eae06c038a8a9`
- current executable catalogue reaches `IC_SZONDI_PRIMARY_000054`
- PR #88 restored full P2A doctrine-gate integrity and made P2A run on the clinical line
- PR #89 hardened the clinical input boundary, error boundary, explicit claim routing,
  P2B lifecycle/provenance checks, epistemic ceiling checks, and monotonic doctrine
  review-state handling
- post-merge P2A on the stabilization baseline passed repository tests, registry
  structure/provenance validation, transversal validation, canonical regeneration,
  and exact doctrine-anchor/source-excerpt validation

`docs/PROJECT_CHECKPOINT.md` is an intentionally historical P1 gate-finalization
record. Do not rewrite it as current state. This file is the short current
continuation checkpoint.

## Current clinical interpretation boundary

The catalogue through `000054` is source-linked and production-gated. Important
methodological boundaries now include:

- profile findings remain possibilities/configurations, not a total person description;
- historical Szondian meanings do not become modern diagnosis, genetics, dangerousness,
  criminality, or concrete behavior without independent support;
- quantitative Linnäus findings are valid within their method but do not by themselves
  establish current illness/health status;
- Linnäus/Triebklasse gives quantitative orientation and does not by itself establish
  an individual Abwehrart, a concrete Triebgefahr–Abwehr relation, chronic defense,
  or Schicksalsdiagnose;
- Rand–Mitte and Vorder-/Hintergänger remain distinct qualitative methods and must not
  be replaced by invented aggregate scores.

Claim `IC_SZONDI_PRIMARY_000015` remains the quantitative Haupttriebklasse/current
Triebgefahr rule for a ten-profile series. Claim `000054` is a separate methodological
guard; it does not invalidate Linnäus.

## Stabilization status

The systemic read-only audit requested before further clinical expansion is closed.
Packages A and B are complete.

The repaired control boundary now includes:
- full P2A validation on the clinical line;
- canonical exact-excerpt verification for doctrine changes;
- revalidation of administered protocols on the real clinical scoring path;
- unexpected `TypeError` programming mismatches are no longer converted into clinical
  `UNRESOLVED` states;
- claim `000054` is routed explicitly;
- new catalogue claims require explicit lifecycle status;
- P2B `source_ids` must match linked doctrine sources exactly;
- mechanical epistemic-ceiling checks apply to genuinely epistemic P2B modes while
  logical/functional modes such as `CONDITIONAL` are not misclassified as certainty;
- evidence packets accept the monotonic reviewed doctrine states `SOURCE_VERIFIED`,
  `CLINICIAN_REVIEWED`, and `ACCEPTED`.

Branch protection / required-check enforcement is not configured through the current
connected tooling. CI runs the required checks, but GitHub-level prevention of a
manual bypass remains an administrative repository setting.

## Report and AI boundary

`ClinicalReport` and `ClinicalEvidencePacket` preserve deterministic observations,
calculations, executable findings, doctrine/source identities, anti-inferences,
uncertainties, release state, and evidence-packet schema version.

They do not yet embed a complete build manifest containing Git commit + doctrine
snapshot/digest + P2B release identity. Add that before a production deployment that
requires retrospective reconstruction of an exported patient report. Do not block
source/doctrine/P2B research on this preview-stage packaging requirement.

AI synthesis remains preview-only. Provenance-envelope validation is not semantic
proof that generated prose obeys every anti-inference. Do not promote AI synthesis
to autonomous production clinical output until semantic overreach has a sufficiently
strong deterministic control.

## Optimization policy

Optimize without weakening clinical semantics.

Keep:
- P1/P2B separation;
- source/doctrine provenance;
- fail-closed ambiguity handling;
- anti-inference guards;
- clinically meaningful positive/negative regression coverage.

Reduce:
- repeated indexing/traversal;
- repeated registry reads;
- repeated claim-selection construction;
- redundant test boilerplate;
- audit-of-audit loops;
- giant chat handoffs and duplicated project history.

Do not introduce infrastructure for hypothetical future needs without a concrete
failure mode.

## Fall 40 policy

Fall 40 is, at most, an ordinary regression specimen. It is not an architectural,
doctrinal, or product-design target. No feature should be justified primarily by
making Fall 40 produce a preferred result.

New unit-level tests should prefer the smallest synthetic profile/series that proves
the invariant. Keep Fall 40 only where an explicit historical end-to-end regression
is useful.

## Immediate next clinical work

Return to clinically useful source-grounded development. Do not reopen another general
audit unless a concrete contradiction or failure appears.

Priority sequence:
1. resume Rand–Mitte research at the smallest source-established intervector relation;
2. prefer an exact executable relation over a diagnostic table or invented score;
3. keep qualitative Rand–Mitte interpretation distinct from Linnäus and from the
   partial Sch complement machinery;
4. after a relation is established, implement doctrine -> claim -> trigger/guards ->
   focused tests -> Runtime/Foundation/P2A -> merge.

The strongest current candidate for the first real Rand–Mitte slice is the primary
source relation between Rand factor `s` and Mitte factor `e` (Gewissenszensur). It
must be reverified against exact admitted source evidence before implementation and
must not be generalized beyond the source-defined configuration.

A separate pre-stabilization work branch for multiple simultaneous Triebgefahren
exists and should be preserved. Its structural work can be reconsidered later from
the current live line; it must not reuse claim ID `000054`.

## Development loop

For an ordinary source-grounded claim or implementation change:
1. establish the canonical basis or concrete technical need;
2. implement the smallest general change;
3. run focused regression coverage plus Runtime, Foundation, and P2A as applicable;
4. stop when the invariant is demonstrated.

Do not add a second audit merely to confirm the first audit unless a concrete
contradiction or failure appears.

## Continuation rule

Start future sessions from this file plus the current Git HEAD/diff. Inspect deeper
historical documents only when the active task specifically requires them. Do not
reconstruct project history in the chat unless it is necessary to resolve a real
technical or doctrinal ambiguity.
