# Szondi3 — current handoff

**Status:** CURRENT CONTINUITY HANDOFF  
**Scope:** software/clinical Szondi3 only. This handoff does not authorize work in `docs/manual/` or on the `manual` branch.  
**Authority rule:** live Git, exact source evidence, executable code and CI outrank this handoff whenever they disagree.

## 1. Repository and active line

- repository: `danono2016/Szondi3`
- active engineering line: `work/p2b-semantic-coverage-audit-001`
- continuity baseline HEAD: `17dc86d7fc068133cde67d16bba3f0c6cea15bb0`
- this continuity package: `work/documentary-continuity-002`
- executable P2B frontier: `IC_SZONDI_PRIMARY_000087`
- historical unused P2B holes: `000022`, `000035`, `000036`
- no authorization exists for `IC_SZONDI_PRIMARY_000088`
- PR #144 / `work/alpha1-executable-richness-001` is a frozen historical clinical-acceptance baseline, not the active development line
- never auto-merge this or the historical integration/baseline PRs

The continuity package is documentation-only and is based exactly on `17dc86d...`. No code, P1, P2A, P2B, reporting/AI runtime or `docs/manual/` change is part of this package.

## 2. Closed remediation that must not be reopened as if pending

### `000021` / `000081`

`IC_SZONDI_PRIMARY_000021` remains a historical identity but is projected `SUPERSEDED`. `IC_SZONDI_PRIMARY_000081` is the guarded executable replacement route for the corresponding IA-B 53 relation. The replacement preserves the distinction between base reaction and quantum level; ordinary Sch `+±` support is not permission to infer the same route under overpressure.

### P2A `000363`–`000366`

The following Lehrbuch doctrine records are materialized and CI-validated at P2A:

- `DR_SZ_LEHR_1972_000363` — exact `S -+!` semantic reserve;
- `DR_SZ_LEHR_1972_000364` — exact ordinary `P --` semantic reserve;
- `DR_SZ_LEHR_1972_000365` — exact ordinary `C 0-` core semantic reserve;
- `DR_SZ_LEHR_1972_000366` — guard that Szondi's `hypomanische Reaktion (C 0-)` is not the psychiatric picture of Hypomanie or Manie.

These records are doctrine reserve only until a separate P2B activation is explicitly authorized. Their materialization did not move the executable frontier beyond `000087`.

### `000013`

PR #165 repaired the executable trigger for `IC_SZONDI_PRIMARY_000013` without changing its identity or semantic text. The current route requires:

- `profile.vector.Sch.base_symbols == ("+", "±")`;
- `profile.factor.k.quantum_level == 0`;
- `profile.factor.p.quantum_level == 0`.

Focused regression coverage validates ordinary q0/q0 activation, overpressure exclusion, and simultaneous coactivation with the doctrinally distinct `IC_SZONDI_PRIMARY_000063`, `000075`, and `000081` routes.

The current baseline HEAD `17dc86d...` is the merge commit for this repair.

## 3. Current source/asset inventory

The real admitted inventory is:

- **10 DOCX textual sources**;
- **10 PDF visual-arbitration originals**;
- **48 WebP stimulus images**.

The initial binary admission contained 10 DOCX + 8 PDFs + 48 WebP. The authentic `Szondi Triebpathologie 1. Teil.pdf` and `Szondi Triebpathologie 2. Teil.pdf` were subsequently admitted as original visual-arbitration assets in commit `b9ea8589bb8e6aa364b54f15e90c51775cd44960`.

Therefore the eight-PDF inventory is historical only. Do not treat either Triebpathologie PDF as missing. `docs/SOURCE_ASSET_MANIFEST.md` is the authoritative current inventory; `docs/ASSET_ADMISSION_VERIFICATION.md` may continue to preserve the older initial-admission checkpoint without being rewritten to falsify history.

The eight `SZ_*` sources remain the primary Szondi doctrinal corpus. Deri and Melon remain post-Szondian layers and do not silently overwrite primary doctrine.

## 4. Epistemic and implementation invariants

The authority chain remains:

`PRIMARY EVIDENCE -> DOCTRINE -> EXECUTABLE P2B -> SOFTWARE FINDINGS -> INTERPRETIVE SUPPORT/RANKING -> AI WORDING -> CLINICIAN JUDGMENT`

Preserve these boundaries:

- P1 calculates deterministic test facts; interpretation must not recalculate them;
- base reaction, `Quantumspannung` and forced null are distinct;
- factor/vector/profile/series/foreground/complement/longitudinal meanings must not migrate silently across scope;
- P2A doctrine does not become executable merely because it exists;
- AI remains closed-world for Szondi interpretation and must not fill doctrinal gaps from general model knowledge;
- source uncertainty and source conflicts remain explicit rather than being stylistically harmonized;
- historical/pathognostic Szondian terminology is not automatically a modern DSM/ICD diagnosis;
- original PDF remains the visual documentary arbiter when OCR/DOCX conflicts on signs, formulas, tables, layout or typography.

## 5. Current engineering problem

The active line is still the P2B semantic-coverage audit. The purpose is to determine whether the executable layer carries enough source-authorized Szondian meaning to support clinically useful formulation without forcing downstream AI to invent bridges.

The structural pass through `000001`–`000087` is not permission to expand the frontier. Any future remediation must remain source-, scope- and trigger-proven. In particular, the newly materialized P2A `000363`–`000366` records do not by themselves authorize new P2B claims.

PR #144 demonstrated the clinical reporting baseline and exposed semantic-sufficiency limitations, but it is now historical/frozen. Do not resume development from that branch.

## 6. Immediate gate and next action

The **only** authorized work before another semantic/product slice is this documentary-continuity package:

- `docs/PROJECT_STATE.md` refreshed to the current active line and baseline HEAD;
- `docs/SOURCE_ASSET_MANIFEST.md` pinned to the real 10 DOCX + 10 PDF + 48 WebP inventory;
- this `docs/HANDOFF.md` added as the current continuity handoff.

The PR must remain docs-only. Its diff must contain no code, no P1/P2A/P2B changes and no `docs/manual/` changes. It is not considered closed until CI is green on the exact PR head and the diff has been explicitly checked for those boundaries.

Only after this package is approved and landed may work resume on the existing P2B semantic-coverage audit. Do not start another gap-filling slice in parallel and do not create `IC_SZONDI_PRIMARY_000088` without separate explicit authorization.

## 7. Restart checklist for the next operator

1. Verify `work/p2b-semantic-coverage-audit-001` and its live HEAD directly on GitHub; do not trust an old chat handoff.
2. Read `docs/PROJECT_STATE.md`, `docs/SOURCE_ASSET_MANIFEST.md`, this handoff, then the semantic audit/matrix.
3. Confirm the executable frontier is still `000087` before touching P2B.
4. Treat `000021/000081`, P2A `000363`–`000366`, and the `000013` q0/q0 trigger repair as closed current state unless live Git proves otherwise.
5. Preserve the 10 DOCX + 10 PDF + 48 WebP inventory; the two Triebpathologie PDFs are admitted.
6. Do not touch `docs/manual/` or the `manual` branch.
7. Require focused tests and green relevant CI on the exact SHA for every future executable remediation.

> **Correct-but-incomplete is preferable to rich-but-invented. Preserve source, scope, trigger boundaries and executable provenance.**
