# Inkonstanzmethode Böszörményi — Janssen 1955 recovery

**Status:** RESEARCH / ALGORITHM NEAR-COMPLETE FROM A NEAR-CONTEMPORARY SECONDARY SOURCE  
**Source status:** Janssen 1955 is not one of the ten canonical manual sources and does not replace the primary Böszörményi 1953 article.  
**Implementation status:** The core algorithm is recoverable; one transition class (`± <-> 0`) remains genuinely unresolved and must not be silently completed.

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

---

## 2. Weighting by kind of change

Janssen states that the raw values are multiplied by constants according to the nature of the change.

Besides `i-Reaktionen` (unchanged reactions), Böszörményi distinguishes three classes.

### qu-Veränderung

Quantitative change without change of direction.

Multiplier:

`M_qu = 1`

Example:

`(+2,-1) -> (+4,-0)`

Raw magnitude `Q = 3`; score `= 3`.

### t-Veränderung

Janssen's exact summary is: changes from `+` or `-` to `±` or `0`, or vice versa.

Multiplier:

`M_t = 1.5`

Worked example:

`(+4,-0) -> (+1,-1)`

`Q = 3 + 1 = 4`; score `= 1.5 * 4 = 6`.

### c-Veränderung

Change into the opposite: `+ -> -` or `- -> +`.

Multiplier:

`M_c = 2`

Worked example:

`(+1,-4) -> (+3,-0)`

`Q = 2 + 4 = 6`; score `= 12`.

### i-Reaktion

Janssen glosses these as `niet veranderde reacties` — unchanged reactions.

With identical positive/negative counts, `Q = 0`, so the contribution is zero.

---

## 3. Formal core recovered

For a factor transition between two profiles:

`I_f(profile_a, profile_b) = M(type) * (abs(Pb-Pa) + abs(Nb-Na))`

Recovered multipliers:

- `qu = 1`
- `t = 1.5`
- `c = 2`
- unchanged = `0 contribution`

For the difference between two complete profiles, Janssen states explicitly that the method is applied to all eight factors and the eight factor values are summed:

`I_profile_pair = sum_f I_f`

---

## 4. Critical historical classifier: Böszörményi is not mature Szondi Table 3

Janssen footnote 66 is essential.

He states that Böszörményi does **not** count reactions composed of unequal positive and negative choice counts as ambivalent. Examples such as `+4/-2` and `+2/-3` are treated as positive and negative respectively, not `±`.

Therefore the Inkonstanzmethode cannot simply reuse the mature Szondi Table-3 classifier.

This matters because Janssen himself explicitly states earlier in the dissertation that his printed Szondigram symbols follow Szondi's mature convention, including `4/2` and `2/4` as ambivalent `±!`; he notes that Deri uses a different convention there. Thus a printed `±` in Janssen's case tables does **not** by itself prove that Böszörményi would classify the underlying raw counts as ambivalent.

A separate historically scoped Böszörményi classifier is required for multiplier selection.

The supported principle is:

- `0`: historical open/null reaction;
- `±`: equal positive and negative counts in the ambivalent range;
- `+`: directional positive, including unequal mixed distributions dominated by positive choices;
- `-`: directional negative, including unequal mixed distributions dominated by negative choices.

The exhaustive 28-cell mapping remains a reconstruction unless the primary article is admitted.

---

## 5. `± <-> 0` — genuinely unresolved after forensic re-check

An earlier reconstruction assigned `± <-> 0` to `qu`, reasoning that both are non-directed. That conclusion is now **withdrawn as too strong**.

### Evidence for `qu`

- Janssen defines `qu` as quantitative change without change of direction.
- His literal definition of `t` lists `+/- <-> ±/0` and does not explicitly list `± <-> 0`.

These points make `qu` a coherent completion.

### Evidence for `t`

Immediately before presenting Böszörményi, Janssen reproduces Susan Deri's change taxonomy. Deri's type `d` explicitly includes transitions from `+`, `±`, or `-` to `0`, or vice versa. Thus **`± <-> 0` is explicitly grouped with opening/closing transitions** in the near-contemporary scheme that Janssen says the Böszörményi method 'fits well' (`sluit o.i. goed aan`).

Böszörményi's `t` category appears to compress much of Deri's types `c` and `d` into one multiplier class. If that compression is complete, `± <-> 0` would naturally be `t`, not `qu`.

Therefore the textual evidence is now genuinely two-sided:

- literal Janssen Böszörményi summary -> leaves the cell unprinted and permits `qu`;
- Janssen's immediately preceding Deri taxonomy -> gives a strong reason to suspect `t`.

### Forensic test case E3

Janssen case E3 is the crucial published case:

- printed factor-`e` sequence: `- , 0 , - , 0 , 0 , ±`;
- mean Böszörményi change score across the five successive transitions: `1.8`;
- therefore total factor-`e` change score: `9`;
- Janssen states that none of the `e=0` reactions was completely open.

The final transition is a printed `0 -> ±`, exactly the edge case we need.

However, Janssen prints **mature Szondi symbols**, not the raw positive/negative counts. Under mature Table 3, an unmarked `±` can arise from several raw distributions, some of which Böszörményi would reclassify as directional because their positive and negative counts are unequal. Likewise a non-completely-open `0` can represent several raw count pairs.

A constraint enumeration using all raw distributions compatible with the printed symbols and the reported total `9` shows that **solutions exist under both hypotheses** (`±<->0 = qu` and `±<->0 = t`). Therefore E3 is a genuine critical case but, from the published symbolic table alone, it does not uniquely identify the multiplier.

This is a useful negative result: we must not claim that Janssen's E3 numerically proves either completion unless the raw profile counts can be recovered.

### Current status of the edge case

`± <-> 0 = UNRESOLVED`

Do not implement it as an exact Böszörményi rule yet.

If a reconstructed implementation is desired before the primary article is found, the safest contract is either:

1. fail closed on this transition; or
2. expose the completion as an explicitly named reconstruction mode, never as source-recovered fact.

---

## 6. Janssen empirical validation data

Janssen applied the method to 80 subjects, each tested three times, comparing profile 1 vs 2 and profile 2 vs 3.

He publishes 160 total Inkonstanz values, including half-points exactly as expected from the `1.5` multiplier.

Aggregate results:

- immediate repetition: mean change score `14.5`;
- one-day interval: mean change score `16.3`;
- about `12%` greater after one day.

These 80 cases are useful as scale/distribution checks, but the published table does not include the corresponding raw `(positive_count, negative_count)` values, so it cannot by itself resolve the `± <-> 0` multiplier.

The individual epilepsy cases E1–E8 are more useful because Janssen gives factor-`e` symbolic series plus factor-specific mean Böszörményi scores. Among them, E3 contains the critical `0 -> ±` transition; unfortunately the raw counts needed to disambiguate the multiplier are not printed.

---

## 7. Canonical-corpus cross-check

Janssen explicitly points to Szondi's *Triebpathologie*, Tabelle 55, pp. 495–497, `Typische Triebprofile bei Epilepsie in der Sukzession`.

That canonical table contains multiple serial `e` changes and independently confirms that factorial mobility is studied through successive profiles. It is a strong doctrinal/structural control for the reconstructed method.

However, Tabelle 55 principally prints symbolic factor reactions rather than the raw choice-count pairs needed for exact Böszörményi arithmetic. It therefore cannot yet function as a numerical checksum for the missing `± <-> 0` multiplier.

---

## 8. What the recovery establishes

### Confirmed from Janssen

- sequential profile-pair comparison;
- raw magnitude `abs(delta positive) + abs(delta negative)`;
- factor-level scoring;
- profile-pair total = sum of eight factor scores;
- `qu/t/c` multipliers `1 / 1.5 / 2`;
- Böszörményi-specific ambivalence convention differs from mature Szondi;
- empirical use on 80 subjects and factor-specific use in individual cases.

### Still unresolved

- exact primary wording from Böszörményi 1953;
- exhaustive historical classification of all 28 count distributions;
- exact `± <-> 0` category;
- original series-level aggregation/ranking details beyond pairwise scores;
- exact group-level aggregation procedure.

---

## 9. Software consequence

Do **not** alter mature P1 reaction scoring.

Any future implementation must be a separate historical-method layer using raw factor counts and a Böszörményi-scoped classifier.

Minimum safe structure:

1. raw pair `(positive_count, negative_count)` for each free foreground factor reaction;
2. Böszörményi-scoped classifier for multiplier selection;
3. `Q = abs(delta positive) + abs(delta negative)`;
4. transition type `i/qu/t/c`;
5. multiplier;
6. factor transition score;
7. optional profile-pair total;
8. explicit unresolved handling for `± <-> 0` unless stronger evidence is admitted.

Forced experimental-complement zero `ø` is outside this free-series method.

No clinical inference should be attached automatically to the numerical score.

---

## Verdict

The core method is **substantially recovered and independently checkable**, but the last edge case is not honestly closed yet.

The important advance is that the uncertainty has become extremely narrow and testable. E3 is now identified as the exact forensic case to solve if raw counts can be recovered; Deri supplies an independent reason to suspect `t`, while Janssen's literal Böszörményi summary leaves room for `qu`.

Until one of those possibilities is eliminated by stronger evidence, the correct status is **NEAR-COMPLETE / ONE EDGE CASE OPEN**, not full recovery.