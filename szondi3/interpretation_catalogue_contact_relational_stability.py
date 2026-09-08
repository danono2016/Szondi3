"""Source-linked P2B Sch/C interpersonal-relation extension after claim 000083."""

from .interpretation_catalogue_contact_participation import *  # noqa: F401,F403
from . import interpretation_catalogue_contact_participation as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000084 = _claim(
    "IC_SZONDI_PRIMARY_000084",
    ("DR_SZ_IA_1956_B_000060",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CATEGORICAL,
    "Ich-Analyse II printed pp.359-360 states that Desintegration Sch 00, totale Introjektion Sch +0 and Introprojektion (Autismus) Sch +- are defense forms in which interpersonal relations are 'stets unsicher, problematisch', giving the corresponding C configurations ±0, ±+, ±-, -± and ±±. Szondi adds inflative Introjektion Sch ++ only with 'teils auch'; that weaker partial case is deliberately excluded from execution rather than universalized.",
    "Când Sch este exact 00 (Desintegration), +0 (totale Introjektion) sau +- (Introprojektion, Autismus), iar C este exact ±0, ±+, ±-, -± sau ±±, toate fără Überdruck, Szondi descrie zwischenmenschliche Beziehungen drept «stets unsicher, problematisch». Sch ++ nu este inclus aici, deoarece sursa îl adaugă numai cu limitarea «teils auch».",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate(
                "profile.vector.Sch.base_symbols",
                _base.Operator.IN,
                (("0", "0"), ("+", "0"), ("+", "-")),
            ),
            _base.Predicate(
                "profile.vector.C.base_symbols",
                _base.Operator.IN,
                (("±", "0"), ("±", "+"), ("±", "-"), ("-", "±"), ("±", "±")),
            ),
            _base.Predicate("profile.factor.d.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.m.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000084",
            "Nu transforma «stets unsicher, problematisch» într-un diagnostic contemporan de tulburare relațională, de personalitate sau de autism și nu extrapola automat la toate relațiile biografice ale persoanei. Nu include Sch ++ în regula executabilă: sursa spune acolo numai «teils auch». Nu extinde la Überdruck și păstrează termenii Desintegration, totale Introjektion, Introprojektion (Autismus) și zwischenmenschliche Beziehungen la nivelul teoretic al lui Szondi.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000084,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
