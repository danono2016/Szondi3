"""Source-linked P2B Kontaktlosigkeit special cases after claim 000081."""

from .interpretation_catalogue_affect_anxiety_comparison import *  # noqa: F401,F403
from . import interpretation_catalogue_affect_anxiety_comparison as _previous

_base = _previous._base
_claim = _previous._claim


def _ordinary_c00_sch(sch_symbols):
    return _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.C.base_symbols", _base.Operator.EQ, ("0", "0")),
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, sch_symbols),
            _base.Predicate("profile.factor.d.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.m.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    )


_CLAIM_000082 = _claim(
    "IC_SZONDI_PRIMARY_000082",
    ("DR_SZ_IA_1956_B_000059",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CATEGORICAL,
    "Ich-Analyse II printed p.359 defines Kontaktlosigkeit C 00 as an infantile interpersonal form in which participation is possible with only one object while contact with other objects fails. Szondi names Integration Sch ±± as a special case: participation with a spiritual idea is maintained without interruption. Execution is restricted to the exact ordinary C 00 / Sch ±± conjunction so the general definition is not projected onto Sch alone.",
    "Când C este exact 00 (Kontaktlosigkeit) și Sch este exact ±± (Integration), fără Überdruck, Szondi descrie cazul special în care participarea la o singură idee spirituală este menținută neîntrerupt. Afirmația aparține definiției sale despre Kontaktlosigkeit: participarea se concentrează asupra unui singur obiect, iar contactul cu celelalte obiecte ale lumii devine indisponibil.",
    _ordinary_c00_sch(("±", "±")),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000082",
            "Nu deduce din Sch ±± singur Kontaktlosigkeit și nu transforma «geistige Idee» într-o credință, ideologie, profesie ori interes concret inventat. Relația executată cere exact C 00 împreună cu Sch ±±, fără Überdruck. Păstrează termenii Partizipation, Kontaktlosigkeit și Integration la nivelul teoretic al sursei.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000083 = _claim(
    "IC_SZONDI_PRIMARY_000083",
    ("DR_SZ_IA_1956_B_000059",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CATEGORICAL,
    "Ich-Analyse II printed p.359 gives Introjektion der Verlassenheit Sch +± as another special context of Kontaktlosigkeit C 00. In Szondi's formulation, the introjected image of the abandoning mother conditions further acts of choice, while the person is 'blind, skotomisiert' for other objects. The runtime claim requires the exact ordinary C 00 / Sch +± conjunction and does not convert this source image into verified biography.",
    "Când C este exact 00 (Kontaktlosigkeit) și Sch este exact +± (Introjektion der Verlassenheit), fără Überdruck, Szondi spune că imaginea introiectată a mamei care părăsește condiționează actele ulterioare de alegere; pentru «alte» obiecte ale lumii persoana este, în formularea lui, «blind, skotomisiert». Aceasta este o relație testologică source-grounded, nu constatarea unei istorii familiale reale.",
    _ordinary_c00_sch(("+", "±")),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000083",
            "Nu transforma Introjektion der Verlassenheit într-o afirmație că mama reală a abandonat persoana, nu reconstrui o biografie familială și nu deduce automat din Sch +± Kontaktlosigkeit. Relația cere exact C 00 împreună cu Sch +±, fără Überdruck. Nu moderniza «blind, skotomisiert» într-un diagnostic contemporan și nu elimina termenii expliciți ai sursei.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000082, _CLAIM_000083)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
