# SZONDI3 — PROJECT CONSTITUTION

**Status:** AUTHORITATIVE  
**Repository:** `danono2016/Szondi3`

## 1. Purpose
Szondi3 is the authoritative clean restart of the Szondi software project. Its purpose is to preserve, formalize and operationalize Szondian doctrine without allowing software architecture, contemporary taste, or later interpretation to rewrite the primary sources.

The durability rules in `docs/FOUNDATION_ARCHITECTURE.md`, change-control rules in `docs/DEVELOPMENT_GOVERNANCE.md`, validation/recovery rules in `docs/VALIDATION_AND_RECOVERY.md`, and doctrinal/reporting rules in `docs/DOCTRINAL_FIDELITY_POLICY.md` are normative companions to this constitution. Ordinary implementation changes may not override them.

## 2. Source-of-truth hierarchy
1. Original Szondi primary sources are the highest doctrinal authority.
2. Verified canonical text derivatives exist only for access and provenance; they do not outrank the originals.
3. Original PDF page/image is the visual arbiter for OCR-sensitive signs, formulas, tables, layout and typography when available.
4. Deri, Mélon and other post-Szondian authors are separate doctrinal layers. They may supplement but never silently overwrite Szondi-primary doctrine.
5. Contemporary psychological/scientific context is always a separate labeled layer.
6. Legacy software is never a doctrinal authority. It may serve only as technical evidence or a behavioral oracle after review.

## 3. Fundamental architectural separation
The project MUST preserve distinct upstream and downstream objects rather than collapsing source access, formal scoring, doctrine and interpretation into one knowledge layer.

### A. Canonical Access
Represents deterministic, addressable access to admitted sources. It is a derivative for access/provenance and does not become doctrine merely because it is machine-readable.

### B. Deterministic Test Facts
Represents source-authorized administration, scoring, profile, vector, series and other formal results. These are protocol facts, not clinical interpretation.

### C. Primary Doctrine Registry
Represents what the source says. It preserves doctrinal content before asking whether that content is executable by software.

### D. Executable Interpretation Layer
Represents what the software is allowed to infer or activate from protocol evidence. Executable claims are derived from the Doctrine Registry and must reference it. They may constrain application but may not rewrite the underlying doctrine.

Canonical direction:

`Primary Sources -> Canonical Access -> Deterministic Test Facts -> Primary Doctrine Registry -> Executable Interpretation Layer -> Clinical Evidence/Graph -> Integration -> Reports`

No downstream layer may silently modify an upstream layer.

## 4. Doctrinal fidelity
The project follows `docs/DOCTRINAL_FIDELITY_POLICY.md`.

Szondi-primary material is preserved even when anachronistic, controversial, politically incorrect, scientifically disputed today, pathologizing by contemporary standards, or uncomfortable in modern clinical language. This includes genetics, heredity, genotropism, familial fate, transgenerational formulations, sexuality, inversion, homosexuality, bisexuality, masculinity/femininity, sadism, masochism, perversion, criminality, psychopathy, psychosis and all other terms actually used by Szondi.

### Permanent clinician-report fidelity rule

The clinician-facing report MUST speak from inside Szondi's conceptual system rather than translating it into a generic contemporary psychological voice. Fidelity includes not only concepts and diagnoses but also terminology, degree of assertion and characteristic rhetorical force.

When supported by source and executable evidence, Szondi's direct, categorical, dramatic, dense and baroque clinical language must not be softened, euphemized, politically corrected, morally sanitized or automatically replaced by contemporary terminology merely because present-day usage would prefer a milder formulation.

The admitted primary corpus is therefore both doctrinal authority and stylistic reference for the clinician-facing Szondian report.

This stylistic freedom never authorizes doctrinal invention or certainty inflation. The source remains the ceiling. Anti-inferences prevent unsupported conclusions; they MUST NOT function as censorship of an explicit Szondian meaning.

> **Constrain AI on doctrinal truth; do not domesticate Szondi's language.**

Any contemporary critique, scientific contextualization or softened communication belongs to a separate labeled downstream layer and may never rewrite the clinician-facing Szondian interpretation.

## 5. Evidence discipline
The project distinguishes source statement, canonical-access derivative, deterministic protocol fact, doctrinal representation, executable condition, protocol observation, Szondian interpolation/inference, integrated clinical hypothesis and contemporary contextualization. These categories must never be silently collapsed.

No software layer may increase certainty beyond the ceiling authorized by source provenance and available evidence.

Unknown or unsupported source structures with possible meaning must fail closed or be explicitly marked unresolved; silent omission is forbidden.

## 6. Series and configuration principle
A single profile must not be treated as the whole person when the source requires series or broader configuration. Factor, vector, profile, series, complement and external context are distinct interpretive levels.

If Szondi provides competing meanings and the discriminating condition is unavailable, the engine preserves the ambiguity rather than choosing by plausibility or narrative fluency.

## 7. Reports
### Clinician report
Must preserve full Szondian doctrinal, diagnostic, terminological and stylistic richness, including original terminology and historically dated formulations when supported by source and evidence. Its target voice is recognizably Szondian rather than generic contemporary-clinical: directness, conceptual density, categorical contrasts and baroque rhetorical force are preserved where faithful Romanian expression permits. Context, provenance and uncertainty may be added for evidential precision; doctrine may not be sanitized.

AI synthesis may integrate and compose authorized findings, but it has no authority to modernize, euphemize or politically correct them. Its freedom is compositional and stylistic inside the source-authorized envelope, not doctrinal.

### Client report
Is a separate downstream communication transformation. It may be milder and phenomenological, but it must never alter the underlying doctrine or clinician-facing interpretation.

## 8. Photograph metadata boundary
Runtime administration may contain only the information necessary to present and score the 48 stimuli: stable card identity, series/position, factor and image.

Historical metadata about photographed persons is excluded from scoring, Doctrine Registry, executable claims, Clinical Graph, integration and reports. It may appear only in isolated Help/historical documentation.

## 9. Migration from Szondi2
Szondi2 is predecessor and audit trail, not a parent authority. Szondi3 uses a total software restart: no executable code is migrated into active use.

Every predecessor component or actually admitted file is classified as one of:
- `SOURCE_ASSET_TRANSFER` — documentary source or stimulus asset copied with identity verification;
- `CONSTITUTIONAL_TRANSFER` — project rule intentionally retained after explicit review;
- `ORACLE_ONLY` — predecessor material usable only for comparison;
- `ARCHIVE_ONLY` — retained solely in Szondi2;
- `RE_DERIVE_FROM_SOURCE` — behavior/concept known from Szondi2 but reconstructed independently from authorized sources.

`TRANSFER_AS_IS` is not an allowed category for executable code. Every actual import is recorded in `docs/MIGRATION_MANIFEST.md`. No bulk copy of Szondi2 is allowed.

Generated canonical TXT from Szondi2 is not transferred as Szondi3 authority; it is a comparison witness only. Szondi3 rebuilds its canonical extraction pipeline independently from admitted original DOCX sources, following `docs/SOURCE_ASSET_MANIFEST.md` and `docs/CANONICAL_ACCESS_SPEC.md`.

## 10. Complexity rule
Complexity is introduced only when demanded by the source or by a demonstrated software requirement. The project must not build theoretical machinery in advance merely because it might be useful later. Simplification may never erase substantive Szondian doctrine.

## 11. CI and generated state
CI is initially read-only: compile, test and verify. Automated write-back to the repository is forbidden unless a later explicit architectural decision demonstrates a clear benefit. Generated state must not masquerade as independently verified truth.

Critical deterministic outputs must be reproducible from declared inputs and generators. A passing CI job is a verification witness, not doctrinal authority.

## 12. Continuity and recovery
The repository, not conversational memory or transfer documents, is the durable project record. A collaborator reconstructs current state from live branch/PR state, Git history, immutable evidence and provenance, current specifications, executable code, tests and CI. `docs/PROJECT_STATE.md` may provide a concise mutable summary but never outranks those live sources.

Source identity failures, provenance breaks, unsupported meaningful structures, certainty inflation, and systematic sanitization of source-authorized clinician-report language are stop-the-line conditions as specified by the normative project policies.

## 13. Restart criterion
Szondi3 exists to make the separation `doctrine != executable formalization` structural and durable. Future errors in executable interpretation should be repairable without another project restart because the primary doctrine remains intact and independently addressable.

A future technical rewrite should replace the implementation shell without destroying immutable evidence, provenance, accepted specifications, doctrine identity or gate history.

## Final rule
> **Preserve Szondi first. Formalize second. Integrate third. Communicate last. Never allow a downstream convenience or contemporary taste to rewrite an upstream source. In the clinician report, constrain AI on doctrinal truth; do not domesticate Szondi's language.**
