"""Source-linked P2B Charakterbildung limitation after claim 000084."""

from .interpretation_catalogue_contact_relational_stability import *  # noqa: F401,F403
from . import interpretation_catalogue_contact_relational_stability as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000085 = _claim(
    "IC_SZONDI_PRIMARY_000085",
    ("DR_SZ_IA_1956_B_000026",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II printed pp.371-372 explicitly rejects a unifunctional, purely introjective account of character formation. Introjektion remains the Einprägung function, but Projektion, Inflation and Negation also participate; Szondi additionally places object choice before introjection under the historical theory of projective Genotropismus and the familiäres Unbewußtes. Execution is therefore a method boundary: a character reading must not be reduced to +k/Introjektion or to one Ego function alone.",
    "În Charakterbildung, Szondi spune explicit că ar fi greșit să considerăm caracterul o modificare unifuncțională, pur introiectivă a Eului. Introjektion rămâne funcția de Einprägung, dar la formarea caracterului participă și Projektion, Inflation și Negation. Prin urmare, o interpretare a caracterului nu poate fi redusă la +k/Introjektion ori la o singură Ich-Funktion.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(_base.Predicate("series.profile_count", _base.Operator.EXISTS),),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000085",
            "Nu echivala caracterul cu +k, cu Introjektion izolată sau cu o singură Ich-Funktion și nu declara că o formulă Sch singulară epuizează Charakterbildung. Nu transforma însă projektiver Genotropismus, familiäres Unbewußtes ori Ahnenbilder în genetică modernă sau într-o inferență genealogică verificată. Păstrează distincția source-grounded: Introjektion imprimă, dar Projektion, Inflation și Negation participă de asemenea la formarea caracterului.",
        ),
    ),
    hereditary_genetic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000085,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
