# SZONDI3 — PROJECT CONSTITUTION

**Status:** AUTHORITATIVE  
**Repository:** `danono2016/Szondi3`

## 1. Purpose
Szondi3 is the authoritative clean restart of the Szondi software project. Its purpose is to preserve, formalize and operationalize Szondian doctrine without allowing software architecture, contemporary taste, or later interpretation to rewrite the primary sources.

## 2. Source-of-truth hierarchy
1. Original Szondi primary sources are the highest doctrinal authority.
2. Verified canonical text derivatives exist only for access and provenance; they do not outrank the originals.
3. Original PDF page/image is the visual arbiter for OCR-sensitive signs, formulas, tables, layout and typography when available.
4. Deri, Mélon and other post-Szondian authors are separate doctrinal layers. They may supplement but never silently overwrite Szondi-primary doctrine.
5. Contemporary psychological/scientific context is always a separate labeled layer.
6. Legacy software is never a doctrinal authority. It may serve only as technical evidence or a behavioral oracle after review.

## 3. Fundamental architectural separation
The project MUST preserve two distinct objects:

### A. Primary Doctrine Registry
Represents what the source says. It preserves doctrinal content before asking whether that content is executable by software.

### B. Executable Interpretation Layer
Represents what the software is allowed to infer or activate from protocol evidence. Executable claims are derived from the Doctrine Registry and must reference it. They may constrain application but may not rewrite the underlying doctrine.

Canonical direction:

`Primary Sources -> Primary Doctrine Registry -> Executable Interpretation Layer -> Clinical Evidence/Graph -> Integration -> Reports`

No downstream layer may silently modify an upstream layer.

## 4. Doctrinal fidelity
The project follows `docs/DOCTRINAL_FIDELITY_POLICY.md`.

Szondi-primary material is preserved even when anachronistic, controversial, politically incorrect, scientifically disputed today, pathologizing by contemporary standards, or uncomfortable in modern clinical language. This includes genetics, heredity, genotropism, familial fate, transgenerational formulations, sexuality, inversion, homosexuality, bisexuality, masculinity/femininity, sadism, masochism, perversion, criminality, psychopathy, psychosis and all other terms actually used by Szondi.

## 5. Evidence discipline
The project distinguishes source statement, doctrinal representation, executable condition, protocol observation, Szondian interpolation/inference, integrated clinical hypothesis and contemporary contextualization. These categories must never be silently collapsed.

No software layer may increase certainty beyond the ceiling authorized by source provenance and available evidence.

## 6. Series and configuration principle
A single profile must not be treated as the whole person when the source requires series or broader configuration. Factor, vector, profile, series, complement and external context are distinct interpretive levels.

If Szondi provides competing meanings and the discriminating condition is unavailable, the engine preserves the ambiguity rather than choosing by plausibility or narrative fluency.

## 7. Reports
### Clinician report
Must preserve full Szondian doctrinal richness, including original terminology and historically dated formulations when supported by source and evidence. Context, provenance and uncertainty may be added; doctrine may not be sanitized.

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

Generated canonical TXT from Szondi2 is not transferred as Szondi3 authority; it is a comparison witness only. Szondi3 rebuilds its canonical extraction pipeline independently from admitted original DOCX sources, following `docs/SOURCE_ASSET_MANIFEST.md`.

## 10. Complexity rule
Complexity is introduced only when demanded by the source or by a demonstrated software requirement. The project must not build theoretical machinery in advance merely because it might be useful later. Simplification may never erase substantive Szondian doctrine.

## 11. CI and generated state
CI is initially read-only: compile, test and verify. Automated write-back to the repository is forbidden unless a later explicit architectural decision demonstrates a clear benefit. Generated state must not masquerade as independently verified truth.

## 12. Restart criterion
Szondi3 exists to make the separation `doctrine != executable formalization` structural and durable. Future errors in executable interpretation should be repairable without another project restart because the primary doctrine remains intact and independently addressable.

## Final rule
> **Preserve Szondi first. Formalize second. Integrate third. Communicate last. Never allow a downstream convenience to rewrite an upstream source.**
