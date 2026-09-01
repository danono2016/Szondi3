"""Current source-linked P2B claim catalogue.

The catalogue through claim 000054 is preserved byte-identically in
``interpretation_catalogue_000054``. This module appends the first narrow
sign-specific Rand-Mitte relation while preserving the same public catalogue
interface.
"""

from .interpretation_catalogue_000054 import *  # noqa: F401,F403
from . import interpretation_catalogue_000054 as _previous

_base = _previous._base
_claim = _previous._claim


_CLAIM_000055 = _claim(
    "IC_SZONDI_PRIMARY_000055",
    (
        "DR_SZ_TRIEBPATH_1_000002",
        "DR_SZ_TRIEBPATH_1_000003",
    ),
    ("SZ_TRIEBPATH_1",),
    _base.AssertionMode.CONDITIONAL,
    "Triebpathologie I explicitly assigns factor e in the Mitte a defense/Stellungnahme function toward the Aggression/Sadismus danger of factor s. In Szondi's exact second example, clinician-admitted visual arbitration of the original PDF establishes s +!! together with ordinary e +; the accompanying prose describes Gutmachung and protection through an inner Gewissen. Execution is limited to that exact quantum configuration.",
    "În configurația exactă s +!! împreună cu e + fără Überdruck la e, lectura Rand–Mitte pune în relație o Triebgefahr intens tensionată în domeniul s cu o tendință e+ de Gutmachung/Gewissensschutz în Mitte. Este o relație testologică de pericol–apărare, nu dovada unei agresiuni comportamentale și nici dovada că apărarea este suficientă sau reușită în viața reală.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.factor.s.base_symbol", _base.Operator.EQ, "+"),
            _base.Predicate("profile.factor.s.quantum_level", _base.Operator.EQ, 2),
            _base.Predicate("profile.factor.e.base_symbol", _base.Operator.EQ, "+"),
            _base.Predicate("profile.factor.e.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000055",
            "Nu transforma s +!! într-o afirmație factuală că persoana este violentă, agresivă în comportament, periculoasă, infracțională sau diagnosticabilă contemporan prin «sadism». Nu transforma e + în dovada unui caracter moral, a autocontrolului real, a inhibiției reușite, a absenței agresiunii ori a unei apărări stabile/cronice. Finding-ul afirmă numai coexistența testologică, în configurația exactă autorizată, a presiunii s +!! cu tendința e + de Gutmachung/Gewissensschutz. Nu extinde la alte niveluri de Überdruck ale lui s sau e fără autorizare separată.",
        ),
    ),
    sexual_content=True,
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (_CLAIM_000055,)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
