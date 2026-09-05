# Inkonstanzmethode Böszörményi — 28-distribution historical classifier

**Status:** HIGH-CONFIDENCE RECONSTRUCTION FROM JANSSEN 1955 + INTERNAL CONSISTENCY  
**Not primary-source complete:** the Böszörményi 1953 article remains unavailable.  
**Do not alter mature Szondi P1 scoring.** This classifier is scoped only to Inkonstanzmethode multiplier selection.

## Direct Janssen constraints

Janssen 1955 (printed p. 53) reports:

- primitive magnitude: `Q = abs(delta positive) + abs(delta negative)`;
- `qu` = quantitative change without change of direction, multiplier `1`;
- `t` = change from `+` or `-` to `±` or `0`, or vice versa, multiplier `1.5`;
- `c` = `+ <-> -`, multiplier `2`;
- unchanged (`i`) contributes zero;
- Böszörményi does **not** treat unequal mixed reactions such as `4/2` or `2/3` as ambivalent; they are positive or negative according to the dominant side.

Janssen's worked `t` example is `4/0 -> 1/1`, showing that `1/1` belongs to `0`, not `±`.

## Exhaustive historical direction classifier over the 28 possible count pairs

For all `(P,N)` with `P >= 0`, `N >= 0`, `P+N <= 6`:

1. `0` if `P <= 1` and `N <= 1`;
2. `±` if `P = N` and `P >= 2`;
3. `+` if `P > N` and `P >= 2`;
4. `-` if `N > P` and `N >= 2`.

This partitions all 28 distributions exhaustively.

### 0

`0/0, 1/0, 0/1, 1/1`

### +

`2/0, 2/1, 3/0, 3/1, 3/2, 4/0, 4/1, 4/2, 5/0, 5/1, 6/0`

### -

`0/2, 1/2, 0/3, 1/3, 2/3, 0/4, 1/4, 2/4, 0/5, 1/5, 0/6`

### ±

`2/2, 3/3`

This differs deliberately from mature Szondi Table 3, where e.g. `4/2` and `2/4` are ambivalent with pressure. The Böszörményi classifier must therefore be a separate historical-method classifier.

## Exhaustive transition-class rule

Given two count pairs A and B:

- `i` if the count pairs are identical (`Q=0`);
- `qu` if the count pairs differ but remain in the same direction class;
- `c` if the classes are `+` and `-` in either order;
- `t` if exactly one class is directed (`+` or `-`) and the other is nondirected (`±` or `0`);
- `qu` for `± <-> 0`.

The final line is an inference, not a recovered primary quotation. It is high-confidence because Janssen defines `qu` as change without directional change and groups `±` and `0` together as the nondirected alternatives in the definition of `t`; assigning `± <-> 0` to `qu` is the unique simple completion that makes `i/qu/t/c` exhaustive without inventing a fifth category.

## Transition matrix

| from/to | + | - | ± | 0 |
|---|---:|---:|---:|---:|
| + | qu/i | c | t | t |
| - | c | qu/i | t | t |
| ± | t | t | qu/i | **qu*** |
| 0 | t | t | **qu*** | qu/i |

`*` = high-confidence reconstruction, not direct primary wording.

## Score

For one factor transition:

`Q = abs(P2-P1) + abs(N2-N1)`

`score = multiplier(type) * Q`

with:

- `i`: `0`
- `qu`: `1`
- `t`: `1.5`
- `c`: `2`

A profile-pair total is the sum over all eight factors.

## Janssen 80-case validation set: what it can and cannot prove

Janssen publishes total Böszörményi Inkonstanz scores for 80 subjects, each with two profile comparisons (1-2 and 2-3), and reports aggregate means 14.5 for immediate repetition and 16.3 for one-day repetition.

These 160 published totals are valuable as a **scale/distribution checksum** and confirm the existence of half-point outcomes expected from the `1.5` multiplier.

However, Janssen does not publish the full raw `(P,N)` values for all eight factors for all 80 profile pairs in the table. Therefore the 80 totals alone cannot uniquely discriminate `± <-> 0 = qu` from `± <-> 0 = t`.

The strongest possible validation strategy is:

1. recover any individual Janssen protocols for which the raw graphical factor counts are printed;
2. recompute the exact published Böszörményi score;
3. prioritize cases containing a direct `± <-> 0` transition;
4. if raw counts for a complete profile pair can be recovered, compare the reconstructed 8-factor total with Janssen's published table value;
5. use the 160 total scores as secondary regression targets once enough raw protocols are recovered.

Janssen's later epilepsy cases provide symbolic serial profiles and factor-e mean Böszörményi scores, but the symbolic notation alone does not always preserve exact `(P,N)` counts. These cases are useful only where the graphical/raw counts can be recovered from the printed source.

## Current verdict

The classifier over all 28 count distributions is now exhaustively reconstructible from Janssen's rule plus the standard open threshold demonstrated by his `4/0 -> 1/1` worked example.

The only non-primary step is `± <-> 0 -> qu`. It is structurally very strong but should remain marked `RECONSTRUCTED_HIGH_CONFIDENCE` until either:

- the 1953 article is found, or
- an independent worked case with raw counts and published total forces that classification.
