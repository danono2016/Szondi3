"""Source-linked P2B Persona-formation extension after claim 000071."""

from .interpretation_catalogue_affect import *  # noqa: F401,F403
from . import interpretation_catalogue_affect as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000072 = _claim(
    "IC_SZONDI_PRIMARY_000072",
    ("DR_SZ_IA_1956_B_000027",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II printed pp.372-374 explicitly describes Persona as a collective character formation and gives ordinary Sch +- as the Introprojektion route of Personabildung. The Sch signs are PDF-arbitrated because the canonical text is typographically damaged; execution is restricted to the exact ordinary configuration.",
    "În configurația exactă Sch +-, fără Überdruck, Szondi descrie una dintre căile de Personabildung: Persona, ca formațiune colectivă de caracter, ia naștere prin Introprojektion. Eul încorporează aici, în forma introproiectivă, conținutul colectiv care participă la făurirea măștii sale de rol și caracter.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "-")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000072",
            "Nu transforma Sch +- într-o afirmație că întreaga personalitate este o «mască», nu inventa rolul social concret sau conținutul colectiv introproiectat și nu echivala Persona lui Szondi cu un diagnostic contemporan. Păstrează însă denumirile source-grounded Persona, Personabildung și Introprojektion. Nu extinde la Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000073 = _claim(
    "IC_SZONDI_PRIMARY_000073",
    ("DR_SZ_IA_1956_B_000027",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II printed pp.372-374 gives ordinary Sch ++ as the collective Introinflation route of Personabildung. The source states that successful Deflation depends on the strength of the stellungnehmendes Ich, which must restrict the claim to Allessein and adapt it to reality; the profile signature alone does not establish whether that restriction succeeds. Execution is restricted to the exact ordinary configuration.",
    "În configurația exactă Sch ++, fără Überdruck, Szondi descrie a doua cale a Personabildung: «kollektive Introinflation». Persona se zidește prin Introinflation; pretenția de Allessein cere însă Deflation prin forța Eului care ia Stellung și o mărginește după realitate. Din Ich-Bild-ul ++ singur nu rezultă că această Deflation a reușit.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "+")),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000073",
            "Nu deduce din Sch ++ singur că Deflation a eșuat, că persoana s-a desprins de realitate sau că se află într-o «catastrofă» psihică; aceste consecințe sunt legate în sursă de incapacitatea Eului de a limita Allessein, iar această incapacitate nu este stabilită de simpla semnătură Sch ++. Nu eufemiza însă termenii kollektive Introinflation, Allessein, Deflation și stellungnehmendes Ich și nu extinde la Überdruck fără autorizare separată.",
        ),
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000072, _CLAIM_000073)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
