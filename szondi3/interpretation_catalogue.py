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
    ("DR_SZ_LEHR_1972_000319", "DR_SZ_LEHR_1972_000330"),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.CONDITIONAL,
    "Lehrbuch treats Triebklasse and Triebformel as distinct complementary constructions: the class primarily localizes the current danger/root side, while the formula additionally displays Symptomfaktoren as manifest outlets/Notausgänge. The same passage states that both constructions are only relatively, not absolutely, stable over time and can transform.",
    "Triebklasse și Triebformel trebuie citite complementar, nu ca sinonime: Triebklasse localizează în primul rând latura actuală de Gefahr/Wurzel, iar Triebformel arată suplimentar Symptomfaktoren, adică latura manifestă prin care tensiunea poate apărea în Erscheinungsbild. Ambele descriu configurații relativ, nu absolut stabile în timp și se pot transforma; niciuna nu descrie exhaustiv persoana.",
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
            "Nu identifica Triebklasse cu Triebformel, nu reduce persoana la una dintre ele și nu transforma Symptomfaktoren în dovada unei descărcări comportamentale concrete. Nu trata nici Haupttriebklasse, nici Triebformel ca structură permanentă, identitate fixă sau prognostic imuabil al persoanei.",
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


INITIAL_CLAIMS = _base.INITIAL_CLAIMS + (
    _CLAIM_000024,
    _CLAIM_000025,
    _CLAIM_000026,
    _CLAIM_000027,
    _CLAIM_000028,
    _CLAIM_000029,
)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
