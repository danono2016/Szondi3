# SZONDI3 — VALIDATION, RECOVERY & DISASTER RULES

**Status:** NORMATIVE RELIABILITY POLICY

## Purpose

This document defines how Szondi3 proves that accepted results are still valid after failures, rewrites, source corrections, tool changes or loss of conversational context.

## 1. Three independent questions

Every important artifact is evaluated separately for:

1. **Identity** — is this exactly the expected input/artifact?
2. **Reproducibility** — can it be regenerated from declared inputs by the declared process?
3. **Semantic validity** — does it represent the source/rule correctly?

Passing one does not imply the others. A byte-identical canonical text can still encode an OCR error. A semantically correct rule can still be implemented non-deterministically. A passing test can still test the wrong doctrine.

## 2. Verification pyramid

Use multiple levels of evidence:

- binary identity checks;
- structural/package validation;
- deterministic unit and invariant tests;
- source-example tests;
- cross-implementation or independent-witness comparison where useful;
- clinician/source review;
- end-to-end golden protocols;
- adversarial cases designed to provoke unsupported certainty.

Critical clinical output should never rest solely on one verification mode.

## 3. Gate records

Each phase gate has one of four states:

- `NOT_STARTED`
- `IN_PROGRESS`
- `BLOCKED`
- `PASS`

There is no implicit pass. A gate record must state acceptance evidence and known residual limitations.

A gate may be reopened if new evidence invalidates an assumption. Reopening is not failure of governance; hiding invalidation is.

## 4. P0 acceptance requirements

`P0_SOURCES_PASS` requires all of the following:

- all authorized DOCX/PDF/stimulus binaries present;
- identity verification against recorded hashes/blob witnesses;
- doctrinal layers separated;
- stimulus metadata boundary enforced;
- canonical access specification accepted;
- source structures inspected before canonical extraction;
- canonical extractor implemented independently;
- deterministic regeneration verified;
- newly generated canonical outputs hashed and inventoried;
- comparison with Szondi2 witnesses performed only after independent generation;
- differences investigated and recorded;
- visual arbitration limitations documented, including absent PDFs for Triebpathologie.

Until all are true, P0 remains `IN_PROGRESS` even if several sub-gates have passed.

## 5. Recovery checkpoints

At every significant accepted milestone, record:

- repository and branch/commit;
- current phase/gate state;
- last verified outputs and hashes if applicable;
- open blockers;
- active work branch/PR if any;
- next safe action;
- commands or workflow needed to reproduce the last accepted result;
- files that a new collaborator must read first.

The checkpoint is human-readable and must not be generated in a way that implies independent verification unless it has actually been reviewed.

## 6. Disaster scenarios

### Chat disappears
Recovery source: repository checkpoint + handoff package + normative docs. No critical fact should require the lost transcript.

### Implementation is corrupted or deleted
Rebuild from source specifications and tests. Do not recover authority by copying Szondi2.

### Generated canonical files are lost
Regenerate from admitted DOCX with the accepted extractor and verify hashes.

### Generated canonical files disagree after regeneration
Stop. Verify source hashes, tool/runtime versions, deterministic ordering and extractor changes. Do not overwrite accepted witnesses until cause is understood.

### Source binary changes unexpectedly
Treat as a new evidence admission event. Do not silently replace the admitted source.

### Primary source correction is discovered
Record the correction, identify downstream objects depending on the affected anchor, invalidate/review them systematically, and regenerate/reapprove as needed.

### Schema migration fails
Keep the previous readable version, restore from Git, fix the migration, and rerun verification. Never manually edit authoritative records to “make the migration pass.”

### A clinician rejects an executable interpretation
Investigate the lowest relevant layer: doctrine representation, trigger formalization, evidence mapping or integration. Preserve the original source doctrine while correcting downstream logic.

## 7. Blast-radius accounting

Every accepted correction that changes meaning should identify potentially affected downstream artifacts. At minimum ask:

- which source anchors changed?
- which deterministic rules depend on them?
- which doctrine entries reference them?
- which executable claims depend on those entries?
- which golden protocols/reports exercise those claims?

This dependency tracing becomes increasingly automated as later layers mature.

## 8. CI role

CI is a witness and enforcement mechanism, not an authority. CI should be read-only unless a future explicit decision permits otherwise.

CI may:

- verify input identities;
- run structural inspections;
- regenerate temporary derivatives;
- compare expected hashes;
- run tests;
- upload inspection/report artifacts.

CI should not silently commit generated truth back to the repository.

## 9. Reproducible environment

Critical deterministic tooling should pin or declare the minimum environment required for reproducibility. Prefer standard formats, standard libraries and dependency-light implementations at the source-access/deterministic core.

When third-party dependencies become necessary, lock their versions and record why they are required.

## 10. Golden corpus policy

Golden protocols are added only with explicit provenance and expected-output justification. They must cover ordinary cases, boundary cases and cases designed to preserve ambiguity.

A golden output is not immutable doctrine. It is an accepted regression witness and may be corrected when better evidence appears, with the correction documented.

## 11. Negative validation

The system must test what it refuses to say, not only what it says. Later phases require cases proving that:

- absent evidence does not become positive evidence;
- `UNRESOLVED` is not converted to assertion;
- single-profile facts do not become series conclusions without authorization;
- post-Szondian claims do not masquerade as Szondi-primary doctrine;
- client-friendly language does not mutate clinician doctrine;
- photograph metadata cannot leak into interpretation.

## 12. Release recovery rule

A release is acceptable only if a clean checkout can reconstruct all deterministic authoritative derivatives using documented commands/workflows and can prove the release against its gate evidence.

## Final reliability rule

> **A trustworthy system is not one that never breaks; it is one that can prove what broke, contain the blast radius, reconstruct the last valid state and move forward without inventing missing truth.**
