# SZONDI3 — CLINICAL GROUNDING FOUNDATION

**Status:** ACTIVE CLINICAL ARCHITECTURE / SUCCESSION ANCHOR  
**P3/P4 foundation merge:** PR #62 -> `a03910465839aea1e226526f2b5f3e7aa32116aa`  
**Purpose:** maintain the smallest durable P3/P4 foundation required for a source-grounded AI-assisted clinician report without creating a second epistemic system beside Szondi3.

## 1. Core invariant

Cabinet Alpha already proved:

`administration -> P1 deterministic calculation -> P2B approved findings -> structured clinical report`

A general LLM can nevertheless recount a series incorrectly, confuse doctrinal levels, import Szondi meanings from pretraining, or convert co-occurrence into a plausible causal story. The grounding workstream therefore adds one invariant before narrative generation:

> **No new Szondian clinical information may originate in the narrative model.**

The model may organize and express an already grounded clinical object. Szondi3 remains responsible for the clinical knowledge supplied to it.

## 2. Minimal architecture

The working clinical path is:

`Administration -> P1 -> P2B -> P3 Clinical Evidence -> P4 Clinical Integration -> narrative model -> clinician working report -> manual therapist synthesis`

P3 and P4 are ordinary Python data structures. They are epistemic layers, not infrastructure products.

Explicitly **not** required for the first grounded vertical slice:

- graph database;
- RDF/OWL or a second ontology;
- vector database;
- generic RAG framework;
- rule-engine framework;
- separate narrative-packet service;
- extra CI workflow;
- second reporting system.

Complexity may be added only after a demonstrated clinical/software failure requires it.

## 3. P3 — Clinical Evidence — MERGED

Module: `szondi3/clinical_evidence.py`

P3 consumes one existing `ClinicalProtocolEvaluation` and adds only information that downstream synthesis must not be allowed to recalculate or invent.

### 3.1 `FactorSeriesPattern`

For every factor `h s e hy k p d m`, P3 records:

- exact ordered P1 symbols including quantum marks;
- base reactions;
- one-based profile positions for positive, negative, null and ambivalent reactions;
- forced-null positions separately;
- profiles carrying quantum tension;
- total quantum units;
- actual longitudinal base-reaction transitions.

These are deterministic observations of the already scored series. They are not Szondian interpretations. Their immediate purpose is to prevent a language model from recounting the protocol itself.

### 3.2 `GroundedFinding`

Every activated P2B finding receives a case-local evidence ID, for example:

- `EF_P01_IC_SZONDI_PRIMARY_000010`
- `EF_SERIES_IC_SZONDI_PRIMARY_000003`

The wrapper preserves the existing P2B finding, including doctrine IDs, source IDs, assertion mode, lifecycle status, source-strength note, sensitive-domain flags and anti-inferences.

### 3.3 `GroundingBoundary`

P3 makes downstream gaps explicit:

- unresolved deterministic calculations;
- unresolved P2B input;
- missing P2B context;
- blocked source conflict/rule.

A later model must not use general knowledge to fill one of these boundaries.

## 4. P4 — Clinical Integration — MERGED

Module: `szondi3/clinical_integration.py`

The first relation vocabulary is intentionally restricted to:

- `COEXISTENCE`
- `CONTRAST`
- `LONGITUDINAL_CHANGE`
- `QUALIFICATION`

There is deliberately no `CAUSES` relation.

Repeated co-occurrence or temporal succession in a Szondi series does not by itself license a claim that one drive configuration caused another. Causal integration may be introduced only if a later source-grounded, reviewed rule demonstrates the exact authorization required.

The only automatically generated relation is within-factor `LONGITUDINAL_CHANGE`, and only where P3 contains an actual base-reaction transition. No cross-factor psychological synthesis is generated automatically.

A future reviewed `IntegrationRelation` must reference support IDs actually present in the same P3 object; orphan support fails closed.

## 5. Direct grounding contract for AI

`ClinicalIntegration.to_grounding_payload()` is the direct first contract for a future narrative model.

It contains:

- deterministic factor-series patterns;
- activated P2B findings;
- full P2B provenance and anti-inference constraints;
- explicit grounding boundaries;
- typed P4 relations.

There is intentionally no separate `NarrativePacket` subsystem. The payload does **not** contain or create therapist synthesis. `TherapistSynthesis` remains `MANUAL_CLINICIAN_INPUT_ONLY`.

## 6. P3/P4 foundation acceptance

PR #62 merged the minimal foundation to `main` as:

`a03910465839aea1e226526f2b5f3e7aa32116aa`

Post-merge verification was green for:

- foundation verification;
- runtime unittest suite;
- canonical access;
- doctrine registry/transversal validation;
- source inspection.

The P3/P4 foundation itself is therefore complete. This does **not** mean complete P3/P4 clinical coverage; it means the narrow architecture is now durable and successors should extend it rather than replace it.

## 7. Active Fall40 P2B tranche

Development branch:

`work/fall40-p2b-grounding-001`

The first Fall40-driven expansion adds ten source-grounded candidate claims, `IC_SZONDI_PRIMARY_000013–000022`. They are intentionally `FORMALIZATION_REVIEWED`, **not** `APPROVED`. Preview/review may expose them; production mode excludes them until explicit clinician review.

The tranche is deliberately limited to primary-source material already represented and `SOURCE_VERIFIED` in the doctrine registry:

| Claim | Grounded meaning / safeguard | Primary doctrine |
|---|---|---|
| `000013` | no factor interpretation without its Partnerfaktor constellation | `DR_SZ_LEHR_1972_000129` |
| `000014` | `!` = Überdruck/Hypertonie, not an independent diagnosis | `DR_SZ_LEHR_1972_000145` |
| `000015` | `+h` = affirmation of Eros/Liebe/Bindungsbedürfnis | `DR_SZ_LEHR_1972_000157`, `000171` |
| `000016` | `+h!` = Eroshypertonie | `DR_SZ_LEHR_1972_000171` |
| `000017` | `-e` belongs to Kain direction; no epilepsy/criminality verdict from sign alone | `DR_SZ_LEHR_1972_000259`, `000261` |
| `000018` | `-e!` = source-described threatening accumulation of grobe Affekte / paroxysmal discharge possibility, partner-sensitive and non-diagnostic alone | `DR_SZ_LEHR_1972_000260` |
| `000019` | `-hy` = Verbergungsdrang | `DR_SZ_LEHR_1972_000262` |
| `000020` | `+d` = Veränderung / Auf-Suche-Gehen | `DR_SZ_LEHR_1972_000293` |
| `000021` | `-m` = Loslösung / Abtrennung / Freiheit; explicit block against semantic reversal | `DR_SZ_LEHR_1972_000294` |
| `000022` | `0s` = actual relative diminution, interpreted relative to h; not absolute absence | `DR_SZ_LEHR_1972_000193` |

The existing twelve Cabinet Alpha claims remain `APPROVED` and unchanged in production status.

## 8. Fall40 deterministic development fixture

Fixture:

`tests/fixtures/fall40_deidentified_series.json`

Status encoded in the fixture:

`DEIDENTIFIED_DEVELOPMENT_FIXTURE_NOT_DOCTRINAL_AUTHORITY`

It contains only the ten scored factor-reaction profiles. It deliberately excludes the long narrative reports produced by unconstrained language models.

The explicit development series is:

```text
I    h+!  s0  e0  hy-   k-  p±  d+  m-
II   h+!  s0  e-  hy-   k-  p+  d+  m-
III  h+   s0  e-  hy-   k+  p+  d+  m-!
IV   h+!  s0  e-  hy-   k+  p±  d+  m-
V    h+   s0  e0  hy-   k+  p±  d+  m-!!
VI   h+!  s0  e-  hy-!  k+  p±  d+  m-!
VII  h+!  s-  e-  hy0   k+  p+  d+  m-!
VIII h+!  s0  e-  hy-   k+  p±  d+  m-!
IX   h+   s0  e-  hy-   k+  p±  d+  m-!
X    h+   s0  e-  hy0   k±  p±  d+  m-!
```

Important reconstruction rule: when an AI narrative count disagreed with an explicit per-profile sequence, the explicit sequence was retained. This matters immediately for `h`: one prose summary said five tensioned `+h` reactions, while the explicit sequence contains **six** (`I, II, IV, VI, VII, VIII`). P3 tests the sequence and obtains the count; no model is allowed to recount it.

Deterministic fixture invariants now tested include:

- `h` positive in all ten; six tensioned profiles; quantum total 6;
- `s`: nine `0`, one `-` at VII;
- `e`: `0` at I/V, `-` in the other eight;
- `hy`: `0` at VII/X, `-!` at VI, otherwise `-`;
- `k`: `-, -, +, +, +, +, +, +, +, ±` with transitions at III and X;
- `p`: `±, +, +, ±, ±, ±, +, ±, ±, ±`;
- `d+` constant in all ten;
- `m-` constant in all ten, quantum total 8, including `m-!!` at V.

This fixture is **not** to be conflated with the historical case numbered Fall40 in Triebpathologie. Its role is solely the de-identified development protocol used to challenge grounding.

## 9. What the Fall40 tests now protect

`tests/test_fall40_p2b_grounding.py` checks both atomic semantics and the full fixture path:

- candidate lifecycle cannot silently become production approval;
- every executable claim must resolve to current `SOURCE_VERIFIED` doctrine;
- partner-factor and quantum safeguards activate from explicit facts;
- `+h` and `+h!` remain distinct;
- `-e` retains Kain terminology while blocking epilepsy/criminality overreach;
- `-hy` retains Verbergungsdrang;
- `+d` retains Auf-Suche-Gehen;
- `-m` retains Loslösung/Abtrennung/Freiheit and explicitly blocks the previously observed reversal into “incapacitate de desprindere”;
- `0s` remains relative and partner-bound;
- preview can expose the tranche, production cannot;
- P3 reproduces the exact ten-profile sequences and quantum totals;
- P4 payload carries doctrine provenance and anti-inferences;
- P4 contains no causal relation.

Narrative outputs from earlier LLM experiments remain adversarial evidence only. Their attractive synthetic statements are not imported as doctrine or integration rules.

## 10. Anti-dinosaur budget

Until the Fall40 grounded narrative vertical slice has been demonstrated, the following budget remains binding:

1. only `clinical_evidence.py` and `clinical_integration.py` are P3/P4 runtime modules;
2. no new external runtime dependency;
3. no new database;
4. no second ontology or semantic type system unless a measured grounding failure demonstrates the need;
5. no additional CI workflow — use existing runtime tests;
6. no second report model;
7. no separate narrative-packet subsystem;
8. one narrative-model call is the default first experiment;
9. P2B grows from concrete clinical capability needs, not catalogue-size goals;
10. every new architectural component must answer a demonstrated failure that cannot be solved in an existing layer.

## 11. Validation required before a narrative model is clinically trusted

The future grounded narrative step must demonstrate:

- **counting:** P3 values, not LLM recounting, determine reported series facts;
- **provenance:** every Szondian proposition maps to supplied P2B/P4 support IDs;
- **ablation:** remove relevant executable support and the proposition disappears instead of returning from pretraining;
- **canary:** a controlled test-only meaning supplied through grounding is followed;
- **mutation:** controlled support change changes narrative predictably;
- **boundary:** unresolved/missing support stays unresolved;
- **causality:** `COEXISTENCE`/`LONGITUDINAL_CHANGE` does not become an unsupported causal chain;
- **model swap:** changing narrative model may change wording/organization, not fundamental grounded content.

## 12. Next safe actions / succession

A successor should first verify current `main`, this active branch/PR, and CI independently. Then:

1. inspect `szondi3/clinical_evidence.py`, `szondi3/clinical_integration.py`, `szondi3/interpretation_catalogue.py`, `tests/test_clinical_grounding.py`, `tests/test_fall40_p2b_grounding.py`, and the Fall40 fixture;
2. preserve claims `000013–000022` as non-production until explicit clinician review;
3. run the existing runtime/provenance tests and repair any branch failure before merge;
4. merge the Fall40 tranche only if all repository checks remain green and the provenance contract holds;
5. after merge, perform clinician review of the candidate wording/scope as a separate lifecycle decision; do not bundle technical merge with clinical approval;
6. only then construct the first one-call narrative experiment from `ClinicalIntegration.to_grounding_payload()`;
7. before accepting narrative generation, implement/run ablation, canary, mutation, boundary and causality tests;
8. never use an unconstrained LLM interpretation as authority for a missing P2B meaning or P4 relation.

If interrupted, repository `main` plus the active branch/PR, tests and this file define the recoverable state. Chat memory is not required.

## Final invariant

> **Szondi3 produces the authorized clinical knowledge. A narrative model may express that knowledge; it may not become an unrecorded second source of Szondian doctrine.**
