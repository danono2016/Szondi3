"""Initial source-linked P2B claim catalogue.

This first tranche contains structural Ego semantics, serial Trieblinnäus semantics,
and safeguards against over-interpretation. The twenty-one claims have received
explicit clinician review for Cabinet Alpha. Szondian terminology is intentionally
preserved: clinical review constrains inference rather than modernizing the source.
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


STATUS = LifecycleStatus.APPROVED
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
        status=STATUS,
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
    _claim(
        "IC_SZONDI_PRIMARY_000013",
        ("DR_SZ_LEHR_1972_000352",),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch states that exact Sch +± (+k with ±p) means on average ('durchschnittlich') Annahme der Weiblichkeit or Annahme der Verlassenheit; the source sentence supplies no discriminator selecting one branch for an individual profile.",
        "Pentru configurația exactă Sch +± (+k cu ±p), Szondi indică, în medie, «Annahme der Weiblichkeit» sau «Annahme der Verlassenheit»; configurația singură nu decide care dintre cele două ramuri este dominantă într-un caz individual.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(
                Predicate("profile.vector.Sch.base_symbols", Operator.EQ, ("+", "±")),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000013",
                "Nu selecta automat una dintre cele două ramuri și nu transforma Sch +± izolat în dovada unei feminități/identități de gen globale, a unui abandon ori pierderi biografice reale, a unui Kastrationskomplex, a Paranoiden, a unui verdrängter Mutterkomplex sau a creativității/productivității persoanei.",
            ),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000014",
        ("DR_SZ_LEHR_1972_000005",),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch states that one Triebprofil is only one Schicksals-/Existenzmöglichkeit, requires eight to ten profiles, and requires each profile to be interpreted as a whole rather than used to fix the person in a psychiatric diagnosis.",
        "Într-o serie de 8–10 Triebprofile, fiecare profil reprezintă numai una dintre Schicksals-/Existenzmöglichkeiten și trebuie interpretat ca întreg; seria este necesară pentru surprinderea pluralității acestor posibilități.",
        TriggerDefinition(
            kind=TriggerKind.CONDITIONAL_CONTEXTUAL,
            predicates=(Predicate("series.profile_count", Operator.IN, (8, 9, 10)),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000014",
                "Nu transforma un singur Triebprofil într-o descriere exhaustivă a persoanei și nu fixa din acesta un diagnostic psihiatric.",
            ),
        ),
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000015",
        (
            "DR_SZ_LEHR_1972_000321",
            "DR_SZ_LEHR_1972_000322",
            "DR_SZ_LEHR_1972_000324",
            "DR_SZ_LEHR_1972_000326",
        ),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "For a ten-profile series, Lehrbuch defines the current Haupttriebklasse from the greatest intravectorial TspD. When the leading class is in the source-defined Gefahr range, that maximum marks the location of the strongest current Triebgefahr; all four Latenzproportionen remain diagnostically relevant and Gefahr/Ventil is phase-dependent rather than a fixed trait.",
        "Într-o Zehnerserie în care P1 stabilește una sau mai multe Haupttriebklassen aflate în zona Gefahr, maxima TspD indică locul/locurile celei mai puternice Triebgefahr actuale; poziția trebuie citită în raport cu toate cele patru Latenzproportionen și ca stare dinamică de fază, nu ca trăsătură fixă.",
        TriggerDefinition(
            kind=TriggerKind.COMPOSITE,
            predicates=(
                Predicate("series.profile_count", Operator.EQ, 10),
                Predicate("linnaeus.danger_leading_drive_classes", Operator.NE, ()),
                Predicate("linnaeus.latency_proportions", Operator.EXISTS),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000015",
                "Nu transforma Haupttriebklasse sau maxima TspD, luată singură, într-un diagnostic clinic, un «profil dominant» prin frecvență, o trăsătură permanentă de personalitate ori un verdict global; nu ignora celelalte Latenzproportionen și caracterul dinamic Gefahr/Ventil.",
            ),
        ),
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000016",
        (
            "DR_SZ_LEHR_1972_000323",
            "DR_SZ_LEHR_1972_000157",
            "DR_SZ_LEHR_1972_000171",
            "DR_SZ_LEHR_1972_000313",
        ),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch defines Unterklasse signs from the positive/negative Wahlrichtung of the unsatisfied Wurzelfaktor; factor h is the Eros radical of love, tenderness and bonding, +h is the Ego's current affirmation of the Eros/Liebes/Bindungsbedürfnis, and a positive Wurzelfaktor may nevertheless remain unsatisfied.",
        "Într-o Zehnerserie în care P1 stabilește exact Haupttriebklasse Sh în zona Gefahr iar Wurzelfaktor h are Wahlrichtung strict pozitivă, subclasa este Sh+; +h exprimă afirmarea actuală de către Eu a Eros-/Liebes-/Bindungsbedürfnis. Ca Wurzelfaktor pozitiv, această direcție poate rămâne o nevoie nesatisfăcută.",
        TriggerDefinition(
            kind=TriggerKind.COMPOSITE,
            predicates=(
                Predicate("series.profile_count", Operator.EQ, 10),
                Predicate("linnaeus.danger_leading_drive_classes", Operator.EQ, ("Sh",)),
                Predicate("linnaeus.strict_positive_roots", Operator.EQ, ("h",)),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000016",
                "Nu transforma Sh+ sau +h, fără alte condiții explicite din sursă, în dovada homosexualității/bisexualității, a travestismului, a unei identități de gen ori feminități globale, a pasivității, a unei relații biografice concrete sau a satisfacției efective a nevoii; nu importa ramuri care apar numai la Überdruck ori în constelații S specifice cu factorul s.",
            ),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
        hereditary_genetic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000017",
        ("DR_SZ_LEHR_1972_000353",),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch explicitly defines exact Sexualvektor S +0 as a Unitendenz / Dominanz der Personenliebe: +h is the sole sexual Strebung in Vordergrund, while -h, +s and -s remain in Hintergrund. The abnormal/pragenital extension is explicitly conditional on Überdruck.",
        "În configurația exactă S +0, Vektorbild-ul sexual este o Unitendenz, «Dominanz der Personenliebe»: +h este singura Strebung sexuală din Vordergrund, iar −h, +s și −s rămân în Hintergrund. Aceasta este o descriere a organizării Vektorbild-ului, nu o dominanță globală a persoanei.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(
                Predicate("profile.vector.S.base_symbols", Operator.EQ, ("+", "0")),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000017",
                "Nu transforma S +0 de bază în dovada unei sexualități anormale/preregenitale, a homosexualității ori altei orientări sexuale, a unei identități de gen, a unei relații biografice concrete sau a unei trăsături globale de personalitate; ramura «Mit Überdruck» necesită o autorizare separată, quantum-aware.",
            ),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000018",
        ("DR_SZ_LEHR_1972_000354",),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch explicitly defines exact Sexualvektor S +- as diagonal Variation I, linking bejahte Personenliebe (+h) with Passivität/Hingabe (-s); sex-specific and Überdruck extensions are additional contextual branches.",
        "În configurația exactă S +−, Vektorbild-ul sexual este diagonale Spaltung Variation I: bejahte Personenliebe (+h) este legată de Passivität/Hingabe (−s), strict la nivelul acestei configurații vectoriale.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(
                Predicate("profile.vector.S.base_symbols", Operator.EQ, ("+", "-")),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000018",
                "Nu transforma S +− izolat într-o personalitate global «pasivă/submisivă», într-o concluzie despre sex/rol de gen, Triebzielinversion, homosexualitate ori altă orientare sexuală, Masochismus sau o relație biografică concretă; ramurile sex-specifice și «Mit Überdruck» cer context/autorizare separată.",
            ),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000019",
        ("DR_SZ_LEHR_1972_000296", "DR_SZ_LEHR_1972_000297"),
        ("SZ_LEHR_1972",),
        AssertionMode.LIMITATION,
        "Lehrbuch explicitly rejects the Mosaikspiel method and requires factor and vector reactions to be interpreted through interfactorial and intervectorial relations; isolated meanings remain general/abstract until correlated with the rest of the drive profile.",
        "Sensurile factoriale și vectoriale izolate au caracter general/abstract și nu trebuie juxtapuse mecanic într-o descriere individualizată; korrelative Deutung cere ca particularizarea să fie susținută de relațiile interfactoriale și intervectoriale ale profilului.",
        TriggerDefinition(
            kind=TriggerKind.LIMITATION_GUARD,
            predicates=(Predicate("series.profile_count", Operator.EXISTS),),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000019",
                "Nu transforma simpla alăturare a findings-urilor autonome într-o corelație clinică sau într-o sinteză globală a persoanei; nu inventa relații interfactoriale/intervectoriale care nu sunt autorizate de un claim source-grounded separat.",
            ),
        ),
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000020",
        ("DR_SZ_LEHR_1972_000358",),
        ("SZ_LEHR_1972",),
        AssertionMode.CONDITIONAL,
        "Lehrbuch defines exact Kontaktvektor C +- structurally as the simultaneous appearance of Sich-Frei-Machen/Abtrennung (-m) and Auf-Suche-Gehen (+d); the surrounding discussion explicitly allows this movement to be physiological and treats stronger psychopathological labels contextually.",
        "În configurația exactă C +−, Vektorbild-ul de contact exprimă simultan Sich-Frei-Machen/Abtrennung prin −m și Auf-Suche-Gehen prin +d, adică desprinderea și pornirea în căutare la nivelul organizării contactuale.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(
                Predicate("profile.vector.C.base_symbols", Operator.EQ, ("+", "-")),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000020",
                "Nu transforma C +− izolat în dovada infidelității, a depresiei, autismului ori altei patologii, a unei pierderi sau separări biografice reale, a căutării efective a unui «obiect substitut» sau a unui verdict global asupra relațiilor persoanei; asemenea ramuri cer context și autorizare separată.",
            ),
        ),
        pathodiagnostic_content=True,
    ),
    _claim(
        "IC_SZONDI_PRIMARY_000021",
        ("DR_SZ_IA_1956_B_000053",),
        ("SZ_IA_1956_B",),
        AssertionMode.PROBABLE,
        "Ich-Analyse II uses the explicit qualifier `scheinen` for Sch +± and compares `Angst seltener` only with the four immediately preceding defense forms; it does not measure the individual's actual anxiety.",
        "Pentru configurația exactă Sch +±, Szondi descrie Annahme — Introjektion der Verlassenheit bzw. der Weiblichkeit — ca o formă care «pare» (`scheinen`) să aibă mai mult succes în Abwehr von Triebgefahren; în comparația exactă a sursei, Angst este mai rară decât la cele patru Abwehrarten imediat precedente (Sch ±+, Sch −0, Sch ±±, Sch ±−). Relația rămâne testologică și comparativă.",
        TriggerDefinition(
            kind=TriggerKind.EXACT_STRUCTURAL,
            predicates=(
                Predicate("profile.vector.Sch.base_symbols", Operator.EQ, ("+", "±")),
            ),
        ),
        anti_inferences=(
            AntiInference(
                "AI_SZONDI_000021",
                "Nu transforma «Angst seltener» într-o afirmație că persoana are puțină anxietate, nu are anxietate, este psihic sănătoasă, are un Eu global mai sănătos/puternic/matur, dispune de coping sau reziliență superioară ori are apărări global sau în viața reală mai eficiente; nu extinde comparația dincolo de cele patru Abwehrarten precizate de sursă și nu selecta automat ramura Verlassenheit versus Weiblichkeit sau biografia/conținutul ei manifest.",
            ),
        ),
        sexual_content=True,
        pathodiagnostic_content=True,
    ),
)


CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
