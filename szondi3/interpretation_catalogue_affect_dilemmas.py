"""Source-linked P2B ethical/moral dilemma relation after claim 000085."""

from .interpretation_catalogue_character_formation import *  # noqa: F401,F403
from . import interpretation_catalogue_character_formation as _previous

_base = _previous._base
_claim = _previous._claim


# P-zone signatures authorized by Ich-Analyse II p.359:
# e± OR hy±, with the double dilemma P ±± included once in the union.
_ORDINARY_P_DILEMMA_SIGNATURES = (
    ("±", "0"),
    ("±", "+"),
    ("±", "-"),
    ("±", "±"),
    ("0", "±"),
    ("+", "±"),
    ("-", "±"),
)


_CLAIM_000086 = _claim(
    "IC_SZONDI_PRIMARY_000086",
    ("DR_SZ_IA_1956_B_000055",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.PROBABLE,
    "Ich-Analyse II printed p.359 says that five ordinary Ego-defense forms — Sch 00, ±0, +0, -0 and 0+ — occur 'oft' with ethical dilemmas e±, moral dilemmas hy±, or the double ethical-moral dilemma P ±±. The source relation is explicitly frequent and disjunctive. Runtime execution therefore enumerates the exact ordinary P signatures satisfying e± OR hy± instead of requiring both factors to be ambivalent.",
    "Când Sch este exact 00, ±0, +0, -0 sau 0+, iar în P apare exact e± ori hy± — inclusiv cazul dublu P ±± — toate fără Überdruck, Szondi spune că aceste Ich-Abwehrarten merg «oft» împreună cu ethische Dilemmen, moralische Dilemmen sau doppelte ethisch-moralische Dilemmen. Relația este frecvențială și disjunctivă: nu cere ca e și hy să fie ambele ambivalente.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate(
                "profile.vector.Sch.base_symbols",
                _base.Operator.IN,
                (("0", "0"), ("±", "0"), ("+", "0"), ("-", "0"), ("0", "+")),
            ),
            _base.Predicate(
                "profile.vector.P.base_symbols",
                _base.Operator.IN,
                _ORDINARY_P_DILEMMA_SIGNATURES,
            ),
            _base.Predicate("profile.factor.e.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.hy.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000086",
            "Nu transforma e±, hy± sau P ±± într-o afirmație că persoana trăiește în mod factual o dilemă etică ori morală, că este vinovată, imorală, indecisă, anxioasă sau diagnosticabilă psihiatric. Nu transforma «oft» într-o regulă invariantă și nu cere cumulativ e± și hy±: sursa formulează alternativele prin «oder». Nu extinde la alte poziții Sch și nu extinde la Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000086,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
