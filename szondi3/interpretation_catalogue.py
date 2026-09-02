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
    ("DR_SZ_TRIEBPATH_1_000002", "DR_SZ_TRIEBPATH_1_000003"),
    ("SZ_TRIEBPATH_1",),
    _base.AssertionMode.CONDITIONAL,
    "Triebpathologie I explicitly assigns factor e in the Mitte a defense/Stellungnahme function toward the Aggression/Sadismus danger of factor s. In Szondi's exact second example, visual arbitration of the original PDF establishes s +!! together with ordinary e +; the accompanying prose describes Gutmachung and protection through an inner Gewissen. Execution is limited to that exact quantum configuration.",
    "În configurația exactă s +!! împreună cu e + fără Überdruck la e, lectura Rand–Mitte pune în relație o Triebgefahr intens tensionată în domeniul s cu o tendință e+ de Gutmachung/Gewissensschutz în Mitte. Este o relație testologică de pericol–apărare, nu dovada unei agresiuni comportamentale și nici dovada că apărarea este suficientă sau reușită în viața reală.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(
        _base.Predicate("profile.factor.s.base_symbol", _base.Operator.EQ, "+"),
        _base.Predicate("profile.factor.s.quantum_level", _base.Operator.EQ, 2),
        _base.Predicate("profile.factor.e.base_symbol", _base.Operator.EQ, "+"),
        _base.Predicate("profile.factor.e.quantum_level", _base.Operator.EQ, 0),
    )),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000055", "Nu transforma s +!! într-o afirmație factuală că persoana este violentă, agresivă în comportament, periculoasă, infracțională sau diagnosticabilă contemporan prin «sadism». Nu transforma e + în dovada unui caracter moral, a autocontrolului real, a inhibiției reușite, a absenței agresiunii ori a unei apărări stabile/cronice. Finding-ul afirmă numai coexistența testologică, în configurația exactă autorizată, a presiunii s +!! cu tendința e + de Gutmachung/Gewissensschutz. Nu extinde la alte niveluri de Überdruck ale lui s sau e fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True,
)

_CLAIM_000056 = _claim(
    "IC_SZONDI_PRIMARY_000056",
    ("DR_SZ_TRIEBPATH_1_000002", "DR_SZ_TRIEBPATH_1_000004"),
    ("SZ_TRIEBPATH_1",),
    _base.AssertionMode.CONDITIONAL,
    "In the first of Szondi's two exact Rand-Mitte examples, visual arbitration of the original Triebpathologie I PDF establishes s +!! together with e 0. The source describes the strongly accumulated Aggressionsansprüche as an 'Aggressionsgefahr' without 'ethischen Schutz'. Execution is limited to this exact configuration and does not turn the historical model language into a behavioral prediction.",
    "În configurația exactă s +!! împreună cu e0, exemplul Rand–Mitte al lui Szondi descrie o tensiune foarte accentuată în domeniul s împreună cu absența, în această relație testologică exactă, a funcției e de protecție/cenzură etică. Sursa numește configurația «Aggressionsgefahr» fără «ethischen Schutz»; termenii sunt istorici și nu afirmă că persoana este agresivă, violentă ori periculoasă în comportament și nici că îi lipsește global conștiința morală.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(
        _base.Predicate("profile.factor.s.base_symbol", _base.Operator.EQ, "+"),
        _base.Predicate("profile.factor.s.quantum_level", _base.Operator.EQ, 2),
        _base.Predicate("profile.factor.e.base_symbol", _base.Operator.EQ, "0"),
        _base.Predicate("profile.factor.e.quantum_level", _base.Operator.EQ, 0),
    )),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000056", "Nu transforma configurația exactă s +!! / e0 într-o afirmație factuală că persoana este agresivă, violentă, periculoasă, infracțională, pe punctul de a descărca agresiunea sau diagnosticabilă contemporan prin «sadism». Nu transforma e0 din acest exemplu într-o afirmație globală că persoana nu are conștiință, moralitate, capacitate etică ori autocontrol și nu deduce un eșec stabil sau cronic al apărării. Finding-ul este strict profil-specific și source-defined; nu generaliza e0 și nu extinde la alte niveluri de Überdruck ale lui s sau la alte reacții e."),),
    sexual_content=True, pathodiagnostic_content=True,
)

_CLAIM_000057 = _claim(
    "IC_SZONDI_PRIMARY_000057", ("DR_SZ_IA_1956_B_000015",), ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II states that Abwehrmechanismen are unconscious Ich-Funktionen and that the defensive activity originates from the Ego, while also stating that the Ego can defend itself through reactions in all four drive zones rather than only inside the Sch vector. The executable rule is therefore a method boundary applying whenever a series is interpreted.",
    "Abwehr-ul pornește, în sistemul lui Szondi, din Eu: mecanismele de apărare sunt Ich-Funktionen inconștiente. Dar locul în care această apărare se realizează nu este închis în vectorul Sch. Eul se poate apăra prin reacții din toate cele patru Triebgebiete — Sexual, Paroxysmal/Affekt, Sch/Ich și Kontakt. De aceea, Sch nu poate fi tratat drept singurul sediu al apărării.",
    _base.TriggerDefinition(kind=_base.TriggerKind.LIMITATION_GUARD, predicates=(_base.Predicate("series.profile_count", _base.Operator.EXISTS),)),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000057", "Nu identifica originea egoică a Abwehr-ului cu localizarea exclusivă a apărării în Sch și nu declara că o reacție din S, P sau C este clinic secundară doar fiindcă mecanismul defensiv își are originea în Eu. Nu deduce însă automat un mecanism defensiv concret din orice reacție extrase din acești vectori; forma apărării cere relația source-grounded specifică."),),
    pathodiagnostic_content=True,
)

_CLAIM_000058 = _claim(
    "IC_SZONDI_PRIMARY_000058", ("DR_SZ_IA_1956_B_000017",), ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Ich-Analyse II differentiates five projective defense modes. Only totale Projektion is projection as an Ego Unifunktion; inflative projection, Introprojektion, the Zwang-held Fluchtreaktion and inhibited projection/Entfremdung belong to the combined Deprojektion group. Therefore the elementary -p projection function alone does not identify totale Projektion as the operative defense mechanism.",
    "Funcția elementară -p aparține Projektion, dar mecanismul proiectiv nu este unitar. Szondi distinge «totale Projektion» — proiecția ca Unifunktion a Eului — de patru forme combinate de «Deprojektion»: inflative Projektion, Introprojektion, proiecția reținută prin Zwang (Fluchtreaktion) și gehemmte Projektion (Entfremdung). Simpla prezență a lui -p nu autorizează numirea mecanismului drept totale Projektion.",
    _base.TriggerDefinition(kind=_base.TriggerKind.LIMITATION_GUARD, predicates=(_base.Predicate("profile.factor.p.base_symbol", _base.Operator.EQ, "-"),)),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000058", "Nu colapsa orice -p în totale Projektion și nu trata Projektion, Deprojektion, Introprojektion, Fluchtreaktion și Entfremdung ca sinonime. Mecanismul concret cere configurația Sch și relația exactă autorizată de sursă; nu completa configurația lipsă prin analogie."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000059 = _claim(
    "IC_SZONDI_PRIMARY_000059", ("DR_SZ_IA_1956_B_000018",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 11 assigns ordinary Sch 0+ to totale Inflation, where Inflation operates as the Ego's unifunctional defense. The printed table and surrounding text establish this exact Sch position; quantum-overpressure variants are not separately authorized here.",
    "În configurația exactă Sch 0+, fără Überdruck la p, Szondi numește mecanismul «totale Inflation»: Inflation lucrează aici ca Unifunktion a Eului. Eul se află sub dominația inflativă fără contrafuncția k în această poziție Sch.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("0", "+")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000059", "Nu înlocui termenul source-grounded «totale Inflation» cu un diagnostic contemporan și nu inventa conținutul concret al contrariilor pe care persoana vrea să le fie. Nu extinde mecanismul la Sch 0+ cu Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000060 = _claim(
    "IC_SZONDI_PRIMARY_000060", ("DR_SZ_IA_1956_B_000018",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 11 assigns ordinary Sch ±+ to Zwangsdeflation: the Ego takes a position against the danger of Inflation and deflates it through Zwang. The exact Sch signature is source-defined; quantum-overpressure variants are not separately authorized here.",
    "În configurația exactă Sch ±+, fără Überdruck, Szondi descrie «Zwangsdeflation»: Eul ia Stellung împotriva Inflationsgefahr și produce Deflation der Inflation prin Zwang. Presiunea inflativă este ținută în frâu prin mecanismul constrângerii.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("±", "+")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000060", "Nu transforma «Zwangsdeflation» într-un diagnostic contemporan de tulburare obsesiv-compulsivă și nu deduce ritualuri, obsesii ori comportamente biografice concrete fără date independente. Nu slăbi însă denumirea source-grounded a mecanismului și nu extinde regula la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000061 = _claim(
    "IC_SZONDI_PRIMARY_000061", ("DR_SZ_IA_1956_B_000018",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 11 assigns ordinary Sch -+ to Hemmung / negierte Inflation, defined as Deflation of Inflation through Negation. The surrounding text states that one inflation direction is negated but that the Ego picture alone does not reveal which concrete one; quantum-overpressure variants are not separately authorized here.",
    "În configurația exactă Sch -+, fără Überdruck, Szondi numește mecanismul «Hemmung» sau «negierte Inflation»: Deflation der Inflation prin Negation. O direcție a Inflation-ului este negată; din Ich-Bild singur nu se poate stabili care este conținutul concret al direcției negate.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("-", "+")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000061", "Nu inventa din Sch -+ conținutul concret al tendinței inflative negate și nu transforma «Hemmung» într-un diagnostic contemporan sau într-o inhibiție biografică globală. Păstrează denumirea și relația source-grounded, dar nu extinde regula la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000062 = _claim(
    "IC_SZONDI_PRIMARY_000062", ("DR_SZ_IA_1956_B_000019",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 12 assigns ordinary Sch +0 to totale Introjektion. In this introjective defense, the dangerous drive need is cleared from Wunschbewusstsein by incorporating both opposed strivings into the Ego; the source describes this as Einverleibung and a transformation from Seinsmacht to Habmacht. Execution is restricted to the exact ordinary Sch position established by the printed table.",
    "În configurația exactă Sch +0, fără Überdruck, Szondi numește mecanismul «totale Introjektion». Eul caută să stăpânească primejdia prin Einverleibung: ambele tendințe opuse sunt încorporate Eului, iar Seinsmacht este prefăcută în Habmacht. Introjektion lucrează aici ca formă totală a apărării introiective.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "0")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000062", "Nu dilua denumirea source-grounded «totale Introjektion», dar nu inventa din Sch +0 obiectul concret încorporat, biografia, profesia, posesia sau conflictul persoanei. Nu transforma Habmacht într-o afirmație factuală despre avere ori proprietate și nu extinde mecanismul la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000063 = _claim(
    "IC_SZONDI_PRIMARY_000063", ("DR_SZ_IA_1956_B_000019",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 12 assigns ordinary Sch +± to inflaprojektive Introjektion, explicitly described as the Vorphase of totale Introjektion. Projection and inflation still persist, but the Ego accepts and incorporates these strivings; the printed table establishes the exact Sch position. Execution is restricted to the ordinary configuration and does not import the table's sex-specific illustrative material as a universal person-level claim.",
    "În configurația exactă Sch +±, fără Überdruck, Szondi descrie «inflaprojektive Introjektion», Vorphase a totalei Introjektion. Projektion și Inflation nu au dispărut: ele persistă, dar Eul le primește și le încorporează. Apărarea are astfel caracter introiectiv, în timp ce tensiunea proiectiv-inflativă rămâne încă prezentă în mecanism.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "±")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000063", "Nu transforma exemplificările sexuale sau de rol din Tabelul 12 în afirmații universale despre persoană și nu deduce automat feminitate, masculinitate, incest, abandon, anxietate relațională ori conținut biografic concret. Păstrează însă termenii source-grounded «inflaprojektive Introjektion» și «Vorphase»; nu extinde regula la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000064 = _claim(
    "IC_SZONDI_PRIMARY_000064", ("DR_SZ_IA_1956_B_000020",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 13 assigns ordinary Sch -- to projektive Negation / Anpassung. The source defines Anpassung as negation of Wunschprojektion: the adapted Ego gives up its wish claims and verifies reality instead of forcing the Wunschwelt upon it. The exact ordinary Sch position is source-defined.",
    "În configurația exactă Sch --, fără Überdruck, Szondi numește mecanismul «projektive Negation / Anpassung». Eul renunță la Wunschprojektion și la pretenția de a impune lumii realitatea dorinței; el verifică Realität și se adaptează ei. Este forma negatoare a Anpassung-ului, pe care Szondi o așază alături de Verdrängung în Tabelul 13.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("-", "-")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000064", "Nu transforma «Anpassung» într-o evaluare contemporană globală că persoana este sănătoasă, matură, conformistă ori bine adaptată în toate domeniile și nu inventa obiectul concret la care se adaptează. Păstrează sensul source-grounded de projektive Negation și nu extinde regula la Überdruck fără autorizare separată."),),
    pathodiagnostic_content=True,
)

_CLAIM_000065 = _claim(
    "IC_SZONDI_PRIMARY_000065", ("DR_SZ_IA_1956_B_000020",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 13 gives the intensified adaptation form Sch -!!- the explicit name Destruktion and states that when negation becomes very strong it is called destruction. Visual arbitration establishes quantum overpressure on k with ordinary negative p. Execution is limited to that exact table configuration.",
    "În configurația exactă Sch -!!-, Szondi duce projektive Negation până la «Destruktion»: când Verneinung devine foarte puternică, Anpassung se transformă, în terminologia lui, în distrugere. Aici Überdruck-ul negativ al lui k stă împreună cu p- și marchează forma intensificată pe care Tabelul 13 o numește fără ocol «Destruktion».",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("-", "-")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 2), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000065", "Nu eufemiza termenul source-grounded «Destruktion», dar nu îl transforma automat într-o afirmație factuală că persoana distruge obiecte, atacă oameni, este violentă, infracțională ori periculoasă. Nu generaliza la alte grade de k-Überdruck sau la p cu Überdruck fără autorizare separată."),),
    pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000066 = _claim(
    "IC_SZONDI_PRIMARY_000066", ("DR_SZ_IA_1956_B_000017",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 10 assigns ordinary Sch 0- to totale Projektion. Both opposed strivings of a drive need are displaced onto a foreign object; with k0 the position-taking Ego is too weak to oppose p-, so projection governs as the projective Unifunktion. Execution is limited to the exact ordinary configuration.",
    "În configurația exactă Sch 0-, fără Überdruck, Szondi numește mecanismul «totale Projektion». Ambele tendințe opuse ale trebuinței sunt hinausverlegt asupra unui obiect străin; Eul Stellung neputând ridica o contrapoziție prin k, Projektion domnește ca Unifunktion proiectivă.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("0", "-")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000066", "Nu inventa obiectul concret asupra căruia se proiectează, conținutul biografic al proiecției ori un diagnostic modern. Nu dilua termenul «totale Projektion» și nu extinde regula la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000067 = _claim(
    "IC_SZONDI_PRIMARY_000067", ("DR_SZ_IA_1956_B_000017",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 10 assigns ordinary Sch 0± to inflative Projektion. One striving is projected onto a foreign object while the other is taken into the Ego; the source names this a Deprojektion through Inflation. Execution is limited to the exact ordinary configuration.",
    "În configurația exactă Sch 0±, fără Überdruck, Szondi descrie «inflative Projektion»: una dintre tendințe este hinausprojiziert asupra obiectului străin, iar cealaltă este preluată de Eu. Projektion nu mai este totală; ea este deproiectată parțial prin Inflation.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("0", "±")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000067", "Nu decide din Ich-Bild singur care este conținutul concret al tendinței proiectate și care este conținutul celei preluate în Eu. Nu transforma termenul într-un diagnostic contemporan și nu extinde regula la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000068 = _claim(
    "IC_SZONDI_PRIMARY_000068", ("DR_SZ_IA_1956_B_000017",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 10 assigns ordinary Sch +- to introjektive Projektion / Introprojektion. Both opposed, previously displaced strivings are incorporated into the Ego; Szondi calls this Deprojektion through Introjektion. Execution is limited to the exact ordinary configuration.",
    "În configurația exactă Sch +-, fără Überdruck, Szondi numește mecanismul «introjektive Projektion / Introprojektion». Cele două tendințe opuse, hinausverlegt, sunt încorporate în propriul Eu: Deprojektion se face aici prin Introjektion.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("+", "-")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000068", "Nu inventa conținutul concret al tendințelor introiectate, obiectul proiectiv ori consecințe biografice. Nu confunda Introprojektion din familia proiectivă cu totale Introjektion Sch +0 și nu extinde regula la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

_CLAIM_000069 = _claim(
    "IC_SZONDI_PRIMARY_000069", ("DR_SZ_IA_1956_B_000017",), ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II Table 10 assigns ordinary Sch ±- to Fugue/Flucht, projection held back through Zwang. The source states that both displaced strivings are restrained: partly through Introjektion and partly through Negation; this is Deprojektion through compulsion. Execution is limited to the exact ordinary configuration.",
    "În configurația exactă Sch ±-, fără Überdruck, Szondi descrie «Fugue / Flucht»: Projektion este zurückgehalten prin Zwang. Ambele tendințe hinausverlegt sunt ținute în frâu, parte prin Introjektion, parte prin Negation; Deprojektion se produce prin constrângere.",
    _base.TriggerDefinition(kind=_base.TriggerKind.EXACT_STRUCTURAL, predicates=(_base.Predicate("profile.vector.Sch.base_symbols", _base.Operator.EQ, ("±", "-")), _base.Predicate("profile.factor.k.quantum_level", _base.Operator.EQ, 0), _base.Predicate("profile.factor.p.quantum_level", _base.Operator.EQ, 0))),
    status=_base.LifecycleStatus.APPROVED,
    anti_inferences=(_base.AntiInference("AI_SZONDI_000069", "Nu transforma denumirea «Fugue / Flucht» într-o afirmație factuală că persoana fuge, comite o fugă patologică sau prezintă automat un sindrom disociativ ori obsesiv contemporan. Păstrează mecanismul source-grounded și nu extinde regula la Überdruck fără autorizare separată."),),
    sexual_content=True, pathodiagnostic_content=True, criminological_content=True,
)

INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (
    _CLAIM_000055, _CLAIM_000056, _CLAIM_000057, _CLAIM_000058,
    _CLAIM_000059, _CLAIM_000060, _CLAIM_000061, _CLAIM_000062,
    _CLAIM_000063, _CLAIM_000064, _CLAIM_000065, _CLAIM_000066,
    _CLAIM_000067, _CLAIM_000068, _CLAIM_000069,
)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
