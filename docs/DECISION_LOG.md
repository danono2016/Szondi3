# SZONDI3 — DECISION LOG

**Status:** APPEND-ONLY PROJECT MEMORY

This log records expensive-to-rediscover decisions. It does not replace source evidence or normative policies. When a decision is reversed, add a new entry referencing the old one rather than deleting history.

## D-001 — Total software restart

**Decision:** Szondi3 does not inherit executable Szondi2 implementation. Source/stimulus evidence may be admitted with identity verification; predecessor behavior is `ORACLE_ONLY` after independent derivation.

**Reason:** prevent inherited assumptions, doctrinal omissions and competing authority from becoming invisible implementation facts.

**Reversal condition:** only an explicit constitutional amendment with a stronger provenance model could alter this.

## D-002 — Doctrine != executable interpretation

**Decision:** Primary Doctrine Registry and Executable Interpretation Layer are structurally separate.

**Reason:** preserve what Szondi says even when software cannot safely determine when/how to activate it.

**Consequence:** doctrine entries may be non-executable; executable claims must reference doctrine.

## D-003 — Original sources outrank canonical derivatives

**Decision:** canonical text is an access/provenance derivative, never higher authority than original DOCX/PDF evidence.

**Reason:** extraction can lose visual/layout information and OCR can be wrong.

## D-004 — Canonical extraction restarted independently

**Decision:** Szondi2 canonical TXT and exporter are not imported as authority. Szondi3 writes a new extractor from a new specification, then compares outputs to predecessor witnesses only after independent generation.

**Reason:** comparison before independent generation would contaminate the restart with inherited behavior.

## D-005 — Structural inspection before extractor

**Decision:** inspect actual OOXML structure of all admitted DOCX files before finalizing extractor behavior.

**Evidence:** workflow run `32763754908`, artifact digest `sha256:144715513a9d6421b7bac5fc15d51705f03dd4b5b1742fda415cfd7c4f556370`.

**Finding:** corpus contains substantial tables, notes, fields, drawings and large numbers of header/footer story parts; paragraph-only extraction is unsafe.

## D-006 — Fail closed on possibly meaningful unknown structure

**Decision:** unsupported source structures that may carry textual/symbolic meaning cause explicit warning/failure rather than silent omission.

**Reason:** source fidelity is more important than completing extraction with hidden loss.

## D-007 — Stimulus binary identity separated from psychological mapping authority

**Decision:** the 48 image binaries are admitted/verified independently from series/position/factor mapping. Legacy mapping is evidence pending primary-source revalidation.

**Reason:** byte identity proves which image is present, not what psychological factor it represents.

## D-008 — Photograph-person metadata excluded from runtime

**Decision:** historical information about photographed persons is Help/history-only and cannot enter scoring, doctrine, interpretation, graph, integration or reports.

**Reason:** it is not needed for administration/scoring and creates an unacceptable contamination/privacy boundary.

## D-009 — Repository is durable project memory

**Decision:** critical state, gate decisions, rationale and next safe action must be committed; chat history is non-authoritative and disposable.

**Reason:** long conversations can terminate, models/tools can change, and future collaborators need recoverable state.

## D-010 — Immutable epistemic core, replaceable technical shell

**Decision:** evidence, provenance, accepted specifications, doctrine identity and gate history must survive language/framework/database/UI rewrites.

**Reason:** major technical change should not require re-establishing the truth basis of the project.

## D-011 — Read-only CI by default

**Decision:** CI verifies but does not write authoritative state back to the repository.

**Reason:** generated state must not masquerade as independently verified truth; repository mutations require explicit reviewed changes.

## D-012 — Machine-enforced evidence lock

**Decision:** admitted source/stimulus identity and required foundation documents are checked by `scripts/verify_foundation.py` against `config/evidence_lock.json`.

**Reason:** constitutional intent alone cannot prevent accidental binary mutation or source-set drift.

**Scope:** identity/structure only; it does not validate doctrine, OCR correctness or stimulus mapping.

## D-013 — P1 closes source-underdetermined procedures by explicit boundary, not invention

**Decision:** `P1_DETERMINISTIC_ENGINE_PASS` does not require manufacturing a unique algorithm where admitted evidence does not determine one. A P1 item may be closed as `RESOLVED_FAIL_CLOSED` or `RESOLVED_OUTSIDE_P1` when that status is source-justified, durably recorded and reflected in executable refusal behavior where applicable.

**Evidence:** `docs/P1_RESOLUTION_SWEEP.md`, `docs/P1_DETERMINISTIC_ENGINE_VERIFICATION.md`, PR #37, merge SHA `5e4d02782d7165dbcea7828ca055a2415b72d262`, and green post-merge workflow runs `32939562736`, `32939562733`, `32939562754`.

**Consequences:**

- authentic but underdetermined `kp/hs` broader abbreviation is not generalized into an invented selector;
- tied abbreviated extrema and non-unique complete-formula partitions fail closed where no source rule resolves them;
- mixed Wurzelfaktor direction receives no invented majority Unterklasse sign;
- incomplete Quantenverrechnung is not completed by inference;
- exact Inkonstanzmethode is reopenable on admission of the identified Böszörményi source rather than reconstructed from tertiary/AI formulas;
- qualitative/clinical procedures route downstream instead of becoming deterministic P1 code.

**Reversal/reopening condition:** newly admitted stronger evidence may reopen the affected boundary through normal governance. Such reopening changes only the lowest affected layer and does not authorize rewriting primary doctrine.

## D-014 — `kp/hs` resolved as outer-line abbreviated projection

**Decision:** the conceptual and executable `kp/hs` problem is closed. The extended abbreviated Triebformel is represented as:

`extended abbreviated formula = symptomatic line / root line`

with the submanifest/sublatent middle line of the complete Triebformel omitted.

For Fall 18, the already source-constrained complete partition is `kp / mdhye / hs`; its extended abbreviated projection is therefore `kp/hs`. `p` and `h` are not appended to `k/s` by a separate neighbour, distance or fixed-cardinality selector. They occur because `p` already belongs to the symptomatic line and `h` already belongs to the root line.

**Epistemic classification:**

- `SOURCE-ESTABLISHED`: Fall 18 prints both `k/s` and `kp/hs` under `Abgekürzte Triebformel`; Triebformel is symptom/root; the complete formula has symptomatic, submanifest/sublatent and root lines; same-line membership follows the admitted TspG rules.
- `IMPLEMENTATION-INFERRED, strongly source-constrained`: the universal executable representation of the extended abbreviation as the projection of the two already-constituted outer lines. This is a structural projection, not a newly invented factor-selection threshold.
- `UNRESOLVED only locally`: if the complete-formula partition itself is non-unique under admitted source rules, that particular extended abbreviation fails closed. Simple-abbreviation extrema ties retain their separate fail-closed policy.

**Cardinality rule:** no artificial `2/2` shape is imposed. The numerator and denominator contain however many factors legitimately belong to the symptomatic and root lines respectively.

**Relationship to D-013:** this decision supersedes only D-013's first consequence concerning the broader `kp/hs` selector. D-013 remains fully in force for ties, non-unique partitions and the other source-underdetermined procedures.

**Durable implementation:** `szondi3/abbreviated_formula.py` derives the extended abbreviation from `unique_formula_partition`; `tests/test_abbreviated_formula.py` includes Fall 18 `kp/hs` and a variable-cardinality outer-line projection witness.
