# SZ_LEHR_1972 — Triventil visual arbitration

**Status:** `RESOLVED — SOURCE-ESTABLISHED`  
**Decision date:** 2026-08-27  
**Source:** `SZ_LEHR_1972` — `SZONDI_PRIMARY`  
**Canonical address:** `BODY U003910–U003912`  
**Visual arbiter:** `sources/originals/Szondi Lehrbuch der experimentellen Triebdiagnostik.pdf`

## Purpose

This record resolves the one numeric Lehrbuch blocker left by an OCR/source-near corruption in the approved canonical evidence. The canonical source remains the default textual basis. The paired admitted PDF is consulted only because the exact numeric typography at `U003912` is materially ambiguous.

No canonical derivative is rewritten by this arbitration.

## Canonical evidence

The approved canonical sequence establishes the context:

- `U003910`: `B. Die Ventil- oder Symptomklassen (Alle vier Latenzgrößen sind unter 5)`;
- `U003911`: the Biventil classes are not specially retained; Szondi distinguishes Triventilklasse and Quadriventilklasse;
- `U003912`: the decisive interval is corrupted in the canonical text as approximately `3^1`.

The surrounding canonical context therefore establishes that the rule concerns the difference between the highest and lowest Latenzgrößen when all four values are Ventile, but the exact numeric interval requires visual arbitration.

## PDF visual arbitration

The corresponding passage is on **PDF page 287 (1-based), printed page 283**.

Direct visual inspection resolves the corrupted token unambiguously as:

`3–4`

The printed sentence states that cases belong to the **Triventilklasse** when the difference between the highest and lowest Latenzgrößen is **3–4**.

## Source-established deterministic rule

On the common ten-profile decision basis:

1. if at least one Latenzgröße is `>= 5`, the case belongs to a Gefahrklasse rather than an all-Ventil class;
2. if **all four Latenzgrößen are below 5**, their possible values are `0..4`;
3. within this all-Ventil domain:
   - `max(Latenzgröße) - min(Latenzgröße) ∈ {3, 4}` → **Triventilklasse**;
   - spread `∈ {0, 1, 2}` → **Quadriventilklasse**.

Thus, in the all-Ventil branch, the existing implementation test `spread >= 3` is mathematically equivalent to the visually established source interval `3–4`, because a spread above 4 is impossible there. The implementation therefore required no behavioral correction.

## Regression coverage

`tests/test_latency_class_structure.py` explicitly covers:

- spread `3` → Triventilklasse;
- spread `4` → Triventilklasse;
- spreads `0`, `1`, `2` → Quadriventilklasse;
- Fall 18 after Tabelle-13 normalization → Quadriventilklasse with spread `2`.

## Epistemic classification

- exact interval `3–4`: **SOURCE-ESTABLISHED by approved canonical context + admitted PDF visual arbitration**;
- current arithmetic behavior: **SOURCE-ESTABLISHED / IMPLEMENTED**;
- former reading `3^1`: **OCR/source-near corruption, retired as evidence for the numeric rule**.

## Final project rule

> **The Lehrbuch Triventil numeric blocker is RESOLVED.**
>
> In an all-Ventil case, `spread ∈ {3,4}` means Triventilklasse; `spread ∈ {0,1,2}` means Quadriventilklasse.
