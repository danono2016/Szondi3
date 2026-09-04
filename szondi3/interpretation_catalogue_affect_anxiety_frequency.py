"""Source-linked P2B Angst-frequency extension after claim 000084."""

from .interpretation_catalogue_contact_relational_stability import *  # noqa: F401,F403
from . import interpretation_catalogue_contact_relational_stability as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000085 = _claim(
    "IC_SZONDI_PRIMARY_000085",
    ("DR_SZ_IA_1956_B_000054",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.PROBABLE,
    "Ich-Analyse II printed pp.358-359 states that restrained Inflation by compulsion Sch ±+, Verdrängung Sch -0, Integration Sch ±± and Flucht Sch ±- are the defense forms that 'am häufigsten' accompany Angstzustände. Szondi explains Angst here as indicating that defended Trieberregungen have remained strong enough to return occasionally despite the defense. The execution preserves this as a frequency association, not an invariant identity or a modern anxiety diagnosis.",
    "La Sch ±+, -0, ±± sau ±-, fără Überdruck, Szondi spune că aceste Abwehrarten merg «am häufigsten» împreună cu Angstzustände. Angst indică aici, în explicația lui, că Trieberregungen apărate au rămas suficient de puternice pentru a putea reveni ocazional în pofida Abwehr-ului. Relația este de frecvență, nu o identitate obligatorie între formula Sch și angoasă.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate(
                "profile.vector.Sch.base_symbols",
                _base.Operator.IN,
                (("±", "+"), ("-", "0"), ("±", "±"), ("±", "-")),
            ),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000085",
            "Nu transforma «am häufigsten mit Angstzuständen» într-o certitudine că persoana are angoasă, într-un diagnostic contemporan de tulburare anxioasă, într-o măsurare a severității ori într-un prognostic. Nu deduce automat conținutul concret al Trieberregungen care ar reveni. Păstrează relația probabilistică source-grounded și termenii Angstzustände, Trieberregungen și Ich-Abwehr. Nu extinde la Überdruck.",
        ),
    ),
    sexual_content=True,
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000085,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
