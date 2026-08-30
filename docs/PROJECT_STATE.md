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
- completed optimization pass: `work/optimization-pass-001`
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
- redundant test boilerplate;
- audit-of-audit loops;
- giant chat handoffs and duplicated project history.

Do not introduce infrastructure for hypothetical future needs without a concrete
failure mode.

## Fall 40 policy

Fall 40 is, at most, an ordinary regression specimen. It is not an architectural,
doctrinal, or product-design target. No feature should be justified primarily by
making Fall 40 produce a preferred result.

New unit-level tests should prefer the smallest synthetic profile/series that
proves the invariant. Keep Fall 40 only where an explicit historical end-to-end
regression is useful.

## Development loop

For an ordinary source-grounded claim or implementation change:
1. establish the canonical basis or concrete technical need;
2. implement the smallest general change;
3. run focused regression coverage plus the normal CI gate;
4. stop when the invariant is demonstrated.

Do not add a second audit merely to confirm the first audit unless a concrete
contradiction or failure appears.

## Optimization pass — COMPLETE

Implemented on `work/optimization-pass-001`:
- shared fact indexing during P2B catalogue evaluation;
- cached repeated claim selection;
- shared per-profile factor maps during evidence-packet construction;
- cached loading of the packaged doctrine registry while keeping custom test
  registries uncached;
- reusable synthesis-validation indexes for repeated proposition checks;
- preview inspection reuses one validation context instead of rebuilding it per
  proposition;
- default continuation checkpoint reduced to this file;
- Fall 40 explicitly demoted to an ordinary regression specimen;
- test policy favors minimal fixtures and avoids duplicating the same invariant
  across layers that cannot fail independently.

The optimization pass is closed. Do not reopen general performance/process audits
without a concrete runtime, maintainability, or correctness symptom. Future work
returns to clinically useful Szondi development.

## Continuation rule

Start future sessions from this file plus the current Git HEAD/diff. Inspect deeper
historical documents only when the active task specifically requires them. Do not
reconstruct project history in the chat unless it is necessary to resolve a real
technical or doctrinal ambiguity.
