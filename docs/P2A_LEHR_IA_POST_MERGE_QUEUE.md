# SZONDI3 — Lehrbuch ↔ Ich-Analyse post-merge integration queue

**Status:** READ-ONLY CANDIDATE QUEUE — NO RELATIONS COMMITTED  
**Layer:** `DOCTRINE_REPRESENTATION` integration planning  
**Dependency:** actual `DC_*`, `XR_*`, and `UQ_*` records wait until referenced doctrine IDs coexist stably on `main`.

## Purpose

This document pre-identifies a small set of high-value Lehrbuch/Ich-Analyse comparisons so the first transversal integration pass can begin immediately after merge without performing broad topic-first exploration.

It does **not** decide relation types. Every candidate below must be re-read in both canonical contexts after merge. If the relation remains uncertain, create `UQ_*` rather than forcing `QUALIFIES`, `EXTENDS`, `RESTATES`, or `CONTRADICTS`.

IA IDs below are current PR #52 branch IDs and remain volatile until merged.

## Queue 1 — p/k functional polarity

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000265` — k = Ich-Einengung/Egosystole; p = Ich-Erweiterung/Egodiastole.
- `DR_SZ_LEHR_1972_000273` — p as diastolic factor; Allodiastole/Partizipation-Projektion and Egodiastole/Inflation.

**Ich-Analyse candidate**

- `DR_SZ_IA_1956_A_000040` — Egodiastole/Ich-Ausdehnung maps to p; Egosystole/Ich-Einengung maps to k and underlies all Ego functions/stages.

**Post-merge question**

Does IA-A merely restate the Lehrbuch polarity, or does its stronger claim that all Ich-Funktionen/Ich-Stadien rest on this polarity materially `EXTEND` the Lehrbuch definition?

**Priority:** very high — foundational for all later Sch/Ego retrieval.

## Queue 2 — four elementary Ego functions and signs

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000268` — four Elementarfunktionen: Projektion, Inflation, Introjektion, Negation.
- `DR_SZ_LEHR_1972_000269` — +k Introjektion / −k Negation.
- `DR_SZ_LEHR_1972_000273` — p/Egodiastole with Projektion/Partizipation and Inflation.

**Ich-Analyse candidate**

- `DR_SZ_IA_1956_A_000043` — PDF-arbitrated exact mapping `-p/+p/+k/-k` to Projektion/Inflation/Introjektion/Negation with source-defined end-directions.

**Post-merge question**

Which parts are direct `RESTATES`, and which are genuine elaborations requiring `EXTENDS` rather than one broad equivalence relation?

**Priority:** very high.

## Queue 3 — Negation versus Verdrängung

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000270` — Negation is an unconscious radical Ego function with several forms including Anpassung, Hemmung, Verdrängung and Entfremdung.
- `DR_SZ_LEHR_1972_000274` — 0p evacuation is differentiated through k; −k is associated with Verdrängung in that correlative configuration.

**Ich-Analyse candidates**

- `DR_SZ_IA_1956_A_000049` — explicit revision: Negation is Hauptbegriff/Ich-Radikal, Verdrängung only a subordinate form; concrete negative forms depend on p and quantity of negation.
- `DR_SZ_IA_1956_B_000020` — detailed negating-defense taxonomy; totale Negation = Verdrängung, projective Negation = Anpassung; Verdrängung is characterized by 0p/absolute Räumung and source-near `quasi` Endstation wording.

**Post-merge questions**

1. Is IA-A `RESTATES` or `EXTENDS` Lehrbuch 000270?
2. Does IA-B 000020 `NARROW` the conditions under which the Lehrbuch 0p/k rule may be called Verdrängung?
3. Can the three-source-local objects jointly justify a later P2B anti-inference: `-k` alone is not equivalent to repression?

**Priority:** critical — direct anti-overinterpretation safeguard.

## Queue 4 — `Ich-Bild` versus `Ich-Mechanismus`

**Lehrbuch candidate**

- `DR_SZ_LEHR_1972_000279` — every Sch configuration requires two modes of reading: phenomenological/static Ich-Bild and functional-defensive Ich-Abwehrmechanismus.

**Ich-Analyse candidates**

- `DR_SZ_IA_1956_B_000016` — formal/descriptive current-static `Ich-Bild` versus functional/dynamic unconscious `Ich-Mechanismus` / Abwehrtechnik.
- `DR_SZ_IA_1956_B_000015` — defense originates from Ego but its operating site may lie in any of the four drive zones.

**Post-merge questions**

1. Is IA-B 000016 a direct `RESTATES`, a more explicit `EXTENDS`, or an explicit later clarification of Lehrbuch 000279?
2. Does IA-B 000015 `QUALIFY` any tendency to identify Ego defense exclusively with the Sch vector?

**Priority:** critical — required before executable Sch narratives.

## Queue 5 — Intronegation / Zwang

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000272` — Zwang as coupled Introjektion + Negation / Intronegation.
- `DR_SZ_LEHR_1972_000283` — Sch ±0 operationalized as Intronegation with simultaneous Introjektion and Verdrängung.

**Ich-Analyse candidate**

- `DR_SZ_IA_1956_B_000019` — introjective defense taxonomy: totale Introjektion, inflaprojektive Introjektion and Intronegation/Zwangsmechanismus; in Zwang one tendency is incorporated while the other is repressed.

**Post-merge question**

Does IA-B primarily `RESTATES` the mechanism, or `EXTEND` it by placing Intronegation inside a broader introjective-defense taxonomy?

**Priority:** high.

## Queue 6 — Projektion, Deprojektion and participation

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000276` — −p has distinct participation, projection and object-search meanings; childhood Sch 0− must not be automatically pathologized.
- `DR_SZ_LEHR_1972_000280` — Sch 0− / total projection in its primordial form as Partizipation/Dualexistenz.
- `DR_SZ_LEHR_1972_000284` — Hemmung as negated Inflation with complementary autistisches Ich.
- `DR_SZ_LEHR_1972_000285` — Entfremdung as a configuration containing projection/inflation/negation without +k.
- `DR_SZ_LEHR_1972_000286` — Sch ±+ explicitly has several source-sanctioned decompositions.

**Ich-Analyse candidates**

- `DR_SZ_IA_1956_A_000043` — −p Projektion with Partizipationsdrang end-direction.
- `DR_SZ_IA_1956_B_000017` — five projective defense forms; only totale Projektion is projection as Unifunktion, the other four belong to Deprojektion.

**Post-merge questions**

1. Which Lehrbuch configuration readings map directly into IA-B's later Deprojektion taxonomy?
2. Where does later taxonomy merely systematize earlier cases versus materially change the interpretation level?
3. Which relations must remain `ALTERNATIVE_FORMULATION` because the sources use different decompositional frames?

**Priority:** high, but after Queues 1–5.

## Queue 7 — Inflation / Deflation

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000275` — +p Inflation / Egodiastole, with explicit anti-overpathologizing condition for Sch 0+.
- `DR_SZ_LEHR_1972_000284` — Hemmung as Deflation through negation.
- `DR_SZ_LEHR_1972_000286` — Sch ±+ polysemy involving Inflation and Zwang.

**Ich-Analyse candidate**

- `DR_SZ_IA_1956_B_000018` — totale Inflation versus three Deflation forms: Introinflation, Zwangsdeflation, Hemmung/negierte Inflation; one submechanism retains `Annahme` strength.

**Post-merge question**

Does IA-B provide a taxonomic `EXTENDS` relation to specific Lehrbuch configuration doctrines, or should several narrower relations be used to preserve source-specific epistemic strength?

**Priority:** high.

## Queue 8 — Integration / Desintegration / experimental Sch ±±

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000277` — Sch ±± can have more than one source-sanctioned meaning and p alone cannot diagnose homosexuality.
- `DR_SZ_LEHR_1972_000287` — Integration = availability of all four elementary functions/defense forms; experimental Sch ±± is not by itself proof of spiritual participation or transcendence.

**Ich-Analyse candidates**

- `DR_SZ_IA_1956_A_000051` — integrated Ego = Sch ±±, Desintegration = Sch 00; integration of all four Ego radicals as ideal, with unifunction danger.
- `DR_SZ_IA_1956_B_000008` — ±± ↔ 00 as one of eight exact complementary Vorder-/Hinter-Ich pairs.
- `DR_SZ_IA_1956_B_000009` — theoretical Ergänzung always possible but actual Integration occurs `nur sehr selten`.
- `DR_SZ_IA_1956_B_000014` — current IA-B source-local limit leaves exhaustiveness of eight complementary Ego fates provisionally open.

**Post-merge questions**

1. How should structural `Sch ±± = integrated Ego image`, complementary-pair membership and real-world achieved Integration remain distinct in retrieval?
2. Which relation is source-explicit versus integration-inferred?
3. Is an open question needed to prevent downstream collapse of testological image, complementary structure and existential ideal?

**Priority:** critical before any Integration-related P2B rule.

## Queue 9 — Vorder-Ich / Hinter-Ich correction to earlier interpretation

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000282` — forensic configuration explicitly requires consideration that a Täter-Ich may have moved into Hinter-Ich.
- `DR_SZ_LEHR_1972_000284` and related configuration entries — complementary Hinter-Ich readings are already present in some Lehrbuch interpretations.
- Additional method-level Lehrbuch targets must be identified by canonical reconsultation rather than assuming the entire book is one doctrine object.

**Ich-Analyse candidates**

- `DR_SZ_IA_1956_B_000006` — Vorder-/Hinter-Ich definition.
- `DR_SZ_IA_1956_B_000007` — explicit retrospective statement that earlier Vorder-Ich-only Ich-Analyse in `Experimentelle Triebdiagnostik` was `eine halbierte`.
- `DR_SZ_IA_1956_B_000010` — symptom analysis without both Ego existences is `stets mangelhaft und oft irreführend`.
- `DR_SZ_IA_1956_B_000011–000014` — complement-profile diagnostic safeguards and provisional limits from Batch 002.

**Post-merge questions**

1. Which exact Lehrbuch doctrine object is the correct target of the source-explicit retrospective correction?
2. Where does Lehrbuch already anticipate Hinter-Ich, making the relation a qualification of scope rather than a contradiction?
3. Should the broad methodological self-correction be represented as one relation plus several narrower dependencies, or as an open question until source boundaries are re-read?

**Priority:** highest methodological integration task.

## Queue 10 — origin and site of defense

**Lehrbuch candidates**

- `DR_SZ_LEHR_1972_000263` — source-level assumption that the Ego chooses among hysteriform defense mechanisms.
- `DR_SZ_LEHR_1972_000279` — Sch read as Ich-Abwehrmechanismus on the functional level.

**Ich-Analyse candidate**

- `DR_SZ_IA_1956_B_000015` — defense always originates from Ego, while defense sites/paths can run through all four drive zones.

**Post-merge question**

Does IA-B `EXTEND` the Lehrbuch defense model by explicitly separating source/origin of defense from its vectorial operating site? This is likely relevant to P2B architecture but must be decided only after canonical reconsultation.

**Priority:** critical structural safeguard.

## Queue 11 — defense ↔ Sexualgefahr mappings

**Lehrbuch candidates**

- configuration-level Sch doctrines in `DR_SZ_LEHR_1972_000275–000287` where Sexualbild is an explicit condition or modifier.

**Ich-Analyse candidate**

- `DR_SZ_IA_1956_B_000021` — Sch defense forms mapped to several types of Sexualgefahr with `scheinen` and `unter Umständen` qualifiers preserved.

**Post-merge policy**

Defer executable use. First determine whether relations are `EXTENDS`, `DEPENDENT_ON`, or merely contextual parallels. Preserve the sexual/pathodiagnostic historical wording and source epistemic qualifiers exactly.

**Priority:** later/high-risk.

## First concept addresses to create after merge

If the canonical re-read confirms these families, the first `DC_*` concepts should be minimal retrieval addresses, approximately:

1. p/k Egodiastole–Egosystole polarity;
2. four elementary Ego functions;
3. Negation versus Verdrängung;
4. Ich-Bild versus Ich-Mechanismus;
5. defense origin versus defense site;
6. Intronegation/Zwang;
7. Projektion/Deprojektion;
8. Inflation/Deflation;
9. Integration/Desintegration;
10. Vorder-Ich/Hinter-Ich/complement profile.

The labels above are not reserved IDs and are not definitions. Stable `DC_*` identities are allocated only on the post-merge integration snapshot.

## Post-merge execution order

For each queue item:

1. fetch both doctrine objects from `main`;
2. fetch their exact canonical U ranges;
3. re-read enough surrounding units to recover scope/epistemic force;
4. inspect PDF only where sign/layout/table evidence matters;
5. decide one narrow relation aspect at a time;
6. if relation typing remains uncertain, create `UQ_*`;
7. validate through `scripts/validate_transversal_doctrine.py`;
8. require clinician/steward review before accepting high-consequence relations.

## Final invariant

> **This queue accelerates reconsultation; it does not pre-decide doctrine. No cross-source relation exists until both sides are stable on `main`, both canonical contexts have been re-read, and the relation survives review.**
