"""Source-linked P2B Affekt- and Kontaktreaktion extension after claim 000074."""

from .interpretation_catalogue_character import *  # noqa: F401,F403
from . import interpretation_catalogue_character as _previous

_base = _previous._base
_claim = _previous._claim


def _ordinary_sch(symbols):
    return _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.IN, symbols),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    )


_CLAIM_000075 = _claim(
    "IC_SZONDI_PRIMARY_000075",
    ("DR_SZ_IA_1956_B_000056",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CATEGORICAL,
    "Ich-Analyse II printed p.359 gives an explicit internal hierarchy for Kain-Gefahr: Annahme / Introjektion der Verlassenheit bzw. Weiblichkeit, Sch +±, defends the groben Affekte des Kains 'mit größtem Erfolg' and protects 'am meisten vor der Kain-Gefahr'. This is a source-level comparative claim, not a modern violence-risk estimate.",
    "La Sch +±, fără Überdruck, Szondi numește Annahme — Introjektion der Verlassenheit bzw. der Weiblichkeit — apărarea care combate «mit größtem Erfolg» groben Affekte des Kains și care îl protejează pe om «am meisten vor der Kain-Gefahr». Ierarhia trebuie păstrată cu forța comparativă a textului.",
    _ordinary_sch((("+", "±"),)),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000075",
            "Nu transforma protecția source-grounded față de Kain-Gefahr într-o evaluare contemporană a riscului de violență, într-o predicție de omucidere sau într-o concluzie biografică despre mamă. Nu elimina însă termenii grobe Affekte des Kains, Kain-Gefahr, Verlassenheit sau Weiblichkeit și nu slăbi superlativele «mit größtem Erfolg» / «am meisten» folosite de Szondi. Nu extinde la Überdruck.",
        ),
    ),
    pathodiagnostic_content=True,
    criminological_content=True,
)


_CLAIM_000076 = _claim(
    "IC_SZONDI_PRIMARY_000076",
    ("DR_SZ_IA_1956_B_000056",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CATEGORICAL,
    "Ich-Analyse II printed p.359 states that Introprojektion (Autismus), Sch +-, and Flucht, Sch ±-, provide 'den ungenügendsten Schutz vor den Tötungsansprüchen Kains'. The superlative is retained as Szondi's own comparative hierarchy.",
    "La Sch +- (Introprojektion, Autismus) sau Sch ±- (Flucht), fără Überdruck, Szondi spune direct că aceste mecanisme oferă «den ungenügendsten Schutz vor den Tötungsansprüchen Kains». Formula nu trebuie eufemizată: este polul de protecție cel mai insuficient din ierarhia descrisă de el.",
    _ordinary_sch((("+", "-"), ("±", "-"))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000076",
            "Nu converti «ungenügendsten Schutz vor den Tötungsansprüchen Kains» într-o predicție că persoana va ucide, într-un scor de periculozitate ori într-un diagnostic modern de autism. Păstrează însă literalmente conceptele Introprojektion (Autismus), Flucht, Tötungsansprüche Kains și forța superlativă a afirmației. Nu extinde la Überdruck.",
        ),
    ),
    pathodiagnostic_content=True,
    criminological_content=True,
)


_CLAIM_000077 = _claim(
    "IC_SZONDI_PRIMARY_000077",
    ("DR_SZ_IA_1956_B_000057",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.PROBABLE,
    "Ich-Analyse II printed p.359 says that the milde Affektnatur Abels is found 'am häufigsten' with Inflaprojektion Sch 0± and Entfremdung Sch -±. The source separately says only a part of Sch -- Drillmenschen belongs to the Abel group and gives Sch +0 merely as an example of the least frequent broader narcissistic/egoistic/autistic class; those weaker relations are not silently universalized.",
    "La Sch 0± (Inflaprojektion) sau Sch -± (Entfremdung), fără Überdruck, Szondi găsește «am häufigsten» milde Affektnatur Abels. Este o relație de frecvență, nu o identitate obligatorie între formulă și Abel-Natur.",
    _ordinary_sch((("0", "±"), ("-", "±"))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000077",
            "Nu transforma «am häufigsten» într-o certitudine că orice Sch 0± sau -± este Abel-Natur. Nu extinde regula la întregul Sch --, unde sursa spune numai «ein Teil», și nu transforma exemplul Sch +0 într-o echivalență exhaustivă pentru apărările narcisice, egoiste sau autiste. Păstrează termenii Abel-Natur, Inflaprojektion și Entfremdung.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000078 = _claim(
    "IC_SZONDI_PRIMARY_000078",
    ("DR_SZ_IA_1956_B_000058",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.PROBABLE,
    "Ich-Analyse II printed p.359 states that Kontaktsperre C -- is found most frequently with Inflation Sch 0+ and Introinflation Sch ++; both are called narcissistic forms of Ego protection. The same paragraph places Kontaktsperre and Kontaktlosigkeit inside the Ego's defense against incestuous, bisexual, inverted or perverse Triebgefahr, but the exact C/Sch relation alone does not identify which concrete danger is present.",
    "Când C este exact -- (Kontaktsperre) și Sch este exact 0+ (Inflation) sau ++ (Introinflation), fără Überdruck, Szondi spune că această asociere apare «am häufigsten». El numește ambele forme Sch «narzißtische Formen des Ich-Schutzes». Contextul este Abwehr-ul unei Triebgefahr pe care textul o poate numi inzestuös, bisexuell, invertiert sau pervers, fără ca simpla formulă C/Sch să aleagă automat una dintre ele.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.vector.C.base_symbols", _base.Operator.EQ, ("-", "-")),
            _base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.IN, (("0", "+"), ("+", "+"))),
            _base.Predicate("profile.factor.d.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.m.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0),
            _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000078",
            "Nu transforma asocierea C -- cu Sch 0+/++ într-o afirmație că persoana are în mod necesar o Triebgefahr incestuoasă, bisexuală, inversată sau perversă și nu selecta arbitrar una dintre aceste forme. Nu eufemiza însă termenii sursei și păstrează «am häufigsten» și «narzißtische Formen des Ich-Schutzes». Nu extinde la Überdruck în C sau Sch.",
        ),
    ),
    sexual_content=True,
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (
    _CLAIM_000075,
    _CLAIM_000076,
    _CLAIM_000077,
    _CLAIM_000078,
)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
