"""Current source-linked P2B claim catalogue.

The previously reviewed catalogue is kept byte-identical in
``interpretation_catalogue_base``. This module appends narrowly reviewed claims
while preserving the same public catalogue interface.
"""

from .interpretation_catalogue_base import *  # noqa: F401,F403
from . import interpretation_catalogue_base as _base

_claim = _base._claim


_CLAIM_000024 = _claim(
    "IC_SZONDI_PRIMARY_000024",
    ("DR_SZ_LEHR_1972_000285",),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.CONDITIONAL,
    "Lehrbuch names the complete tritendency Sch −± as `gehemmte Projektion` / `Entfremdung` and analyzes the whole Ich-Bild directly. Because the source does not explicitly establish how quantum overpressure modifies this tritendency, production execution is conservatively limited to ordinary −k and ±p without Überdruck.",
    "În configurația exactă Sch −±, cu −k și ±p fără Überdruck, Ich-Bild-ul poate fi denumit, strict testologic, «Entfremdung» / «gehemmte Projektion».",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("-", "±")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000024",
            "Nu transforma eticheta testologică «Entfremdung / gehemmte Projektion» într-un diagnostic clinic contemporan, într-o afirmație despre pierderea reală a contactului cu realitatea, într-o ramură nosologică vecină, într-o incapacitate funcțională, într-o biografie de înstrăinare ori într-o trăsătură globală/stabilă; nu promova finding-ul la SERIES și nu extinde regula la Sch −± cu Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000025 = _claim(
    "IC_SZONDI_PRIMARY_000025",
    ("DR_SZ_LEHR_1972_000312",),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.DEFINITIONAL,
    "Lehrbuch defines Symptomfaktoren through constant or nearly constant ambivalent/null reactions and places them on the Erscheinungsbild side of the Triebformel; this role does not by itself establish an unconscious causal process.",
    "Într-o Triebformel completă rezolvată, factorii de pe linia simptomatică aparțin laturii de Erscheinungsbild a formulei. Rolul de Symptomfaktor descrie poziția lor formală în formulă și nu stabilește, singur, cauza inconștientă a manifestării.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("formula.symptomatic_factors", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000025",
            "Nu transforma apartenența la linia simptomatică într-un diagnostic, într-o cauză inconștientă demonstrată sau într-o explicație exhaustivă a manifestării clinice.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000026 = _claim(
    "IC_SZONDI_PRIMARY_000026",
    (
        "DR_SZ_LEHR_1972_000313",
        "DR_SZ_LEHR_1972_000347",
        "DR_SZ_LEHR_1972_000348",
    ),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.CONDITIONAL,
    "Lehrbuch describes Wurzel-/Konduktorfaktoren as the formula side of unsatisfied needs / Konduktornatur and historically links Konduktorfaktoren to genealogical validation. It also describes the test as addressing both familial-hereditary and personally acquired/repressed domains; therefore the historical Konduktornatur concept must not be converted into a modern genetic inference from the formula alone.",
    "Într-o Triebformel completă rezolvată, factorii de pe linia Wurzel indică, în modelul lui Szondi, latura nevoilor pulsionale nesatisfăcute / Konduktornatur. Szondi le numește istoric și Konduktorfaktoren și le-a confruntat cu date genealogice, dar simpla lor apariție în formulă nu dovedește o transmitere genetică modernă și nici o patologie familială concretă. Poziția de Wurzelfaktor nu înseamnă automat Verdrängung.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("formula.root_factors", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000026",
            "Nu echivala simpla poziție de Wurzelfaktor cu Verdrängung, diagnostic, cauză inconștientă unică sau trăsătură globală a persoanei; nu o transforma în dovada unei moșteniri genetice contemporane, a unei variante genetice, a unei boli ereditare ori a unei patologii concrete la rude fără date genealogice independente.",
        ),
    ),
    pathodiagnostic_content=True,
    hereditary_genetic_content=True,
)


_CLAIM_000027 = _claim(
    "IC_SZONDI_PRIMARY_000027",
    (
        "DR_SZ_LEHR_1972_000319",
        "DR_SZ_LEHR_1972_000330",
        "DR_SZ_LEHR_1972_000355",
    ),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.CONDITIONAL,
    "Lehrbuch treats Triebklasse and Triebformel as distinct complementary constructions: the class primarily localizes the current danger/root side, while the formula additionally displays Symptomfaktoren as possible manifest outlets/Notausgänge. The same source states that both constructions are only relatively, not absolutely, stable over time and can transform.",
    "Triebklasse și Triebformel trebuie citite complementar, nu ca sinonime: Triebklasse localizează în primul rând latura actuală de Gefahr/Wurzel, iar Triebformel arată suplimentar Symptomfaktoren ca posibile Triebventile/Notausgänge, adică latura manifestă prin care tensiunea poate apărea în Erscheinungsbild. Ambele descriu configurații relativ, nu absolut stabile în timp și se pot transforma; niciuna nu descrie exhaustiv persoana.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.COMPOSITE,
        predicates=(
            _base.Predicate("linnaeus.leading_drive_classes", _base.Operator.EXISTS),
            _base.Predicate("formula.symptomatic_factors", _base.Operator.EXISTS),
            _base.Predicate("formula.root_factors", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000027",
            "Nu identifica Triebklasse cu Triebformel, nu reduce persoana la una dintre ele și nu transforma un posibil Triebventil/Notausgang în dovada unei descărcări comportamentale concrete. Nu trata nici Haupttriebklasse, nici Triebformel ca structură permanentă, identitate fixă sau prognostic imuabil al persoanei.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000028 = _claim(
    "IC_SZONDI_PRIMARY_000028",
    ("DR_SZ_LEHR_1972_000316", "DR_SZ_LEHR_1972_000318"),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.CONDITIONAL,
    "Lehrbuch defines Triebformel as a symptom/root fraction and explicitly states that its interpretive purpose is to reveal the relation between symptom and unterbliebene Triebbefriedigung. This authorizes a relational reading of the two formula sides, not a deterministic causal chain for an individual.",
    "Într-o Triebformel completă rezolvată, sensul central al formulei este relația dintre latura simptomatică și latura satisfacției pulsionale rămase neîmplinite. Formula organizează această relație în termenii modelului lui Szondi; ea nu dovedește singură că un anumit simptom concret este produs în mod unic de un anumit Wurzelfaktor.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.COMPOSITE,
        predicates=(
            _base.Predicate("formula.symptomatic_factors", _base.Operator.EXISTS),
            _base.Predicate("formula.root_factors", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000028",
            "Nu transforma relația Symptomfaktoren–Wurzelfaktoren într-o cauzalitate clinică univocă, într-o explicație exhaustivă a simptomului sau într-o afirmație că un anumit factor-rădăcină produce direct un anumit comportament ori simptom biografic concret.",
        ),
    ),
    sexual_content=True,
    pathodiagnostic_content=True,
)


_CLAIM_000029 = _claim(
    "IC_SZONDI_PRIMARY_000029",
    ("DR_SZ_LEHR_1972_000322", "DR_SZ_LEHR_1972_000326"),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.CONDITIONAL,
    "Lehrbuch interprets Gefahr- and Ventil-class positions dynamically and phase-dependently. The four normalized Latenzproportionen locate current relative danger/outlet structure, while class membership may correspond to a phase before versus after an Ausbruch/Entladung; it is not a fixed trait label.",
    "Configurația Gefahr/Ventil descrie, în modelul lui Szondi, o stare dinamică a raporturilor pulsionale la momentul testării. Pozițiile de Gefahr și Ventil trebuie citite relativ și dependent de fază; ele nu reprezintă etichete fixe ale persoanei și nu permit singure concluzia că o descărcare pulsională concretă a avut sau va avea loc.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.COMPOSITE,
        predicates=(
            _base.Predicate("linnaeus.latency_proportions", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000029",
            "Nu transforma Gefahrklasse, Ventilklasse sau o poziție Gefahr/Ventil într-o trăsătură stabilă, într-un diagnostic, într-o predicție de comportament ori într-o dovadă că un Ausbruch/Entladung concret tocmai s-a produs sau urmează inevitabil; interpretarea rămâne dependentă de faza testării și de ansamblul celor patru Latenzproportionen.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000030 = _claim(
    "IC_SZONDI_PRIMARY_000030",
    ("DR_SZ_IA_1956_B_000038",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "In Szondi's historical Wahn-series material, the leading Ich-Bild is interpreted in relation to the clinical phase present at the time of testing. A mismatch with an earlier recorded episode is therefore not automatically a test failure and does not authorize projecting the earlier episode back into the current series.",
    "În interpretarea patodiagnostică a unei serii, mai ales când rezultatul este comparat cu episoade clinice anterioare, configurația actuală trebuie raportată la faza existentă la momentul testării. Un episod istoric nu poate fi retroproiectat automat în profilurile actuale și o neconcordanță cu anamneza veche nu dovedește singură eșecul testului.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.IN, (8, 9, 10)),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000030",
            "Nu reconstrui retrospectiv un episod clinic anterior din seria actuală și nu cere ca o configurație istorică să reapară obligatoriu la testarea prezentă. Când există anamneză longitudinală, compară separat faza clinică istorică și momentul testării; nu declara automat testul invalid doar din neconcordanța temporală.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000031 = _claim(
    "IC_SZONDI_PRIMARY_000031",
    ("DR_SZ_TRIEBPATH_2_000001",),
    ("SZ_TRIEBPATH_2",),
    _base.AssertionMode.LIMITATION,
    "Triebpathologie II states explicitly that the experiment permits inference only to the possibility of an act and that the committed act itself is not diagnosed. This is a general testological limit, not merely the narrower Sozialindex safeguard already encoded in claim 000006.",
    "Din experimentul Szondi se poate susține, acolo unde există suport doctrinar specific, numai posibilitatea unei fapte; testul, prin el însuși, nu dovedește că persoana a comis efectiv o faptă concretă.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000031",
            "Nu transforma o posibilitate/dispoziție susținută de test într-o afirmație factuală că persoana a comis, a săvârșit sau a realizat efectiv o faptă concretă; existența faptei necesită dovezi independente de experimentul Szondi.",
        ),
    ),
    criminological_content=True,
)


_CLAIM_000032 = _claim(
    "IC_SZONDI_PRIMARY_000032",
    ("DR_SZ_LEHR_1972_000334",),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.LIMITATION,
    "Lehrbuch explicitly states that Proporzmethoden are only partial, not total, interpretive procedures. They provide sector-specific Einzeldata rather than a reading of Gesamtpersönlichkeit or Gesamtschicksal; the concrete meaning and validity conditions remain specific to each proportion method.",
    "Metodele proporționale oferă date parțiale despre anumite raporturi ale seriei; ele nu constituie, singure, o interpretare totală a persoanei. Sensul clinic al fiecărui indice proporțional trebuie limitat la sectorul și regulile pe care sursa le definește pentru acel indice și integrat cu restul profilului/seriei.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.IN, (8, 9, 10)),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000032",
            "Nu transforma Dur–Moll, Sozialindex sau altă proporție source-defined într-un rezumat global al persoanei, într-un diagnostic total, într-o explicație cauzală ori într-o predicție comportamentală autonomă; nu atribui unei proporții un sens clinic generic care nu este autorizat separat de sursă.",
        ),
    ),
    sexual_content=True,
)


_CLAIM_000033 = _claim(
    "IC_SZONDI_PRIMARY_000033",
    ("DR_SZ_LEHR_1972_000336",),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.LIMITATION,
    "Lehrbuch gives an approximately 2 D:1 M male Dur-Moll calibration in its historical empirical/genetic framework, but explicitly says that whether this calibration still applies in the present would have to be investigated. The same passage states that psychosexual normality from the index does not establish normality in other sectors of existence.",
    "Etalonarea Dur–Moll de aproximativ 2D:1M aparține cadrului empiric și istoric al lui Szondi și nu trebuie tratată ca normă universală actuală fără revalidare. Chiar dacă indexul ar susține, în termenii sursei, o «normalitate psihosexuală», aceasta nu autorizează concluzia că persoana este «normală» în alte sectoare ale existenței.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("dur_moll.index.available", _base.Operator.EQ, True),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000033",
            "Nu prezenta raportul istoric aproximativ 2D:1M ca normă masculină universală sau validată pentru populația actuală; nu generaliza o eventuală «normalitate psihosexuală» la personalitatea ori sănătatea globală și nu transforma legătura istorică a lui Szondi cu Gentheorie într-o inferență genetică modernă despre persoană.",
        ),
    ),
    sexual_content=True,
    hereditary_genetic_content=True,
)


_CLAIM_000034 = _claim(
    "IC_SZONDI_PRIMARY_000034",
    ("DR_SZ_LEHR_1972_000344",),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.CONDITIONAL,
    "Lehrbuch explains the quantity of image choices in each factor space by the current magnitude of Bedürfnisspannung: greater need tension attracts repeated choices and can produce Quantumspannung. The executable trigger uses only P1 quantum marks and does not add a new scoring threshold.",
    "Prezența Quantumspannung (`!`) într-unul sau mai mulți factori indică, în modelul lui Szondi, o Bedürfnisspannung actuală crescută în spațiul factorilor respectivi. Este o informație despre tensiunea nevoii exprimată în profilul testologic actual, nu despre severitatea clinică globală a persoanei.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.quantum_tension_factors", _base.Operator.NE, ()),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000034",
            "Nu transforma Quantumspannung într-un scor de severitate psihopatologică, într-un diagnostic, într-o trăsătură stabilă/globală, într-o măsură generică a intensității persoanei sau într-o predicție că nevoia respectivă va produce un comportament ori un act concret; interpretarea rămâne locală factorului și profilului actual.",
        ),
    ),
)


_CLAIM_000037 = _claim(
    "IC_SZONDI_PRIMARY_000037",
    ("DR_SZ_IA_1956_A_000047",),
    ("SZ_IA_1956_A",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse defines Introprojektion as the coupled Ego bifunction +k/-p and gives its testological Ich-Bild as Sch +−. The same passage places autistic thinking/behavior and a broader theory of Weltbild formation around this mechanism, but those contextual claims are not imported into the minimal executable relation. Because the source does not establish quantum-overpressure variants, production execution is conservatively limited to ordinary +k and −p.",
    "În configurația exactă Sch +−, cu +k și −p fără Überdruck, Ich-Bild-ul poate fi denumit testologic «Introprojektion»: proiecția prin −p și introiecția/asimilarea prin +k funcționează împreună. Finding-ul descrie această bifuncție a Eului, nu un diagnostic clinic.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "-")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000037",
            "Nu transforma Sch +− / Introprojektion într-un diagnostic de autism, într-o afirmație că persoana are comportament autist, într-o descriere a conținutului concret al Weltbild-ului, într-o dovadă că proiectează efectiv arhetipuri, într-o trăsătură globală/stabilă sau într-un finding SERIES; variantele cu Überdruck necesită autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000038 = _claim(
    "IC_SZONDI_PRIMARY_000038",
    ("DR_SZ_IA_1956_A_000046",),
    ("SZ_IA_1956_A",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse explicitly distinguishes Identifizierung from Identität and gives the cross-factor reaction coupling −m with +k for introjective identification. +k supplies Introjektion/Einverleibung; the source's lost-object and narcissistic wording remains source-local context rather than a factual biography or modern diagnosis. Because quantum-overpressure variants are not separately established, production execution is limited to ordinary −m and +k.",
    "În cuplarea exactă −m cu +k, fără Überdruck, Szondi descrie testologic o «introjektive Identifizierung»: identificarea se organizează prin Introjektion/Einverleibung (+k), în relație cu −m. Esențial, Identifizierung nu este echivalentă cu Identität; finding-ul descrie un mecanism testologic, nu identitatea persoanei.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.COMPOSITE,
        predicates=(
            _base.Predicate("profile.factor.m.base_symbol", _base.Operator.EQ, "-"),
            _base.Predicate("profile.factor.k.base_symbol", _base.Operator.EQ, "+"),
            _base.Predicate("profile.factor.m.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000038",
            "Nu transforma −m/+k într-o afirmație despre identitatea globală a persoanei, într-o dovadă că a existat o pierdere, un deces ori o separare biografică reală, într-o identificare cu un obiect sau o persoană concretă, într-un diagnostic ori o trăsătură modernă de narcisism sau într-un finding SERIES; nu extinde regula la variante cu Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000039 = _claim(
    "IC_SZONDI_PRIMARY_000039",
    ("DR_SZ_IA_1956_B_000003", "DR_SZ_IA_1956_B_000004"),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II defines intrafactorial k-dialectic as the coexistence of Introjektion (+k) and Negation (−k), testologically expressed by ±k. In the exact Sch ±0 configuration it names this bifunction Intronegation / Zwang-Ich. The source's stronger Dur-Ich and Zwangsschicksal extension is historical contextual doctrine and is not promoted into an individual prediction. Because quantum-overpressure variants are not separately established here, production execution is conservatively limited to ordinary ±k and 0p.",
    "În configurația exactă Sch ±0, fără Überdruck, factorul k exprimă simultan cele două tendințe complementare Introjektion (+k) și Negation (−k). Szondi numește această bifuncție «Intronegation» și, la nivel testologic, «Zwang-Ich». Finding-ul descrie dialectica internă a Eului k, nu dovedește o tulburare compulsivă a persoanei.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("±", "0")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000039",
            "Nu transforma Sch ±0 / «Zwang-Ich» într-un diagnostic de tulburare obsesiv-compulsivă sau alt diagnostic contemporan, într-o dovadă a unor obsesii ori compulsii reale, într-un «Zwangsschicksal» inevitabil, într-o concluzie despre masculinitate/sex/identitate de gen, într-o trăsătură globală ori stabilă sau într-un finding SERIES; nu extinde regula la variante cu Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000040 = _claim(
    "IC_SZONDI_PRIMARY_000040",
    ("DR_SZ_IA_1956_B_000016",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II explicitly separates the formal/descriptive level of the Ich-Bild from the functional/dynamic level of the Ich-Mechanismus. Ich-Bilder are current static Ego states; a dynamic unconscious function or defense technique is a different interpretive level and must not be inferred merely by renaming the same Sch reaction.",
    "În interpretarea vectorului Sch, «Ich-Bild» și «Ich-Mechanismus» sunt niveluri distincte. Ich-Bild-ul descrie mai întâi o configurație actuală, statică a Eului; atribuirea unui mecanism dinamic/inconștient sau a unei tehnici de apărare cere suport interpretativ separat. O formulă Sch nu devine automat dovada unui mecanism psihic activ doar prin etichetare.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000040",
            "Nu transforma direct un Ich-Bild sau o formulă Sch într-un mecanism defensiv demonstrat, într-un proces inconștient factual, într-un comportament observat, într-o trăsătură stabilă/globală ori într-un diagnostic; trecerea de la nivelul static-descriptiv la cel funcțional-dinamic necesită o regulă source-grounded separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000041 = _claim(
    "IC_SZONDI_PRIMARY_000041",
    ("DR_SZ_IA_1956_B_000020",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II differentiates Negation from Verdrängung and defines the exact Sch −0 configuration as totale Negation / Verdrängung. Its distinguishing p-component is 0p, described as complete evacuation from Egodiastole (`absolute Räumung`) and only quasi an Endstation of the negation process. Because the source does not separately establish quantum-overpressure variants, production execution is conservatively limited to ordinary −k and 0p.",
    "În configurația exactă Sch −0, fără Überdruck, Ich-Bild-ul este numit de Szondi «totale Negation / Verdrängung»: −k indică Negation, iar 0p marchează, în terminologia sursei, evacuarea completă din Egodiastole («absolute Räumung»). Este o clasificare testologică a configurației, nu dovada conținutului concret al unui proces de refulare.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("-", "0")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000041",
            "Nu transforma Sch −0 într-o dovadă că un mecanism psihodinamic modern de refulare a fost observat direct, nu inventa reprezentarea, dorința sau conținutul presupus refulat și nu infera traumă, amnezie, evitare, diagnostic ori o trăsătură globală/stabilă. «Quasi Endstation» nu înseamnă stadiu final inevitabil al persoanei. Nu promova finding-ul la SERIES și nu extinde regula la variante cu Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000042 = _claim(
    "IC_SZONDI_PRIMARY_000042",
    ("DR_SZ_IA_1956_B_000027",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II gives two testological routes of Personabildung and maps collective Introinflation to the exact Sch ++ configuration: Introjektion (+k) and Inflation (+p) operate together. The surrounding Persona/Allessein/reality-danger discussion is contextual and must not be converted into factual biography or diagnosis. Because quantum-overpressure variants are not separately established, production execution is limited to ordinary +k and +p.",
    "În configurația exactă Sch ++, cu +k și +p fără Überdruck, Szondi descrie o bifuncție testologică pe care o numește «Introinflation» / «kollektive Introinflation»: Introjektion (+k) și Inflation (+p) funcționează împreună. Finding-ul descrie forma Sch actuală; nu dovedește un rol social, o Persona concretă sau o pierdere a contactului cu realitatea.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "+")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000042",
            "Nu transforma Sch ++ / Introinflation într-o dovadă a unei Persona jungiene concrete, a unui rol social adoptat, a grandiozității, omnipotenței, «Allessein»-ului factual, a pierderii contactului cu realitatea sau a unui diagnostic; nu deduce conținutul colectiv introiectat și nu transforma finding-ul într-o trăsătură globală/stabilă ori într-un finding SERIES. Variantele cu Überdruck necesită autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _base.INITIAL_CLAIMS + (
    _CLAIM_000024,
    _CLAIM_000025,
    _CLAIM_000026,
    _CLAIM_000027,
    _CLAIM_000028,
    _CLAIM_000029,
    _CLAIM_000030,
    _CLAIM_000031,
    _CLAIM_000032,
    _CLAIM_000033,
    _CLAIM_000034,
    _CLAIM_000037,
    _CLAIM_000038,
    _CLAIM_000039,
    _CLAIM_000040,
    _CLAIM_000041,
    _CLAIM_000042,
)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
