# SZONDI3 — PROJECT CHECKPOINT

**Checkpoint date:** 2026-08-26  
**Checkpoint type:** HISTORICAL P1 GATE-FINALIZATION RECORD  
**Repository:** `danono2016/Szondi3`  
**P1 gate-finalization commit:** `0cfe097f10c445044fcc60f561d60aae3e299dd2`  
**Gate recorded here:** `P1_DETERMINISTIC_ENGINE_PASS`

> **CURRENT-STATE NOTE — 2026-08-27:** this file records the accepted P1 state on 2026-08-26; it is **not** the current phase-resume checkpoint. P2A has subsequently been authorized and is active. Current Lehrbuch P2A state is in `docs/LEHRBUCH_P2A_PROGRESS.md`; current parallel Ich-Analyse state is on PR #52 and must be rechecked before integration. `kp/hs` is resolved by Decision Log `D-014` / `docs/KP_HS_RESOLUTION.md`; the Triventil OCR blocker is resolved by D-015 / `docs/TRIVENTIL_VISUAL_ARBITRATION.md`. Use `docs/CHAT_TRANSFER_PACKAGE.md` for current succession state.

## Accepted foundation

P0 remains accepted as `P0_SOURCES_PASS`. The admitted evidence boundary remains identity-locked by `config/evidence_lock.json`: 10 DOCX sources, 8 PDF visual arbiters and 48 WebP stimuli. The eight `SZ_*` sources remain `SZONDI_PRIMARY`; Deri and Mélon remain separate post-Szondian layers. Primary wording is preserved without modernization or sanitization, and photographed-person historical metadata remains excluded from runtime scoring, doctrine, interpretation and reports.

## P1 result

P1 reconstructed the source-authorized deterministic test engine without clinical interpretation. The integrated implementation covers:

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

The roadmap gate was satisfied:

1. source-authorized administration/scoring procedures implemented — PASS;
2. primary source examples/invariants represented in tests — PASS;
3. short-series normalization handled explicitly where authorized — PASS;
4. known ambiguity preserved rather than silently resolved — PASS;
5. negative/fail-closed behavior tested — PASS;
6. no clinical interpretation entered P1 — PASS;
7. every residual P1 item had a durable closure status — PASS.

Therefore the explicit gate recorded here is:

> **`P1_DETERMINISTIC_ENGINE_PASS`**

## Semantic closure witness

PR #37, `Close P1 resolution sweep and verify deterministic gate`, merged to `main` as:

`5e4d02782d7165dbcea7828ca055a2415b72d262`

PR #37 closed the resolution sweep, added the integrated P1 verification record and added the final negative validation for tied abbreviated-Triebformel extrema.

Post-merge CI on that semantic closure SHA was green:

- Foundation verification — run `32939562736` — `success`;
- P0 source inspection — run `32939562733` — `success`;
- P0 canonical access — run `32939562754` — `success`.

## Durable gate-finalization witness

PR #38, `Finalize P1 deterministic engine gate`, recorded the accepted P1 state in `docs/P1_DETERMINISTIC_ENGINE_VERIFICATION.md`, this checkpoint, `docs/CHAT_TRANSFER_PACKAGE.md` and `docs/DECISION_LOG.md`.

PR #38 merged to `main` as:

`0cfe097f10c445044fcc60f561d60aae3e299dd2`

Post-merge CI on that gate-finalization SHA was green:

- Foundation verification — run `32941382584` — `success`;
- P0 source inspection — run `32941382567` — `success`;
- P0 canonical access — run `32941382560` — `success`.

The canonical-access workflow runs `python -m unittest discover -s tests -p 'test_*.py' -v` as part of integrated verification.

## Known residual limitations at P1 checkpoint time

These were explicit source/scope boundaries, not unfinished P1 debt. Later decisions supersede individual bullets where stated:

- **SUPERSEDED by D-014:** Fall 18 `kp/hs` was authentic source evidence but the P1 checkpoint did not yet generalize its broader representation. Current project status: `kp/hs` RESOLVED; see `docs/KP_HS_RESOLUTION.md`.
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

## Historical next-action statement

At the time this checkpoint was written, P2A had not yet been started or authorized by this checkpoint. That historical restriction remains useful as gate history, but it is **superseded as current project state** by the later P2A authorization and active source-local work.

Current successors must use `docs/CHAT_TRANSFER_PACKAGE.md`, verify active PRs/CI, and obey current source ownership rather than restarting from this historical transition point.
