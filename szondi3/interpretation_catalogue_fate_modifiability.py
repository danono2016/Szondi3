"""Source-linked P2B fate-modifiability boundary after claim 000086.

This module is the single current executable/public P2B catalogue frontier.
"""

from .interpretation_catalogue_affect_dilemmas import *  # noqa: F401,F403
from . import interpretation_catalogue_affect_dilemmas as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000087 = _claim(
    "IC_SZONDI_PRIMARY_000087",
    ("DR_SZ_IA_1956_A_000038",),
    ("SZ_IA_1956_A",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse I printed pp.105-106 explicitly makes the inherited/familial drive dialectic personally modifiable. Szondi says that a person's conscious Stellungnahme can influence the familiarly given Triebdialektik and that a change of personal position can bring a deep change in the drive dialectic and thus in individual fate. The following passage describes Umkehrung as Dominanzwechsel between polar qualities rather than transformation of their Ursubstanz and places integration of the inherited opposites as the aim. Execution is therefore a non-determinism boundary: source-grounded familial/hereditary doctrine must not be rendered as fixed or unavoidable personal fate.",
    "În teoria lui Szondi, faptul că o Triebdialektik este familial angelegt nu o face un destin personal fix. Ich-Analyse I afirmă că persönliche, bewußte Stellungnahme poate influența dialectica pulsională, iar schimbarea poziției persoanei poate aduce o schimbare profundă a dialecticii și astfel a Schicksal-ului. «Umkehrung» este descrisă ca Dominanzwechsel între calitățile polare, nu ca schimbare a Ursubstanz; opoziția familial dată este «persönlich umstellbar» și poate fi integrată.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(_base.Predicate("series.profile_count", _base.Operator.EXISTS),),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000087",
            "Nu transforma o formulă de test, o Trieb-/Abwehranlage, familiäres Unbewußtes ori o afirmație ereditară din sistemul lui Szondi într-un destin inevitabil, într-o predicție biografică fixă sau într-o concluzie că persoana nu își poate modifica poziția. Păstrează însă limita sursei: Szondi nu spune că persoana schimbă Ursubstanz-ul dispozițiilor polare, ci că prin persönliche Stellungnahme poate modifica raportul lor de dominanță și integrarea lor. Nu traduce această teorie istorică în genetică modernă și nu pretinde eficacitatea empirică contemporană a mecanismului.",
        ),
    ),
    hereditary_genetic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000087,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}

CATALOGUE_ROLE = "CURRENT_EXECUTABLE_PUBLIC_CATALOGUE"
CURRENT_CATALOGUE = True
CURRENT_CATALOGUE_MODULE = __name__
CATALOGUE_FRONTIER = INITIAL_CLAIMS[-1].claim_id
