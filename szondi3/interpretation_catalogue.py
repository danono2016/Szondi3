"""Current source-linked P2B claim catalogue.

Claims through ``IC_SZONDI_PRIMARY_000043`` remain byte-identical in
``interpretation_catalogue_000043``. This module appends narrowly reviewed
claims while preserving the public catalogue interface.
"""

from .interpretation_catalogue_000043 import *  # noqa: F401,F403
from . import interpretation_catalogue_000043 as _previous
from . import interpretation_catalogue_base as _base

_claim = _base._claim


_CLAIM_000044 = _claim(
    "IC_SZONDI_PRIMARY_000044",
    (
        "DR_SZ_SA_1948_000058",
        "DR_SZ_SA_1948_000059",
        "DR_SZ_SA_1948_000060",
        "DR_SZ_SA_1948_000061",
        "DR_SZ_SA_1948_000062",
    ),
    ("SZ_SA_1948",),
    _base.AssertionMode.LIMITATION,
    "Schicksalsanalyse 1948 explicitly limits its then-current scope to Triebschicksal, distinguishes Mental- and Sozial-Schicksal as additional components of Gesamtschicksal, states that life is always more than Triebschicksal, and says the method is still far from representing the person's complete Lebensplan. This is a scope boundary for the whole drive analysis, not only for an isolated profile or proportion.",
    "Chiar interpretarea unei serii Szondi complete rămâne, în termenii sursei, o analiză a Triebschicksal-ului și nu este echivalentă cu Gesamtschicksal-ul sau cu viața întreagă a persoanei. Szondi distinge separat Mental-Schicksal și Sozial-Schicksal și afirmă explicit că «Leben ist stets mehr als Triebschicksal»; metoda nu poate reprezenta din test singur Lebensplan-ul complet.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000044",
            "Nu transforma seria Szondi, Triebprofilurile, Triebklasse, Triebformel sau indicii seriei într-o descriere exhaustivă a vieții ori a persoanei, într-un Gesamtschicksal sau Lebensplan complet și nu deduce din ele singure destinul mental/rațional, situația socială concretă, biografia, viitorul, boala ori moartea persoanei. Aceste domenii cer informații independente și nu sunt absorbite de Triebschicksal.",
        ),
    ),
)


_CLAIM_000045 = _claim(
    "IC_SZONDI_PRIMARY_000045",
    (
        "DR_SZ_SA_1948_000127",
        "DR_SZ_SA_1948_000172",
        "DR_SZ_SA_1948_000243",
    ),
    ("SZ_SA_1948",),
    _base.AssertionMode.LIMITATION,
    "Schicksalsanalyse 1948 itself places strong epistemic limits on its hereditary/genotropic theory: concrete Anlagematerial can be established only approximately and only through especially careful, large-scale Familienforschung; the hoped-for experimental strengthening of the Gentheorie des Schicksals is explicitly conditional on future research; and quantitative gene action / multiple allelomorphs in humans are described as nearly terra incognita. Historical genetic terminology therefore does not authorize a modern individual genetic finding from the Szondi protocol.",
    "Termenii ereditari și genotropi din teoria istorică a lui Szondi nu constituie o identificare genetică a persoanei. Chiar în cadrul sursei, Anlagematerial-ul concret poate fi stabilit numai aproximativ și prin Familienforschung foarte amplă și atentă; confirmarea experimentală a Gentheorie des Schicksals era lăsată cercetărilor viitoare, iar mecanismele cantitative ale genelor la om erau descrise drept aproape «terra incognita».",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000045",
            "Nu transforma un profil sau o serie Szondi, un Wurzelfaktor, un termen precum Konduktor/Genotropismus/Erbanlage ori o asociere istorică din sursă în dovada unei gene, alele, mutații, predispoziții ereditare moderne, statut de purtător, mod de transmitere, boală familială concretă sau diagnostic la rude. Nu atribui genetic alegerea partenerului, profesia, talentul, boala, cauza morții ori riscul de suicid pe baza testului; asemenea afirmații ar necesita dovezi genetice, medicale și genealogice independente, nu inferență din protocolul Szondi.",
        ),
    ),
    hereditary_genetic_content=True,
    pathodiagnostic_content=True,
)


_CLAIM_000046 = _claim(
    "IC_SZONDI_PRIMARY_000046",
    (
        "DR_SZ_IA_1956_B_000006",
        "DR_SZ_IA_1956_B_000007",
        "DR_SZ_IA_1956_B_000009",
        "DR_SZ_IA_1956_B_000011",
        "DR_SZ_IA_1956_B_000043",
    ),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II treats foreground and complementary Ego configurations dialectically, explicitly calls a Vorder-Ich-only analysis half-analysis, and requires Komplementprofile to be interpreted rather than ignored. The source also distinguishes theoretical and experimental complement profiles in its stated procedure and separates the theoretical possibility of complementarity from actual integration, which it describes as very rare. The executable rule therefore activates only when a real experimental complement administration has been supplied; it does not synthesize a complement from the foreground profile.",
    "Când a fost administrat și calculat efectiv un profil complementar experimental (E.K.P.), acesta trebuie păstrat ca profil complementar distinct și citit corelativ cu Vorderprofil-ul, nu ignorat și nici amestecat în seria profilurilor de prim-plan. E.K.P. oferă o a doua configurație testologică, experimental obținută, relevantă pentru lectura complementară; nu este echivalent automat cu profilul complementar teoretic (Th.K.P.) și nu dovedește că această configurație este deja manifestă sau că va deveni ulterior prim-plan.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.CONDITIONAL_CONTEXTUAL,
        predicates=(
            _base.Predicate("protocol.experimental_complement.present", _base.Operator.EQ, True),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000046",
            "Nu trata E.K.P. drept «adevăratul Eu ascuns», a doua personalitate, diagnostic latent demonstrat, comportament secret sau predictor al unei schimbări viitoare. Nu îl identifica automat cu Th.K.P., nu presupune că perechea se va integra efectiv și nu transforma posibilitatea complementară într-o succesiune inevitabilă; Szondi separă posibilitatea teoretică de integrarea reală și afirmă că aceasta din urmă apare foarte rar. Nu introduce E.K.P. în calculele seriei libere de Vordergrundprofile și nu importa automat etichetele istorice/pathodiagnostice ale perechilor complementare fără reguli source-grounded separate.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000047 = _claim(
    "IC_SZONDI_PRIMARY_000047",
    (
        "DR_SZ_IA_1956_B_000008",
        "DR_SZ_IA_1956_B_000009",
        "DR_SZ_IA_1956_B_000011",
        "DR_SZ_IA_1956_B_000043",
    ),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II gives an exact Table-9 mapping of the sixteen Sch positions into eight theoretical complementary pairs and uses experimentally obtained complement profiles as evidence in complementary Ego analysis. Production execution is deliberately restricted to ordinary Sch reactions without quantum overpressure or forced nulls, so no source-unstated normalization is introduced.",
    "În această administrare, Sch-ul profilului complementar experimental (E.K.P.) coincide exact, la nivelul reacțiilor obișnuite, cu poziția Sch complementară teoretică (Th.K.P.) definită de Tabelul 9 pentru Sch-ul Vorderprofil-ului. Aceasta susține o concordanță structurală între cele două poziții Sch în cadrul modelului complementar al lui Szondi; nu stabilește singură conținutul clinic al relației.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("protocol.experimental_complement.sch_theoretical_relation", _base.Operator.EQ, "MATCH"),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000047",
            "Nu transforma concordanța structurală E.K.P.–Th.K.P. la Sch într-o dovadă a unei a doua personalități, a unui diagnostic latent, a unui comportament ascuns, a unei succesiuni viitoare inevitabile sau a integrării efective a celor două poziții. Nu importa automat denumirile istorice, sexuale ori pathodiagnostice din Tabelul 9; acestea cer claims separate. Concordanța arată numai că E.K.P. reproduce, în această administrare și în condițiile autorizate, perechea Sch teoretică definită de sursă.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000048 = _claim(
    "IC_SZONDI_PRIMARY_000048",
    (
        "DR_SZ_IA_1956_B_000008",
        "DR_SZ_IA_1956_B_000014",
        "DR_SZ_IA_1956_B_000043",
    ),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Table 9 defines eight fundamental theoretical Sch complement pairs, while Ich-Analyse II explicitly leaves open whether additional forms of complementary Ego relation exist and separately constructs theoretical and experimental complement profiles. An ordinary experimental complement that does not reproduce the Table-9 theoretical Sch pair must therefore be preserved as observed rather than forced into the theoretical mapping.",
    "În această administrare, Sch-ul E.K.P. nu coincide exact cu poziția Sch a Th.K.P. prevăzută de Tabelul 9 pentru Vorderprofil. Aceasta înseamnă numai lipsa concordanței structurale exacte cu perechea teoretică fundamentală respectivă; E.K.P. rămâne dat experimental distinct și nu trebuie «corectat» pentru a se potrivi Th.K.P. Szondi însuși lasă deschisă posibilitatea altor forme ale relațiilor complementare.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("protocol.experimental_complement.sch_theoretical_relation", _base.Operator.EQ, "MISMATCH"),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000048",
            "Nu declara administrarea invalidă, nu concluziona că nu există nicio relație complementară și nu înlocui E.K.P. observat cu Th.K.P. calculat. Nu selecta arbitrar o altă pereche, nu inventa un Hinter-Ich și nu deriva diagnostic, comportament sau prognostic din simpla neconcordanță. Tipologia celor opt perechi este fundamentală în sursă, dar nu este declarată exhaustivă definitiv.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (
    _CLAIM_000044,
    _CLAIM_000045,
    _CLAIM_000046,
    _CLAIM_000047,
    _CLAIM_000048,
)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
