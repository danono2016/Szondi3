# P2B Semantic Coverage Matrix

Status: **STRUCTURAL FIRST PASS COMPLETE — SOURCE ADJUDICATION IN PROGRESS — VALIDATED REMEDIATIONS RECORDED — NO NEW P2B FRONTIER AUTHORIZATION**

Baseline: `2dfbfccb4951b3042c26e2637d285fd7b598de50`

Audit branch: `work/p2b-semantic-coverage-audit-001`

This matrix inventories the P2B identity surface from `IC_SZONDI_PRIMARY_000001` through `000087`. This file is documentation-only: it does not itself change activation, doctrine, scoring, reports, or AI behavior. It does record explicitly authorized remediation state already present on the branch.

There are **84 present claim identities** in the `000001`-`000087` interval. Historical holes `000022`, `000035`, and `000036` are preserved as holes and are not candidates for reuse. `000021` remains a historical identity but is projected as `SUPERSEDED` in the current public catalogue; the public frontier remains `000087`.

## Reading rules

- The A/B1/B2/C/D class is a **semantic-sufficiency class**, not a substitute for trigger validation.
- A claim with a trigger-fidelity problem is marked `BLOCKED: TRIGGER` until the trigger boundary is resolved; it is not forced into A/B1/B2/C/D.
- A lifecycle remediation such as current-frontier `SUPERSEDED` is recorded explicitly rather than forced into A/B1/B2/C/D.
- `A candidate` means the current semantic packet appears proportionate to the reviewed doctrine at this stage, but full source-by-source reverse audit is not yet complete.
- `B1 candidate` means the already-linked doctrine itself contains clinically useful semantic reserve that the executable wording does not fully carry.
- `B2 candidate` means enrichment would require an additional reviewed doctrine relation or source reconsultation.
- `D/guard candidate` is used for guards/limitations whose job is epistemic boundary precision rather than narrative richness.
- No row below authorizes a new executable identity or broader behavioral implementation.

## Matrix 000001-000023

| ID | Trigger / scope | Linked doctrine | Current semantic packet | Critical boundary | Preliminary class | Next audit action |
|---|---|---|---|---|---|---|
| 000001 | Linnäus negative Wurzelfaktor / SERIES | LEHR 313 | negative root is not automatically Verdrängung; may be Verzicht/Anpassung | no repression inference from sign alone | D/guard candidate | source spot-check |
| 000002 | Linnäus positive Wurzelfaktor / SERIES | LEHR 313 | positive root may remain unsatisfied | positive does not mean satisfied | D/guard candidate | source spot-check |
| 000003 | TspQu exists / SERIES | LEHR 328 | TspQu is not autonomous; must be confronted with profile | no diagnosis from quotient alone | D/guard candidate | source spot-check |
| 000004 | `% Sy.-Re.` + TspQu / SERIES | LEHR 329 | partial quantitative relation only | no clinical diagnosis | D/guard candidate | preserve known threshold conflict separately |
| 000005 | Dur-Moll output / SERIES | LEHR 337 | Dur-Moll does not establish social valuation by itself | Sozialindex required | D/guard candidate | source spot-check |
| 000006 | Sozialindex low range / SERIES | LEHR 340 | historical social-index association remains probabilistic | no criminal act inference; preserve `scheint` | D/guard candidate | modality check |
| 000007 | factor p− / PROFILE | IA-A 43 | Projektion -> Einssein/Gleichsein/Partizipationsdrang | factor meaning, not biography | A candidate | source spot-check |
| 000008 | factor p+ / PROFILE | IA-A 43 | Inflation -> Verdoppelung/Vollkommenheit/Allessein | factor meaning, no global grandiosity diagnosis | A candidate | source spot-check |
| 000009 | factor k+ / PROFILE | IA-A 43 | Introjektion -> Einverleibung/Inbesitznahme/Alleshaben | no automatic concrete possession/biography | **B1 candidate** | linked doctrine already also says Assimilation of Wertobjekte/Wertvorstellungen of inner and outer world; define safe semantic reserve |
| 000010 | factor k− / PROFILE | IA-A 43,49 | Negation family; Verdrängung is subordinate, not synonym | no automatic repression | A candidate | source spot-check |
| 000011 | exact Sch ±± / PROFILE | IA-A 51; IA-B 9 | integrated Ego testologically | no global/permanent integration | A candidate | source spot-check |
| 000012 | exact Sch 00 / PROFILE | IA-A 51; IA-B 10 | Desintegration testologically | no global/permanent Ego loss | A candidate | source spot-check |
| 000013 | exact Sch +± / PROFILE | LEHR 352 | Annahme der Weiblichkeit **or** Annahme der Verlassenheit | test does not discriminate content branch | A candidate | quantum boundary spot-check |
| 000014 | 8-10 profile method / SERIES | LEHR 5 | each profile = one current Schicksals-/Existenzmöglichkeit and must be interpreted as a whole | no exhaustive person description or psychiatric diagnosis from one profile | **D/guard** | source-adjudicated methodological guard; preserve series-level scope |
| 000015 | 10-profile Linnäus danger leader / SERIES | LEHR 321,322,324,326 | greatest TspD locates strongest current Triebgefahr; all four Latenzproportionen remain relevant | current/phase-dynamic, not a fixed trait or diagnosis | **A** | source-adjudicated; preserve dynamic wording and full latency context |
| 000016 | exact Sh danger + strict positive h root / SERIES | LEHR 323,157,171,313 | +h = current Eros/Liebe/Bindung affirmation; a positive Wurzelfaktor may remain unsatisfied | no orientation/gender/biography inference; no import of overpressure or s-branches | **A** | source-adjudicated; preserve exact Sh/positive-root trigger and unsatisfied-root boundary |
| 000017 | exact S +0 / PROFILE | LEHR 353 | Unitendenz / Dominanz der Personenliebe; +h sole foreground S striving | `Mit Überdruck` is an additional branch and is not imported by this packet | **A** | source-adjudicated; base-symbol core remains valid without q0 gating; keep overpressure extension excluded |
| 000018 | exact S +− / PROFILE | LEHR 354 | diagonal split: +h Personenliebe with −s Passivität/Hingabe | sex-specific and `Mit Überdruck` extensions require separate support and are not imported | **A** | source-adjudicated; base-symbol core remains valid without q0 gating; keep contextual extensions excluded |
| 000019 | any interpreted series / GUARD | LEHR 296,297 | anti-Mosaikspiel: isolated meanings remain general/abstract until source-grounded correlation | no invented interfactorial/intervectorial synthesis | **D/guard** | source-adjudicated global composition constraint; preserve as limitation |
| 000020 | exact C +− / PROFILE | LEHR 358 | Sich-Frei-Machen/Abtrennung + Auf-Suche-Gehen | no actual separation, infidelity, substitute object, depression/autism or other pathology from the vector alone | **A** | source-adjudicated structural core; preserve contextual/pathological anti-inferences |
| 000021 | historical Sch +± base-only trigger / PROFILE; current frontier lifecycle `SUPERSEDED` | IA-B 53 | historical probabilistic Annahme comparison; no current executable finding | precise ordinary-only route is 000081; historical identity must remain unchanged | **RESOLVED: SUPERSEDED** | preserve historical identity; exclude from current execution |
| 000022 | — | — | **historical hole; no current claim** | must remain unused | — | preserve |
| 000023 | exact P 0− with hy quantum 0 / PROFILE | LEHR 361 | historical `sensitive Beziehungsangst` as testological marker | no modern anxiety diagnosis; no hy-Überdruck import | A candidate | source spot-check |

## Matrix 000024-000054

| ID | Trigger / scope | Linked doctrine | Current semantic packet | Critical boundary | Preliminary class | Next audit action |
|---|---|---|---|---|---|---|
| 000024 | exact ordinary Sch −± / PROFILE | LEHR 285 | Entfremdung / gehemmte Projektion | exact configuration only | A candidate | source spot-check |
| 000025 | symptomatic factor relation / SERIES | LEHR 312 | formula factor = Erscheinungsbild, not unconscious cause | no etiological inversion | D/guard candidate | source spot-check |
| 000026 | Wurzelfaktor / SERIES | LEHR 313,347,348 | root factor is unsatisfied; historical Konduktornatur context | no modern genetic/carrier conclusion; no automatic repression | D/guard candidate | hereditary-language audit |
| 000027 | Triebklasse + Triebformel / SERIES | LEHR 319,330,355 | class and formula are distinct/complementary | do not collapse either into diagnosis | D/guard candidate | source spot-check |
| 000028 | formula relation / SERIES | LEHR 316,318 | symptom ↔ underfulfilled drive satisfaction relation | not deterministic causality | D/guard candidate | modality check |
| 000029 | Gefahr/Ventil outputs / SERIES | LEHR 322,326 | phase-dynamic Gefahr/Ventil | no fixed trait | D/guard candidate | source spot-check |
| 000030 | historical Wahn-related series comparison / SERIES | IA-B 38 | current test phase need not reproduce old episode | mismatch is not test failure and does not license retroprojection | D/guard candidate | historical/pathognostic audit |
| 000031 | pathognostic act possibility / PROFILE/SERIES | TRIEBPATH II 1 | source can indicate possibility, not committed act | no act attribution | D/guard candidate | source modality check |
| 000032 | Proporz methods / SERIES | LEHR 334 | partial quantitative methods | no total personality conclusion | D/guard candidate | source spot-check |
| 000033 | Dur-Moll calibration / SERIES | LEHR 336 | historical calibration and psychosexual classification | no global normality or modern sex/gender conclusion | D/guard candidate | historical-context audit |
| 000034 | factor quantum `!` / PROFILE | LEHR 344 | heightened current Bedürfnisspannung local to factor/profile | not severity, behavior, diagnosis; does not import factor semantic branch automatically | A candidate | keep narrow; critical control for s+! |
| 000035 | — | — | **historical hole; no current claim** | must remain unused | — | preserve |
| 000036 | — | — | **historical hole; no current claim** | must remain unused | — | preserve |
| 000037 | exact ordinary Sch +− / PROFILE | IA-A 47 | introprojective Ego configuration (+k/−p) | no automatic autism/worldview branch | A candidate | compare overlap with 000068/000072; meanings are distinct, not assumed duplicate |
| 000038 | exact ordinary −m/+k / PROFILE | IA-A 46 | introjektive Identifizierung; Einverleibung; Identifizierung != Identität | no proof of actual biographical loss | **B1 candidate** | linked doctrine itself additionally contains `Aufrichtung des verlorenen Objektes im Ich` and calls introjective +k identification narcissistic; separate concept from biography; `psychischer Kannibalismus` still requires B2 relation |
| 000039 | exact ordinary Sch ±0 / PROFILE | IA-B 3,4 | Intronegation / Zwang-Ich | no OCD diagnosis | A candidate | source spot-check |
| 000040 | Ich-Bild / GUARD | IA-B 16 | static/descriptive configuration is not automatically dynamic mechanism | no mechanism inference from image alone | D/guard candidate | source spot-check |
| 000041 | exact ordinary Sch −0 / PROFILE | IA-B 20 | totale Negation/Verdrängung; 0p absolute Räumung; `quasi` Endstation | preserve `quasi`; no absolute developmental law | A candidate | source spot-check |
| 000042 | exact ordinary Sch ++ / PROFILE | IA-B 27 | Introinflation / kollektive Introinflation | Persona/Allessein/reality branches require their own support | A candidate | compare distinct semantic route 000073 |
| 000043 | Wahn taxonomy / GUARD | IA-B 34 | requires clinical history + series | no diagnosis from isolated test configuration | D/guard candidate | historical/pathognostic audit |
| 000044 | series meaning / SERIES | SA 1948 58-62 | Triebschicksal from test series is not whole life/fate | Mental-/Sozialschicksal separate | D/guard candidate | source spot-check |
| 000045 | heredity/genotropism theory / GUARD | SA 1948 | historical Szondian hereditary model | no modern genetic inference | D/guard candidate | historical-language audit |
| 000046 | E.K.P. exists / COMPLEMENT | IA-B 6,7,9,11,43 | E.K.P. is a distinct observed complementary profile | never mix with foreground; never equate automatically with Th.K.P./Hinter-Ich | A candidate | preserve outside AI ordinary report scope |
| 000047 | E.K.P.-Th.K.P. Sch exact match / COMPLEMENT | IA-B 8,9,11,43 | structural Sch concordance only | no latent true self/global complement inference | A candidate | source spot-check |
| 000048 | E.K.P.-Th.K.P. mismatch / COMPLEMENT | IA-B 8,14,43 | preserve observed E.K.P.; do not force theoretical complement | no arbitrary replacement | A candidate | source spot-check |
| 000049 | E.K.P./Th.K.P. Sch match + later same Sch foreground / SERIES | IA-B 6,8,9 | possible `sukzessive Kontrastwirkung` | implementation-inferred trigger; not proof whole Hinter-Ich manifested | **B2 / trigger-review candidate** | reconsult exact sufficiency of operational discriminator before any enrichment |
| 000050 | both +k and −k somewhere in foreground series / SERIES | IA-A 40,48 | variation between opposite Egosystole poles | no split-personality inference | A candidate | implementation-inference review |
| 000051 | both −p and +p somewhere in foreground series / SERIES | IA-A 40,43,45 | variation between Egodiastole poles | no inferred phase order; preserve source assumption language | A candidate | implementation-inference review |
| 000052 | >=3 reactions in syndrome construction context / SERIES | TRIEBPATH II 2; LEHR 350 | minimum repetition condition is necessary, not sufficient | test syndrome != clinical diagnosis | D/guard candidate | source spot-check |
| 000053 | latency/class direction / SERIES | TRIEBPATH II 3 | cannot determine current illness vs health by itself | no present mental-state diagnosis | D/guard candidate | source spot-check |
| 000054 | Linnäus result exists / SERIES | LEHR 362,302,359 | quantitative orientation valid in own layer; qualitative Rand-Mitte/Vorder-Hinter needed for individual defense relation | absence of qualitative analysis does not invalidate quantitative output | D/guard candidate | source spot-check |

## Matrix 000055-000087

| ID | Trigger / scope | Linked doctrine | Current semantic packet | Critical boundary | Preliminary class | Next audit action |
|---|---|---|---|---|---|---|
| 000055 | exact s+!! + ordinary e+ / PROFILE | TRIEBPATH I 2,3 | intense s danger with e+ Gutmachung/Gewissensschutz | no aggressive behavior or defense-success inference | A candidate | source spot-check |
| 000056 | exact s+!! + e0 / PROFILE | TRIEBPATH I 2,4 | Aggressionsgefahr without ethischen Schutz in source model | no behavior/global conscience inference | A candidate | source spot-check |
| 000057 | defense-zone interpretation / GUARD | IA-B 15 | Ego defense operates across all four drive zones | do not reduce defense to Sch alone | D/guard candidate | source spot-check |
| 000058 | p− / PROFILE | IA-B 17 | five projective modes exist | p− alone cannot identify total projection | D/guard candidate | source spot-check |
| 000059 | exact ordinary Sch 0+ / PROFILE | IA-B 18 | totale Inflation, unifunctional defense | no psychosis/grandiosity diagnosis | A candidate | source spot-check |
| 000060 | exact ordinary Sch ±+ / PROFILE | IA-B 18 | Zwangsdeflation / stance against Inflation | no OCD | A candidate | source spot-check |
| 000061 | exact ordinary Sch −+ / PROFILE | IA-B 18 | Hemmung / negierte Inflation | content remains undetermined | A candidate | source spot-check |
| 000062 | exact ordinary Sch +0 / PROFILE | IA-B 19 | totale Introjektion; both opposite strivings incorporated; Einverleibung; Seinsanspruch -> Habanspruch | no automatic pathological/narcissistic spectrum from current linked doctrine | **B2 candidate** | reconsult/additional doctrine relation required for Egoismus, Egozentrismus, Narzißmus, Habmachtsucht and historical extremes |
| 000063 | exact ordinary Sch +± / PROFILE | IA-B 19 | inflaprojektive Introjektion; Vorphase of total introjection | no automatic branch content | A candidate | source spot-check |
| 000064 | exact ordinary Sch −− / PROFILE | IA-B 20 | projektive Negation / Anpassung; reality-check/adaptation in source model | no global mental-health conclusion | A candidate | source spot-check |
| 000065 | exact Sch −!!− with k q2 / PROFILE | IA-B 20 | Destruktion / strong Verneinung | no actual violence/destruction behavior | A candidate | exact quantum/source notation check |
| 000066 | exact ordinary Sch 0− / PROFILE | IA-B 17 | totale Projektion | no psychosis/biography inference | A candidate | source spot-check |
| 000067 | exact ordinary Sch 0± / PROFILE | IA-B 17 | inflative Projektion | no automatic content selection | A candidate | source spot-check |
| 000068 | exact ordinary Sch +− / PROFILE | IA-B 17 | introjektive Projektion / Introprojektion; displaced strivings incorporated | distinct from total introjection | A candidate | compare distinct semantic route 000037/000072 |
| 000069 | exact ordinary Sch ±− / PROFILE | IA-B 17 | Fugue/Flucht; projection held by Zwang | historical construct, not literal travel/flight behavior | A candidate | source spot-check |
| 000070 | exact ordinary S (++/0+/+0) plus exact Sch defense set / PROFILE | IA-B 21 | source relation between `aktuell gesteigerte, grobsinnliche Sexualität` and specified Ego defenses | no sexual behavior, orientation or diagnosis inference; do not euphemize source wording | A candidate | exact S notation/quantum review |
| 000071 | exact ordinary Sch ±+, −0, ±±, ±− / PROFILE | IA-B 54 | `am häufigsten` with Angstzustände; defended excitations may return | no actual anxiety diagnosis | A candidate | modality check |
| 000072 | exact ordinary Sch +− / PROFILE | IA-B 27 | Persona formation through collective Introprojektion | no total personality reduction | A candidate | distinct from 000037/000068 |
| 000073 | exact ordinary Sch ++ / PROFILE | IA-B 27 | Persona via kollektive Introinflation | Allessein requires source-grounded Deflation/reality relation | A candidate | distinct from 000042 |
| 000074 | character analysis from foreground only / GUARD | IA-B 29 | Vordergänger-only character analysis is half-analysis | no invented Hinter-Ich/ancestry | D/guard candidate | source spot-check |
| 000075 | exact ordinary Sch +± / PROFILE | IA-B 56 | Annahme protects with `größtem Erfolg` against gross Kain affects / `am meisten vor der Kain-Gefahr` | no violence-risk inference | A candidate | compare with 000081 without collapsing distinct claim |
| 000076 | exact ordinary Sch +− or ±− / PROFILE | IA-B 56 | source says least adequate protection against `Tötungsansprüche Kains` for Introprojektion/Autismus or Flucht | no homicide/autism diagnosis | A candidate | historical/pathognostic audit |
| 000077 | exact ordinary Sch 0± or −± / PROFILE | IA-B 57 | `am häufigsten` mild Abel affect nature | probabilistic, no global temperament certainty | A candidate | modality check |
| 000078 | exact ordinary C −− plus Sch 0+ or ++ / PROFILE | IA-B 58 | source says narcissistic forms of Ego protection occur most often in specified contact configuration | source context cannot select specific incest/bisexual/inverted/perverse branch | A candidate | historical/sexual branch audit |
| 000079 | Sublimationsart context / GUARD | IA-B 24 | Ego defense matters for sublimation; source table incomplete | no exhaustive taxonomy | D/guard candidate | source spot-check |
| 000080 | character/fate relation / GUARD | IA-B 25 | `Charakter ist Schicksal` is limited; character is only introjected/imprinted part | fate exceeds character | D/guard candidate | source spot-check |
| 000081 | exact Sch +± **and k/p quantum 0** / PROFILE | IA-B 53 | probabilistic Annahme/Angst comparison with `scheinen`; ordinary-only | do not extend to Überdruck; sole current executable route for this IA-B 53 relation | **A candidate** | preserve q0/q0 boundary and supersession of 000021 |
| 000082 | exact ordinary C 00 + Sch ±± / PROFILE | IA-B 59 | contactlessness with participation in one spiritual idea; other objects absent | no global social isolation/psychosis inference | A candidate | source spot-check |
| 000083 | exact ordinary C 00 + Sch +± / PROFILE | IA-B 59 | Introjektion der Verlassenheit; source model of abandoning-mother image conditioning later choices; `blind/skotomisiert` toward other objects | no proof of actual mother history | A candidate | biographical anti-inference audit |
| 000084 | exact ordinary Sch 00/+0/+− plus specified C set / PROFILE | IA-B 60 | interpersonal relationships `stets unsicher, problematisch` in source-defined configurations | configuration relation, not universal biography | A candidate | exact domain review |
| 000085 | introjective character formation / GUARD | IA-B 26 | rejects pure one-function model; other Ego functions participate | no modern genetics from historical genotropism | D/guard candidate | source spot-check |
| 000086 | exact ordinary Sch set + P signature e± or hy± / PROFILE | IA-B 55 | Szondi says `oft` ethical/moral/double dilemmas | disjunctive and probabilistic; no actual moral conflict certainty | A candidate | trigger-domain and modality check |
| 000087 | series exists / SERIES | IA-A 38 | familial/inherited drive dialectic is modifiable; Stellungnahme can alter dominance/integration; Umkehrung = dominance change | no fixed fate; no modern genetic efficacy claim; do not claim change of `Ursubstanz` | D/guard candidate | historical/genetic language audit |

## Resolved systemic trigger finding: 000021 versus 000081

This was the first defect found by the matrix pass that was **not merely a richness problem**.

Both identities link to `DR_SZ_IA_1956_B_000053` and carry the same core semantic relation: for Sch +±, Annahme is described with the source qualifier `scheinen`, with Angst rarer than in the four immediately preceding defense forms.

At the frozen baseline, however:

- `000021` activated from `profile.vector.Sch.base_symbols == ("+", "±")` alone;
- `000081` required the same base symbols **plus** `k.quantum_level == 0` and `p.quantum_level == 0`, and explicitly prohibited extension to Überdruck.

That baseline allowed duplicate activation for ordinary Sch +± and leakage of `000021` into Sch +± with overpressure.

The authorized remediation preserves the historical `000021` definition but projects it as `SUPERSEDED` in the current public catalogue. Runtime lifecycle filtering excludes `SUPERSEDED` before trigger evaluation. `000081` remains `APPROVED` and is now the sole executable route for this semantic relation.

Focused regressions prove that ordinary Sch +± q0/q0 surfaces `000081` but not `000021`, while k- or p-overpressure surfaces neither. Existing Annahme tests were also aligned to the full `000081` support bundle: vector Sch base symbols, k quantum level and p quantum level. The transferred remediation passed Foundation verification, Runtime tests and P2A doctrine registry on the active branch.

**Resolution: CLOSED.** `000021` is no longer `BLOCKED: TRIGGER`; it is a preserved historical identity with current lifecycle `SUPERSEDED`. Other overlap/quantum audits remain open.

## Source-adjudicated checkpoint: 000014-000020

Canonical reconsultation of the primary Lehrbuch and current executable definitions supports the following checkpoint: `000014 D/guard`, `000015 A`, `000016 A`, `000017 A`, `000018 A`, `000019 D/guard`, `000020 A`.

- `000014`: Szondi states that one Triebprofil discloses only one of many Schicksals-/Existenzmöglichkeiten, requires eight to ten profiles, and requires each profile to be interpreted in its Ganzheit. The current claim is therefore a correctly scoped methodological guard, not an independent person-level narrative finding.
- `000015`: the source defines the greatest intravectorial TspD as the locator of the strongest **current** Triebgefahr and embeds that result in the full set of Latenzproportionen. The current packet preserves both the localization and phase-dynamic boundary.
- `000016`: the source derives Unterklasse signs from the Wahlrichtung of the unsatisfied Wurzelfaktor, and +h denotes the affirmed Eros-/Liebes-/Bindungsbedürfnis. A positive root can remain unsatisfied; the current packet and trigger preserve that distinction.
- `000017`: S +0 is source-defined as Unitendenz / Dominanz der Personenliebe, with +h alone in the foreground. `Mit Überdruck` is an additional semantic branch, not a replacement of the base vector organization. Because the executable packet carries only the core vector meaning and explicitly blocks the overpressure extension, q0 gating is not required for this core claim.
- `000018`: S +− is source-defined as the diagonal coupling of Personenliebe (+h) with Passivität/Hingabe (−s). Sex-specific and `Mit Überdruck` readings are contextual extensions. The executable packet carries only the core vector organization and blocks those extensions, so q0 gating is likewise not required merely to state the core.
- `000019`: the Lehrbuch explicitly rejects `Mosaikspiel` and requires korrelative Deutung through interfactorial and intervectorial relations. The executable limitation is semantically proportionate and remains a global anti-synthesis guard.
- `000020`: C +− is source-defined structurally through simultaneous Sich-Frei-Machen/Abtrennung (−m) and Auf-Suche-Gehen (+d). The same discussion makes clear that this movement can be physiological and that depressive/autistic or object-loss readings are contextual; the current anti-inferences correctly block promotion of those branches from the vector alone.

**Trigger result for this slice: no new blocker.** In particular, the base-symbol selectors of `000017` and `000018` are not equivalent to importing their `Mit Überdruck` branches; those richer branches remain excluded by claim content and anti-inference. This differs from a claim whose asserted meaning itself is adjudicated as ordinary-only.

This checkpoint is documentation-only. It does not mutate P1, P2A, P2B, reporting/AI runtime, lifecycle, source excerpts, or the public frontier.

## Already-confirmed semantic reserve inside existing support

Two clinically important thinness cases can now be separated more precisely:

### `000009` (+k)

Its already-linked doctrine `DR_SZ_IA_1956_A_000043` explicitly defines +k not only as Einverleibung/Inbesitznahme/Alleshaben but also as **Assimilation der Wertobjekte und Wertvorstellungen der äußeren und inneren Welt**. This is a genuine B1 reserve: no new trigger and no new doctrine relation is required to acknowledge that source-authorized semantic field. Whether downstream wording should expose all of it remains a separate versioned P2B/report design decision.

### `000038` (−m/+k)

Its already-linked doctrine `DR_SZ_IA_1956_A_000046` explicitly says Identifizierung != Identität, links introjective identification to Einverleibung and to **Aufrichtung des verlorenen Objektes im Ich**, and calls the introjective (+k) and inflative (+p) identification forms narcissistic. This supports a B1 semantic reserve **at the level of Szondi's conceptual mechanism**. It still does not authorize the case-level assertion that a real biographical object was in fact lost. The separate expression `psychischer Kannibalismus` is not admitted into this B1 packet by this record and remains a B2 reconsultation question.

By contrast, `000062` (Sch +0) remains B2: its current linked doctrine supports totale Introjektion, Einverleibung, incorporation of opposing strivings and Seinsanspruch -> Habanspruch, but the broader source field `Egoismus, Egozentrismus, Narzißmus, Habmachtsucht` requires an explicitly reviewed additional support relation before executable enrichment.

## Reverse-audit queue exposed by the control specimen

These remain **C candidates at P2B, not claim authorizations**, but their P2A support is now materialized and CI-validated:

- exact `S −+!` -> `DR_SZ_LEHR_1972_000363`: vector-level `Sadismus mit Unterdrückung des Eros`, with the exact q1 configuration separated from generic overpressure language; historical retired `000235` is provenance only and is not reused;
- exact ordinary `P −−` -> `DR_SZ_LEHR_1972_000364`: `innere Panik`, `Beklemmungen`, `Immobilisierung` / `Sich-tot-Stellen` dynamic;
- exact ordinary `C 0−` -> `DR_SZ_LEHR_1972_000365`, qualified by `DR_SZ_LEHR_1972_000366`: contact-vector semantic field plus the explicit boundary that Szondi's `hypomanische Reaktion` is not psychiatric Hypomanie/Manie.

The existing generic quantum claim `000034` must **not** be widened to smuggle these vector meanings into P2B. No `IC_SZONDI_PRIMARY_000088` or later identity has been created.

Operator counter-verification for the newly rematerialized P2A round remains pending as a provenance-control condition before a future P2B activation decision.

## Gate status after this pass

- Structural inventory of `000001`-`000087`: **complete**.
- Historical holes: **preserved**.
- First trigger-boundary conflict `000021`/`000081`: **resolved, regression-covered, active-branch CI validated**.
- Source adjudication `000014`-`000020`: **complete for this slice** (`D/guard, A, A, A, A, D/guard, A`); no new trigger blocker found.
- Control-specimen P2A gaps: **materialized as LEHR 000363-000366 and P2A-CI validated; no P2B routes created**.
- Known B1 semantic reserve: **identified** (`000009`, `000038`).
- Known B2 semantic reserve: **identified** (`000062`, plus the `psychischer Kannibalismus` extension question for `000038`).
- Reverse C queue: **started, not complete**.
- Canonical reconsultation for every row: **not complete**.
- Operator counter-verification for the new P2A rematerialization round: **pending**.
- New P2B implementation authorization: **NO**.
- Public P2B frontier: **000087**.