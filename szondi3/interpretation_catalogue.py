"""Source-linked P2B claim catalogue.

The first twelve claims form the clinician-approved Cabinet Alpha production
nucleus.  The Fall40 tranche extends the preview/review surface with a deliberately
small set of source-verified factor semantics and interpretation safeguards.  Those
new claims remain FORMALIZATION_REVIEWED until explicit clinician review; production
mode therefore continues to admit only the original approved nucleus.
"""

from fractions import Fraction

from .interpretation import (
    AntiInference,
    AssertionMode,
    ClaimDefinition,
    EpistemicClass,
    LifecycleStatus,
    Operator,
    Predicate,
    TriggerDefinition,
    TriggerKind,
)


APPROVED = LifecycleStatus.APPROVED
FORMALIZATION_REVIEWED = LifecycleStatus.FORMALIZATION_REVIEWED
PRIMARY = "SZONDI_PRIMARY"


def _claim(
    claim_id: str,
    doctrine_ids: tuple[str, ...],
    source_ids: tuple[str, ...],
    assertion_mode: AssertionMode,
    source_strength_note: str,
    claim: str,
    trigger: TriggerDefinition,
    *,
    status: LifecycleStatus = APPROVED,
    anti_inferences: tuple[AntiInference, ...] = (),
    sexual_content: bool = False,
    pathodiagnostic_content: bool = False,
    criminological_content: bool = False,
    hereditary_genetic_content: bool = False,
) -> ClaimDefinition:
    return ClaimDefinition(
        schema_version=1,
        claim_id=claim_id,
        rule_version=1,
        status=status,
        source_layer=PRIMARY,
        doctrine_ids=doctrine_ids,
        source_ids=source_ids,
        epistemic_class=EpistemicClass.SOURCE_ESTABLISHED_TRIGGER,
        assertion_mode=assertion_mode,
        source_strength_note=source_strength_note,
        claim=claim,
        trigger=trigger,
        anti_inferences=anti_inferences,
        sexual_content=sexual_content,
        pathodiagnostic_content=pathodiagnostic_content,
        criminological_content=criminological_content,
        hereditary_genetic_content=hereditary_genetic_content,
    )


INITIAL_CLAIMS = (
    _claim(
        "IC_SZONDI_PRIMARY_000001",
        ("DR_SZ_LEHR_1972_000313",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "Szondi explicitly states that a negative Wurzelfaktor reaction is not synonymous with Verdrängung.",
        "Un Wurzelfaktor cu Wahlrichtung negativă nu înseamnă automat Verdrängung; sursa admite și Verzicht sau Anpassung.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("linnaeus.strict_negative_roots", Operator.NE, ()),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000001",
                "Nu concluziona Verdrängung numai dintr-un Wurzelfaktor negativ.",
            ),
        ),
        pathodiagnostic_content=True,
        hereditary_genetic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000002",
        ("DR_SZ_LEHR_1972_000313",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "Szondi explicitly allows a constantly positive Wurzelfaktor reaction to represent an unsatisfied need without repression.",
        "O Wahlrichtung pozitivă constantă a Wurzelfaktor-ului nu exclude o nevoie nesatisfăcută și nu dovedește absența conflictului pulsional.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("linnaeus.strict_positive_roots", Operator.NE, ()),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000002",
                "Nu interpreta automat Wurzelfaktor pozitiv ca absență a unei nevoi nesatisfăcute.",
            ),
        ),
        pathodiagnostic_content=True,
        hereditary_genetic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000003",
        ("DR_SZ_LEHR_1972_000328",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "The source explicitly forbids behavioral inference from TspQu alone and requires confrontation with profile reactions.",
        "TspQu nu se interpretează autonom; concluziile despre comportament trebuie confruntate cu reacțiile factorilor și vectorilor din profile.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("series.indices.available", Operator.EQ, True),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000003",
                "Nu deduce comportamentul numai din mărimea TspQu.",
            ),
        ),
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000004",
        ("DR_SZ_LEHR_1972_000329",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "Szondi says %Sy-Re must be evaluated with TspQu and that these data are never sufficient for clinical diagnosis.",
        "%Sy-Re și TspQu sunt date parțiale ale seriei și nu sunt suficiente, singure, pentru un diagnostic clinic.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("series.indices.available", Operator.EQ, True),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000004",
                "Nu formula un diagnostic clinic numai din %Sy-Re și/sau TspQu.",
            ),
        ),
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000005",
        ("DR_SZ_LEHR_1972_000337",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "The source says Dur-Moll must never be used alone for social valuation and requires synoptic reading with Sozialindex.",
        "Dur–Moll nu poate fundamenta singur evaluarea socială a unei persoane sau a unui grup; sursa cere lectura sinoptică împreună cu Sozialindex.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("dur_moll.index.available", Operator.EQ, True),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000005",
                "Nu produce o evaluare socială numai din Dur–Moll.",
            ),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
        criminological_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000006",
        ("DR_SZ_LEHR_1972_000340",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "The source's normal-zone statement is qualified ('scheint'), while the prohibition against inferring a criminal act below 40% is explicit.",
        "Un Sozialindex sub 40% nu autorizează concluzia că persoana a comis sau va comite o faptă criminală/antisocială.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(
                Predicate("social_index.positive_percentage", Operator.LT, Fraction(40, 1)),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000006",
                "Nu infera o faptă criminală din Sozialindex < 40%.",
            ),
        ),
        pathodiagnostic_content=True,
        criminological_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000007",
        ("DR_SZ_IA_1956_A_000043",),
        ("SZ_IA_1956_A",),
        AssertionMode.DEFINITIONAL,
        "Ich-Analyse defines -p as Projektion, with Einssein/Gleichsein and Partizipationsdrang as its end-direction.",
        "În lectura funcției elementare a Eului, -p desemnează Projektion, orientată spre Einssein/Gleichsein și Partizipationsdrang.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.p.base_symbol", Operator.EQ, "-"),),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000008",
        ("DR_SZ_IA_1956_A_000043",),
        ("SZ_IA_1956_A",),
        AssertionMode.DEFINITIONAL,
        "Ich-Analyse defines +p as Inflation, directed toward Verdoppelung/Vollkommenheit/Allessein.",
        "În lectura funcției elementare a Eului, +p desemnează Inflation, orientată spre Verdoppelung, Vollkommenheit și Allessein.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.p.base_symbol", Operator.EQ, "+"),),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000009",
        ("DR_SZ_IA_1956_A_000043",),
        ("SZ_IA_1956_A",),
        AssertionMode.DEFINITIONAL,
        "Ich-Analyse defines +k as Introjektion, directed toward Einverleibung/Inbesitznahme/Alleshaben.",
        "În lectura funcției elementare a Eului, +k desemnează Introjektion, orientată spre Einverleibung, Inbesitznahme și Alleshaben.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.k.base_symbol", Operator.EQ, "+"),),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000010",
        ("DR_SZ_IA_1956_A_000043", "DR_SZ_IA_1956_A_000049"),
        ("SZ_IA_1956_A",),
        AssertionMode.DEFINITIONAL,
        "Ich-Analyse defines -k as the Negation family; Verdrängung is explicitly only one subordinate form of Negation.",
        "În lectura funcției elementare a Eului, -k indică familia Negation; Verdrängung este numai o Unterform și nu trebuie echivalată automat cu orice -k.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.k.base_symbol", Operator.EQ, "-"),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000010",
                "Nu transforma automat orice -k în Verdrängung.",
            ),
        ),
        pathodiagnostic_content=True,
        criminological_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000011",
        ("DR_SZ_IA_1956_A_000051", "DR_SZ_IA_1956_B_000009"),
        ("SZ_IA_1956_A", "SZ_IA_1956_B"),
        AssertionMode.CONDITIONAL,
        "A identifies Sch ±± as integriertes Ich; B explicitly distinguishes theoretical complement from actual integration, which occurs only very rarely.",
        "Sch ±± poate fi denumit, la nivel testologic, configurația «integriertes Ich»; această etichetă nu dovedește că persoana a realizat efectiv integrarea globală descrisă de Szondi.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(
                Predicate("profile.vector.Sch.base_symbols", Operator.EQ, ("±", "±")),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000011",
                "Nu echivala Sch ±± cu dovada unei integrări reale, stabile, existențiale sau spirituale a persoanei.",
            ),
        ),
        pathodiagnostic_content=True,
        criminological_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000012",
        ("DR_SZ_IA_1956_A_000051", "DR_SZ_IA_1956_B_000010"),
        ("SZ_IA_1956_A", "SZ_IA_1956_B"),
        AssertionMode.CONDITIONAL,
        "A names Sch 00 Desintegration; B requires Vorder-/Hinter-Ich dialectic for adequate symptom analysis.",
        "Sch 00 poate fi denumit, la nivelul Ich-Bild-ului testologic, «Desintegration»; un profil izolat nu autorizează transformarea etichetei într-un verdict global și permanent asupra persoanei.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(
                Predicate("profile.vector.Sch.base_symbols", Operator.EQ, ("0", "0")),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000012",
                "Nu transforma Sch 00 dintr-un profil izolat într-un verdict global/permanent fără analiza dialecticii Vorder-Ich/Hinter-Ich relevante.",
            ),
        ),
        pathodiagnostic_content=True,
        criminological_content=True,
    ),
)


FALL40_CANDIDATE_CLAIMS = (
    _claim(
        "IC_SZONDI_PRIMARY_000013",
        ("DR_SZ_LEHR_1972_000129",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "Szondi states as a general rule that the interpretation of one factor always depends on the constellation of its partner factor.",
        "Niciun Triebfaktor nu se interpretează izolat: semnificația lui trebuie citită în constelația Partnerfaktor-ului din același vector.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("profile.available", Operator.EQ, True),),
        ),
        status=FORMALIZATION_REVIEWED,
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000013",
                "Nu transforma o reacție factorială izolată într-o concluzie clinică independentă de Partnerfaktor.",
            ),
        ),
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000014",
        ("DR_SZ_LEHR_1972_000145",),
        ("SZ_LEHR_1972",),
        AssertionMode.DEFINITIONAL,
        "Szondi defines quantum tension as Überdruck/Hypertonie of the affirmative or negative Ego stance toward the tendency.",
        "Semnul de Quantumspannung (!) marchează Überdruck/Hypertonie a afirmării sau negării tendinței respective; nu constituie prin el însuși o categorie clinică separată.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.quantum_factors", Operator.NE, ()),),
        ),
        status=FORMALIZATION_REVIEWED,
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000014",
                "Nu deduce un diagnostic numai din prezența unui semn de Quantumspannung (!).",
            ),
        ),
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000015",
        ("DR_SZ_LEHR_1972_000157", "DR_SZ_LEHR_1972_000171"),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch defines h as the Eros radical and describes +h as the Ego's affirmation of Eros/Liebe/Bindungsbedürfnis.",
        "+h exprimă afirmarea actuală a Erosului, a nevoii de iubire, tandrețe, atracție și Bindung.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.h.base_symbol", Operator.EQ, "+"),),
        ),
        status=FORMALIZATION_REVIEWED,
        sexual_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000016",
        ("DR_SZ_LEHR_1972_000171",),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "For positive h with Überdruck, Szondi explicitly names an above-average accumulation of Eros: Eroshypertonie.",
        "+h cu Quantumspannung indică, în limbajul sursei, Eroshypertonie: o acumulare peste medie a Erosului afirmată de Eu.",
        TriggerDefinition(
            kind=TriggerKind.COMPOSITE,
            predicates=(
                Predicate("profile.factor.h.base_symbol", Operator.EQ, "+"),
                Predicate("profile.factor.h.quantum_level", Operator.GT, 0),
            ),
        ),
        status=FORMALIZATION_REVIEWED,
        sexual_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000017",
        ("DR_SZ_LEHR_1972_000259", "DR_SZ_LEHR_1972_000261"),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch places -e on the Kain side of the factor's ethical polarity and explicitly warns that a medium -e reaction does not by itself establish serious epileptiform illness.",
        "În polaritatea factorului e, −e aparține direcției Kain; această reacție nu autorizează singură diagnosticul unei boli epileptiforme și nici un verdict criminologic asupra persoanei.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.e.base_symbol", Operator.EQ, "-"),),
        ),
        status=FORMALIZATION_REVIEWED,
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000017",
                "Nu deduce epilepsie, faptă violentă sau criminalitate numai din −e.",
            ),
        ),
        pathodiagnostic_content=True,
        criminological_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000018",
        ("DR_SZ_LEHR_1972_000260",),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Szondi states that hypertonically negative e indicates an extremely threatening accumulation of coarse affects, with paroxysmal discharge risk; the partner hy modifies the danger assessment.",
        "−e cu Quantumspannung indică, în formularea lui Szondi, o acumulare extrem de amenințătoare a groben Affekte și posibilitatea unei descărcări paroxismale; aprecierea pericolului depinde și de Partnerfaktor hy.",
        TriggerDefinition(
            kind=TriggerKind.COMPOSITE,
            predicates=(
                Predicate("profile.factor.e.base_symbol", Operator.EQ, "-"),
                Predicate("profile.factor.e.quantum_level", Operator.GT, 0),
            ),
        ),
        status=FORMALIZATION_REVIEWED,
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000018",
                "Nu transforma −e! singur într-un diagnostic clinic sau într-o predicție de violență.",
            ),
        ),
        pathodiagnostic_content=True,
        criminological_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000019",
        ("DR_SZ_LEHR_1972_000262",),
        ("SZ_LEHR_1972",),
        AssertionMode.DEFINITIONAL,
        "Lehrbuch defines -hy as the hiding pole of hy, linked to Verbergung, shame and retreat from display, with extreme withdrawal toward unreality/immobility in the source model.",
        "−hy aparține polului Verbergungsdrang: ascundere, rușine și retragere din expunere; în formele extreme descrise de sursă, retragerea poate merge spre irealitate și imobilizare.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.hy.base_symbol", Operator.EQ, "-"),),
        ),
        status=FORMALIZATION_REVIEWED,
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000020",
        ("DR_SZ_LEHR_1972_000293",),
        ("SZ_LEHR_1972",),
        AssertionMode.DEFINITIONAL,
        "Lehrbuch defines +d as the change/search pole opposed to -d persistence: Veränderung and Auf-Suche-Gehen toward new objects and values.",
        "+d exprimă Veränderung și Auf-Suche-Gehen: orientarea spre căutarea unor obiecte și valori noi, în opoziție cu Beharrung/Kleben al lui −d.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.d.base_symbol", Operator.EQ, "+"),),
        ),
        status=FORMALIZATION_REVIEWED,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000021",
        ("DR_SZ_LEHR_1972_000294",),
        ("SZ_LEHR_1972",),
        AssertionMode.DEFINITIONAL,
        "Lehrbuch defines -m as Loslösung/Abtrennung/Freiheit from the object, opposed to +m Anklammerung/Akzeptation/Sicherung.",
        "−m exprimă Loslösung, Abtrennung și Freiheit față de obiect; direcția sa de bază este desprinderea/separarea, nu incapacitatea de a se desprinde.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(Predicate("profile.factor.m.base_symbol", Operator.EQ, "-"),),
        ),
        status=FORMALIZATION_REVIEWED,
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000021",
                "Nu inversa sensul lui −m în 'incapacitate de desprindere'; sursa îl definește prin Loslösung/Abtrennung/Freiheit.",
            ),
        ),
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000022",
        ("DR_SZ_LEHR_1972_000193",),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "Szondi states that 0s is an actual relative diminution and must always be evaluated in relation to the strength of partner factor h.",
        "0s indică o diminuare actuală și relativă a factorului s; trebuie evaluat numai în raport cu forța Partnerfaktor-ului h și nu ca absență absolută a tendinței s.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("profile.factor.s.base_symbol", Operator.EQ, "0"),),
        ),
        status=FORMALIZATION_REVIEWED,
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000022",
                "Nu interpreta 0s ca absență absolută/permanentă a factorului s și nu îl citi fără h.",
            ),
        ),
        sexual_content=True,
    ),
)


EXECUTABLE_CLAIMS = INITIAL_CLAIMS + FALL40_CANDIDATE_CLAIMS
CLAIMS_BY_ID = {claim.claim_id: claim for claim in EXECUTABLE_CLAIMS}

if len(CLAIMS_BY_ID) != len(EXECUTABLE_CLAIMS):
    raise ValueError("Duplicate executable P2B claim identity")
