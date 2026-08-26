# SZONDI3 — PROJECT CHECKPOINT

**Checkpoint date:** 2026-08-26  
**Repository:** `danono2016/Szondi3`  
**Authoritative branch:** `main` after merge of the P1 finalization record  
**Current phase:** `P1 — Deterministic Test Engine` — CLOSED  
**Current gate:** `P1_DETERMINISTIC_ENGINE_PASS`  
**Next roadmap phase:** `P2A — Primary Doctrine Registry` — NOT STARTED / NOT AUTHORIZED BY THIS CHECKPOINT

## Accepted foundation

P0 remains accepted as `P0_SOURCES_PASS`. The admitted evidence boundary remains identity-locked by `config/evidence_lock.json`: 10 DOCX sources, 8 PDF visual arbiters and 48 WebP stimuli. The eight `SZ_*` sources remain `SZONDI_PRIMARY`; Deri and Mélon remain separate post-Szondian layers. Primary wording is preserved without modernization or sanitization, and photographed-person historical metadata remains excluded from runtime scoring, doctrine, interpretation and reports.

## P1 result

P1 reconstructed the source-authorized deterministic test engine without clinical interpretation. The integrated implementation now covers:

- all 48 stimulus identities and source-derived series/position/factor mapping;
- foreground administration and complete VGP recording;
- EKP/background complements and forced-null `ø` distinction;
- factor count/reaction scoring including quantum intensity;
- formal vectors and profiles;
- ordered repeated profile series and Tabelle 13 normalization;
- Tendenzspannungsquotient, symptom percentage, TspG and TspD;
- Latenzproportionen, Gefahr/Ventil and Triventil/Quadriventil structure;
- Haupttriebklasse with ties preserved;
- Wurzelfaktor direction evidence and strict unambiguous Unterklasse;
- complete and abbreviated Triebformel deterministic core with ambiguity preserved;
- Dur-Moll arithmetic;
- Sozialindex arithmetic.

The final source-resolution record is `docs/P1_RESOLUTION_SWEEP.md`. The gate verification record is `docs/P1_DETERMINISTIC_ENGINE_VERIFICATION.md`.

## P1 acceptance

The roadmap gate is satisfied:

1. source-authorized administration/scoring procedures implemented — PASS;
2. primary source examples/invariants represented in tests — PASS;
3. short-series normalization handled explicitly where authorized — PASS;
4. known ambiguity is preserved rather than silently resolved — PASS;
5. negative/fail-closed behavior is tested — PASS;
6. no clinical interpretation entered P1 — PASS;
7. every residual P1 item has a durable closure status — PASS.

Therefore the explicit gate is:

> **`P1_DETERMINISTIC_ENGINE_PASS`**

## Semantic closure witness

PR #37, `Close P1 resolution sweep and verify deterministic gate`, merged to `main` as:

`5e4d02782d7165dbcea7828ca055a2415b72d262`

PR #37 closed the resolution sweep, added the integrated P1 verification record and added the final negative validation for tied abbreviated-Triebformel extrema.

Post-merge CI on that semantic closure SHA was green:

- Foundation verification — run `32939562736` — `success`;
- P0 source inspection — run `32939562733` — `success`;
- P0 canonical access — run `32939562754` — `success`.

The canonical-access workflow runs `python -m unittest discover -s tests -p 'test_*.py' -v` as part of the integrated verification.

## Known residual limitations

These are explicit source/scope boundaries, not unfinished P1 debt:

- Fall 18 `kp/hs` is authentic source evidence but no unsupported universal multi-factor abbreviated-formula selector is invented.
- Mixed-direction Wurzelfaktor evidence does not receive an invented Unterklasse majority sign.
- Non-unique complete-Triebformel partitions fail closed.
- Szondi's incomplete Quantenverrechnung is not completed by inference.
- Exact Böszörményi Inkonstanzmethode computation remains reopenable if its identified original publication is later admitted; no tertiary/AI formula is substituted.
- Empirical/clinical short-series constancy claims are not converted into deterministic arithmetic.
- Rand-Mitte, verbal/association methods and clinical meanings of Dur-Moll/Sozialindex belong downstream.

## Recovery / reproduction

For a clean verification checkout, at minimum run:

```bash
python scripts/verify_foundation.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

The authoritative CI reproduction path is `.github/workflows/p0-canonical-access.yml`, which additionally regenerates canonical access twice, checks byte identity, verifies the derivative manifest and validates provenance/visual-arbitration inputs.

## Next safe action

Do **not** continue directly from this checkpoint without the normal successor qualification/authorization process.

A successor chat must begin with `docs/CHAT_TRANSFER_PACKAGE.md`, follow `docs/CHAT_SUCCESSION_PROTOCOL.md`, independently verify current `main`, PR and CI state, produce the required READ ONLY qualification report, and stop for explicit steward authorization.

Only after such authorization may the successor begin the next roadmap phase:

**`P2A — Primary Doctrine Registry`**.

This checkpoint does not start P2A.
