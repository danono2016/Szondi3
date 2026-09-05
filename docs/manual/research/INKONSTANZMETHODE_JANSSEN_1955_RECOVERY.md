# Inkonstanzmethode Böszörményi — Janssen 1955 recovery

**Status:** RESEARCH / ALGORITHM NEAR-COMPLETE FROM A NEAR-CONTEMPORARY SECONDARY SOURCE  
**Source status:** Janssen 1955 is not one of the ten canonical manual sources and does not replace the primary Böszörményi 1953 article.  
**Implementation status:** A historically scoped implementation is now plausible, but the remaining inferred edge case must be marked as reconstruction unless the primary article is eventually admitted.

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

- `0`: open/null reaction according to the historical test convention;
- `±`: positive and negative counts equal in the ambivalent range;
- `+`: directional positive reaction, including unequal mixed distributions dominated by positive choices;
- `-`: directional negative reaction, including unequal mixed distributions dominated by negative choices.

The exact exhaustive mapping of all 28 distributions is still not printed by Janssen, so any implementation should keep this classifier local to the method and preserve a source/reconstruction note.

---

## 5. The `± <-> 0` edge case — strongest reconstruction

Janssen does not explicitly print `± <-> 0` as an example. However, his three change categories plus the wording of the definitions strongly constrain the missing cell.

The key observation is that Böszörményi’s multiplier system is organized by **directional relation**, not by symbolic inequality alone:

- `qu`: quantitative change **without change of direction**;
- `t`: crossing between a **directed** reaction (`+` or `-`) and a **non-directed** reaction (`±` or `0`), or vice versa;
- `c`: reversal between the two opposite directed reactions (`+ <-> -`).

Janssen’s definition of `t` deliberately groups `±` and `0` together as the two destinations/sources opposite the directed class `+/-`. This yields a natural two-superclass structure for multiplier selection:

- directed: `{+, -}`;
- non-directed: `{±, 0}`.

Under that structure, the only exhaustive placement for `± <-> 0` is `qu`, because the transition remains within the same non-directed superclass and therefore changes quantity/form without changing directional orientation.

This gives an exhaustive symmetric transition table:

| from/to | + | - | ± | 0 |
|---|---:|---:|---:|---:|
| + | qu/i | c | t | t |
| - | c | qu/i | t | t |
| ± | t | t | qu/i | **qu (reconstructed)** |
| 0 | t | t | **qu (reconstructed)** | qu/i |

Here `i` applies only when the underlying positive/negative counts are unchanged; otherwise same-class transitions are `qu`.

### Why this reconstruction is strong

1. It follows Janssen’s literal definition of `qu` as quantitative change without directional change.
2. It follows Janssen’s literal grouping of `±` and `0` together in the definition of `t` as the non-directed alternatives to `+/-`.
3. It makes the four-category system exhaustive without inventing a fourth multiplier or an exception.
4. It is symmetric, as all printed examples and definitions are symmetric with respect to transition direction.
5. It is historically simple and consistent with the conceptual apparatus of the method.

### Confidence label

`± <-> 0 -> qu` should be treated as **HIGH-CONFIDENCE RECONSTRUCTION**, not as a verbatim recovered rule, until the 1953 article is found.

This is materially different from an arbitrary guess: the rule is the unique simple completion of Janssen’s published classifier if `qu/t/c` are exhaustive categories, as his exposition strongly implies.

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

These published totals provide an independent regression target if the underlying profile count data for a subset of Janssen’s subjects can be recovered.

Later in the dissertation Janssen also reports factor-specific Böszörményi change means (for example factor `e` in individual epilepsy cases), confirming that the method is usable at the individual-factor level as Szondi’s Lehrbuch summary says.

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

### Reconstructed with high confidence

- `± <-> 0` belongs to `qu`, because it is a quantitative/form change without crossing from non-directed to directed orientation.

### Still not directly recovered

- exact primary wording/names from Böszörményi 1953;
- exhaustive Böszörményi classification of all 28 count distributions;
- original series-level aggregation/ranking procedure beyond pairwise factor values (although Szondi’s Lehrbuch confirms factor Inkonstanzziffern and rank ordering across a series);
- exact group-level aggregation method from the 1953 article.

---

## 9. Software consequence

Do **not** alter mature P1 reaction scoring.

If implementation is authorized, introduce a separate historical-method layer with:

1. raw factor count pair `(positive_count, negative_count)` from each free foreground profile;
2. Böszörményi-scoped reaction/direction classification used only for multiplier selection;
3. change magnitude `Q`;
4. change type `i/qu/t/c`;
5. multiplier;
6. factor transition score;
7. profile-pair total as sum of eight factor scores;
8. series aggregation kept explicit and provenance-labelled.

Forced experimental-complement zero `ø` is outside this free-series method and must not be normalized to an ordinary `0`.

No clinical inference should be attached automatically to the numeric score.

A safe implementation label before primary-source admission would be something like:

`BOSZORMENYI_INKONSTANZ_JANSSEN_1955_RECONSTRUCTION`

rather than claiming verbatim primary recovery.

---

## Verdict

The problem has moved from **“formula unknown”** to **“formula operationally recoverable from Janssen, with one edge case solved by high-confidence constrained reconstruction rather than direct quotation.”**

The remaining uncertainty is now mainly historical/provenance, not mathematical architecture. If the 1953 article never becomes available, Janssen 1955 is strong enough to support a separately labelled reconstructed implementation, provided the Böszörményi-specific classifier remains historically scoped and the inferred `± <-> 0 -> qu` rule is explicitly documented as reconstruction.