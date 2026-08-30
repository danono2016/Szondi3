"""Current source-linked P2B claim catalogue.

The previously reviewed catalogue is kept byte-identical in
``interpretation_catalogue_base``. This module appends the next narrowly reviewed
claim while preserving the same public catalogue interface.
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


INITIAL_CLAIMS = _base.INITIAL_CLAIMS + (_CLAIM_000024,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
