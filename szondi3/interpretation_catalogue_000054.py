"""Current source-linked P2B claim catalogue.

The catalogue through claim 000053 is preserved byte-identically in
``interpretation_catalogue_000053``. This module appends the next narrowly
reviewed claim while preserving the same public catalogue interface.

The legacy archived catalogue used an implicit APPROVED helper. From this tip
forward, the helper exported to successor catalogue layers requires an explicit
lifecycle status so adding a claim and approving it cannot be the same accidental
operation.
"""

from .interpretation_catalogue_000053 import *  # noqa: F401,F403
from . import interpretation_catalogue_000053 as _previous

_base = _previous._base


def _claim(
    claim_id: str,
    doctrine_ids: tuple[str, ...],
    source_ids: tuple[str, ...],
    assertion_mode: _base.AssertionMode,
    source_strength_note: str,
    claim: str,
    trigger: _base.TriggerDefinition,
    *,
    status: _base.LifecycleStatus,
    anti_inferences: tuple[_base.AntiInference, ...] = (),
    sexual_content: bool = False,
    pathodiagnostic_content: bool = False,
    criminological_content: bool = False,
    hereditary_genetic_content: bool = False,
) -> _base.ClaimDefinition:
    """Create a source-established claim only with an explicit lifecycle decision."""
    return _base.ClaimDefinition(
        schema_version=1,
        claim_id=claim_id,
        rule_version=1,
        status=status,
        source_layer=_base.PRIMARY,
        doctrine_ids=doctrine_ids,
        source_ids=source_ids,
        epistemic_class=_base.EpistemicClass.SOURCE_ESTABLISHED_TRIGGER,
        assertion_mode=assertion_mode,
        source_strength_note=source_strength_note,
        claim=claim,
        trigger=trigger,
        anti_inferences=anti_inferences,
        sexual_content=sexual_content,
        pathodiagnostic_content=pathodiagnostic_content,
        criminological_content=criminological_content,
        hereditary_genetic_content=hereditary_genetic_content,
    )


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
    status=_base.LifecycleStatus.APPROVED,
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
