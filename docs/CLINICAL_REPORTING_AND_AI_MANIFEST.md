# Szondi3 — Clinical Reporting and AI Manifest

**Status:** NORMATIVE PRODUCT DIRECTION / CLINICIAN-FACING REPORTING CONTRACT  
**Applies to:** all clinician-facing interpretation, AI synthesis, wording, report composition, interpretation ranking and source presentation  
**Owner decision:** this document records the intended product direction after the first Alpha-0 report review. It is not a chat handoff and must remain valid across future development chats until explicitly revised by the clinician-owner.

## 1. Product objective

Szondi3 must not expose a dump of deterministic findings, doctrine records and technical safeguards as if that were a clinical interpretation.

The intended product is:

`deterministic test facts -> source-faithful Szondian meanings -> structured interpretive selection -> coherent Romanian clinical formulation -> clinician judgment`

The report must be clinically usable, concise enough to think with, faithful enough to remain recognizably Szondian, and traceable enough to audit when needed.

### Governing maxim

> **Preserve Szondi first. Structure uncertainty precisely. Let AI explain and formulate, never invent.**

A second non-negotiable maxim is:

> **AI may make Szondi intelligible; it may not make Szondi milder, more contemporary, more politically acceptable, more certain or less certain than the admitted sources authorize.**

---

## 2. Immutable authority and role separation

The epistemic direction remains one-way:

`PRIMARY SOURCE -> VERIFIED DOCTRINE -> EXECUTABLE INTERPRETATION -> DETERMINISTIC CASE FACTS -> INTERPRETIVE SUPPORT/RANKING -> AI CLINICAL WORDING -> CLINICIAN JUDGMENT`

No downstream layer may rewrite an upstream layer.

### Deterministic software

The deterministic program owns:

- administration facts;
- scoring;
- factor reactions;
- vector configurations;
- quantum/intensity;
- forced-null status;
- series indices and formulas;
- executable claim activation;
- scope;
- source/doctrine links;
- future interpretive support scores, if and only if a separate deterministic scoring contract has been explicitly designed, reviewed and tested.

It does **not** own free clinical prose.

### Doctrine layer

The doctrine layer owns what Szondi actually says, with the source's own level of certainty, terminology, conditions and rhetorical force.

It must not be modernized for comfort.

### AI layer

AI owns only:

1. faithful Romanian explanation of already-authorized Szondian meanings;
2. composition of authorized material into readable clinical prose;
3. translation and explanation of German terminology;
4. presentation of deterministic interpretive predominance supplied by software;
5. generation of explicitly marked clinical exploration directions that remain inside the authorized meaning ceiling;
6. linguistic compression of complexity without semantic deletion.

AI does **not** calculate the test, create doctrine, activate claims, invent correlations, invent support percentages, infer hidden biography, generate diagnoses or fill doctrinal gaps from general model knowledge.

### Clinician layer

The clinician owns the final clinical judgment, acceptance/rejection of AI formulations, external case context and the final synthesis.

---

## 3. Closed-world AI rule

For Szondi interpretation, AI is closed-world.

A clinically meaningful statement may be generated only from:

- deterministic facts supplied by the current case;
- admitted doctrine/source material linked to those facts;
- explicitly authorized interpretive relations;
- clinician-entered context, when clearly marked as clinician context and never back-projected into the test score.

General model knowledge, memory, plausibility, contemporary psychodynamic theory or common psychological associations may not silently supply missing Szondian meaning.

If support is missing, the correct output is omission or an explicit statement that no authorized synthesis is available at that level.

**Fluency is never evidence.**

---

## 4. Fidelity to Szondi's voice

### 4.1 No euphemization

Clinician-facing wording must preserve Szondi's baroque, categorical, direct, uncomfortable, archaic or historically pathologizing language when that language is actually source-authorized.

Examples of terms that must not be softened merely because they are uncomfortable include, when source-relevant:

- `totaler Narzißmus`;
- `Macht-Ich`;
- `Allessein`;
- `Alleshaben`;
- `Wahn`;
- `Destruktion`;
- `abnorme Sexualität`;
- `prägenitale Sexualität`;
- `Kain` terminology;
- hereditary/genotropic terminology;
- other historically direct expressions used by Szondi.

`totaler Narzißmus` must not be silently converted into a harmless phrase such as "accentuation of the self". `Macht-Ich` must not be reduced to "need for affirmation". The original semantic force must remain visible.

### 4.2 No dramatization beyond the source

Fidelity also prohibits inflation.

If Szondi writes `kann`, `scheint`, `wir nehmen an`, `wahrscheinlich`, `u. E.` or otherwise marks a possibility, assumption or suspicion, AI must preserve that epistemic strength.

Source uncertainty may not be upgraded to certainty.

### 4.3 Historical terminology is attributed, not erased

When historical terminology could be confused with a modern diagnosis or modern identity category, the report must preserve the Szondian term first and then, separately, state the modern interpretive boundary where necessary.

The boundary must not rewrite the original term.

Correct order:

1. what Szondi says;
2. what the term means in Romanian;
3. only then, if materially necessary, what must not be automatically equated with a contemporary diagnosis/fact.

---

## 5. Language contract for the clinical report

### 5.1 Main prose language

The clinician-facing report is written in **Romanian**.

Internal English software language is forbidden from the ordinary clinical reading surface.

Terms such as the following belong only in technical audit/debug views, not in normal clinical prose:

- `APPROVED`;
- `AVAILABLE`;
- `NOT_APPLICABLE`;
- `claim` / `finding` as internal objects;
- `source-grounded`;
- `quantum-aware`;
- `release policy`;
- `production mode`;
- `synthesis contract`;
- internal route/status vocabulary.

### 5.2 German terminology

German is preserved where it carries Szondian conceptual identity, but the clinician must never need to know German in order to understand the report.

At first occurrence, every important German term must receive an immediate, clear Romanian translation or explanation, for example:

- `Allessein` (**a fi totul / aspirația de a fi totul**);
- `Alleshaben` (**a avea totul / aspirația de a poseda totul**);
- `Vordergrund` (**prim-plan**);
- `Hintergrund` (**fundal**);
- `Vordergänger` (**configurația / existența de prim-plan**, with context-specific explanation);
- `Hintergänger` (**configurația / existența complementară de fundal**);
- `stellungnehmendes Ich` (**Eul care ia poziție**);
- `Personabildung` (**formarea persoanei / formarea configurației personale**, depending on source context).

If no single Romanian equivalent is adequate, keep the German term and explain its semantic range explicitly rather than inventing a falsely neat translation.

### 5.3 German quotations

A German quotation must never be the only intelligible version available to the clinician.

Whenever a German quotation is displayed, its complete Romanian translation must be available immediately with it.

Long original quotations normally belong in `Surse / De ce apare?`, not in the main flow of the clinical report.

---

## 6. Technical material must not contaminate the clinical reading surface

The ordinary report must not display technical identifiers such as:

- `IC_SZONDI_PRIMARY_...`;
- `DR_SZ_...`;
- Git SHA values;
- doctrine snapshot IDs;
- release hashes;
- P2B catalogue hashes;
- evidence digests;
- internal execution statuses.

They remain preserved in the audit/provenance layer and must remain reachable through explicit source/technical inspection.

### Separation of surfaces

The product must distinguish:

1. **Raport clinic** — readable clinical product;
2. **Surse / De ce apare?** — doctrine, source excerpt, translation, page and provenance;
3. **Audit tehnic** — internal IDs, hashes, runtime status and release metadata.

Nothing is discarded. It is placed at the appropriate layer.

---

## 7. A report is not a P2B dump

P2B may remain atomic for traceability and testing. The clinical report must not simply print activated atomic claims one after another.

This is especially important because Szondi explicitly rejects mechanical `Mosaikspiel` interpretation.

### Anti-Mosaikspiel rule

AI may not obtain a "whole-person interpretation" by mechanically juxtaposing independent meanings of factor/vector/profile findings.

A relation such as:

`A + B -> combined clinical meaning C`

is permitted only when the relation itself is authorized by admitted doctrine/executable interpretation or by a separately approved composition rule grounded in the source.

If the relation is not authorized, AI must keep the observations separate.

A fluent invented bridge is still an invention.

---

## 8. Distinguish case findings from method safeguards

General method limits are not patient findings.

Statements such as:

- do not diagnose from TspQu alone;
- do not infer modern genetics from historical heredity terminology;
- do not equate one Sch formula with a demonstrated defense mechanism;
- do not turn one or two factor reactions into a syndrome;

are important software/method boundaries, but they must not be counted or displayed as if they were active clinical findings about the person.

The main report must distinguish at minimum:

- **case-specific Szondian interpretations**;
- **case-relevant cautions**, only where needed;
- **general method limits**, normally outside the primary interpretation flow.

---

## 9. Clinical formulation architecture

For an important interpretation, the intended clinician-facing structure is:

### A. În termenii lui Szondi

A direct, source-faithful Romanian rendering that preserves the author's terminology and rhetorical force. Important German terms remain visible with immediate Romanian translation.

### B. Formulare clinică

AI converts the authorized Szondian meaning into clear, ordinary Romanian clinical language **without replacing, neutralizing or contradicting the Szondian formulation**.

This section must be clinically usable, not a paraphrase of software metadata.

It may say what the configuration places in the foreground of exploration, how the tendencies are organized, what tension or direction is dominant, and what the clinician should understand from that organization.

It may not invent biography or diagnosis.

### C. De explorat clinic

When useful, AI may offer a small number of concrete exploration directions/questions that can be checked against interview, history, therapeutic relationship and other independent clinical data.

These are hypotheses for exploration, not facts derived from the test.

### D. Limită relevantă

Only when materially necessary, include a short boundary preventing a likely modern overreading. Do not attach long generic anti-inference paragraphs to every interpretation.

---

## 10. Directness versus hedging

The report must not drown valid meaning in repetitive `poate`, `dacă`, `însă`, `nu se poate exclude`, `ar putea`, `dar` language.

Uncertainty must be represented structurally, not through verbal fog.

When the deterministic layer identifies one clearly predominant authorized interpretation, AI should formulate it directly and clearly within the Szondian/testological frame.

When the deterministic layer identifies genuine competition between interpretations, the report should show the competing readings explicitly rather than embedding all of them into one vague paragraph.

---

## 11. Precise indetermination: interpretive support, not invented probability

The project adopts the concept of **structured / precise indetermination**.

Several source-authorized interpretations may sometimes compete at the same interpretive level. The product should not print every possibility indiscriminately. It should identify what is predominant, what is secondary and when no clear predominance exists.

### 11.1 Terminology

Do **not** call the numeric value a statistical probability unless future empirical validation establishes calibrated probabilities.

The preferred concept is:

- **pondere de susținere interpretativă**;
- or **grad relativ de susținere**.

A displayed value such as `~70%` means relative support inside a defined interpretive competition set. It does not mean "70% probability that this is clinically true".

### 11.2 AI must never generate the score

AI is forbidden to invent, estimate, adjust or normalize interpretive percentages.

Scores must be supplied by deterministic software.

AI receives, for example:

`Interpretarea A: support=0.68`  
`Interpretarea B: support=0.24`  
`Interpretarea C: support=0.08`

and only decides how to express those supplied values in Romanian according to the presentation contract.

### 11.3 No percentages until a scoring contract exists

The current project does **not** yet have authority to display such percentages merely because this manifest describes the desired model.

Before any support percentage is shown in production, a separate versioned deterministic **Interpretive Support Scoring Contract** must define and test:

- eligible evidence features;
- doctrinal basis for each feature;
- weighting or scoring rule;
- negative/contradictory evidence handling;
- normalization rule;
- comparison family membership;
- scope rules;
- series/foreground/complement boundaries;
- missing-data behavior;
- rounding/presentation behavior;
- regression tests;
- clinician approval.

Until then, AI must not fake numerical certainty.

### 11.4 Compare only interpretations of the same level

Percentages may be normalized together only for interpretations that belong to an explicit **interpretive family** of genuinely competing alternatives at the same level.

Do not place, for example, a factor meaning, a vector configuration and an inter-factor relation into one 100% competition simply because all are active.

`+k`, `Sch ++` and `-m/+k` may represent different levels/relations and are not automatically competitors.

This restriction prevents a mathematical form of `Mosaikspiel`.

### 11.5 Candidate deterministic evidence dimensions

A future scoring contract may consider only source-authorized/deterministic dimensions such as:

- exact factor reaction match;
- vector configuration match;
- authorized interfactorial relation;
- authorized intervectorial relation;
- quantum/Überdruck when source-relevant;
- repetition/consistency across a series;
- isolated versus recurrent occurrence;
- source-authorized foreground/complement relations;
- series formula/index evidence when applicable;
- explicit contradictory or weakening evidence.

This list is a design space, not permission to assign arbitrary weights.

### 11.6 Initial experimental presentation gates

The following are **provisional product defaults**, not Szondian doctrine and not permission to implement scores without the scoring contract above:

- **single predominant interpretation:** top support `>= 65%` **and** margin over second place `>= 20 percentage points`;
- **multiple supported interpretations:** if no single interpretation passes the dominance gate and the runner-up remains materially supported (initially around `>= 25%`), show the two strongest readings with their approximate support weights;
- **structured indetermination:** when the leading readings are close (initially a margin of roughly `<= 10–15 points`) or no interpretation reaches a meaningful support level, explicitly state that there is no clear predominance rather than forcing a synthesis.

These thresholds must remain configurable/versioned during alpha evaluation and may be revised only explicitly, based on clinical/product evidence.

### 11.7 Approximate display, exact internal score

If percentages become authorized, the report should avoid false precision. Prefer approximate whole-number or coarse rounded display (for example `~70%`, not `68.347%`) while retaining exact deterministic values internally for audit.

---

## 12. Keep testological support separate from clinical concordance

Future product design may allow the clinician to record a separate judgment such as clinical concordance (`scăzută / moderată / ridicată` or another explicitly designed scale).

This must never rewrite the deterministic Szondian support score.

For example:

- **Suport testologic:** ~70%
- **Concordanță clinică apreciată de clinician:** moderată

The two answer different questions and must remain separate.

AI must not increase a testological support score because the biography "fits".

---

## 13. Scope preservation

AI must preserve the exact level at which a meaning is authorized:

- factor;
- vector;
- profile;
- series;
- foreground;
- complement;
- longitudinal comparison.

A profile reaction is not automatically a stable trait. A series statement is not automatically true of every individual profile. Complement material is not foreground material. A structural longitudinal difference is not improvement or deterioration unless separately supported.

Base reaction, quantum/intensity and forced null remain distinct facts.

---

## 14. Biography, diagnosis and modern categories

AI may not invent as facts:

- trauma;
- loss;
- death;
- separation;
- family history;
- profession;
- talent;
- sexual orientation;
- gender identity;
- criminal act;
- medical condition;
- psychiatric diagnosis;
- genetic status;
- future behavior;
- any other concrete life event not independently known.

Historical Szondian constructs may be stated fully and directly. They do not automatically become DSM/ICD categories or contemporary factual diagnoses.

The correct pattern is:

> **Szondi's meaning, intact -> Romanian explanation -> clinical exploration -> separate modern boundary only where needed.**

Not:

> **modern safety rewrite -> diluted Szondi.**

---

## 15. E.K.P. and complement material

E.K.P. remains distinct from Vordergrund profiles and from theoretical complement.

The report may and should preserve Szondi's own terminology of `Vordergänger`, `Hintergänger`, complementarity and related direct formulations when source-authorized, with full Romanian explanation.

AI may not turn E.K.P. into:

- "the true hidden self";
- a second personality;
- a proven latent diagnosis;
- a secret behavior profile;
- an inevitable future transition.

This boundary must not neutralize Szondi's actual complement theory; it only prevents unsupported person-level promotion.

---

## 16. Source ambiguity and conflict

AI may not reconcile conflicting sources by stylistic preference or probabilistic language generation.

If admitted Szondi sources conflict or leave a rule ambiguous:

- preserve the conflict;
- route it to doctrinal/source arbitration;
- do not silently choose the version that produces the cleanest report.

If OCR is corrupt, never repair the source quotation silently. Preserve canonical evidence and explicit PDF arbitration separately.

---

## 17. Fail-closed generation rules

AI must abstain or narrow the statement when any of the following occurs:

- missing source support;
- missing executable support;
- unsupported relation between otherwise valid findings;
- scope mismatch;
- unresolved source conflict;
- scoring/ranking not deterministically supplied;
- translation uncertainty that would materially change meaning;
- insufficient evidence for a coherent correlation.

"No authorized correlated synthesis at this level" is a valid product output.

Invented elegance is not.

---

## 18. Clinical report acceptance criteria

A clinician-facing report is not acceptable if any of the following is true:

1. ordinary clinical prose contains internal English software statuses or identifiers;
2. an important German term appears without immediate Romanian explanation;
3. a German quotation is presented without full Romanian translation;
4. source-authorized direct/baroque Szondian language has been softened or replaced;
5. source uncertainty has been inflated into certainty;
6. generic method safeguards are counted as patient findings;
7. atomic findings are mechanically concatenated into a whole-person narrative;
8. AI introduces a relation not represented upstream;
9. AI introduces biography or diagnosis not independently known;
10. AI invents or modifies a percentage/support score;
11. a percentage is called a probability without empirical calibration;
12. different interpretive levels are normalized into one artificial competition;
13. ambiguity is hidden inside verbose hedging instead of being structured;
14. technical audit material overwhelms the clinical reading surface;
15. there is no actual clinical formulation beyond doctrine/audit text;
16. the report cannot be understood by a Romanian-speaking clinician who knows no German;
17. the clinician cannot trace an important interpretation back to source on demand.

Any such case is a reporting defect, not an invitation for AI to improvise around the defect.

---

## 19. Alpha product direction

After review of the first Alpha-0 working report, the immediate product priority is **not** another subsystem and not automatic expansion of the P2B frontier.

The priority is to make the current instrument produce a coherent clinical reading under this manifest.

The next product work should therefore concentrate on:

1. removing technical/internal language from the normal report;
2. enforcing Romanian-first language with complete German translation;
3. preserving Szondi's direct/baroque terminology without euphemization;
4. separating case interpretation from method safeguards and audit;
5. creating real AI clinical formulation from authorized meanings;
6. preventing software `Mosaikspiel` through explicit composition rules;
7. designing, **before implementation**, the deterministic interpretive-support contract required for precise indetermination and relative support weights;
8. testing the resulting report on a small number of real pseudonymized clinical administrations before expanding product scope again.

Do not build support percentages, ranking heuristics or AI scoring by intuition. The scoring contract must come first.

Do not expand architecture merely because it is possible. Alpha observations decide what earns implementation.

---

## 20. Permanent new-chat orientation

For any future development chat involving reports, AI wording, synthesis, interpretive selection, clinical presentation or uncertainty handling:

1. verify live Git state;
2. read `docs/PROJECT_MISSION.md`;
3. read **this manifest** before proposing or implementing clinician-facing interpretation behavior;
4. inspect only the relevant source/doctrine/code layers;
5. make the smallest change that advances the clinical product without violating this contract.

This is not a conversational handoff protocol. The repository is the durable memory.

---

## Final rule

> **The deterministic program decides what is present and, once explicitly designed, how strongly competing authorized interpretations are supported. AI decides only how to say that material clearly in Romanian. Szondi's own voice remains recognizable. The clinician decides what it means in the actual human case.**
