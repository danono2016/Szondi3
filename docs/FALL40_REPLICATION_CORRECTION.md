# Fall 40 — replication findings and correction strategy

## What the five independent readings showed

The same verified Zehnerserie was given to five independent AI conversations with the same neutral request and without the published case interpretation. The result was highly reproducible.

### Stable AI strengths

All five readings independently recovered approximately the same global organization:

- strong and persistent `h+ / h+!`;
- persistent `e- / hy-` as negative affect combined with concealment/restriction;
- `k+` as introjective/possessive Ego direction;
- `p+ / p±` as Ego expansion/affirmation with conflict;
- constant `d+ / m-` as search plus separation/contact difficulty;
- a coherent cross-vector narrative rather than isolated sign commentary.

This means the generative layer is already good at clinical integration. The correction target is not generic narrative ability.

### Stable AI failures

1. **Null reaction flattened into absence or weak availability.** In all five readings, repeated `s0` was treated primarily as absent, neutralized, or unavailable direct aggression. This is not a safe general rule. Szondi's Lehrbuch explicitly states that Nullreaktionen may be testological signs of a *Triebmanifestation* and that their actual meaning must be decided from the whole profile, especially serial recordings. In the published Fall 40 interpretation, repeated `s0` receives a case-specific sadism significance. The general correction is therefore not “s0 always means sadism”; it is “0 must never be silently equated with absence.”

2. **Factor-first reading flattened vector Gestalts.** The five reports repeatedly decomposed `P` into `e-` plus `hy-`, but none spontaneously reconstructed the source's differentiated treatment of `P--`, `P0-`, and `P-0`. The same problem appeared in `Sch`: `Sch-±`, `Sch-+`, and the rare `Sch±±` were largely dissolved into a story about the trajectory of factor `k`.

3. **Frequency became an implicit priority rule.** AI naturally privileged the most frequent signs. Szondi can assign high clinical weight to a rarer configuration. Frequency is an important deterministic fact, not the sole measure of interpretive weight.

4. **Exact counting was not reliable enough.** Some readings miscounted tensioned reactions. Counting belongs to deterministic P1, not to prose generation.

5. **Source vocabulary was domesticated.** Terms such as `Sadismus`, `kainitisch`, `Entfremdung`, `Inflation`, and sharp Szondian formulations tended to be replaced by contemporary, softer language such as “vulnerability”, “regulation”, “relational sensitivity”, “autonomy”, and “resources”. This changes the author's conceptual texture.

6. **Safety caveats became stylistic boilerplate.** Correct epistemic limits were repeatedly restated in generic language. This reduced density without improving precision.

## Correction principle

**Preserve Szondi's term; constrain the inference made from it.**

A source-authorized label such as `Sadismus`, `Projektion`, `Inflation`, `Entfremdung`, `Desintegration`, or `kainitische Gesinnung` may be reported as Szondian testological terminology. What must be blocked is an unsupported conversion of that label into a biographical fact, diagnosis, historical act, or predicted conduct.

## Implemented correction

### 1. Deterministic morphology before interpretation

`szondi3.series_morphology.series_morphology_facts()` now exposes:

- exact series profile count;
- exact factor base-reaction frequencies;
- exact quantum/tension frequencies;
- real null reactions separately from forced complement nulls;
- exact vector-configuration frequencies for `S`, `P`, `Sch`, and `C`;
- undefined vector configurations when a forced null makes ordinary configuration coding invalid.

These facts are injected into the clinical series protocol before P2B/generative integration. The AI no longer needs to count a series visually.

### 2. Configuration-first synthesis policy

`szondi3.clinical_synthesis_policy.DEFAULT_CLINICAL_SYNTHESIS_POLICY` states the downstream rules explicitly:

- configuration before factor decomposition;
- deterministic counts only;
- preserve source-authorized Szondian vocabulary;
- do not equate `0` with absence;
- frequency is not the only interpretive weight;
- do not force contemporary “resources/vulnerabilities/regulation/autonomy/attachment” balancing language;
- consolidate epistemic caveats rather than repeating boilerplate;
- AI integrates authorized material; it does not invent doctrine.

### 3. Regression test

A ten-profile morphology regression test fixes the exact counts that were repeatedly mishandled by free prose generation, including the `P`, `Sch`, and `C` configuration distributions. A second test keeps forced null (`ø`) distinct from an ordinary `0`.

## Deliberately not implemented as a Fall 40 rule

The published Fall 40 meanings are not copied into universal executable doctrine merely because they occur in this case. In particular:

- repeated `s0` in Fall 40 must not become a universal rule `s0 = Sadismus`;
- the case-linked catastrophic/homicidal language attached to a rare Ego configuration must not replace or silently override broader source doctrine;
- the link between contact separation and aggressive/perverse sexuality must be formalized only when its source scope and conditions have been established.

The experiment identifies retrieval/formalization gaps; it does not license case-specific overgeneralization.

## Next five tests

The next independent cases should test whether the corrected system does four things better:

1. preserves exact morphology without counting errors;
2. recognizes authorized vector configurations before building factor narratives;
3. retains Szondi's own terminology without euphemistic modernization;
4. keeps strong source language testological unless the available evidence authorizes a stronger clinical inference.

The unit of success remains the quality and fidelity of the resulting clinical report, not the quantity of governance artifacts.
