# Szondi3 — current project state

This file is the default continuation checkpoint for future development sessions.
It is intentionally short. Git history, tests, doctrine registries, and source
artifacts remain the authorities for detail; they should not be duplicated into
large chat handoffs.

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

## Current working branches

- clinical provenance base: `work/ai-clinical-provenance-strategy-001`
- optimization pass: `work/optimization-pass-001`
- optimization PR: #66

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
- repeated packet/validation setup;
- redundant test boilerplate;
- audit-of-audit loops;
- giant chat handoffs and duplicated project history.

Do not introduce infrastructure for hypothetical future needs without a concrete
failure mode.

## Fall 40 policy

Fall 40 is, at most, an ordinary historical regression specimen. It is not an
architectural, doctrinal, or product-design target. No feature should be justified
primarily by making Fall 40 produce a preferred result.

New runtime or P2B tests should use the smallest synthetic fixture that demonstrates
the invariant. Fall 40 should be used only when the regression specifically concerns
that historical end-to-end specimen.

## Test policy

Prefer the smallest test that can fail for the intended reason:
- one positive activation case;
- one clinically important negative/boundary case;
- generic invariant tests for provenance, fail-closed behavior, and schema rules.

Do not duplicate the same safety invariant at every layer unless the layers can fail
independently. Full CI remains the integration gate; local development should not
re-run unrelated audit suites after every small change.

## Development loop

For an ordinary source-grounded claim or implementation change:
1. establish the canonical basis or concrete technical need;
2. implement the smallest general change;
3. run focused regression coverage plus the normal CI gate;
4. stop when the invariant is demonstrated.

Do not add a second audit merely to confirm the first audit unless a concrete
contradiction or failure appears.

## Current optimization pass

Already implemented on `work/optimization-pass-001`:
- shared fact indexing during P2B catalogue evaluation;
- cached repeated claim selection;
- shared per-profile factor maps during evidence-packet construction;
- cached loading of the packaged doctrine registry while keeping custom test
  registries uncached;
- reusable synthesis-validation context that indexes findings and canonical
  doctrine once for repeated proposition checks;
- this short project-state checkpoint as the default continuation surface.

All runtime changes preserve public clinical semantics, provenance, and fail-closed
behavior. The corresponding normal CI gates have remained green through the latest
completed runtime optimization.

## Continuation rule

Start future sessions from this file plus the current Git HEAD/diff. Inspect deeper
historical documents only when the active task specifically requires them. Do not
reconstruct project history in the chat unless it is necessary to resolve a real
technical or doctrinal ambiguity.
