"""Source-linked P2B Annahme/Angst comparison after claim 000080."""

from .interpretation_catalogue_sublimation_fate import *  # noqa: F401,F403
from . import interpretation_catalogue_sublimation_fate as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000081 = _claim(
    "IC_SZONDI_PRIMARY_000081",
    ("DR_SZ_IA_1956_B_000053",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.PROBABLE,
    "Ich-Analyse II printed pp.358-359 says that Annahme, Sch +±, 'scheinen' to have more success in the defense against Triebgefahren because Angst is rarer than with the four immediately preceding defense forms: Sch ±+, Sch -0, Sch ±± and Sch ±-. The comparison is source-level and probabilistic; it does not measure the person's anxiety or establish global defense efficacy.",
    "La Sch +±, fără Überdruck, Szondi formulează probabilistic că Annahme — Introjektion der Verlassenheit respectiv der Weiblichkeit — «scheinen» să aibă mai mult succes în Abwehr von Triebgefahren, deoarece Angst este mai rară decât la cele patru Abwehrarten imediat precedente: Sch ±+, -0, ±± și ±-. Este o comparație testologică de frecvență, nu măsurarea angoasei reale a persoanei și nici dovada unei eficiențe globale a apărării.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "±")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000081",
            "Nu transforma «Angst seltener» într-o afirmație că persoana nu are sau nu va avea angoasă, într-un diagnostic de sănătate psihică, reziliență, coping ori prognostic și nu declara Sch +± drept apărare global superioară. Nu selecta automat între Verlassenheit și Weiblichkeit și nu inventa concluzii biografice sau de gen. Păstrează însă calificatorul source-grounded «scheinen» și domeniul comparativ exact: Sch ±+, -0, ±± și ±-. Nu extinde la Überdruck.",
        ),
    ),
    sexual_content=True,
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000081,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
