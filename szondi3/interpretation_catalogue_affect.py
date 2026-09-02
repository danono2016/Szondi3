"""Source-linked P2B affect-defense extension after claim 000070."""

from .interpretation_catalogue import *  # noqa: F401,F403
from . import interpretation_catalogue as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000071 = _claim(
    "IC_SZONDI_PRIMARY_000071",
    ("DR_SZ_IA_1956_B_000054",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.PROBABLE,
    "Ich-Analyse II printed pp.358-359 states that four ordinary Ego-defense forms occur most frequently with Angstzustände: Sch ±+ (Inflation held back through Zwang), Sch -0 (Verdrängung), Sch ±± (Integration), and Sch ±- (Flucht). The source adds that anxiety signals that the defended drive excitations remain strong enough to return occasionally. The frequency wording 'am häufigsten' is preserved and is not converted into an invariant rule.",
    "În configurațiile Sch ±+, -0, ±± sau ±-, fără Überdruck, Szondi spune că aceste forme de Ich-Abwehr merg «am häufigsten» împreună cu Angstzustände. Angoasa semnalează aici că excitațiile pulsionale împotriva cărora Eul se apără au rămas destul de puternice pentru a putea reveni din când în când. Relația este una de frecvență în sistemul lui Szondi, nu o identitate obligatorie între formula Sch și apariția angoasei.",
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
            "AI_SZONDI_000071",
            "Nu transforma formularea source-grounded «am häufigsten mit Angstzuständen» într-o regulă invariantă că orice profil Sch ±+, -0, ±± sau ±- trebuie să prezinte angoasă și nu o traduce automat într-un diagnostic contemporan de tulburare anxioasă. Nu eufemiza însă termenii Angstzustände, Trieberregungen sau Ich-Abwehr și nu elimina teza lui Szondi că angoasa semnalează persistența excitațiilor pulsionale apărate. Nu extinde la Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000071,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
