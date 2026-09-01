"""Current source-linked P2B claim catalogue.

The catalogue through claim 000053 is preserved byte-identically in
``interpretation_catalogue_000053``. This module appends the next narrowly
reviewed claim while preserving the same public catalogue interface.
"""

from .interpretation_catalogue_000053 import *  # noqa: F401,F403
from . import interpretation_catalogue_000053 as _previous

_claim = _previous._claim
_base = _previous._base


_CLAIM_000054 = _claim(
    "IC_SZONDI_PRIMARY_000054",
    (
        "DR_SZ_LEHR_1972_000362",
        "DR_SZ_LEHR_1972_000302",
        "DR_SZ_LEHR_1972_000359",
    ),
    ("SZ_LEHR_1972",),
    _base.AssertionMode.LIMITATION,
    "Lehrbuch states explicitly that Linnäus provides only a rapid quantitative orientation over Schicksalsmöglichkeiten while qualitative Rand–Mitte and Vorder-/Hintergänger methods remain indispensable and case-specific. Rand–Mitte separately requires correlation of Randgefahren with Abwehrarten der Mitte. Therefore Linnäus outputs do not themselves establish the individual's defense relation, but their quantitative validity is not cancelled when qualitative analysis is absent.",
    "Rezultatele Linnäus oferă o orientare cantitativă asupra Trieb-/Schicksalsmöglichkeiten, dar nu stabilesc singure Abwehrart-ul individual și nici relația concretă Triebgefahr–Abwehr. Aceste concluzii cer analiză calitativă source-grounded, în special Rand–Mitte; lipsa unei asemenea analize nu invalidează rezultatul Linnäus în propriul său domeniu cantitativ.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("linnaeus.latency_proportions", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000054",
            "Nu deduce Abwehrart, caracterul cronic al unei apărări, organizarea individuală Triebgefahr–Abwehr sau o Schicksalsdiagnose direct din Haupttriebklasse, TspD, Gefahr-/Ventilklasse ori Latenzproportionen. Nu declara însă Linnäus nevalid sau neinterpretabil în propriul său strat cantitativ numai pentru că Rand–Mitte ori Vorder-/Hintergänger nu a fost executată; metodele sunt complementare, nu un gate secvențial de validitate.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000054,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
