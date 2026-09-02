"""Current source-linked P2B claim catalogue.

The catalogue through claim 000054 is preserved byte-identically in
``interpretation_catalogue_000054``. This module appends narrow sign-specific
Rand-Mitte relations and post-integration Ich-Analyse structural safeguards while
preserving the same public catalogue interface.
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
    "Triebpathologie I explicitly assigns factor e in the Mitte a defense/Stellungnahme function toward the Aggression/Sadismus danger of factor s. In Szondi's exact second example, visual arbitration of the original PDF establishes s +!! together with ordinary e +; the accompanying prose describes Gutmachung and protection through an inner Gewissen. Execution is limited to that exact quantum configuration.",
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


_CLAIM_000056 = _claim(
    "IC_SZONDI_PRIMARY_000056",
    (
        "DR_SZ_TRIEBPATH_1_000002",
        "DR_SZ_TRIEBPATH_1_000004",
    ),
    ("SZ_TRIEBPATH_1",),
    _base.AssertionMode.CONDITIONAL,
    "In the first of Szondi's two exact Rand-Mitte examples, visual arbitration of the original Triebpathologie I PDF establishes s +!! together with e 0. The source describes the strongly accumulated Aggressionsansprüche as an 'Aggressionsgefahr' without 'ethischen Schutz'. Execution is limited to this exact configuration and does not turn the historical model language into a behavioral prediction.",
    "În configurația exactă s +!! împreună cu e0, exemplul Rand–Mitte al lui Szondi descrie o tensiune foarte accentuată în domeniul s împreună cu absența, în această relație testologică exactă, a funcției e de protecție/cenzură etică. Sursa numește configurația «Aggressionsgefahr» fără «ethischen Schutz»; termenii sunt istorici și nu afirmă că persoana este agresivă, violentă ori periculoasă în comportament și nici că îi lipsește global conștiința morală.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("profile.factor.s.base_symbol", _base.Operator.EQ, "+"),
            _base.Predicate("profile.factor.s.quantum_level", _base.Operator.EQ, 2),
            _base.Predicate("profile.factor.e.base_symbol", _base.Operator.EQ, "0"),
            _base.Predicate("profile.factor.e.quantum_level", _base.Operator.EQ, 0),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000056",
            "Nu transforma configurația exactă s +!! / e0 într-o afirmație factuală că persoana este agresivă, violentă, periculoasă, infracțională, pe punctul de a descărca agresiunea sau diagnosticabilă contemporan prin «sadism». Nu transforma e0 din acest exemplu într-o afirmație globală că persoana nu are conștiință, moralitate, capacitate etică ori autocontrol și nu deduce un eșec stabil sau cronic al apărării. Finding-ul este strict profil-specific și source-defined; nu generaliza e0 și nu extinde la alte niveluri de Überdruck ale lui s sau la alte reacții e.",
        ),
    ),
    sexual_content=True,
    pathodiagnostic_content=True,
)


_CLAIM_000057 = _claim(
    "IC_SZONDI_PRIMARY_000057",
    ("DR_SZ_IA_1956_B_000015",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II states that Abwehrmechanismen are unconscious Ich-Funktionen and that the defensive activity originates from the Ego, while also stating that the Ego can defend itself through reactions in all four drive zones rather than only inside the Sch vector. The executable rule is therefore a method boundary applying whenever a series is interpreted.",
    "Abwehr-ul pornește, în sistemul lui Szondi, din Eu: mecanismele de apărare sunt Ich-Funktionen inconștiente. Dar locul în care această apărare se realizează nu este închis în vectorul Sch. Eul se poate apăra prin reacții din toate cele patru Triebgebiete — Sexual, Paroxysmal/Affekt, Sch/Ich și Kontakt. De aceea, Sch nu poate fi tratat drept singurul sediu al apărării.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.EXISTS),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000057",
            "Nu identifica originea egoică a Abwehr-ului cu localizarea exclusivă a apărării în Sch și nu declara că o reacție din S, P sau C este clinic secundară doar fiindcă mecanismul defensiv își are originea în Eu. Nu deduce însă automat un mecanism defensiv concret din orice reacție extrase din acești vectori; forma apărării cere relația source-grounded specifică.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000058 = _claim(
    "IC_SZONDI_PRIMARY_000058",
    ("DR_SZ_IA_1956_B_000017",),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II differentiates five projective defense modes. Only totale Projektion is projection as an Ego Unifunktion; inflative projection, Introprojektion, the Zwang-held Fluchtreaktion and inhibited projection/Entfremdung belong to the combined Deprojektion group. Therefore the elementary -p projection function alone does not identify totale Projektion as the operative defense mechanism.",
    "Funcția elementară -p aparține Projektion, dar mecanismul proiectiv nu este unitar. Szondi distinge «totale Projektion» — proiecția ca Unifunktion a Eului — de patru forme combinate de «Deprojektion»: inflative Projektion, Introprojektion, proiecția reținută prin Zwang (Fluchtreaktion) și gehemmte Projektion (Entfremdung). Simpla prezență a lui -p nu autorizează numirea mecanismului drept totale Projektion.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("profile.factor.p.base_symbol", _base.Operator.EQ, "-"),
        ),
    ),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000058",
            "Nu colapsa orice -p în totale Projektion și nu trata Projektion, Deprojektion, Introprojektion, Fluchtreaktion și Entfremdung ca sinonime. Mecanismul concret cere configurația Sch și relația exactă autorizată de sursă; nu completa configurația lipsă prin analogie.",
        ),
    ),
    sexual_content=True,
    pathodiagnostic_content=True,
    criminological_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (
    _CLAIM_000055,
    _CLAIM_000056,
    _CLAIM_000057,
    _CLAIM_000058,
)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
