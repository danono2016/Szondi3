# Inkonstanzmethode Böszörményi — constrained historical reconstruction

**Status:** RESEARCH / HISTORICAL RECONSTRUCTION ONLY  
**Do not implement as Böszörményi method.** The primary article is not admitted and the exact algorithm remains unknown.

## Research question

Can the lost/absent calculation procedure of Georg Böszörményi's **Inkonstanzmethode** (worked out 1939–1940 under Szondi, published posthumously in *Szondiana I*, 1953, pp. 199–210) be reconstructed closely enough from the admitted/canonical corpus and near-contemporary evidence to form falsifiable candidate algorithms?

This document separates:

1. what Szondi states explicitly;
2. what Deri states explicitly;
3. what Mélon states explicitly;
4. external historical comparators;
5. our reconstruction hypotheses.

No hypothesis below is to be named or shipped as `BOSZORMENYI_INKONSTANZMETHODE` until the 1953 article itself is admitted and checked.

---

## 1. What Szondi explicitly tells us

### Lehrbuch, p. 266 — direct evidence

Szondi describes the method as developed by his collaborator **Georg Böszörményi** in 1939–1940 under Szondi's direction. Its task is:

> den Grad der Veränderlichkeit, der Inkonstanz, bei den einzelnen Faktorreaktionen im Test zahlenmäßig auszudrücken

That is: to express numerically the degree of variability/inconstancy of the **individual factor reactions**.

The full technique is not reproduced. Szondi refers the reader to:

G. Böszörményi, **"Bestimmung der faktoriellen Schwankungen im Szondi-Test"**, *Szondiana I*, Huber, Bern/Stuttgart, 1953, pp. 199–210.

Szondi gives three use cases:

1. determine **factorial variability over time** (`im Zeitablauf`) from serial administrations of one person;
2. rank the factors by **Inkonstanzziffern**; the relatively most constant factors are also considered informative;
3. extend the procedure to homogeneous groups and calculate variability of the individual factors at group level.

He adds that the procedure is **laborious** (`Umständlichkeit des Verfahrens`) and therefore rarely used in routine diagnosis.

### Hard constraints from this passage

Any serious reconstruction must therefore satisfy all of the following:

- output exists **per factor**, not only as one global person score;
- output is numeric (`Inkonstanzziffer`);
- it uses a **series** and concerns change **through time**;
- factor scores can be put in a **rank order**;
- it has a meaningful extension to **groups**;
- hand calculation in the 1940s/1950s is possible but sufficiently tedious to justify Szondi's remark;
- it cannot depend on mathematical machinery unavailable or implausibly exotic for a clinical test method developed in 1939–1940.

These constraints already make some modern reconstructions much more plausible than others.

---

## 2. A second direct Szondi constraint: serial change is not merely symbolic

In the `Lehrbuch` discussion of Vollreaktion and Nullreaktion, Szondi describes a possible serial succession:

**Quantumspannung → Ambivalenz → Entladung**.

He says this succession becomes visible only in serial testing, and that often only some phases are actually captured. He also explicitly says that drive needs are not rigid/stable factors but dynamically flowing and changeable processes, and that observing a factor as `beweglich` in a series has diagnostic importance.

This does **not** authorize an automatic equation:

- `± = Ambivalenzphase in every occurrence`;
- `0 = Entladung in every occurrence`.

It does show, however, that serial change in Szondi's mature methodology includes at least two dimensions:

- **direction/form of reaction**;
- **quantity/tension/loading**.

Therefore a reconstruction that throws away the quantitative configuration before comparing two profiles is prima facie less faithful than one that preserves it.

---

## 3. Deri 1949: the strongest near-contemporary clue

Susan Deri's *Introduction to the Szondi Test* was published in 1949, after the Inkonstanzmethode had reportedly been worked out (1939–1940) but before Böszörményi's posthumous 1953 publication.

Deri does not identify her classification as Böszörményi's formula. It must **not** be silently equated with it. But her detailed classification tells us how changes were being conceptualized within the Szondi tradition at approximately the right historical moment.

### Deri's graded classes of change

Deri explicitly compares a factor constellation **from one testing to another** and orders types of change by increasing diagnostic significance.

#### a. Same direction and same absolute count, different concrete pictures

If the same number and direction are preserved but different photographs of the same factor are chosen, she treats this as practically no dynamic change.

**Constraint:** Böszörményi may have worked above the level of individual card identity. A method based solely on picture-by-picture switching would not match this Deri principle.

#### b. Same factorial direction, changed loading/distribution

Examples include:

- `+3 → +4`;
- `+3 → +2/−1`.

Deri says the importance depends on the **number of squares added to or subtracted from the first reaction**.

**Constraint:** at least in Deri's formal structural analysis, reaction change has a natural quantitative magnitude measured in actual choice/square counts.

#### c. Directional change involving ambivalence, but no full reversal

`+ ↔ ±` or `− ↔ ±`.

This is more than a mere quantitative loading change but less than a complete reversal.

#### d. Transition to/from open (`0` in the later notation family)

`+ / − / ± ↔ open`.

Deri interprets this as a substantial change in dynamic strength and says the importance of the transition depends partly on the **number of squares in the factor before the open reaction**.

Again, raw magnitude matters.

#### e. Factorial reversal

`+ ↔ −`.

Deri states explicitly that the significance depends on the **number of squares which actually changed their position from plus to minus, or reverse**.

Thus a lightly loaded reversal and a heavily loaded reversal are not equivalent.

#### f. Vectorial mirror reversal

A simultaneous reversal of both factors in a vector is treated as a still stronger structural event.

This is vector-level, whereas Böszörményi's method as summarized by Szondi explicitly produces factor-level `Inkonstanzziffern`. Therefore this category may be relevant to a broader theory of serial change but is not necessarily part of the factor-score algorithm.

### Deri's methodological instruction

Deri recommends writing the series symbolically (`+`, `−`, `±`, `0`) for rapid visual inspection, **but warns not to rely solely on the symbolic record**, because quantitative and qualitative details must be checked on the graphic profiles.

This is a major constraint against reconstructions that use only a 4-state symbolic sequence.

---

## 4. Mélon: a later variability index that must NOT be confused with Böszörményi

Jean Mélon, in *Théorie et pratique du Szondi* (1975), gives an explicit **indice de variabilité globale (IVG)** and cites his 1974 *Szondiana X* paper.

His rule is simple:

> créditer d'un point chaque changement de signe factoriel et faire la somme des changements survenus, pour les huit facteurs dans la série des dix profils

In plain terms: give **one point for each change of factorial sign** and sum all such changes across the eight factors over the ten-profile series.

Mélon reports a normal global interval of roughly **10–35** and interprets extreme low/high values cautiously and historically in relation to rigidity/disorganization.

### Why this matters

This establishes that a **sequential sign-change count** was genuinely used inside the later Szondi tradition.

But it is not the same object Szondi describes for Böszörményi:

- Mélon: one **global** IVG over eight factors;
- Böszörményi/Szondi summary: **individual factor** Inkonstanzziffern that can be ranked.

The Mélon index therefore strengthens the historical plausibility of **successive-profile comparison**, but does not reveal Böszörményi's weighting/calculation.

---

## 5. External near-contemporary comparator: David & Rabinowitz 1951

External historical search identified H. P. David & W. Rabinowitz, **"The development of a Szondi instability score"**, *Journal of Consulting Psychology* 15 (1951), 334–336.

A contemporary dissertation summarizing the method states that their Szondi Instability Score (SIS):

- quantified, on a simple scale, types of change **from one profile to the next**;
- was based on the initial reaction to each **individual picture**;
- was independent of the Szondi factor to which the picture belonged.

This is clearly a **different method** from Böszörményi's factor-level Inkonstanzziffer.

Its importance for reconstruction is negative and historical:

- serial instability was naturally operationalized by **successive-profile comparisons** in the same period;
- however, multiple competing instability methods existed;
- therefore one must not infer Böszörményi's formula from generic 1950s "instability score" literature.

The same external literature shows that this SIS could reach scores above 90, which further demonstrates that its scale is structurally unlike Mélon's later global sign-change index and should not be mixed with it.

---

## 6. Revised hypothesis space

The evidence changes the ranking of the hypotheses proposed before this search.

### H1 — sequential, weighted factor change (CURRENT LEADING HYPOTHESIS)

For each factor, compare its reaction in profile `t` with its reaction in profile `t+1`, assign a numerical change value, and aggregate over the series.

Generic form:

`I_f = Σ_t C(R_f(t), R_f(t+1))`

where `C` is some historically simple change-scoring function.

Why H1 is now strongest:

- Szondi says change `im Zeitablauf`;
- Deri explicitly classifies changes `from one testing to another`;
- Mélon's later IVG counts successive sign changes;
- David/Rabinowitz independently use successive-profile transitions;
- the labor can easily become substantial if each interval must be inspected in the graphic profile for direction **and** number of squares.

The earlier argument that `Umständlichkeit` implies all-pairs comparison is therefore weakened considerably.

### H1a — raw Manhattan-type square change

A minimal candidate:

`C = |S_t − S_{t+1}| + |A_t − A_{t+1}|`

with `S` = sympathetic count, `A` = antipathetic count.

Historically this does not require geometric language; it is merely total absolute change in the two choice counts.

Strengths:

- matches Deri's repeated emphasis on number of squares added/subtracted/moved;
- distinguishes small loading changes from large reversals;
- preserves information erased by the four symbolic classes;
- trivial to calculate with 1940s arithmetic.

Weakness:

- Deri treats some qualitatively different changes as different **categories**, not merely different magnitudes. A raw absolute-difference score may therefore underrepresent the categorical distinction between ambivalence, opening, and reversal.

Status: **plausible sub-hypothesis, not demonstrated**.

### H1b — sequential categorical + magnitude score

Each successive transition is first placed into a class broadly like Deri's:

- quantitative within-direction change;
- transition to/from ambivalence;
- transition to/from open;
- plus/minus reversal;

then magnitude (number of squares changed) modifies the score.

This fits Deri best conceptually and would indeed be more laborious.

Weakness: without Böszörményi, the numerical weights are entirely unknown. Any implementation now would invent the central part of the method.

Status: **conceptually strongest but currently non-computable without invented weights**.

### H1c — simple per-factor sign-change count

For each factor, one point whenever the symbolic reaction class changes between successive profiles.

This is essentially a factor-specific analogue of Mélon's later global IVG.

Strengths:

- historically simple;
- directly produces factor-specific counts/ranks;
- consistent with successive-profile logic.

Weaknesses:

- conflicts with Deri's insistence that intensity of change must be checked from graphic profiles;
- treats `+3→+4` as no change if both remain `+`, despite Deri classifying that as a real (small) change;
- cannot explain why the original procedure would be especially laborious.

Status: **possible but now judged less likely than H1a/H1b**.

### H2 — all-pairs factor dispersion

Compare every pair among `N` administrations and average/sum a distance.

Generic form:

`I_f = (1 / choose(N,2)) Σ_{i<j} C(R_f(i), R_f(j))`

Earlier this was attractive because it naturally yields a global dispersion and is laborious by hand.

Evidence against relative priority:

- explicit wording in Deri favors `one testing to another`;
- later variability methods also work successively;
- Szondi's `im Zeitablauf` is more naturally sequential than order-free dispersion.

Status: **still falsifiable, but downgraded**.

### H3 — dispersion around a modal/mean factor state

A 1930s–1940s statistician could have summarized variability by range, mean deviation, variance-like dispersion, or deviation from a modal reaction.

This would fit the words `Schwankungen`, `Streuung`, and group extension.

But no admitted text currently points specifically to a mean/modal center calculation.

Status: **low-to-moderate plausibility; retain only as a control hypothesis**.

---

## 7. What the reconstruction strongly suggests Böszörményi probably did NOT do

### Not a modern vector-direction/coherence analysis

Nothing in the source vocabulary points to resultant vectors, angular persistence, cosine similarity, trajectory direction, or a modern geometric state-space formalism.

Those can be legitimate **modern exploratory descriptors**, but they should be kept in a separate method family.

### Probably not pure card-identity switching

Deri explicitly says that exchanging the actual photographs while retaining the same factor count/direction produces practically no change in interpretation.

David/Rabinowitz's picture-level SIS therefore should not be imported backward into Böszörményi.

### Probably not only a global person score

Szondi specifically speaks of Inkonstanzziffern of individual factors and their rank order.

A global score may be derived secondarily, but it cannot be the sole primitive if Szondi's summary is accurate.

---

## 8. Reverse-engineering plan from existing corpus

The exact article is absent, but the current corpus can still be mined for **constraints**.

### Search target A — explicit Inkonstanz values/ranks

Search all canonical works for:

- `Inkonstanzziffer` / `Inkonstanzziffern`;
- `Rangreihe der Inkonstanzziffern`;
- Böszörményi references;
- numerical factor rankings explicitly attributed to constancy/inconstancy.

Current result: in the ten admitted sources, the only direct Böszörményi methodological discussion located is the `Lehrbuch` p. 266 summary. No numerical worked example of his method has yet been found.

### Search target B — complete ten-profile series with qualitative judgments

Deri contains formalized ten-profile examples and explicit judgments such as:

- steady factors;
- frequently open/ambivalent factors;
- repeated reversals;
- areas with the most frequent complete reversals.

Where the original graphic counts can be reliably recovered, compute candidate H1a/H1c/H2 values and test whether they reproduce the published qualitative ranking.

This cannot identify the formula alone, but it can falsify candidates.

### Search target C — cases where the same endpoints hide different paths

Use serial cases with gradual reversal versus abrupt reversal.

A credible Böszörményi reconstruction should probably distinguish at least some of these if its purpose is time-course variability. H2 (order-free all-pairs dispersion) may fail to distinguish paths that H1 captures.

### Search target D — group extension

Any candidate must aggregate naturally at group level in a way consistent with Szondi's statement that Böszörményi provided a group calculation technique.

Possible historically simple extensions:

- mean/median factor Inkonstanzziffer by group;
- frequency distribution of factor scores;
- pooled sums normalized by number of intervals.

No current evidence chooses among these.

---

## 9. New important distinction: three different historical "variability" methods

The research now identifies at least three non-equivalent historical objects:

### Böszörményi Inkonstanzmethode (1939–40 / published 1953)

- factor-level;
- serial;
- exact algorithm unavailable;
- source status: **HOLD / REOPENABLE_ON_SOURCE_ADMISSION**.

### David–Rabinowitz Szondi Instability Score (1951)

- profile-to-profile;
- picture-level, factor-independent;
- American psychometric research score;
- not the Böszörményi method.

### Mélon Indice de variabilité globale (1974)

- one point per factorial **sign change**;
- summed over 8 factors across 10 profiles;
- global score;
- later Szondian tradition, but not evidence of Böszörményi's exact algorithm.

This distinction must be preserved in any future manual/software work.

---

## 10. Current probability ranking (heuristic, not statistical)

These percentages are **research confidence estimates**, not source facts:

- **H1 family: successive-profile factor comparison:** ~80–90% confidence.
- **H1b categorical + magnitude weighting:** ~45–60% as the likely internal scoring logic.
- **H1a raw absolute square-change sum:** ~25–40% as an exact formula candidate.
- **H1c simple sign-change count:** ~15–25% as exact Böszörményi formula, despite later support from Mélon.
- **H2 all-pairs dispersion:** ~10–20%.
- **H3 mean/modal dispersion statistic:** ~10–20%.

The estimates overlap because H1b could include an H1a-like magnitude component.

The main progress is not identification of the exact formula; it is the substantial narrowing of the search space.

---

## 11. Falsification criteria for the missing article

When Böszörményi 1953 is eventually admitted, check immediately:

1. **Comparison unit** — consecutive profiles, all pairs, or deviation from a center?
2. **Primitive data** — picture identities, raw factor counts, reaction symbols, or combinations?
3. **Direction sensitivity** — does `+↔−` receive special treatment?
4. **Open/zero sensitivity** — is opening/closing separately weighted?
5. **Ambivalence sensitivity** — is `±` treated categorically?
6. **Magnitude** — do the number of squares moved/added/subtracted enter the score?
7. **Normalization** — raw sum, average per interval, percentage, table lookup?
8. **Scale** — expected numerical range of a factor Inkonstanzziffer.
9. **Group method** — how individual scores are combined across subjects.
10. **Worked examples** — use them as exact unit tests before implementation.

If the article contradicts the reconstruction, the article wins immediately.

---

## 12. Software policy resulting from this research

### Authentic historical method

Keep:

`Inkonstanzmethode = HOLD / REOPENABLE_ON_SOURCE_ADMISSION`.

Do not implement any of H1/H2/H3 under the historical method's name.

### Optional exploratory research layer

If desired, a separate experimental module may later compute source-transparent descriptors from existing series:

- raw `(n_sym, n_anti)` trajectories;
- symbolic 4×4 transition matrices;
- stationary-run counts;
- exact transition counts;
- explicitly named modern metrics (e.g. Manhattan path length), always labelled as **modern exploratory formalizations**.

No such descriptor is currently authorized to generate a clinical finding.

---

## 13. Source ledger

### Canonical/admitted

- Leopold Szondi, *Lehrbuch der experimentellen Triebdiagnostik*, p. 266 — direct summary of Böszörményi Inkonstanzmethode.
- Leopold Szondi, *Lehrbuch*, discussion of Vollreaktion/Nullreaktion and serial succession `Quantumspannung → Ambivalenz → Entladung`.
- Susan Deri, *Introduction to the Szondi Test* (1949), section `Significance of Constancy or Changes in the Factorial Reactions` — graded change classes and requirement to return from symbolic record to graphic profile for intensity.
- Jean Mélon, *Théorie et pratique du Szondi* (1975), pp. around 170–171 — explicit later `indice de variabilité globale`, one point for each factorial sign change over the 10-profile series; cites Mélon 1974.

### External historical corroboration — not canonical for the manual

- H. P. David & W. Rabinowitz, `The development of a Szondi instability score`, *Journal of Consulting Psychology* 15 (1951), 334–336 — bibliographic existence confirmed; method summarized in a contemporary dissertation as successive-profile, picture-level, factor-independent.
- A later dissertation on epilepsy using the SIS describes it explicitly as measuring change from one profile to the next and reports subject-level interval scores.
- Google Books currently indexes a digitized Cornell copy of *Szondiana I* (1953) and exposes `Inkonstanzziffern` among searchable/common terms, but the article pages were not available through the present access path. This is a promising acquisition lead, not admitted evidence.

---

## Bottom line

The reverse engineering has produced a real result:

**The most plausible architecture of Böszörményi's method is now a factor-specific sum/aggregation of weighted changes between successive profiles, with the magnitude and/or qualitative class of each change likely relevant.**

What remains unknown is exactly the central piece: **the weighting rule**.

Deri makes a purely symbolic one-point-per-change rule look too crude as a reconstruction of the original method; Mélon proves that such a simple sign-change index later existed, but as a different global index. The all-pairs hypothesis is still logically possible but is no longer the leading candidate.

Therefore the correct next historical move is not coding. It is either:

1. obtain *Szondiana I*, pp. 199–210; or
2. continue falsification of H1a/H1b/H1c/H2 against complete serial cases in the canonical corpus where the authors themselves describe relative constancy/change.
