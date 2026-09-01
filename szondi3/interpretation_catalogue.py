"""Current source-linked P2B claim catalogue.

Claims through ``IC_SZONDI_PRIMARY_000043`` remain byte-identical in
``interpretation_catalogue_000043``. This module appends the next narrowly
reviewed claim while preserving the public catalogue interface.
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


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000044,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
