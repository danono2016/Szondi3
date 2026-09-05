"""Source-linked P2B sublimation/fate method extensions after claim 000078."""

from .interpretation_catalogue_affect_contact import *  # noqa: F401,F403
from . import interpretation_catalogue_affect_contact as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000079 = _claim(
    "IC_SZONDI_PRIMARY_000079",
    ("DR_SZ_IA_1956_B_000024",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II makes Art der Ich-Abwehr the central differentiating principle for Sublimationsart, but explicitly calls Table 15 incomplete and leaves further relations to future work. It also states, at the presented stage of investigation, that Sublimierung mit Negation is rejected. Execution is therefore a method boundary: Sch/Abwehr findings may constrain a source-authorized sublimation reading, but the test must not manufacture a complete sublimation taxonomy from the incomplete table.",
    "În lectura sublimării, Szondi păstrează continuitatea Triebgefahr ↔ Abwehrart: particularitatea Sublimationsart depinde de felul Ich-Abwehr. Dar Tabelle 15 este declarată chiar de el «nur eine unvollständige Übersicht», iar completarea raporturilor rămâne «eine wichtige Arbeit der Zukunft». De aceea, mecanismul Sch poate delimita o interpretare a sublimării numai acolo unde sursa o autorizează; nu avem voie să transformăm tabelul incomplet într-o taxonomie totală. În stadiul cercetării prezentat aici, Szondi respinge explicit posibilitatea unei «Sublimierung mit Negation».",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(_base.Predicate("series.profile_count", _base.Operator.EXISTS),),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000079",
            "Nu deduce automat o Sublimationsart, profesie, talent, vocație sau nivel de humanizare dintr-o formulă Sch izolată. Nu completa Tabelle 15 prin analogie și nu prezenta cele cinci căi descrise drept clasificare exhaustivă, deoarece Szondi o numește explicit incompletă. Nu inventa o Sublimierung mit Negation împotriva poziției explicite a sursei. Păstrează însă fără modernizare relația source-grounded dintre Triebgefahr, Ich-Abwehr și Sublimationsart.",
        ),
    ),
    hereditary_genetic_content=True,
    sexual_content=True,
    pathodiagnostic_content=True,
)


_CLAIM_000080 = _claim(
    "IC_SZONDI_PRIMARY_000080",
    ("DR_SZ_IA_1956_B_000025",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II narrows the formula 'Charakter ist Schicksal': Schicksal precedes and exceeds Charakter. Character is the part of fate that the Ego has impressed into itself through Introjektion; Wahl/Projektion and Einpraegung/Introjektion are therefore not interchangeable levels. A testological character reading must not be presented as the person's whole fate.",
    "«Charakter ist Schicksal» nu înseamnă la Szondi identitatea totală dintre caracter și destin. Schicksal precede Charakter și este mai larg decât el. Caracterul este «das von dem Ich durch Introjektion in das Ich eingeprägte Stück des Schicksals»: partea destinului pe care Eul a imprimat-o în sine prin Introjektion. Wahl/Projektion și Einprägung/Introjektion trebuie păstrate distincte; analiza caracterului nu epuizează Schicksal-ul persoanei.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(_base.Predicate("series.profile_count", _base.Operator.EXISTS),),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000080",
            "Nu echivala Charakter cu întregul Schicksal și nu prezenta o trăsătură de caracter ori un Ich-Bild ca verdict asupra destinului complet al persoanei. Nu confunda Wahl/Projektion cu Einprägung/Introjektion. Păstrează definiția categorică a caracterului, dar păstrează și limita ei: caracterul este numai un Stück des Schicksals.",
        ),
    ),
    hereditary_genetic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000079, _CLAIM_000080)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
