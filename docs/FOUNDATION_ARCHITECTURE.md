# SZONDI3 — FOUNDATION ARCHITECTURE

**Status:** NORMATIVE FOUNDATION CONTRACT  
**Applies to:** every project phase, implementation, dataset, report and future migration

## Purpose

Szondi3 must remain trustworthy under major changes: new developers, new chats, new implementation languages, changed interpretation strategies, source corrections, failed experiments, partial rewrites, CI failures, and future disagreement about doctrine or architecture.

The project therefore treats recoverability, provenance and layer separation as first-class requirements rather than documentation afterthoughts.

## 1. Non-negotiable invariants

The following invariants are stronger than any implementation choice.

1. **Original evidence remains immutable.** Admitted DOCX, PDF and stimulus binaries are never edited in place.
2. **Source authority is directional.** Downstream software may depend on upstream evidence; downstream convenience may never redefine upstream truth.
3. **Doctrine and executability are different objects.** A source statement may exist without an executable trigger. An executable rule must point back to doctrine/source evidence.
4. **Generated artifacts never become authority by repetition.** Hashes, canonical text, indexes, graphs, reports and caches remain derivatives with explicit generators and provenance.
5. **No silent omission.** Any unsupported or unhandled source structure that might carry meaning must be surfaced as an explicit warning, unsupported case or gate failure.
6. **No silent certainty inflation.** Each layer may preserve or reduce certainty; it may not increase it beyond evidence and source authority.
7. **Ambiguity is data.** Unresolvable source ambiguity, competing interpretations and contradictory passages are preserved rather than narratively smoothed.
8. **Historical photograph metadata remains outside runtime.** Runtime uses only card identity, series/position, factor and image identity/path.
9. **Predecessor software is never authority.** Szondi2 can be an oracle after independent derivation, never the reason a new rule is true.
10. **Every material result is reproducible or explicitly non-reproducible.** There is no category called “probably reproducible.”

A change violating any invariant requires an explicit constitutional amendment, not an ordinary implementation PR.

## 2. Layer model

The project is divided into irreversible epistemic boundaries:

`Immutable Sources -> Canonical Access -> Deterministic Test Facts -> Primary Doctrine Registry -> Executable Interpretation -> Clinical Evidence Graph -> Integration -> Reports`

Each boundary has a one-way dependency rule. A later layer may reference an earlier layer. An earlier layer must not import conclusions from a later layer.

### Immutable Sources
Original admitted binaries plus their identity/provenance records.

### Canonical Access
Deterministic, addressable derivatives whose sole job is faithful machine access. Canonical access is not doctrine and does not repair source content silently.

### Deterministic Test Facts
Administration, selections, counts, reactions, vectors, profiles, series and other source-authorized formal results.

### Primary Doctrine Registry
Source-near representation of what Szondi and separately identified post-Szondian authors state, including ambiguity, historical terminology and conditions.

### Executable Interpretation
Formal conditions under which doctrine may be activated from protocol evidence. This layer can say “not supported” or “unresolved”; it cannot rewrite doctrine.

### Clinical Evidence Graph
Traceable protocol facts, activated claims, contradictions, series relationships and provenance.

### Integration
Explicit, testable synthesis rules. No free-form reconciliation can manufacture convergence.

### Reports
Communication products only. Reports never become evidence for upstream layers.

## 3. Immutable core vs replaceable shell

The project intentionally separates what must survive a rewrite from what may be replaced.

### Immutable or append-only core
- admitted source binaries and their hashes/blob identities;
- constitutional/fidelity/foundation policies;
- provenance records;
- accepted source-derived specifications;
- clinician-approved doctrinal entries and their source anchors;
- gate decisions and decision log entries.

### Replaceable implementation shell
- programming language;
- framework;
- database technology;
- UI;
- serialization format, if migrated losslessly;
- indexing/search implementation;
- narrative generation model;
- build tooling.

A major technical rewrite should therefore replace the shell while leaving the epistemic core independently verifiable.

## 4. Provenance contract

Every derived object that can affect interpretation must be able to answer:

- What source or protocol evidence produced me?
- Which exact version of that evidence?
- Which rule/specification transformed it?
- Which implementation version executed the rule?
- Which upstream objects did I depend on?
- What uncertainty or unresolved condition was present?

Identifiers must be stable within their layer. Human-readable labels may change; identity must not silently drift.

## 5. Determinism contract

For deterministic layers, identical admitted inputs plus identical specification/implementation versions must produce byte-identical or semantically identical declared outputs.

Every deterministic pipeline must eventually provide:

- input identity verification;
- deterministic ordering;
- stable normalization rules;
- explicit encoding/newline rules when bytes matter;
- content hash of outputs;
- regeneration command;
- independent verification command;
- failure on unexpected source structure.

If a pipeline contains an intentionally non-deterministic component, that component must be downstream, clearly labeled and unable to alter upstream evidence.

## 6. Fail-closed rules

The system must stop rather than guess when any of the following occurs:

- admitted source hash mismatch;
- missing source asset;
- unknown source version;
- unsupported OOXML structure with possible textual or symbolic meaning;
- provenance break;
- executable claim without doctrine linkage;
- report statement without evidence path;
- incompatible schema migration without explicit adapter/verification;
- source disagreement requiring human arbitration;
- confidence greater than the upstream ceiling.

“Best effort” is acceptable only for explicitly non-authoritative exploratory tooling and must never silently feed production interpretation.

## 7. Schema evolution

Every durable schema has a version. Breaking changes require an explicit migration path and validation proving that old accepted records can be interpreted or intentionally retired.

No field may be repurposed to mean something different. Deprecation is preferable to semantic mutation.

Source identifiers, doctrine identifiers and clinical evidence identifiers must never be recycled.

## 8. Change containment

A defect should be repaired in the lowest layer where it originates.

Examples:
- OCR access error -> canonical access layer;
- reaction calculation error -> deterministic engine;
- misrepresented Szondi statement -> doctrine registry;
- overly permissive activation -> executable interpretation;
- poor synthesis -> integration;
- harsh wording for client -> client-report transformation.

A downstream problem is not permission to mutate upstream doctrine.

## 9. Independent witnesses

Critical claims should have more than one kind of verification when practical:

- source binary hash + Git blob identity;
- deterministic regeneration + output hash;
- source example + invariant test;
- automated validation + clinician review for doctrinal/clinical layers;
- primary-source derivation + predecessor comparison only after derivation.

Agreement between independent witnesses raises confidence. Disagreement triggers investigation; no witness wins automatically merely because it is older.

## 10. Decision discipline

Architectural or doctrinal decisions that would be expensive to rediscover must be written down with:

- context;
- decision;
- alternatives rejected;
- evidence;
- consequences;
- reversal conditions.

A future chat or developer should be able to reconstruct why the project is shaped this way without relying on conversational memory.

## 11. Continuity and disaster recovery

The repository, not a chat transcript, is the durable project memory.

At every stable checkpoint the repository must contain enough information for a competent new collaborator to determine:

- what is authoritative;
- what has passed verification;
- what is provisional;
- what is forbidden;
- what is currently being worked on;
- the next safe action;
- how to reproduce the last accepted result.

No critical project state may exist only in a chat.

## 12. Gate principle

A phase gate is evidence, not optimism. A gate passes only when its documented acceptance criteria are met and the result is recorded. Partially completed work remains explicitly partial.

Later phases may prototype experimentally, but no prototype may be used as authoritative evidence for an earlier unfinished gate.

## 13. Human authority boundary

Software can preserve, calculate, link, compare and enforce formal conditions. It must not impersonate source authority or clinician judgment.

Human review is mandatory where the source is visually ambiguous, doctrinally conflicting, clinically consequential, or formally underdetermined.

The software must make such review easier by preserving the exact evidence path rather than hiding it behind narrative fluency.

## Final foundation rule

> **Build so that code can be replaced, models can be replaced, chats can disappear and interpretations can be corrected without losing the evidence, provenance, doctrine or reasons that made the project trustworthy.**
