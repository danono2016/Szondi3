# Szondi3 Clinical-AI Transfer Package — Continuation & Completion Manual

Status: **MANDATORY SUCCESSOR ENTRY POINT**  
Repository: `danono2016/Szondi3`  
Working branch: `work/ai-clinical-provenance-strategy-001`  
Prepared: **2026-08-30**  
Implementation checkpoint verified for the current executable catalogue: `ae1b070f63b65bb377f36c4c76adb18666a6eb46`  
Checkpoint commit message: `Update catalogue count regression`  
PR: **#65 — Build minimal provenance-constrained clinical evidence packet**  
At the checkpoint: **OPEN / DRAFT / MERGEABLE / NOT MERGED**  
Base: `main@d192c984eff9d753de4ee60955accec3d6252938`  
CI at the checkpoint: all five current PR workflows completed successfully; this is **not** a formal project gate.

> **Important:** this document may itself be committed after the implementation checkpoint above, so the branch head may become one documentation-only commit newer. A successor must re-verify the actual branch head, PR state, base, and CI before editing.

---

## 0. Read this first — takeover protocol for a new chat

A new chat must not reconstruct the project from generic Szondi knowledge, from model memory, from old reports, or from the PR description. It must begin by reading this file and then independently checking the repository.

Use this first message in the successor chat:

```text
Continuăm proiectul Szondi3 din repo danono2016/Szondi3, ramura
work/ai-clinical-provenance-strategy-001, PR #65.

Înainte de orice modificare:
1. citește integral docs/CHAT_TRANSFER_PACKAGE.md;
2. verifică independent head-ul actual al ramurii, main, starea PR #65 și CI;
3. verifică szondi3/interpretation_catalogue.py și nu presupune numărul sau sensul claim-urilor din memoria conversației;
4. tratează sursele canonice + doctrine registry + P2B executabil ca singura autoritate semantică pentru interpretări individuale;
5. dacă există contradicții între handoff, cod, PR, teste sau surse, oprește-te și prezintă contradicția înainte de orice schimbare ireversibilă;
6. nu face merge, nu marca PR ready și nu declara gate-uri formale fără acordul meu explicit.

Obiectivul este să continuăm și să ducem la bun sfârșit strategia Clinical-AI source-bounded, fără a mări libertatea semantică a LLM-ului. Începe prin a-mi spune starea verificată și care este următorul pas minim sigur.
```

If GitHub access is temporarily unavailable, upload this Markdown file to the new chat and instruct it to treat all commit/PR state as a **checkpoint requiring later verification**, not as current truth.

---

## 1. Mission of the project

The target is a Szondi clinical interpretation/report pipeline that is:

- faithful to Léopold Szondi's own method and terminology;
- deterministic wherever the test algebra is deterministic;
- source-grounded wherever meaning is clinical/interpretive;
- case-specific without invented biography, diagnosis, behavior, or psychodynamic bridges;
- auditable from every person-specific proposition down to facts and canonical evidence;
- fail-closed when the evidence does not authorize a conclusion;
- rich enough to be clinically useful **because P2B coverage becomes richer**, not because the model receives more interpretive freedom.

The project is deliberately not trying to create a general-purpose psychology RAG system or an autonomous AI diagnostician.

---

## 2. Absolute authority hierarchy

The non-negotiable hierarchy is:

```text
PRIMARY EVIDENCE
      ↓
DOCTRINE
      ↓
EXECUTABLE INTERPRETATION (P2B)
      ↓
SOFTWARE BEHAVIOR / MATERIALIZED FINDINGS
      ↓
AI SYNTHESIS / WORDING
```

The direction may **never** be reversed. In particular, this is forbidden:

```text
LLM intuition → search for a Szondi quote that appears to justify it
```

The correct sequence is:

```text
observed clinical/report gap
→ canonical source evidence
→ narrowly stated doctrine
→ reviewed executable claim
→ deterministic activation/regression
→ materialized evidence packet
→ AI wording
```

### Semantic admissibility theorem

A person-specific AI proposition is admissible only when its **entire clinical meaning** is already contained in one or more active P2B claims, whose predicates are satisfied by deterministic P1 facts and whose doctrine IDs resolve to canonical source evidence.

The model may paraphrase, order, connect sentences stylistically, and make the report readable. It may not add a new clinical relationship, diagnosis, motive, behavior, biography, prognosis, or causal bridge.

If a desired sentence cannot be traced downward to P1 facts and upward to P2B + doctrine, the sentence is not yet allowed.

---

## 3. What the AI is — and is not

The LLM is a **bounded formulator**.

It is **not**:

- the scorer of the Szondi test;
- an authority on Szondi doctrine;
- a substitute for source review;
- a free clinical interpreter;
- a diagnostic engine;
- a validator of its own output;
- a mechanism for repairing `UNRESOLVED` source evidence;
- a source of person-specific meaning from pretraining or web search.

Runtime Szondi meaning comes from the closed evidence packet, not from model memory or external browsing.

The local deterministic validator remains authoritative over what the model output is structurally permitted to contain.

---

## 4. Source and doctrine rules

### 4.1 Canonical source layers

Canonical source files live under `sources/originals/`. Doctrine objects live under `doctrine/registry/` and point back to canonical source anchors. Primary Szondi sources currently include, among others:

- `SZ_LEHR_1972` — *Lehrbuch der experimentellen Triebdiagnostik*;
- `SZ_IA_1956_A` / `SZ_IA_1956_B` — *Ich-Analyse*;
- `SZ_SA_1948` — *Schicksalsanalyse*.

Secondary works may help find passages, but they do not become runtime authority merely because they are useful commentary.

### 4.2 Doctrine is not automatically executable person-level meaning

A doctrine object can be SOURCE_VERIFIED and still remain `executionStatus: NOT_ASSESSED`. That means the source meaning is recorded, not that it may automatically be asserted about a tested person.

Promotion requires a narrowly scoped P2B claim with explicit predicates, scope, assertion strength, and anti-inference boundaries.

### 4.3 PDF/source verification workflow

When signs, formulas, tables, page layout, or corrupted extraction matter:

1. read `/home/oai/skills/pdfs/SKILL.md` before PDF work;
2. prefer render/visual inspection over OCR;
3. treat visual inspection as authoritative for `+`, `−`, `±`, `0`, `!` etc.;
4. use OCR only as a last resort;
5. remember that `validate_doctrine_evidence.py` proves address/excerpt integrity, not semantic correctness;
6. preserve source wording and historical terminology; control overreach through inference limits rather than silent modernization.

The Lehrbuch canonical file previously used in source arbitration had SHA-256:

`d3ee38846647644633aed2ad3c6ad35daedb39135838650482f68fed08f15a4b`

Do not assume this hash forever; re-verify if the canonical source file changes.

---

## 5. Anti-dinosaur rule — architecture must stay small

Do **not** add any of the following merely because they sound sophisticated:

- general RAG platform;
- vector database;
- provider abstraction framework;
- ontology or graph database;
- second LLM validator;
- new governance bureaucracy;
- additional CI workflows without a concrete need;
- alternate P1 scoring path;
- hidden case-specific rules;
- generic “semantic enrichment” layer;
- anticipatory abstractions for hypothetical future needs.

A new architectural layer is justified only by a concrete observed failure that cannot be solved by extending an existing layer more simply.

The working maxim is:

> **Correct-but-incomplete beats rich-but-invented.**

---

## 6. Historical material that is explicitly non-authoritative

Do not restore or imitate automatically:

- Szondi1;
- Szondi2;
- old AI-generated clinical reports;
- abandoned prompt strategies;
- historical PRs #61–#64;
- a published case interpretation as though it were a universal rule;
- chat-generated “indexes” or heuristic constructs that are not in the source.

These are useful only as failure/history evidence unless a current source-grounded claim independently supports the same behavior.

Fall 40 is a regression specimen, never doctrine and never a runtime hard-coded special case.

---

## 7. Current executable vertical slice

The intended flow is:

```text
ClinicalProtocolEvaluation
    ↓
ClinicalReport
    ↓
ClinicalEvidencePacket
    ↓
OpenAI preview request
    ↓
SynthesisProposition
    ↓
deterministic local validation
```

Important code areas to inspect first:

- `szondi3/clinical_facts.py`
- `szondi3/clinical_protocol.py`
- `szondi3/interpretation_catalogue.py`
- `szondi3/clinical_report.py`
- `szondi3/clinical_ai.py`
- `szondi3/clinical_ai_preview.py`
- `doctrine/registry/`
- `tests/`

### Evidence packet boundary

`ClinicalEvidencePacket` is the closed-world Szondian semantic boundary supplied to the model. It materializes the relevant profile/series observations, approved findings, exact support facts, doctrine/evidence passages, and anti-inference guard texts.

### Clinician-facing lexical fidelity

**Clinician-facing lexical fidelity:** the Szondi report is a technical report for the clinician, not direct client-facing communication. Preserve source-authorized historical Szondian terminology and characteristic wording; do not euphemize, sanitize, or modernize it merely to conform to contemporary clinical idiom. Keep the German term visible when Romanian wording risks semantic drift or importation of a foreign contemporary construct. This requirement never licenses terminology, branches, diagnoses, biography, or stronger meanings that active P2B claims do not authorize.

### Local synthesis gate

The local validator must reject propositions that use, omit, or mismatch the wrong:

- claim ID;
- fact IDs;
- doctrine IDs;
- anti-inference IDs;
- scope (`PROFILE` vs `SERIES`);
- assertion strength/topic permissions.

Do not weaken this gate to make a model answer pass.

### Provider bridge

The preview bridge is intentionally minimal. It uses the Responses API with Structured Outputs and keeps external tools disabled (`tools: []`) and storage disabled (`store: false`). No repository-stored API key is permitted.

---

## 8. Current P2B catalogue — **21 approved claims at checkpoint ae1b070...**

This section reflects the executable `szondi3/interpretation_catalogue.py` at the verified checkpoint. **If memory, PR text, or an older handoff says otherwise, the catalogue wins after re-verification.**

### 000001 — negative Wurzelfaktor is not automatically Verdrängung

- Doctrine: `DR_SZ_LEHR_1972_000313`
- Scope: series/Linnäus limitation guard
- Meaning: a negative Wurzelfaktor direction can also involve Verzicht or Anpassung; do not equate it automatically with repression.
- Guard: `AI_SZONDI_000001`

### 000002 — positive Wurzelfaktor does not exclude unmet need

- Doctrine: `DR_SZ_LEHR_1972_000313`
- Scope: series/Linnäus limitation guard
- Meaning: constant positive direction can still be an unsatisfied need; it does not prove absence of conflict.
- Guard: `AI_SZONDI_000002`

### 000003 — TspQu is not an autonomous behavioral predictor

- Doctrine: `DR_SZ_LEHR_1972_000328`
- Meaning: TspQu must be confronted with profile factor/vector reactions; no behavioral inference from magnitude alone.
- Guard: `AI_SZONDI_000003`

### 000004 — %Sy-Re / TspQu alone cannot establish clinical diagnosis

- Doctrine: `DR_SZ_LEHR_1972_000329`
- Guard: `AI_SZONDI_000004`

### 000005 — Dur–Moll cannot alone ground social valuation

- Doctrine: `DR_SZ_LEHR_1972_000337`
- Requires synoptic reading with Sozialindex.
- Guard: `AI_SZONDI_000005`

### 000006 — Sozialindex <40% does not authorize criminal-act inference

- Doctrine: `DR_SZ_LEHR_1972_000340`
- Guard: `AI_SZONDI_000006`

### 000007 — exact factor `-p`

- Doctrine: `DR_SZ_IA_1956_A_000043`
- Meaning: Projektion; Einssein/Gleichsein; Partizipationsdrang.

### 000008 — exact factor `+p`

- Doctrine: `DR_SZ_IA_1956_A_000043`
- Meaning: Inflation; Verdoppelung/Vollkommenheit/Allessein.

### 000009 — exact factor `+k`

- Doctrine: `DR_SZ_IA_1956_A_000043`
- Meaning: Introjektion; Einverleibung/Inbesitznahme/Alleshaben.

### 000010 — exact factor `-k`

- Doctrines: `DR_SZ_IA_1956_A_000043`, `DR_SZ_IA_1956_A_000049`
- Meaning: Negation family; Verdrängung is only one subordinate form.
- Guard: `AI_SZONDI_000010`

### 000011 — exact `Sch ±±`

- Doctrines: `DR_SZ_IA_1956_A_000051`, `DR_SZ_IA_1956_B_000009`
- Meaning: may be named testologically `integriertes Ich`.
- Guard: does **not** prove real/global/stable/existential/spiritual integration.
- Guard ID: `AI_SZONDI_000011`

### 000012 — exact `Sch 00`

- Doctrines: `DR_SZ_IA_1956_A_000051`, `DR_SZ_IA_1956_B_000010`
- Meaning: testological `Desintegration` label.
- Guard: an isolated profile does not justify a global/permanent verdict; Vorder-/Hinter-Ich dialectic matters.
- Guard ID: `AI_SZONDI_000012`

### 000013 — exact `Sch +±`

- Doctrine: `DR_SZ_LEHR_1972_000352`
- Source says, on average: `Annahme der Weiblichkeit` **or** `Annahme der Verlassenheit`.
- The exact configuration does not select which branch applies to an individual.
- Guard blocks automatic inference of global femininity/gender identity, real abandonment/loss biography, Kastrationskomplex, Paranoiden, verdrängter Mutterkomplex, creativity/productivity.
- Guard ID: `AI_SZONDI_000013`

### 000014 — a profile is one Existenz-/Schicksalsmöglichkeit, not the whole person

- Doctrine: `DR_SZ_LEHR_1972_000005`
- Trigger: series of 8, 9, or 10 profiles.
- Meaning: each profile is only one possibility and must be interpreted as a whole; the series is required to capture plurality.
- Guard: no exhaustive personality or psychiatric diagnosis from one profile.
- Guard ID: `AI_SZONDI_000014`

### 000015 — Zehnerserie Haupttriebklasse / current Triebgefahr

- Doctrines: `DR_SZ_LEHR_1972_000321`, `000322`, `000324`, `000326`
- Trigger requires exactly 10 profiles, a P1 danger-leading class, and all four Latenzproportionen.
- Meaning: maximum intravectorial TspD identifies the current Haupttriebklasse / location(s) of strongest current Triebgefahr when in the source-defined danger range.
- All four Latenzproportionen remain relevant; Gefahr/Ventil is dynamic and phase-dependent.
- Guard blocks “dominant profile by frequency”, diagnosis, fixed trait, or global verdict.
- Guard ID: `AI_SZONDI_000015`

### 000016 — exact serial subclass `Sh+`

- Doctrines: `DR_SZ_LEHR_1972_000323`, `000157`, `000171`, `000313`
- Trigger: Zehnerserie; exact danger leading class `Sh`; strict positive root `h`.
- Meaning: subclass `Sh+`; +h is current affirmation of Eros-/Liebes-/Bindungsbedürfnis; as a positive Wurzelfaktor it can still remain unsatisfied.
- Guard blocks homosexuality/bisexuality, travestism, global gender/femininity, passivity, concrete relationship biography, proof of satisfaction, and context-specific Überdruck/S-vector branches.
- Guard ID: `AI_SZONDI_000016`

### 000017 — exact Sexualvektor `S +0`

- Doctrine: `DR_SZ_LEHR_1972_000353`
- Meaning: Unitendenz / `Dominanz der Personenliebe`; +h is the sole sexual Strebung in Vordergrund while −h,+s,−s remain in Hintergrund.
- This is a Vektorbild organization, not global dominance of the person.
- `Mit Überdruck` extensions require separate quantum-aware authorization.
- Guard ID: `AI_SZONDI_000017`

### 000018 — exact Sexualvektor `S +−`

- Doctrine: `DR_SZ_LEHR_1972_000354`
- Meaning: diagonale Spaltung, Variation I; bejahte Personenliebe (+h) linked with Passivität/Hingabe (−s), strictly at this vector configuration level.
- Sex-specific and Überdruck branches are not automatically included.
- Guard ID: `AI_SZONDI_000018`

### 000019 — anti-`Mosaikspiel` / korrelative Deutung limitation

- Doctrines: `DR_SZ_LEHR_1972_000296`, `DR_SZ_LEHR_1972_000297`
- Assertion mode: LIMITATION.
- Meaning: isolated factor/vector meanings remain general/abstract and must not be mechanically juxtaposed into an individualized global portrait. Szondi requires interfactorial/intervectorial correlative interpretation.
- Critical guard: **do not pretend that a list of autonomous findings is itself a clinical correlation; do not invent a relation unless a separate source-grounded claim authorizes that relation.**
- Guard ID: `AI_SZONDI_000019`

### 000020 — exact Kontaktvektor `C +−`

- Doctrine: `DR_SZ_LEHR_1972_000358`
- Meaning: simultaneous `Sich-Frei-Machen/Abtrennung` through −m and `Auf-Suche-Gehen` through +d; detachment and setting-out-to-search at the level of contact organization.
- Guard blocks automatic infidelity, depression, autism/other pathology, real loss/separation biography, actual search for substitute object, or a global relational verdict.
- Guard ID: `AI_SZONDI_000020`

### 000021 — exact `Sch +±`: source-qualified Ich-Abwehr / Affektschicksal relation

- Doctrine: `DR_SZ_IA_1956_B_000053`
- Scope: **PROFILE only**.
- Assertion mode: `PROBABLE`; the source qualifier `scheinen` is mandatory.
- Meaning: Annahme — `Introjektion der Verlassenheit bzw. der Weiblichkeit` — is described as appearing more successful in `Abwehr von Triebgefahren`, with `Angst seltener` than in the four immediately preceding source-defined defense forms: `Sch ±+`, `Sch −0`, `Sch ±±`, `Sch ±−`.
- Guard: this does **not** measure the person's actual anxiety, establish absence/low anxiety, mental health, Ego strength/maturity, coping/resilience, prognosis, or global/real-life defensive effectiveness; it does not select `Verlassenheit` versus `Weiblichkeit` or authorize biography/gender content.
- Guard ID: `AI_SZONDI_000021`

### Critical resolved contradiction

An older conversational handoff incorrectly associated IDs 000016–000018 with `Sch -+`, `Sch -±`, and `Sch ++`, and another stale note described 000019/000020 as different P/C correlations. **That mapping is not the current executable catalogue.** The verified repository at `ae1b070...` defines 000016–000021 exactly as above.

`Sch -+`, `Sch -±`, and `Sch ++` remain potentially source-grounded research candidates, but they are **not** current P2B claims under IDs 16–18. Never reuse or renumber current claim IDs to fit old conversation memory.

---

## 9. Current methodological doctrine that should shape future work

The most important recent source work is no longer just “more symbol meanings”; it clarifies **how Szondi says interpretation must be constructed**.

### `DR_SZ_LEHR_1972_000296` — no Mosaikspiel

Factor/vector tables cannot be mechanically concatenated into an individual diagnosis/character portrait.

### `DR_SZ_LEHR_1972_000297` — korrelative Deutung

Each Wahlreaktion is to be interpreted in interfactorial and intervectorial relations, not as an isolated reaction.

### `DR_SZ_LEHR_1972_000298` — context levels matter

The same reaction may require different interpretation depending on individual context such as sex, age, culture/social context and source-historical categories. Do not turn this into data collection requirements automatically; it is an anti-context-free boundary unless a specific executable claim needs such facts.

### `DR_SZ_LEHR_1972_000299` — Elementarfunktion ≠ Inhalt

Never conflate an elementary function with a fixed manifest content.

### `DR_SZ_LEHR_1972_000300` / `000301` — methods are complementary, not one hybrid index

Szondi distinguishes qualitative-dialectical, quantitative, and proportional methods. The principal methods include Rand–Mitte, Komplementmethode, Linnäus, Dur–Moll, and Sozialindex. Do not collapse them into a single invented score.

### `DR_SZ_LEHR_1972_000302` — Rand–Mitte structural definition

- Rand: vectors **S + C**.
- Mitte: vectors **P + Sch**.
- The method concerns the dialectic of Randgefahren and Abwehr/censorship in the middle.

### `DR_SZ_LEHR_1972_000303` — one profile is episodic/current

A single Rand–Mitte profile speaks to current/episodic drive dangers and defensive activities; series-level interpretation must remain explicitly series-level. Do not derive generic “variation = health” or “constancy = rigidity/pathology” rules from this.

### `DR_SZ_LEHR_1972_000304` — Rand–Mitte as first orientation, not statistical summation

Szondi recommends Rand–Mitte as an initial orientation and rejects losing the relation between Triebgefahr and Abwehrart through mere statistical summation.

### `DR_SZ_LEHR_1972_000359` — explicit fail-closed Rand–Mitte boundary

Source-verified but currently not a P2B claim by itself. It says not to make Schicksalsdiagnose from Mitte alone; the correlations between Randgefahren and Abwehrarten must be examined carefully **case by case**, and Mitte tables cannot replace exact Randanalyse.

This doctrine is highly relevant to future work but is **not** permission for a universal `high Rand + weak Mitte = crisis` algorithm.

---

## 10. Latest strategy: keep three kinds of “tension/danger” distinct

A major recent conceptual correction is that the project must **not** invent standalone metrics such as a “Rand pressure index” or “Mitte defense index”. Those constructs are not Szondi's method and would distort it.

Keep at least these three levels distinct:

```text
FACTOR LEVEL
  + / - / ± / 0
  Vollreaktion / Quantumspannung
  ! / !! / !!!

PROFILE-STRUCTURAL LEVEL
  Rand = S + C
  Mitte = P + Sch
  source-defined Randgefahr ↔ Abwehrart correlations

SERIES / LINNÄUS LEVEL
  TspG
  TspD
  Latenzproportionen
  Gefahr / Ventil
  Haupttriebklasse
```

They may later converge in a source-authorized interpretation, but they are **not interchangeable indicators**.

### Four generic equivalences that are forbidden

```text
!!  ≠ automatically Triebgefahr or imminent discharge
±   ≠ automatically crisis
0   ≠ automatically Abwehrbruch
Komplementprofil ≠ deterministic future discharge channel
```

### Quantumspannung / Vollreaktion

The current source boundary to preserve is:

```text
4 choices in the same direction → !
5 → !!
6 → !!!
```

Vollreaktion means a strongly loaded current need/tendency in the source sense; do not automatically translate it into imminent dangerous discharge. A premanifest/discharge interpretation requires an explicit source-defined context.

### `±`

Treat primarily as Ambivalenzreaktion, not as a generic “crisis” marker. Source material can describe dynamic transitions around ambivalence, but that does not license `± = crisis` globally. `Sch ±±` alone already demonstrates why such a rule would contradict the source taxonomy.

### `0`

Treat as Nullreaktion, not generic collapse. Depending on context it may reflect discharge/satisfaction, socialization/sublimation/manifestation, or rarer weakness. `e0`, `k0`, `p0` must therefore never be hard-coded as automatic failure of ethical censor, repression, or ego.

Also, `k` must not be reduced to “repression”: current P2B claim 000010 explicitly preserves `-k` as the broader Negation family.

---

## 11. Linnäus: exact quantitative role

Do not describe TspG as “total psychic energy” or “total volume of tension in the person”. That is an invented reinterpretation.

Source-grounded working distinctions:

- TspG is built from the series distribution of ambivalent/null reactions and participates in Symptomfaktor vs Wurzel-/Konduktorfaktor ranking;
- TspD is the intravectorial difference between the two factors' TspG values;
- Latenzproportionen characterize the vector positions;
- in a 10-profile series, source-defined 5–10 is Gefahr and 0–4 is Ventil;
- maximum relevant TspD in the danger range gives the current Haupttriebklasse / strongest current Triebgefahr location;
- all four Latenzproportionen matter;
- Gefahr/Ventil are phase-dynamic, not fixed personality traits.

Terminology: preserve the source/project term **TspQu** (`Tendenzspannungsquotient`), not an improvised `TspQ`.

Current claim 000015 intentionally remains limited to an exact Zehnerserie. P1 can normalize shorter series, but short-series P2B use requires separately reviewed provenance rather than silent extrapolation.

---

## 12. Komplementmethode — current boundary

Do not turn complement into a future-behavior predictor.

Where source and implementation distinguish them, preserve the difference between experimental complement and theoretical complement. Vordergrund and complement are read dialectically/jointly. Theoretical complement concerns a complementary simultaneous/latent structure; it is not automatically “where the drive will discharge next”.

A future complement claim must therefore be source-bounded and configuration-specific. Never implement:

```text
VGP tension at factor X → complement sign Y → patient will discharge through behavior Y
```

without a primary source rule that explicitly authorizes that person-level implication.

---

## 13. Fall 40 benchmark — exact verified deterministic state

Fall 40 is a regression specimen only.

### TspG

```text
h  = 0
s  = 9
e  = 2
hy = 2
k  = 1
p  = 7
d  = 0
m  = 0
```

### TspD / Latenz

```text
S   = 9  → lower-tension factor h → designation Sh   → danger
P   = 0  → tie → no designation                       → ventil
Sch = 6  → lower-tension factor k → designation Schk → danger
C   = 0  → tie → no designation                       → ventil
```

Latency class: `danger_class`; danger count: 2. Unique current leading drive class: `Sh`.

This is **Haupttriebklasse at the vector/TspD level**, not “the dominant profile” and not a frequency-based global personality label.

Known regression-sensitive activations from the current development history include:

- claim 000013 `Sch +±`: profiles 4, 5, 6, 8, 9;
- claim 000016: strict serial subclass `Sh+` where its P1 predicates are satisfied;
- claim 000017 `S +0`: profiles 1,2,3,4,5,6,8,9,10;
- claim 000018 `S +−`: profile 7 only.

Do not assume any other Fall 40 activation without running the current tests/evaluation.

---

## 14. Testing philosophy — especially negative regressions

A new P2B claim is not complete merely because one positive fixture activates it.

For each new exact/correlative claim, prefer tests that establish:

1. exact positive activation;
2. a near-neighbor negative case differing by one critical predicate;
3. exact support fact IDs;
4. exact doctrine IDs;
5. exact anti-inference IDs;
6. correct PROFILE/SERIES scope;
7. non-activation when series/profile requirements fail;
8. local-validator rejection when scope or guard bundles are tampered with.

Near-neighbor negatives are especially important for quantum-aware rules. If a base configuration is only authorized without Überdruck, explicitly test that the same signs with quantum tension do **not** accidentally activate the base claim.

The current head's latest commit, `Use existing correlative doctrine in regressions`, follows exactly this philosophy.

---

## 15. Controlled live-preview history and policy

The provider is used diagnostically to observe actual wording behavior, not to discover Szondi meaning.

Known controlled evidence from this work includes:

- first retained raw preview: `/mnt/data/szondi3_live_preview_20260829T204455Z.json`; 18 raw/validated propositions, 0 rejected; structurally safe, no observed semantic overreach, but clinically thin/enumerative;
- second retained raw preview: `/mnt/data/szondi3_live_preview_20260829T220517Z.json`; 23 propositions, including five exact claim-000013 outputs on Fall 40 profiles 4,5,6,8,9; 0 rejected in the local gate;
- the current PR history mentions three controlled Fall 40 live previews in total. Do not invent details about any artifact not actually present in the successor environment; inspect the raw file if it is to be used as evidence.

The lesson from the previews was not “give the model more freedom”. It was the opposite: **report richness followed P2B coverage**.

### Credential hygiene

If a new one-shot provider preview is needed:

- the user runs it locally;
- do not ask the user to paste the API secret into chat;
- use a temporary/restricted project API key if desired;
- only the `/v1/responses` permission is needed for the one-shot harness;
- never commit a credential;
- revoke/delete the temporary key after capture.

### Obsolete harness warning

`/mnt/data/szondi3_live_preview_once_v4.py` was created earlier and pins historical head `f63151f6cf73139d545534374bc7908f21105b2c`. It was designed around claims 13–15. It must **not** be blindly reused as a current-head harness.

If a new live preview is justified, first make a minimal current-head harness whose deterministic preflight checks the current catalogue and expected support bundles. Do not build a provider framework.

---

## 16. The central problem now: from safe atoms to source-defined correlations

The project has reached an important point. Atomic meanings are useful, but Szondi explicitly warns against a `Mosaikspiel`. A clinically rich report cannot be obtained by simply concatenating twenty-one true local statements.

The safe path to richer interpretation is therefore:

> **build a library of exact, source-defined COMPOSITE correlations — not a generic synthesis heuristic.**

Examples of what this means architecturally:

- if the primary source explicitly links a particular Rand configuration with a particular Mitte defense, encode that exact relationship with exact predicates and guards;
- if a source statement is only an illustration, do not universalize it;
- if a relation depends on quantum tension, include quantum predicates;
- if it depends on sex/age/series context, include only the facts actually required by the source;
- if the source does not supply a discriminator, preserve the alternatives rather than letting the LLM choose;
- if the relation is not source-defined, the model may not invent it merely to make the report coherent.

Current claim 000019 is deliberately a **limitation**, not an engine that fabricates correlations. Current claim 000020 is an example of a narrow structural Vektorbild claim. Future richness should grow in this direction.

---

## 17. Recommended next step for the successor chat

Do not immediately add another broad feature or another live preview.

### Completed evidence-driven step

The controlled v6 live preview on the prior 20-claim catalogue produced 47 raw propositions, 47 accepted and 0 rejected. It respected claim 000019, kept all ten claim-000020 `C +−` findings PROFILE-local, and did not invent forbidden biography/pathology or multi-claim correlations. Its main failure mode was safe-but-fragmented output, classified as a P2B coverage gap rather than model or prompt failure.

That observed gap led to one narrow source reconsultation and the approved promotion of claim 000021: exact PROFILE-local `Sch +±` with the source's probabilistic `scheinen` / `Angst seltener` relation and hard guards against person-level anxiety or mental-health inference.

### Next safe rule

Re-verify current branch/PR/CI and inspect the clinician-visible effect of the 21-claim catalogue before adding another claim. If a concrete gap remains, return to canonical primary evidence for one exact source-defined relation. Do not generalize Rand–Mitte into a scoring engine, do not infer from frequency alone, and do not run another provider preview automatically.

---

## 18. Safe source-to-code workflow for every new claim

```text
1. Name the exact observed gap.
2. Search canonical primary source, not the web, for the relationship.
3. Inspect sufficient source context; visually arbitrate signs/formulas if needed.
4. Create/adjust doctrine only if the source actually supports the statement.
5. Decide whether the doctrine is executable person-level meaning at all.
6. Write the narrowest P2B claim:
     - exact predicates
     - correct scope
     - assertion mode/strength
     - source/doctrine IDs
     - anti-inference guards
7. Expose only the missing deterministic P1 facts, if any.
8. Add positive and near-neighbor negative tests.
9. Verify exact claim→fact→doctrine→guard bundles.
10. Run the existing workflow suite.
11. Optionally run one controlled live preview.
12. Inspect raw + local-gated output.
13. Repeat only if the observed failure justifies another claim.
```

If the source is ambiguous, leave it unresolved or encode the alternatives. Do not ask the model to choose.

---

## 19. Stop conditions

The successor must stop and report the problem rather than continue automatically if any of the following occurs:

- handoff and repository disagree about current claim IDs or code state;
- PR description and catalogue disagree;
- source extraction and rendered PDF signs disagree;
- doctrine statement is stronger than the source;
- a case passage is being generalized into a universal rule;
- a proposed claim predicts real behavior/biography without explicit source support;
- an isolated factor/vector meaning is being turned into a diagnosis;
- a new architecture layer is being proposed without an observed failure;
- model output contains meaning not traceable to an active claim;
- a report needs a bridge the source/P2B layer does not yet contain;
- somebody proposes to “repair” missing coverage by granting the LLM broader instructions;
- a change would merge the PR, mark it ready, or declare formal gates without explicit user authorization.

---

## 20. Things specifically **not** to do

- Do not reintroduce a “Rand pressure index” or “Mitte defense index”.
- Do not make `high Rand + low/zero Mitte = crisis` a universal formula.
- Do not map `!!` directly to imminent dangerous discharge.
- Do not map every `±` to crisis.
- Do not map every `0` to Abwehrbruch.
- Do not reduce `k` to repression.
- Do not call TspG “total psychic energy”.
- Do not rename TspQu as an improvised metric.
- Do not make Komplementprofil a deterministic future-discharge predictor.
- Do not summarize autonomous findings into a global portrait without a source-defined correlation.
- Do not infer sex/gender/orientation/diagnosis from historical Szondi labels beyond the exact authorized claim.
- Do not infer actual crime from Sozialindex.
- Do not infer concrete relationship, loss, move, job, partner, or behavioral history from vector configurations unless separately source-authorized.
- Do not add a second LLM to police the first.
- Do not hard-code Fall 40.

---

## 21. Research backlog — not executable until promoted

The following are useful research directions, **not current permission to assert person-specific conclusions**:

### A. Exact Rand–Mitte correlations

Identify source passages that explicitly bind a Randgefahr configuration to a specific Abwehrart in Mitte. Prefer exact configuration predicates rather than generic “strong/weak” indexes. `DR_SZ_LEHR_1972_000359` is a methodological boundary, not a lookup table.

### B. Quantumspannung / Vollreaktion

Determine which factor-level interpretations of `! / !! / !!!` are clinically useful enough for P2B and which require context. Avoid automatic “imminent discharge” semantics. Add quantum-aware negative regressions.

### C. Komplementmethode

Promote only exact source-defined Vordergrund/complement relationships. Keep theoretical vs experimental complement distinct where relevant. No temporal prediction unless the source explicitly supplies it.

### D. Short series (3–9) Haupttriebklasse

P1 already has source-based normalization machinery, but current claim 000015 deliberately uses exactly 10 profiles. Extend only after claim-local provenance for shorter-series execution is reviewed.

### E. `Sch -+`, `Sch -±`, `Sch ++`

There is primary-source doctrine around Hemmung, Entfremdung/gehemmte Projektion, and Introinflation, but these are **not** current claim IDs 16–18. Any promotion must get new IDs and current anti-inference review; severe/diagnostic branches must remain conditional.

### F. Additional exact S/P/C/Sch Vektorbilder

Continue only where the source gives a clear structural meaning and isolate stronger pathological, sex-specific, or Überdruck branches.

### G. Longitudinal/serial dynamics

Do not invent “Triebrotation”, “variation = adaptive health”, “extreme frequency = rigidity/pathology”, or a chronological film narrative from repeated signs unless a primary source explicitly supports the exact relationship.

### H. Correlative report synthesis

This is the most clinically important backlog: find enough source-defined interfactorial/intervectorial relations that the final report can move beyond atomized findings **without** reverting to Mosaikspiel or LLM invention.

---

## 22. Current benchmark of engineering quality

The project should prefer the following kind of evidence over broad feature count:

- exact P1 facts;
- exact P2B predicates;
- exact doctrine IDs;
- source-verified passages;
- explicit anti-inference guards;
- positive + nearest-neighbor negative regressions;
- scope-preserving validator tests;
- controlled raw provider captures;
- clinician inspection of the actual generated prose.

A feature is not “done” because code exists. It is done when the source meaning, executable trigger, negative boundary, materialized evidence, and model behavior all agree.

---

## 23. Definition of done for the Clinical-AI strategy

Do not equate “20 claims” or “green CI” with completion. A reasonable completion condition is reached only when:

1. deterministic test scoring/protocol calculations are stable for the intended use;
2. the intended report sections have sufficient **source-grounded P2B coverage** to produce coherent clinical prose;
3. meaningful correlations are source-defined rather than generated by Mosaikspiel or model intuition;
4. every person-specific clause in AI output is traceable to exact active evidence;
5. unsupported diagnosis, biography, behavior, and future prediction remain blocked;
6. local validation fails closed under tampered/wrong-scope outputs;
7. several realistic benchmark series — not just Fall 40 — have been inspected through the full packet → model → local-gate path;
8. report richness is acceptable to the clinician without granting semantic freedom to the model;
9. source ambiguity remains visible rather than silently repaired;
10. only after explicit user approval should PR #65 be considered for `ready`/merge or any formal downstream gate declaration.

---

## 24. Current repository/PR checkpoint and staleness warnings

Verified immediately before creating this handoff:

```text
repo:   danono2016/Szondi3
branch: work/ai-clinical-provenance-strategy-001
head:   ae1b070f63b65bb377f36c4c76adb18666a6eb46
commit: Update catalogue count regression
PR:     #65 OPEN / DRAFT / MERGEABLE / NOT MERGED at the last explicit PR verification; re-check before acting on it
base:   main@d192c984eff9d753de4ee60955accec3d6252938
claims: 21 APPROVED in interpretation_catalogue.py
CI:     all five current PR workflows completed successfully at implementation checkpoint ae1b070...
```

The PR body was already stale at this checkpoint: it still said 18 claims and cited an older checkpoint. The previous `docs/CHAT_TRANSFER_PACKAGE.md` was also stale and cited an older implementation head. **Never use PR prose or a handoff hash as a substitute for checking the code.**

The transfer-package update may advance the branch by a documentation-only commit after `ae1b070...`; the successor must record both the implementation checkpoint and the actual current head.

---

## 25. Compact resumption checklist

Before changing anything, the new chat should be able to answer all of these:

- What is the current branch head?
- Is PR #65 still draft/open/not merged?
- What is the current `main` base?
- How many executable claims exist **in code**?
- What do claim IDs 16–21 actually mean?
- Are all current workflows green?
- What exact report failure are we solving next?
- Is that failure semantic/P2B, factual/P1, model wording, or validator behavior?
- What primary source passage authorizes the proposed new meaning?
- What is the nearest-neighbor case that must **not** activate it?
- What anti-inference is necessary?
- Does the change preserve PROFILE/SERIES scope?
- Are we accidentally reconstructing Mosaikspiel?
- Are we inventing a metric not used by Szondi?
- Can the problem be solved without adding an architectural layer?

If any answer is unclear, investigate before coding.

---

## 26. Project ethos in one paragraph

Szondi3 should become more clinically expressive by making its **authorized semantic substrate more exact and more complete**, not by making the language model more autonomous. The mathematical/testological structure belongs in deterministic P1; the historical theoretical meaning belongs in canonical doctrine; person-specific interpretive permissions belong in narrow P2B claims; the report packet materializes only those permissions; the LLM writes within them; the local validator enforces them. Every time the report feels too thin, first ask **which exact Szondian relation is missing from P2B**. That question, answered from primary evidence with negative boundaries, is the path to finishing the project without losing fidelity.

---

## 27. One-line orthodoxy

> **Do not ask the model to know more Szondi; make Szondi3 prove more Szondi to the model.**
