# SZONDI3 — DEVELOPMENT GOVERNANCE

**Status:** NORMATIVE CHANGE-CONTROL POLICY

## Purpose

This document defines how Szondi3 changes without eroding its evidence base. It exists to prevent authority drift, hidden migration from predecessor code, undocumented assumptions and temporary shortcuts that later become permanent.

## 1. Branch and PR discipline

Authoritative changes are developed on a branch and reviewed through a pull request whenever the connector/tooling permits it. Direct writes to `main` are reserved for narrow bootstrap/recovery cases and must be documented afterwards.

Every material PR should state the affected layers, source/specification basis, invariants touched, tests/verification performed, generated-artifact impact, unresolved issues and rollback considerations.

A passing CI status is necessary when applicable but never sufficient for doctrinal correctness.

## 2. Change classes

Every material change belongs primarily to one class:

- `EVIDENCE_ADMISSION` — immutable source/stimulus evidence and identity records;
- `FOUNDATION_POLICY` — constitution, fidelity, provenance, gates, governance;
- `SOURCE_ACCESS` — canonical extraction/access and source-addressing infrastructure;
- `DETERMINISTIC_RULE` — administration/scoring/formal procedures;
- `DOCTRINE_REPRESENTATION` — source-near doctrine registry;
- `EXECUTABLE_INTERPRETATION` — triggerable claims derived from doctrine;
- `CLINICAL_GRAPH` — evidence representation/linking;
- `INTEGRATION` — synthesis/aggregation rules;
- `REPORTING` — clinician/client communication;
- `NON_AUTHORITATIVE_TOOLING` — developer convenience with no authority path.

A PR spanning unrelated classes should normally be split.

## 3. Specification-before-implementation

For source access, scoring, interpretation and integration, intended behavior is specified before or together with implementation. Existing code is not a specification.

A specification identifies inputs, outputs, invariants, error behavior, ambiguity behavior, source/provenance requirements and deterministic expectations.

## 4. Test-before-trust

Tests should derive from source examples, independently stated invariants and adversarial cases, not merely from current implementation outputs.

Regression tests are witnesses to accepted behavior, not doctrinal authority. When a test conflicts with primary evidence, investigate and correct the test or implementation rather than preserving behavior for compatibility alone.

## 5. No hidden migration

Copying, translating or mechanically porting Szondi2 executable logic is prohibited unless a future explicit policy changes this rule. Consulting Szondi2 after an independent Szondi3 derivation is allowed as `ORACLE_ONLY`.

If predecessor behavior materially influenced an investigation, record that fact. The new rule must still stand on source evidence without predecessor dependence.

## 6. Generated-artifact policy

Generated artifacts must live in paths clearly distinguishable from immutable inputs and hand-authored normative documents. They must state or encode their generator/version and inputs whenever they can affect later work.

Generated output must not be manually patched. Fix the source, specification or generator and regenerate.

A generated artifact may be committed for auditability or convenience only if its derivative status is unmistakable.

## 7. Review depth by risk

Review effort scales with epistemic and clinical risk.

Low-risk developer tooling can rely mainly on automated tests. Source access, scoring and schema changes require deterministic verification. Doctrine representation requires source review. Executable interpretation, integration and reports require adversarial testing and clinician review proportional to clinical consequence.

## 8. Stop-the-line conditions

Development pauses at the affected boundary when source identity cannot be verified, source material is missing or contradictory in a way that affects behavior, a meaningful source structure could be silently dropped, accepted deterministic results cannot be reproduced, provenance cannot be reconstructed, a claim lacks sufficient source support, a schema change cannot prove safe migration, or manual/source review reveals semantic error despite green CI.

The correct response is to record the blocker, not to invent a default.

## 9. Evidence for merge

A merge-worthy change should leave a future reviewer able to answer “why is this correct?” from the repository alone. Depending on layer, evidence may include source citation/anchor, immutable hash/blob identity, specification section, unit/invariant tests, deterministic output hash, structural inspection, clinician approval, adversarial protocol result or migration verification.

## 10. Reversal and rollback

Every merge is conceptually reversible at the implementation level. Evidence and decision history are append-only in spirit: reversal should add a correction/decision, not erase the fact that an earlier decision existed.

If an accepted rule is later found wrong, preserve enough history to identify which outputs may have been affected.

## 11. Naming and identity

Names should communicate layer and role. Stable identifiers are never recycled. Renaming a human-facing title must not change object identity. Do not encode disputed interpretation into identifiers when a neutral stable identity is sufficient.

## 12. Dependency rule

Keep the authoritative core dependency-light. Source verification, canonical access and deterministic scoring should avoid unnecessary frameworks and remote services. External services may assist downstream workflows but must not be required to reconstruct core evidence and deterministic results.

## 13. Security and privacy boundary

Do not place client-identifying clinical data in the repository. Test protocols used in source control must be synthetic, canonical published examples, or explicitly de-identified and authorized.

Historical metadata about photographed subjects remains excluded from runtime and clinical outputs as defined by the constitution.

## 14. Operational continuity

The repository is the durable record; chat/session transfer documents are not part of the development protocol.

Continuity is reconstructed from live branch state, Git history, source/provenance records, current specifications, executable code and CI. `docs/PROJECT_STATE.md` may summarize the mutable frontier, but it never outranks live repository evidence.

Do not create mandatory handoff packages, chat succession protocols, chat qualification rubrics or conversational checkpoints. If a durable rule matters, place it in the appropriate normative specification or policy. If a historical decision matters, preserve it in Git history or the relevant decision/provenance record.

## Final governance rule

> **No important assumption should need to be remembered; no important result should need to be believed without a reproducible evidence path.**
