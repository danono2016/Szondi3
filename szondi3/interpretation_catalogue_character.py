"""Source-linked P2B dynamic-character method extension after claim 000073."""

from .interpretation_catalogue_persona import *  # noqa: F401,F403
from . import interpretation_catalogue_persona as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000074 = _claim(
    "IC_SZONDI_PRIMARY_000074",
    ("DR_SZ_IA_1956_B_000029",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II states that a dynamic Charakteranalyse must treat Vordergänger and Hintergänger as complementary character halves and must be supplemented by fortlaufende Ich-Analyse and familial comparison through the Ahnentafel. Szondi calls a character analysis that neglects the Hintergänger 'nur eine halbe Analyse'. The executable use is therefore a method boundary, not a genealogical inference from a test profile.",
    "Pentru Szondi, o Charakteranalyse care rămâne numai la Vordergänger este «nur eine halbe Analyse». Caracterul trebuie urmărit în dubla sa existență de Vordergänger și Hintergänger, iar analiza dinamică se completează prin fortlaufende Ich-Analyse și prin confruntarea cu Ahnentafel. Hintergänger-ul poate purta tocmai acele trăsături familiale pe care wählendes Ich le-a respins și le-a împins în fundal.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(_base.Predicate("series.profile_count", _base.Operator.EXISTS),),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000074",
            "Nu prezenta analiza caracterului drept completă dacă Hintergänger-ul și dimensiunea familială cerute de metodă nu au fost efectiv examinate. Nu inventa însă dintr-un profil ce trăsătură ancestrală concretă se află în Hintergänger și nu substitui automat Ahnentafel-ul printr-o formulă Sch sau printr-o inferență AI. Păstrează fără eufemizare formula source-grounded «nur eine halbe Analyse».",
        ),
    ),
    hereditary_genetic_content=True,
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000074,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
