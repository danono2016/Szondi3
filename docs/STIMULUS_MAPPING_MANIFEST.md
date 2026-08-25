# SZONDI3 — STIMULUS MAPPING MANIFEST

**Status:** `PRIMARY_SOURCE_VERIFIED`  
**Authority:** admitted Szondi primary source  
**Runtime boundary:** stable card identity, series, position, factor and image identity/path only

## Primary-source basis

The series/position/factor mapping is established directly from:

- Lipót Szondi, *Lehrbuch der experimentellen Triebdiagnostik*, Text-Band, 3rd expanded edition, 1972;
- admitted source ID: `SZ_LEHR_1972`;
- admitted PDF: `sources/originals/Szondi Lehrbuch der experimentellen Triebdiagnostik.pdf`;
- printed page 357;
- **Tabelle 19. Ursprung der Bilder des Testapparates**.

The table was checked visually from the admitted PDF, not inferred from OCR or legacy software. It gives six groups (`Gruppe I`–`VI`), eight numbered positions in each group, and the factor belonging to each position.

The 48 files currently present under `assets/stimuli/` were checked against this table. Result: **48/48 filenames agree with the primary-source series/position/factor mapping; 0 discrepancies.**

Each series contains exactly one occurrence of each factor `h, s, e, hy, k, p, d, m`.

## Verified mapping

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

## Boundary

The mapping above is source-authorized for the deterministic test layer. Historical biographical/diagnostic metadata concerning the photographed persons is not part of the runtime asset model and remains excluded from scoring, interpretation and reporting.

The 48 image binaries themselves remain identity-locked by the immutable stimulus tree recorded in `config/evidence_lock.json`.
