# SZONDI3 — PROJECT CHECKPOINT

**Checkpoint date:** 2026-08-25  
**Repository:** `danono2016/Szondi3`  
**Authoritative branch:** `main` after merge of this checkpoint  
**Current phase:** `P0 — Constitution + Sources`  
**P0 gate:** `P0_SOURCES_PASS`

## What is established

The Szondi3 foundation is complete enough to support development without adding more source infrastructure.

- Exactly 10 admitted DOCX sources, 8 admitted PDF visual arbiters and 48 admitted WebP stimuli are identity-locked by `config/evidence_lock.json`.
- The eight `SZ_*` sources are `SZONDI_PRIMARY`; Deri and Mélon remain separate post-Szondian layers.
- Primary wording is preserved without modernization or sanitization, including genetic/hereditary/genotropic, sexual, pathological and historically anachronistic formulations.
- Historical metadata about photographed persons is excluded from runtime scoring, doctrine, interpretation and reports.
- `scripts/canonical_access.py` provides deterministic source-near access; the full ten-source corpus regenerates byte-identically and is independently structure/provenance verified.
- Required DOCX/PDF visual arbitration has been performed for all eight paired sources. `SZ_TRIEBPATH_1` and `SZ_TRIEBPATH_2` have no admitted paired PDF; visual uncertainty that cannot be resolved from admitted evidence remains explicit rather than guessed.
- The 48-card series/position/factor mapping is now established directly from Lipót Szondi, *Lehrbuch der experimentellen Triebdiagnostik*, 3rd expanded edition (1972), p. 357, Tabelle 19, `Ursprung der Bilder des Testapparates`.
- All 48 filenames in `assets/stimuli/` agree with that primary-source mapping: 48/48, with zero discrepancies. See `docs/STIMULUS_MAPPING_MANIFEST.md`.

## P0 acceptance

The P0 gate defined in `docs/RESTART_ROADMAP.md` is satisfied:

1. documentary corpus present and identity-verifiable — PASS;
2. stimulus binaries present and identity-verifiable — PASS;
3. source layers unambiguously separated — PASS;
4. canonical access reproducible — PASS;
5. relevant source limitations explicitly recorded — PASS;
6. stimulus mapping required for administration established from primary evidence — PASS.

Therefore the explicit gate is:

> **`P0_SOURCES_PASS`**

This gate does not mean every historical source imperfection has been corrected. It means the admitted evidence boundary is stable, transparent and sufficient for the next deterministic layer.

## Development rule from here

Build forward from the Szondi3 foundation and admitted sources. Do not add validation layers merely because they are possible. Legacy projects are outside the Szondi3 development and validation path and must not be used as source truth, design authority, implementation template or gate.

When ambiguity appears, return to admitted source evidence. When a defect appears, repair the lowest affected Szondi3 layer.

## Next phase

After this gate is merged and CI is green, the next authorized phase is:

**P1 — DETERMINISTIC TEST ENGINE**

Start with the first roadmap item: **stimulus identity and series presentation**, using the now primary-source-verified mapping. Then proceed to the source-derived administration protocol. No clinical interpretation belongs in P1.
