# Clinical report composition reverse-engineering — reference case

**Status:** RESEARCH / GATE-1 PREPARATION — NOT A RUNTIME CONTRACT  
**Date:** 2026-09-15  
**Base:** `work/p2b-semantic-coverage-audit-001` @ `719de4461b4bf10609946d06c8f42305b0d6c3ef`  
**Reference profile:** `h- s+ e+ hy0 k+ p+ d- m-`  
**Vectors:** `S -+ | P +0 | Sch ++ | C --`

## 1. Purpose

This document tests, rather than assumes, the current architectural hypothesis:

> A clinically coherent Szondi report requires an explicit composition layer between active executable meanings and AI wording.

The immediate question is narrower:

> Can the manually successful reference report be decomposed into deterministic meanings, source-authorized relations, editorial organization, hypothetical illustration and interview translation without relying on hidden model knowledge or invented bridges?

This is the first Gate-1 specimen. One case can support or weaken the hypothesis, but cannot validate a general architecture.

### Hard scope

This document changes no runtime behavior. It changes no P1, P2A, P2B, scoring, claim activation, AI prompt, report schema, archive, renderer or manual. It creates no new executable claim and does not authorize `IC_SZONDI_PRIMARY_000088`.

The analytical relation IDs `AR-REF-*` and nucleus IDs `N-REF-*` below are **documentary aliases only**. They are not production identities and must not be consumed by runtime code.

---

## 2. Correction of reference IDs against the live matrix

Fresh inspection of the active branch is authoritative over earlier conversational shorthand. The current `docs/P2B_SEMANTIC_COVERAGE_MATRIX.md` maps the reference meanings as follows:

| Analytical alias | Live executable route | Trigger | Current executable meaning | Critical boundary |
|---|---|---|---|---|
| `M-PPLUS` | `IC_SZONDI_PRIMARY_000008` | factor `p+` | Inflation -> Verdoppelung / Vollkommenheit / Allessein | factor meaning; no global grandiosity diagnosis |
| `M-KPLUS` | `IC_SZONDI_PRIMARY_000009` | factor `k+` | Introjektion -> Einverleibung / Inbesitznahme / Alleshaben | no automatic concrete possession or biography; semantic reserve remains B1 |
| `M-ID` | `IC_SZONDI_PRIMARY_000038` | ordinary `-m/+k` | introjektive Identifizierung; Einverleibung; Identifizierung != Identitaet | no proof of actual biographical loss; richer adjacent doctrine remains outside current claim |
| `M-INTROINFL` | `IC_SZONDI_PRIMARY_000042` | ordinary `Sch ++` | Introinflation / kollektive Introinflation | Persona/Allessein/reality branches require their own support |
| `M-PERSONA` | `IC_SZONDI_PRIMARY_000073` | ordinary `Sch ++` | Persona via kollektive Introinflation; Allessein requires source-grounded Deflation/reality relation | no proof of completed Persona or successful Deflation |
| `M-CONTACT` | `IC_SZONDI_PRIMARY_000078` | ordinary `C --` plus ordinary `Sch 0+` or `Sch ++` | narcissistic forms of Ego protection occur most often in the specified contact configuration | source context cannot select a specific incest/bisexual/inverted/perverse branch |
| `G-MOSAIC` | `IC_SZONDI_PRIMARY_000019` | interpretation guard | anti-Mosaikspiel: isolated meanings remain general/abstract until source-grounded correlation | no invented interfactorial/intervectorial synthesis |
| `G-WHOLE` | `IC_SZONDI_PRIMARY_000014` | series/profile method guard | a profile is a current existence/fate possibility and is interpreted as a whole | no exhaustive person description or diagnosis from one profile |

This correction matters. The architecture must be derived from the live executable catalogue, not from remembered numbering.

---

## 3. Primary-source anchors rechecked for this specimen

The source check was repeated against the project PDFs, not only against the report prose.

### 3.1 Elementary functions: `+p` and `+k`

**Szondi, _Ich-Analyse_, printed p. 160.**

The source defines:

- `+p` / Inflation as the elementary Ego striving toward doubling, perfection and `Allessein`;
- `+k` / Introjektion as the elementary Ego striving toward incorporation, taking possession, assimilation of value objects/value representations and `Alleshaben`.

This supports `M-PPLUS` and `M-KPLUS` as **atomic meanings**. It does not, by itself, authorize a causal relation between them.

### 3.2 Introjective identification: `-m/+k`

**Szondi, _Ich-Analyse_, printed pp. 196-197.**

The source explicitly states that identification is not equivalent to identity, places introjective identification on the process of introjection/incorporation, and gives the testological coupling `-m; +k` for the process under discussion.

This supports `M-ID` as an already-composite executable relation. It also gives a direct boundary against converting identification into a whole-person identity verdict.

### 3.3 Persona through introinflation: ordinary `Sch ++`

**Szondi, _Ich-Analyse_, printed pp. 372-374, especially p. 374.**

The source states that Personabildung can occur through collective introinflation `Sch = ++`; when collective inflation precedes it, introjection can contribute to Deflation. The success of this Deflation depends on the strength of the `stellungnehmendes Ich`, which narrows the `Allessein` claim and reduces it through adaptation to reality.

This supports the Persona/Deflation route represented in the live catalogue by `M-PERSONA`. It does **not** say that ordinary `Sch ++` proves that Deflation has succeeded in this person.

### 3.4 Contact blockage and narcissistic Ego protection

**Szondi, _Ich-Analyse_, printed pp. 358-359.**

In the section `Abwehrmechanismen mit Ich- und Kontaktreaktionen`, Szondi places incestuous, bisexual, inverted or perverse drive danger in the historical doctrinal context and states that with `Kontaktsperre` the most frequent Ego defenses are Inflation `Sch 0+` and Introinflation `Sch ++`; both are called narcissistic forms of Ego protection.

This supports `M-CONTACT` and its hard historical vocabulary. The source relation is between a contact configuration and named forms of Ego protection; it does not select one sexual branch as a person-level fact.

---

## 4. Minimal candidate composition model for the reference case

The reference report appears to require three clinical nuclei. At this stage these are analysis objects, not production objects.

### `N-REF-01` — appropriation, expansion and limit

**Members / explanatory inputs**

- `M-KPLUS` / `000009` — Introjektion / Alleshaben;
- `M-PPLUS` / `000008` — Inflation / Allessein;
- `M-INTROINFL` / `000042` — ordinary `Sch ++` / Introinflation;
- `M-PERSONA` / `000073` — ordinary `Sch ++` / Persona-Deflation-Stellungnahme route.

**Authorized bridges**

- `AR-REF-001`: ordinary `Sch ++` authorizes the joint configuration of introjection and inflation under `Introinflation`;
- `AR-REF-002`: ordinary `Sch ++`, on the Persona route, authorizes discussion of `Allessein -> Deflation -> Stellungnahme/reality` while leaving success/failure open.

**Forbidden promotions**

- grandiosity diagnosis;
- delusion of grandeur;
- loss of reality contact as an observed fact;
- completed/mature Persona;
- successful or failed Deflation asserted as fact;
- invented biography explaining why the configuration exists.

### `N-REF-02` — introjective identification

**Member**

- `M-ID` / `000038`.

**Authorized relation**

- `AR-REF-003`: `-m/+k` -> introjective identification / incorporation; identification != global identity.

**Forbidden bridge**

The shared `+k` does not authorize `N-REF-02 -> N-REF-01`, nor the reverse. Introjective identification does not automatically cause Introinflation.

### `N-REF-03` — contact blockage and narcissistic Ego protection

**Member**

- `M-CONTACT` / `000078`.

**Authorized relation**

- `AR-REF-004`: ordinary `C --` with ordinary `Sch ++` -> Kontaktsperre associated, in Szondi's wording, most frequently with narcissistic forms of Ego protection; historical danger vocabulary remains contextual rather than person-selecting.

**Forbidden bridges**

- `N-REF-01 -> N-REF-03` as cause;
- `N-REF-02 -> N-REF-03` as cause;
- modern narcissistic diagnosis;
- inferred sexual orientation, sexual conduct or specific perversion.

---

## 5. Statement-level anatomy of the reference report

### Status vocabulary

- `DETERMINISTIC` — direct rendering of an active executable meaning/boundary.
- `AUTHORIZED_COMPOSITION` — combines multiple meanings only through a source-authorized executable relation.
- `EDITORIAL` — organizes the report or compares supported items without asserting a new person-level mechanism.
- `HYPOTHETICAL_EXAMPLE` — concrete illustration that must remain visibly hypothetical.
- `INTERVIEW_QUESTION` — converts an authorized meaning/open branch into something to investigate.
- `UNAUTHORIZED` — crosses the semantic ceiling or implies a bridge not supported by the current executable/source relation.

A separate `verdict` is used because an `EDITORIAL` sentence can still be too suggestive and require rewriting.

| ID | Report proposition / function | Active meanings | Relation / composition type | Status | Verdict | Reason / boundary |
|---|---|---|---|---|---|---|
| `R01` | The profile contains three distinct interpretive nuclei: Sch++, introjective identification, and C--/Sch++. | N1, N2, N3 | `EDITORIAL_CLUSTERING` | `EDITORIAL` | KEEP | This describes the structure of the available interpretation; it does not assert that the three mechanisms form one psychodynamic mechanism. |
| `R02` | One nucleus is more internally articulated than the others. | N1 | `EDITORIAL_RANKING` | `EDITORIAL` | KEEP WITH WORDING GUARD | This may describe **available semantic articulation**, not clinical dominance, severity or centrality of the person. Avoid `dominant`, `core personality`, or numeric support unless a separate scoring contract exists. |
| `R03` | The three nuclei form a coherent field around what is taken in, made one's own, expanded, limited and protected. | N1, N2, N3 | attempted thematic bridge | `UNAUTHORIZED` | REWRITE | `preluat/facut propriu/extins/limitat` is grounded mainly in N1/N2; `protejat` imports N3 and makes the set sound like one mechanism. Coherence is literary, not currently source-authorized. Keep the nuclei separate or mark this only as a reading map, not a person-level dynamic. |
| `R04` | `+k` means introjection: incorporation, appropriation/taking possession, making something one's own. | `M-KPLUS` | `ATOMIC_MEANING` | `DETERMINISTIC` | KEEP | Supported by `000009` and the elementary-function source. Avoid turning it into a concrete possession history. |
| `R05` | `+p` means inflation: doubling, perfection, totality / `Allessein`. | `M-PPLUS` | `ATOMIC_MEANING` | `DETERMINISTIC` | KEEP | Supported by `000008`. Do not promote factor meaning to global grandiosity diagnosis. |
| `R06` | In ordinary `Sch ++`, `+k` and `+p` are not merely adjacent; the configuration is Introinflation. | `M-KPLUS`, `M-PPLUS`, `M-INTROINFL` | `EXACT_CONFIGURATION_RELATION`; `AR-REF-001` | `AUTHORIZED_COMPOSITION` | KEEP | This is the clearest example of the composition layer: the bridge is supplied by executable/source doctrine, not by coexistence. |
| `R07` | What is introjected can participate in Ego expansion within the Introinflation configuration. | N1 | paraphrase of `AR-REF-001` | `AUTHORIZED_COMPOSITION` | KEEP WITH WORDING GUARD | Safe only when explicitly anchored to `Sch ++`/Introinflation. It must not be emitted from `+k` alone. |
| `R08` | A role, idea, competence or possibility may be taken up and become disproportionately totalizing. | N1 | `HYPOTHETICAL_INSTANTIATION` | `HYPOTHETICAL_EXAMPLE` | KEEP WITH HYPOTHETICAL MARKER | These are invented ordinary-life examples, not test facts. Wording must use `de pilda`, `ar putea`, `s-ar putea`, etc. |
| `R09` | The configuration does not by itself establish grandiosity, delusion or loss of reality. | `M-PPLUS`, `M-INTROINFL`, `M-PERSONA` | `SOURCE_BOUNDARY` | `DETERMINISTIC` | KEEP | Protects against overpromotion of historical/pathological neighbors. |
| `R10` | Ask whether an important acquisition remains delimited or starts to occupy too much of the Ego image. | N1 | `INTERVIEW_TRANSLATION` | `INTERVIEW_QUESTION` | KEEP | It operationalizes the authorized expansion/limit problem; it does not assert the answer. |
| `R11` | The same ordinary `Sch ++` route opens the problem of limit/Deflation and Stellungnahme. | `M-PERSONA` | `EXACT_CONFIGURATION_RELATION`; `AR-REF-002` | `DETERMINISTIC` / `AUTHORIZED_COMPOSITION` | KEEP | This is not imported from generic psychotherapy; it is source-grounded in the Persona-through-Introinflation route. |
| `R12` | `Allessein` must be narrowed through Deflation by a Stellung-taking Ego in relation to reality. | `M-PERSONA` | `DEVELOPMENTAL_RELATION`; `AR-REF-002` | `DETERMINISTIC` | KEEP | Preserve the source's route and conditions; do not claim the person has completed it. |
| `R13` | “What happens when reality says: up to here?” | `M-PERSONA` | `INTERVIEW_TRANSLATION` | `INTERVIEW_QUESTION` | KEEP | A clinically useful translation of the Deflation/Stellungnahme question. It must remain a question, not evidence of poor limit tolerance. |
| `R14` | Two outcomes remain open: realistic limitation versus persistence of the totalizing claim. | `M-PERSONA` | `DEVELOPMENTAL_BIFURCATION` | `AUTHORIZED_COMPOSITION` | KEEP WITH SOURCE STRENGTH | The source describes success as dependent on the strength of the Stellung-taking Ego and describes the danger of failure. The report must not choose a branch for the person. |
| `R15` | `-m/+k` gives introjective identification. | `M-ID` | `AUTHORIZED_INTERFACTOR_RELATION`; `AR-REF-003` | `DETERMINISTIC` | KEEP | The executable claim already contains the relation; the writer need not infer it. |
| `R16` | Identification is not identity; the formula does not define the whole person. | `M-ID` | `SOURCE_BOUNDARY` | `DETERMINISTIC` | KEEP | Direct source/executable boundary. |
| `R17` | Example: admiration is not yet introjective identification; a quality becomes explanatory only when it is actually taken up/incorporated. | `M-ID` | `HYPOTHETICAL_INSTANTIATION` | `HYPOTHETICAL_EXAMPLE` | KEEP WITH HYPOTHETICAL MARKER | Useful contrast. The specific admired quality/person must never be asserted as actual biography. |
| `R18` | The fact that N1 and N2 share `+k` does not mean introjective identification causes Introinflation. | N1, N2, `G-MOSAIC` | `NO-BRIDGE_ASSERTION` | `DETERMINISTIC` | KEEP | This is the anti-Mosaikspiel rule applied concretely. Shared constituent != authorized causal bridge. |
| `R19` | We may notice a recurring theme of “appropriation”, but not infer causality between N1 and N2. | N1, N2 | `EDITORIAL_COMPARISON` + `NO-BRIDGE_ASSERTION` | `EDITORIAL` | KEEP WITH BOUNDARY | Similar wording is a comparison of meanings, not a new mechanism. The no-causality clause is essential. |
| `R20` | `C --` with ordinary `Sch ++` is linked to Kontaktsperre and narcissistic forms of Ego protection. | `M-CONTACT` | `AUTHORIZED_INTERVECTOR_RELATION`; `AR-REF-004` | `DETERMINISTIC` | KEEP | The relation is already executable in `000078`; no writer-created bridge is required. |
| `R21` | “Narcissistic” predicates the source-described form of Ego protection, not a modern global diagnosis of the person. | `M-CONTACT` | `SOURCE_BOUNDARY` | `DETERMINISTIC` | KEEP | Controls predication without euphemizing the historical term. |
| `R22` | Example: in a difficult moment the person might reduce exchange, withdraw from interaction and rely more on internal organization. | `M-CONTACT` | `HYPOTHETICAL_INSTANTIATION` | `HYPOTHETICAL_EXAMPLE` | REWRITE NARROWER | `contact blockage` supports an example of interruption/closure of contact. `rely more on internal organization` adds an explanatory move not explicitly needed by `000078`; omit unless independently authorized. |
| `R23` | The doctrinal context names incestuous, bisexual, inverted or perverse drive danger. | `M-CONTACT` | `HISTORICAL_SOURCE_CONTEXT` | `DETERMINISTIC` | KEEP | Hard terms should not be softened when source-relevant. |
| `R24` | The formula does not establish the person's orientation, conduct, desire or diagnosis and cannot select one of those branches. | `M-CONTACT` | `SOURCE_BOUNDARY` | `DETERMINISTIC` | KEEP | Explicit critical boundary of `000078`. |
| `R25` | “How is what becomes one's own managed?” as the global clinical question. | N1, N2, N3 | attempted global thematic synthesis | `UNAUTHORIZED` | REWRITE | The question elegantly binds N1/N2, but N3 is not source-linked to “what becomes one's own”. If used globally it risks making contact protection a consequence of appropriation. Restrict it to N1/N2 or present N3 as a separate line of inquiry. |
| `R26` | Some things may be introjected; some may support Ego expansion; some may be taken from others by introjective identification; separately, contact may become blocked under a narcissistic Ego-protection configuration. | N1, N2, N3 | `EDITORIAL_CLUSTERING` with explicit separation | `EDITORIAL` | KEEP | Safe because it enumerates supported nuclei and marks the contact route as separate rather than causal. |
| `R27` | This organization is not a single psychodynamic causality; introjection is not said to cause contact blockage, identification is not said to cause narcissistic protection, and Ego expansion is not said to explain the contact vector. | N1, N2, N3, `G-MOSAIC` | `NO-BRIDGE_ASSERTION` | `DETERMINISTIC` / `EDITORIAL` | KEEP | This is the crucial boundary that allows a coherent report without a fabricated whole-person mechanism. |
| `R28` | `Sch ++` is the most internally articulated nucleus in this specimen because the executable material includes both Introinflation and Persona/Deflation routes. | N1 | `EDITORIAL_RANKING` | `EDITORIAL` | KEEP WITH PRECISE WORDING | This is a property of **available authorized semantic richness**, not a deterministic support score or claim that Sch++ is the person's central conflict. |
| `R29` | “The profile raises the problem of how the Ego appropriates, expands and limits what it makes its own, while two other configurations separately open identification-through-taking-up and Ego protection through contact blockage.” | N1, N2, N3 | `EDITORIAL_META_SUMMARY` | `EDITORIAL` | KEEP | This is the strongest safe global sentence found so far because it gives N1 a composed formulation while explicitly keeping N2 and N3 separate. It is a report-map statement, not a new inter-nucleus mechanism. |
| `R30` | Explore concrete episodes of investment, limit, reduction/redefinition, and whether one role/acquisition becomes overly defining. | N1 | `INTERVIEW_TRANSLATION` | `INTERVIEW_QUESTION` | KEEP | Questions test the N1 bifurcation against independent clinical material. |
| `R31` | Explore what qualities/modes are taken from others and distinguish admiration, imitation and incorporation. | N2 | `INTERVIEW_TRANSLATION` | `INTERVIEW_QUESTION` | KEEP | Directly operationalizes introjective identification. |
| `R32` | Explore what precedes contact blockage and what function the interruption has. | N3 | `INTERVIEW_TRANSLATION` | `INTERVIEW_QUESTION` | KEEP WITH CAUTION | Asking what precedes/what function it has is legitimate inquiry; the answer must come from interview/context, not be back-filled by test theory. |
| `R33` | The profile does not establish biography, diagnosis, global personality structure, sexual orientation/conduct, grandiosity, reality loss, or success/failure of Deflation. | N1, N2, N3 | `GLOBAL_BOUNDARY` | `DETERMINISTIC` | KEEP | Compresses already-supported anti-inferences without creating a new positive meaning. |
| `R34` | The report yields “a map of places worth investigating.” | N1, N2, N3 | `EDITORIAL_META_SUMMARY` | `EDITORIAL` | KEEP | This describes appropriate clinical use of the test output, not a person-level fact. |

---

## 6. What the anatomy actually shows

### 6.1 The composition hypothesis survives the first specimen — but in a narrower form than initially imagined

The reference case does require composition, but most legitimate composition is **already partly encoded in executable P2B claims**:

- `000038` already encodes the `-m/+k` relation;
- `000042` already encodes ordinary `Sch ++ -> Introinflation`;
- `000073` already encodes the Persona/Deflation route for ordinary `Sch ++`;
- `000078` already encodes `C -- + Sch 0+/++ -> Kontaktsperre / narcissistic Ego protection`.

The main missing operation is therefore not necessarily “discover arbitrary relations among all findings”. In this specimen it is more specific:

> **Expose the semantic topology between composite executable claims and the atomic meanings that explain their constituents, then build a nucleus from those already-authorized relations.**

For N1, the writer needs `+k` and `+p` as explanatory components, but it may join them only because `000042` supplies the exact Sch++ bridge. `000073` then extends that same exact configuration with the Persona/Deflation route.

This suggests that a full universal `ClinicalMeaningGraph` may be unnecessary. A smaller typed **composition/dependency layer over P2B** may be sufficient.

### 6.2 `ClinicalReportPlan` is safe but not semantically complete for narrative composition

The current planner groups by exact deterministic support-fact set. That protects provenance. It also means:

- atomic `+p` and `+k` meanings remain separate plan units;
- the ordinary `Sch ++` routes can form a same-fact-bundle unit;
- the contact and identification relations remain other units.

For a clinical explanation, however, the Sch++ nucleus benefits from showing what `+k` and `+p` mean before explaining what their configured relation means. The planner does not currently express this **constituent/explanatory dependency**.

This is a more precise diagnosis than “V4 needs a graph”.

### 6.3 A second missing category is editorial meta-synthesis

The anatomy found an important distinction that the earlier architecture did not make explicitly.

A sentence can mention several independent nuclei without claiming a new psychological relation if it is clearly a statement about the **map of the report**:

> N1 raises X, while N2 and N3 separately open Y and Z.

This is not the same as:

> N1 causes N2 and N3, or all three are one mechanism.

Therefore future architecture probably needs to distinguish:

1. **semantic composition** — requires an authorized relation;
2. **editorial clustering/meta-summary** — may enumerate independent nuclei but must not predicate a new mechanism of the person;
3. **psychodynamic synthesis** — forbidden unless explicitly authorized.

If every multi-nucleus sentence is forced to cite one semantic nucleus, V4 remains too restrictive. If every multi-nucleus sentence is freely allowed, anti-Mosaikspiel collapses. The missing distinction is **propositional role**, not merely paragraph `kind`.

### 6.4 The manual “gold” report was useful but not infallible

The reverse-engineering exercise found two attractive formulations that should **not** be promoted as reference-safe in their current wording:

- `R03`: the claim that all three nuclei form one coherent field of what is “taken in, made one's own, expanded, limited and protected”;
- `R25`: the global question “How is what becomes one's own managed?” when applied implicitly to N3 as well.

Both are clinically elegant, but they risk smuggling N3 into an appropriation-centered mechanism for which the current source/executable layer supplies no bridge.

This is a positive result of the method: the architecture is not being reverse-engineered merely to justify prose we already like. The prose itself is being audited and revised where needed.

### 6.5 The safest strong synthesis is asymmetrical

The strongest safe global formulation found in this case is asymmetrical:

> The profile raises the problem of how the Ego appropriates, expands and limits what it makes its own, **while two other configurations separately open** the theme of identification through taking-up and the theme of Ego protection through contact blockage.

Why this works:

- N1 receives true internal semantic composition;
- N2 and N3 remain independent;
- the sentence still reads as one clinical overview;
- no unsupported inter-nucleus causality is created.

This may be a reusable narrative pattern, but Gate 1 must test it on other profiles before it becomes a contract.

---

## 7. Provisional type system suggested by this specimen

The anatomy does **not** yet justify implementation. It does suggest a smaller candidate type system for further testing:

### Meaning nodes

- `ATOMIC_MEANING`
- `COMPOSITE_EXECUTABLE_MEANING`

### Relation / dependency edges

- `CONSTITUENT_EXPLAINS_COMPOSITE`
- `EXACT_CONFIGURATION_AUTHORIZES_RELATION`
- `SAME_TRIGGER_EXTENDS_MEANING`
- `NO_BRIDGE`

### Narrative roles

- `SEMANTIC_ASSERTION`
- `EDITORIAL_META_SUMMARY`
- `HYPOTHETICAL_INSTANTIATION`
- `INTERVIEW_TRANSLATION`
- `BOUNDARY`

This is intentionally smaller than a general ontology.

For the reference case, a possible dependency view is:

```text
000009 (+k atomic) ----\
                        >---- 000042 (Sch++ Introinflation) ----\
000008 (+p atomic) ----/                                      \
                                                               >---- N-REF-01
000073 (Sch++ Persona/Deflation) -----------------------------/

000038 (-m/+k introjective identification) ------------------------ N-REF-02

000078 (C-- + Sch++ contact / narcissistic protection) ------------ N-REF-03

NO-BRIDGE: N-REF-01 <X> N-REF-02
NO-BRIDGE: N-REF-01 <X> N-REF-03
NO-BRIDGE: N-REF-02 <X> N-REF-03
```

The important point is that the relation nodes are not invented by the writer: the live P2B routes provide them.

---

## 8. Implications for a future validator

This specimen weakens the idea that `SYNTHESIS / EXPLANATION / EXAMPLE / CONTRAST / LIMIT` should be the primary safety grammar.

The more important questions are:

1. Is this proposition a semantic assertion or a report-meta assertion?
2. If semantic, which active executable meaning or authorized nucleus supports it?
3. If it combines constituents, which executable relation authorizes the combination?
4. If it spans nuclei, is it merely enumerating/reporting them, or claiming a new person-level relation?
5. Does it import a forbidden inference?
6. If it is an example, is hypothetical status visible?
7. If it is an interview question, does it ask for missing evidence rather than presuppose it?

A future semantic validator should therefore validate **proposition role + support topology**, not just prose category.

---

## 9. What this case supports

This first specimen supports the following propositions provisionally:

1. **A composition layer is useful**, because the report must know that `+k` and `+p` may be explained together under ordinary Sch++ only through the Introinflation route.
2. **The layer may be smaller than a full graph ontology.** Much of the clinically important relational meaning already exists as composite P2B claims.
3. **Composite claims need explicit links to their explanatory constituents.** This is what the current report plan does not encode.
4. **Editorial multi-nucleus prose must be modeled separately from semantic multi-nucleus synthesis.** Otherwise the system is either too rigid (V4) or too permissive (Mosaikspiel).
5. **The manual report can itself contain over-integration.** Reverse-engineering must be allowed to reject attractive sentences.
6. **Clinical coherence does not require one whole-person causal story.** It can be achieved by one internally composed nucleus plus clearly separated secondary nuclei and good editorial framing.

---

## 10. What this case does not prove

This specimen does **not** establish that:

- every profile naturally decomposes into 2-4 nuclei;
- ordinary Sch/vector relations are representative of the whole Szondi system;
- the same dependency types cover series-level, quantum, E.K.P., foreground/background or index-based interpretations;
- a graph is the best implementation structure;
- a deterministic nucleus builder can be complete;
- AI semantic validation is solved;
- the current reference report is a universal template;
- N1 is clinically dominant in the person;
- a support percentage can be assigned;
- V4 should be re-enabled or promoted.

---

## 11. Gate-1 next requirement

Before any runtime implementation, repeat the same anatomy on **2-3 deliberately divergent profiles**.

The next profiles must be chosen to stress different failure modes, not to make the hypothesis look good. At minimum the set should include:

1. a case with several active meanings but **few/no authorized bridges**;
2. a case where a **different exact vector/intervector relation** supplies a legitimate composition;
3. a case with **sensitive/hard historical vocabulary or quantum conditions**, so the composition layer must preserve scope and source strength.

For each case, create the same statement-level mapping and ask:

- Do `ATOMIC -> COMPOSITE -> NUCLEUS` dependencies recur?
- Do the same narrative roles recur?
- Are new relation types genuinely general, or case-specific patches?
- Can the deterministic nucleus dump be clinically intelligible without AI?

### Gate-1 success criterion

Proceed to a minimal composition contract only if a small, recurring set of relation/dependency types explains the three/four cases without encoding the final prose by hand.

### Kill criterion

Stop this direction if:

- each case needs bespoke relations that merely restate the desired report;
- most clinically useful integration still comes from unsourced writer inference;
- editorial framing cannot be cleanly separated from semantic assertion;
- a nucleus object becomes a hand-written report in structured form;
- preserving scope/quantum/source modality makes the composition model unusably complex.

---

## 12. Decision at the end of specimen 1

**Result: CONTINUE TO GATE-1 CROSS-CASE TESTING — DO NOT IMPLEMENT YET.**

The specimen does not validate a `ClinicalMeaningGraph`. It does, however, identify a concrete and narrower missing structure:

> **a typed topology connecting atomic P2B meanings, already-composite executable relations, explicit no-bridge boundaries, and editorial meta-synthesis.**

This is enough to justify the next research step, but not enough to justify a new runtime subsystem.

The next work item is therefore not V5 and not a prompt change. It is selection and reverse-engineering of the divergent Gate-1 control profiles.
