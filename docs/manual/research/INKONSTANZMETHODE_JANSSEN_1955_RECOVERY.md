# Inkonstanzmethode Böszörményi — Janssen 1955 recovery

**Status:** RESEARCH / ALGORITHM SUBSTANTIALLY RECOVERED FROM A NEAR-CONTEMPORARY SECONDARY SOURCE  
**Source status:** Janssen 1955 is not one of the ten canonical manual sources and does not replace the primary Böszörményi 1953 article.  
**Implementation status:** DO NOT yet ship as the exact Böszörményi method until the remaining edge case and source-admission decision are resolved.

## Source

H. J. M. N. Janssen, *De diagnostische waarde van de Szondi-test*, dissertation, Nijmegen, 1955, section III.D, printed pp. 53–57.

Janssen explicitly cites:

G. Böszörményi, “Die Inkonstanzmethode” / “Bestimmung der faktoriellen Schwankungen im Szondi-Test”, *Szondiana I* (1953), p. 199 sq.

Janssen does not merely mention the method. He describes the calculation rule, gives the multipliers, gives worked numerical examples, and applies the method to 80 subjects.

---

## 1. Primitive quantity: absolute change in positive and negative choice counts

For each factor, compare two profiles.

Let:

- `P1`, `N1` = positive and negative choice counts in profile 1;
- `P2`, `N2` = positive and negative choice counts in profile 2.

Janssen states that Böszörményi first calculates how many positive choices and how many negative choices have been added or subtracted.

The raw magnitude is therefore:

`Q = abs(P2 - P1) + abs(N2 - N1)`

Worked example in Janssen, p. 53:

`(+2,-1) -> (+4,-0)`

Two positive choices added, one negative choice removed:

`Q = 2 + 1 = 3`.

This confirms the core of the earlier H1a reconstruction.

---

## 2. The decisive second stage: weighting by KIND of change

Janssen then states that the raw values are multiplied by constants according to the nature of the change.

Besides `i-Reaktionen` (unchanged reactions), Böszörményi distinguishes three classes.

### qu-Veränderung

Quantitative change without change of direction.

Multiplier:

`M_qu = 1`

Janssen uses the same example:

`(+2,-1) -> (+4,-0)`

Raw magnitude `Q = 3`; therefore score `= 1 * 3 = 3`.

### t-Veränderung

Janssen defines these as changes from `+` or `-` to `±` or `0`, or vice versa.

Multiplier:

`M_t = 1.5`

Worked example, p. 53:

`(+4,-0) -> (+1,-1)`

Raw magnitude:

`Q = |1-4| + |1-0| = 3 + 1 = 4`

Score:

`1.5 * 4 = 6`.

### c-Veränderung

Change into the opposite: `+ -> -` or `- -> +`.

Multiplier:

`M_c = 2`

Worked example, p. 54:

`(+1,-4) -> (+3,-0)`

Raw magnitude:

`Q = |3-1| + |0-4| = 2 + 4 = 6`

Score:

`2 * 6 = 12`.

### i-Reaktion

Janssen glosses these as `niet veranderde reacties` — unchanged reactions.

With identical positive/negative counts, `Q = 0`, so the contribution is necessarily zero regardless of whether a separate multiplier was defined in the original article.

---

## 3. Formal core recovered

For a factor transition between two profiles:

`I_f(profile_a, profile_b) = M(type) * (abs(Pb-Pa) + abs(Nb-Na))`

with the recovered multipliers:

- `qu = 1`
- `t = 1.5`
- `c = 2`
- unchanged = `0 contribution`

For the difference between TWO COMPLETE PROFILES, Janssen states explicitly that the method is applied to all eight factors and the eight factor values are summed:

`I_profile_pair = sum_f I_f`

This is direct evidence that the primitive comparison is between profile pairs and that the factor-level scores can also be retained independently.

---

## 4. Critical historical classifier: Böszörményi’s ambivalence convention is NOT the mature Szondi Table-3 convention

Janssen footnote 66 is essential.

He states that Böszörményi does **not** count reactions composed of unequal positive and negative choice counts as ambivalent. His examples include distributions such as `+4/-2` and `+2/-3`, which are treated as positive and negative respectively, not `±`.

Therefore the transition-type classifier for the Inkonstanzmethode CANNOT simply reuse the mature Szondi reaction classifier implemented for the Lehrbuch Table 3.

This matters directly to our existing software, where mature Szondi correctly classifies:

- `4/2 -> ±!`
- `2/4 -> ±!`

For Böszörményi’s multiplier selection, Janssen says the classification convention is different. The method needs a **historically scoped Böszörményi direction classifier**, not a change to P1 scoring.

The likely scoped rule supported by Janssen is:

- `0`: both counts within the null/open range;
- `±`: equal positive and negative counts in the ambivalent range;
- `+`: unequal mixed reaction dominated by positive choices;
- `-`: unequal mixed reaction dominated by negative choices.

However, this exact generalized classifier should still be checked against the primary article before being frozen, because Janssen gives the principle and examples rather than an exhaustive table of all 28 distributions.

---

## 5. One remaining edge case: `± <-> 0`

Janssen’s exhaustive prose list contains only:

- qu: quantitative change without directional change;
- t: `+/- <-> ±/0`;
- c: `+ <-> -`.

The text does **not explicitly state** how a direct `± <-> 0` transition is classified.

This is now the principal remaining algorithmic ambiguity.

Do not silently assign it to `t` or `qu` without either:

1. the Böszörményi 1953 primary article; or
2. an independent near-contemporary source that explicitly classifies this transition.

This single edge case is why the recovery is “substantial” rather than “complete”.

---

## 6. Janssen empirical validation data

Janssen applied the method to 80 subjects, each tested three times, comparing:

- profile 1 vs profile 2;
- profile 2 vs profile 3.

He publishes the resulting total Inkonstanz values in a large table (printed p. 54 onward), including half-points, exactly as expected from the `1.5` multiplier.

His aggregate result:

- immediate repetition: mean change score `14.5`;
- one-day interval: mean change score `16.3`;
- one-day interval therefore about `12%` greater.

These published totals provide a future independent regression target if the underlying profile count data for a subset of Janssen’s subjects can be recovered.

Later in the dissertation Janssen also reports factor-specific Böszörményi change means (e.g. k and p in normal and schizophrenic groups), confirming that the method is usable at the individual-factor level as Szondi’s Lehrbuch summary says.

---

## 7. What this does to the earlier reconstruction hypotheses

### H1 — sequential weighted factor change

**CONFIRMED in architecture.**

Böszörményi compares factor reactions between profile observations and weights the raw count change by change type.

### H1a — raw Manhattan-type count difference

**CONFIRMED as the primitive magnitude.**

`abs(delta positive) + abs(delta negative)` is exactly the first calculation step described by Janssen.

### H1b — categorical + magnitude score

**CONFIRMED in principle and multipliers recovered.**

The missing weights are now known from Janssen:

- qu `1`
- t `1.5`
- c `2`

### H1c — simple symbolic sign-change count

**FALSIFIED as an adequate reconstruction of Böszörményi.**

The real method uses raw positive/negative choice-count magnitude and different change-class multipliers.

### H2 — all-pairs dispersion

**Strongly disfavoured as the primitive procedure.**

Janssen operationalizes the method directly between two profiles and applies it to successive comparisons 1–2 and 2–3.

### H3 — deviation from mean/modal state

**Not supported as the primitive method.**

---

## 8. Current confidence

### Recovered with high confidence

- factor-level positive/negative count differences;
- absolute-difference sum as raw magnitude;
- qu/t/c categories;
- multipliers 1 / 1.5 / 2;
- profile-pair total as sum of eight factor scores;
- sequential use in Janssen’s empirical application;
- Böszörményi-specific ambivalence convention differs from mature Szondi Table 3;
- factor-specific Inkonstanz values exist and can be averaged/ranked.

### Not yet fully recovered

- exact primary wording/names from Böszörményi 1953;
- exhaustive Böszörményi classification of all 28 count distributions;
- explicit treatment of `± <-> 0`;
- original series-level aggregation/ranking procedure beyond pairwise factor values (although Szondi’s Lehrbuch confirms factor Inkonstanzziffern and rank ordering across a series);
- exact group-level aggregation method from the 1953 article.

---

## 9. Software consequence

Do **not** alter mature P1 reaction scoring.

If/when implementation is authorized, introduce a separate historical-method layer with:

1. raw factor count pair `(positive_count, negative_count)` from each free foreground profile;
2. Böszörményi-scoped direction classification used only for multiplier selection;
3. change magnitude `Q`;
4. change type `qu/t/c/i`;
5. multiplier;
6. factor transition score;
7. optional profile-pair total as sum of eight factor scores.

Forced experimental-complement zero `ø` is outside this free-series method and must not be normalized to an ordinary `0`.

No clinical inference should be attached automatically to the numeric score.

---

## Verdict

The problem has moved from **“formula unknown”** to **“formula substantially recovered, one important edge case plus primary-source confirmation remaining.”**

This is the closest point so far to a source-grounded implementation contract. The remaining work is now narrow and falsifiable rather than open-ended reconstruction.
