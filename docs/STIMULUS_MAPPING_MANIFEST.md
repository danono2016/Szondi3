# SZONDI3 — STIMULUS MAPPING MANIFEST

**Status:** EVIDENCE INVENTORY / NOT YET RUNTIME  
**Classification:** `SOURCE_ASSET_TRANSFER` candidate mapping evidence

## Evidence origins

### Minimal mapping evidence
- repository: `danono2016/Szondi2`
- branch: `work/szondi-engine-master`
- path: `src/main/resources/szondi/cards.csv`
- Git blob: `66350d48f04076557b3a1bd404e494c30fadd484`

### Image binary evidence
- repository: `danono2016/szondi-`
- branch: `main`
- directory: `app/baseline-v2.0.0/resources/assets/images`
- immutable Git tree: `bdb6a6006e8f988efc6a0023ddc04bbbc339f251`
- observed file count: 48
- each WebP has an individual predecessor Git blob identity and byte size.

The older legacy `app/baseline-v2.0.0/resources/assets/cards.csv` is not admitted as runtime evidence because it historically carried photograph metadata beyond the permitted runtime boundary.

## Rule

This file records the minimal 48-stimulus mapping found in the audited predecessor and attaches it to the identified immutable image set. It is not copied as a runtime schema and is not yet authoritative for Szondi3 administration.

Before administration code is written, the mapping must be independently revalidated against authorized Szondi primary source material and the admitted image set. After revalidation, Szondi3 will create its own minimal runtime asset model from zero.

No historical metadata about photographed persons is admitted here.

## Observed predecessor mapping

| series | position | factor | image filename |
|---|---:|---|---|
| I | 1 | k | `I-01-k.webp` |
| I | 2 | s | `I-02-s.webp` |
| I | 3 | p | `I-03-p.webp` |
| I | 4 | d | `I-04-d.webp` |
| I | 5 | h | `I-05-h.webp` |
| I | 6 | e | `I-06-e.webp` |
| I | 7 | m | `I-07-m.webp` |
| I | 8 | hy | `I-08-hy.webp` |
| II | 1 | hy | `II-01-hy.webp` |
| II | 2 | m | `II-02-m.webp` |
| II | 3 | e | `II-03-e.webp` |
| II | 4 | h | `II-04-h.webp` |
| II | 5 | d | `II-05-d.webp` |
| II | 6 | p | `II-06-p.webp` |
| II | 7 | s | `II-07-s.webp` |
| II | 8 | k | `II-08-k.webp` |
| III | 1 | h | `III-01-h.webp` |
| III | 2 | e | `III-02-e.webp` |
| III | 3 | s | `III-03-s.webp` |
| III | 4 | m | `III-04-m.webp` |
| III | 5 | k | `III-05-k.webp` |
| III | 6 | d | `III-06-d.webp` |
| III | 7 | hy | `III-07-hy.webp` |
| III | 8 | p | `III-08-p.webp` |
| IV | 1 | p | `IV-01-p.webp` |
| IV | 2 | hy | `IV-02-hy.webp` |
| IV | 3 | d | `IV-03-d.webp` |
| IV | 4 | k | `IV-04-k.webp` |
| IV | 5 | m | `IV-05-m.webp` |
| IV | 6 | s | `IV-06-s.webp` |
| IV | 7 | e | `IV-07-e.webp` |
| IV | 8 | h | `IV-08-h.webp` |
| V | 1 | e | `V-01-e.webp` |
| V | 2 | d | `V-02-d.webp` |
| V | 3 | hy | `V-03-hy.webp` |
| V | 4 | p | `V-04-p.webp` |
| V | 5 | s | `V-05-s.webp` |
| V | 6 | k | `V-06-k.webp` |
| V | 7 | h | `V-07-h.webp` |
| V | 8 | m | `V-08-m.webp` |
| VI | 1 | m | `VI-01-m.webp` |
| VI | 2 | h | `VI-02-h.webp` |
| VI | 3 | k | `VI-03-k.webp` |
| VI | 4 | s | `VI-04-s.webp` |
| VI | 5 | p | `VI-05-p.webp` |
| VI | 6 | hy | `VI-06-hy.webp` |
| VI | 7 | d | `VI-07-d.webp` |
| VI | 8 | e | `VI-08-e.webp` |

## Structural observations to revalidate

The predecessor mapping has six series of eight positions and exactly one occurrence of each factor `h, s, e, hy, k, p, d, m` in every series. This is an observed predecessor invariant, not yet a Szondi3 implementation rule.

The discovered binary directory contains all 48 expected filenames and no missing terminal entry through `VI-08-e.webp`. The directory tree identity provides immutable predecessor-set provenance, but it does not validate the psychological factor mapping.

## Pending before runtime admission

1. Binary-copy the identified 48-image tree into Szondi3 without the legacy metadata CSV.
2. Verify copied binary identities against predecessor blobs/tree-derived inventory.
3. Verify series/position/factor mapping independently from primary source evidence.
4. Create a Szondi3-native runtime asset schema only after steps 1–3 pass.
5. Keep historical photograph-person metadata outside runtime permanently.
