"""Current source-linked P2B claim catalogue.

Claims through ``IC_SZONDI_PRIMARY_000043`` remain byte-identical in
``interpretation_catalogue_000043``. This module appends narrowly reviewed
claims while preserving the public catalogue interface.
"""

from .interpretation_catalogue_000043 import *  # noqa: F401,F403
from . import interpretation_catalogue_000043 as _previous
from . import interpretation_catalogue_base as _base

_claim = _base._claim


_CLAIM_000044 = _claim(
    "IC_SZONDI_PRIMARY_000044",
    (
        "DR_SZ_SA_1948_000058",
        "DR_SZ_SA_1948_000059",
        "DR_SZ_SA_1948_000060",
        "DR_SZ_SA_1948_000061",
        "DR_SZ_SA_1948_000062",
    ),
    ("SZ_SA_1948",),
    _base.AssertionMode.LIMITATION,
    "Schicksalsanalyse 1948 explicitly limits its then-current scope to Triebschicksal, distinguishes Mental- and Sozial-Schicksal as additional components of Gesamtschicksal, states that life is always more than Triebschicksal, and says the method is still far from representing the person's complete Lebensplan. This is a scope boundary for the whole drive analysis, not only for an isolated profile or proportion.",
    "Chiar interpretarea unei serii Szondi complete rămâne, în termenii sursei, o analiză a Triebschicksal-ului și nu este echivalentă cu Gesamtschicksal-ul sau cu viața întreagă a persoanei. Szondi distinge separat Mental-Schicksal și Sozial-Schicksal și afirmă explicit că «Leben ist stets mehr als Triebschicksal»; metoda nu poate reprezenta din test singur Lebensplan-ul complet.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000044",
            "Nu transforma seria Szondi, Triebprofilurile, Triebklasse, Triebformel sau indicii seriei într-o descriere exhaustivă a vieții ori a persoanei, într-un Gesamtschicksal sau Lebensplan complet și nu deduce din ele singure destinul mental/rațional, situația socială concretă, biografia, viitorul, boala ori moartea persoanei. Aceste domenii cer informații independente și nu sunt absorbite de Triebschicksal.",
        ),
    ),
)


_CLAIM_000045 = _claim(
    "IC_SZONDI_PRIMARY_000045",
    (
        "DR_SZ_SA_1948_000127",
        "DR_SZ_SA_1948_000172",
        "DR_SZ_SA_1948_000243",
    ),
    ("SZ_SA_1948",),
    _base.AssertionMode.LIMITATION,
    "Schicksalsanalyse 1948 itself places strong epistemic limits on its hereditary/genotropic theory: concrete Anlagematerial can be established only approximately and only through especially careful, large-scale Familienforschung; the hoped-for experimental strengthening of the Gentheorie des Schicksals is explicitly conditional on future research; and quantitative gene action / multiple allelomorphs in humans are described as nearly terra incognita. Historical genetic terminology therefore does not authorize a modern individual genetic finding from the Szondi protocol.",
    "Termenii ereditari și genotropi din teoria istorică a lui Szondi nu constituie o identificare genetică a persoanei. Chiar în cadrul sursei, Anlagematerial-ul concret poate fi stabilit numai aproximativ și prin Familienforschung foarte amplă și atentă; confirmarea experimentală a Gentheorie des Schicksals era lăsată cercetărilor viitoare, iar mecanismele cantitative ale genelor la om erau descrise drept aproape «terra incognita».",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("series.profile_count", _base.Operator.EXISTS),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000045",
            "Nu transforma un profil sau o serie Szondi, un Wurzelfaktor, un termen precum Konduktor/Genotropismus/Erbanlage ori o asociere istorică din sursă în dovada unei gene, alele, mutații, predispoziții ereditare moderne, statut de purtător, mod de transmitere, boală familială concretă sau diagnostic la rude. Nu atribui genetic alegerea partenerului, profesia, talentul, boala, cauza morții ori riscul de suicid pe baza testului; asemenea afirmații ar necesita dovezi genetice, medicale și genealogice independente, nu inferență din protocolul Szondi.",
        ),
    ),
    hereditary_genetic_content=True,
    pathodiagnostic_content=True,
)


_CLAIM_000046 = _claim(
    "IC_SZONDI_PRIMARY_000046",
    (
        "DR_SZ_IA_1956_B_000006",
        "DR_SZ_IA_1956_B_000007",
        "DR_SZ_IA_1956_B_000009",
        "DR_SZ_IA_1956_B_000011",
        "DR_SZ_IA_1956_B_000043",
    ),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II treats foreground and complementary Ego configurations dialectically, explicitly calls a Vorder-Ich-only analysis half-analysis, and requires Komplementprofile to be interpreted rather than ignored. The source also distinguishes theoretical and experimental complement profiles in its stated procedure and separates the theoretical possibility of complementarity from actual integration, which it describes as very rare. The executable rule therefore activates only when a real experimental complement administration has been supplied; it does not synthesize a complement from the foreground profile.",
    "Când a fost administrat și calculat efectiv un profil complementar experimental (E.K.P.), acesta trebuie păstrat ca profil complementar distinct și citit corelativ cu Vorderprofil-ul, nu ignorat și nici amestecat în seria profilurilor de prim-plan. E.K.P. oferă o a doua configurație testologică, experimental obținută, relevantă pentru lectura complementară; nu este echivalent automat cu profilul complementar teoretic (Th.K.P.) și nu dovedește că această configurație este deja manifestă sau că va deveni ulterior prim-plan.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.CONDITIONAL_CONTEXTUAL,
        predicates=(
            _base.Predicate("protocol.experimental_complement.present", _base.Operator.EQ, True),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000046",
            "Nu trata E.K.P. drept «adevăratul Eu ascuns», a doua personalitate, diagnostic latent demonstrat, comportament secret sau predictor al unei schimbări viitoare. Nu îl identifica automat cu Th.K.P., nu presupune că perechea se va integra efectiv și nu transforma posibilitatea complementară într-o succesiune inevitabilă; Szondi separă posibilitatea teoretică de integrarea reală și afirmă că aceasta din urmă apare foarte rar. Nu introduce E.K.P. în calculele seriei libere de Vordergrundprofile și nu importa automat etichetele istorice/pathodiagnostice ale perechilor complementare fără reguli source-grounded separate.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000047 = _claim(
    "IC_SZONDI_PRIMARY_000047",
    (
        "DR_SZ_IA_1956_B_000008",
        "DR_SZ_IA_1956_B_000009",
        "DR_SZ_IA_1956_B_000011",
        "DR_SZ_IA_1956_B_000043",
    ),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.CONDITIONAL,
    "Ich-Analyse II gives an exact Table-9 mapping of the sixteen Sch positions into eight theoretical complementary pairs and uses experimentally obtained complement profiles as evidence in complementary Ego analysis. Production execution is deliberately restricted to ordinary Sch reactions without quantum overpressure or forced nulls, so no source-unstated normalization is introduced.",
    "În această administrare, Sch-ul profilului complementar experimental (E.K.P.) coincide exact, la nivelul reacțiilor obișnuite, cu poziția Sch complementară teoretică (Th.K.P.) definită de Tabelul 9 pentru Sch-ul Vorderprofil-ului. Aceasta susține o concordanță structurală între cele două poziții Sch în cadrul modelului complementar al lui Szondi; nu stabilește singură conținutul clinic al relației.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate("protocol.experimental_complement.sch_theoretical_relation", _base.Operator.EQ, "MATCH"),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000047",
            "Nu transforma concordanța structurală E.K.P.–Th.K.P. la Sch într-o dovadă a unei a doua personalități, a unui diagnostic latent, a unui comportament ascuns, a unei succesiuni viitoare inevitabile sau a integrării efective a celor două poziții. Nu importa automat denumirile istorice, sexuale ori pathodiagnostice din Tabelul 9; acestea cer claims separate. Concordanța arată numai că E.K.P. reproduce, în această administrare și în condițiile autorizate, perechea Sch teoretică definită de sursă.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000048 = _claim(
    "IC_SZONDI_PRIMARY_000048",
    (
        "DR_SZ_IA_1956_B_000008",
        "DR_SZ_IA_1956_B_000014",
        "DR_SZ_IA_1956_B_000043",
    ),
    ("SZ_IA_1956_B",),
    _base.AssertionMode.LIMITATION,
    "Table 9 defines eight fundamental theoretical Sch complement pairs, while Ich-Analyse II explicitly leaves open whether additional forms of complementary Ego relation exist and separately constructs theoretical and experimental complement profiles. An ordinary experimental complement that does not reproduce the Table-9 theoretical Sch pair must therefore be preserved as observed rather than forced into the theoretical mapping.",
    "În această administrare, Sch-ul E.K.P. nu coincide exact cu poziția Sch a Th.K.P. prevăzută de Tabelul 9 pentru Vorderprofil. Aceasta înseamnă numai lipsa concordanței structurale exacte cu perechea teoretică fundamentală respectivă; E.K.P. rămâne dat experimental distinct și nu trebuie «corectat» pentru a se potrivi Th.K.P. Szondi însuși lasă deschisă posibilitatea altor forme ale relațiilor complementare.",
    _base.TriggerDefinition(
        kind=_base.TriggerKind.LIMITATION_GUARD,
        predicates=(
            _base.Predicate("protocol.experimental_complement.sch_theoretical_relation", _base.Operator.EQ, "MISMATCH"),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000048",
            "Nu declara administrarea invalidă, nu concluziona că nu există nicio relație complementară și nu înlocui E.K.P. observat cu Th.K.P. calculat. Nu selecta arbitrar o altă pereche, nu inventa un Hinter-Ich și nu deriva diagnostic, comportament sau prognostic din simpla neconcordanță. Tipologia celor opt perechi este fundamentală în sursă, dar nu este declarată exhaustivă definitiv.",
        ),
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000049 = _base.ClaimDefinition(
    schema_version=1,
    claim_id="IC_SZONDI_PRIMARY_000049",
    rule_version=1,
    status=_base.STATUS,
    source_layer=_base.PRIMARY,
    doctrine_ids=(
        "DR_SZ_IA_1956_B_000006",
        "DR_SZ_IA_1956_B_000008",
        "DR_SZ_IA_1956_B_000009",
    ),
    source_ids=("SZ_IA_1956_B",),
    epistemic_class=_base.EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER,
    assertion_mode=_base.AssertionMode.POSSIBLE,
    source_strength_note=(
        "Ich-Analyse II explicitly defines sukzessive Kontrastwirkung as the later "
        "movement of the complementary Ego existence into the foreground. The runtime "
        "trigger is a conservative implementation inference: it requires a real E.K.P. "
        "whose ordinary Sch position first matches the Table-9 theoretical complement, "
        "followed by the exact same ordinary Sch position in one or more later foreground profiles."
    ),
    claim=(
        "În seria cronologică apare o secvență compatibilă, la nivelul Sch, cu ceea ce "
        "Szondi numește sukzessive Kontrastwirkung: E.K.P. a coincis mai întâi cu Th.K.P., "
        "iar aceeași poziție Sch complementară apare ulterior într-un Vorderprofil. "
        "Aceasta este o concordanță serială posibilă cu trecerea ulterioară în prim-plan "
        "a poziției complementare; nu dovedește că întregul Hinter-Ich a devenit manifest."
    ),
    trigger=_base.TriggerDefinition(
        kind=_base.TriggerKind.COMPOSITE,
        predicates=(
            _base.Predicate(
                "protocol.experimental_complement.sch_theoretical_relation",
                _base.Operator.EQ,
                "MATCH",
            ),
            _base.Predicate(
                "protocol.experimental_complement.sch_later_foreground_matches",
                _base.Operator.NE,
                (),
            ),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000049",
            "Nu transforma această reapariție serială a aceleiași poziții Sch în dovada unei schimbări globale de personalitate, a manifestării întregului Hinter-Ich, a integrării, a unei decompensări, a unui diagnostic ori a unei evoluții inevitabile. Nu presupune cauzalitate între E.K.P. și profilul ulterior și nu extinde relația de la Sch la ceilalți vectori fără concordanțe source-grounded separate. Ordinea temporală și identitatea structurală susțin numai o compatibilitate testologică cu sukzessive Kontrastwirkung.",
        ),
    ),
    inference_rationale=(
        "The source defines successive contrast by later foreground emergence of the complementary Ego existence. "
        "Because runtime does not equate E.K.P. with Hinter-Ich, activation requires two additional safeguards: "
        "the observed E.K.P. Sch must first equal the Table-9 theoretical Sch complement, and that same ordinary "
        "Sch position must then be observed in a later foreground administration."
    ),
    reversal_condition=(
        "Retire or narrow this trigger if source review shows that E.K.P.–Th.K.P. Sch concordance plus later exact "
        "foreground recurrence is insufficient to operationalize sukzessive Kontrastwirkung, or if later source "
        "evidence requires additional vectorial/clinical conditions."
    ),
)


_CLAIM_000050 = _base.ClaimDefinition(
    schema_version=1,
    claim_id="IC_SZONDI_PRIMARY_000050",
    rule_version=1,
    status=_base.STATUS,
    source_layer=_base.PRIMARY,
    doctrine_ids=(
        "DR_SZ_IA_1956_A_000040",
        "DR_SZ_IA_1956_A_000048",
    ),
    source_ids=("SZ_IA_1956_A",),
    epistemic_class=_base.EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER,
    assertion_mode=_base.AssertionMode.CONDITIONAL,
    source_strength_note=(
        "Ich-Analyse I explicitly defines +k Introjektion and -k Negation as the functional "
        "opposite pair of the stellungnehmendes k-Ich, gathered under Egosystole/Ich-Einengung; "
        "the source describes +k as the 'yes' and -k as the 'no' direction of this k function. "
        "The runtime trigger is an implementation inference limited to the directly observed fact "
        "that both source-defined k directions occur somewhere in the repeated foreground series."
    ),
    claim=(
        "În seria de Vordergrundprofile apar atât +k, cât și -k. În modelul lui Szondi, "
        "acestea sunt funcții opuse ale aceluiași k-Ich/Egosystole: +k este direcția "
        "introiectivă de acceptare/încorporare, iar -k direcția de negare/refuz. Prezența "
        "ambelor în serie trebuie păstrată ca variație între cei doi poli funcționali k, "
        "nu ca dovadă a două Euri incompatibile."
    ),
    trigger=_base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate(
                "series.sch.k_opposed_signs_present",
                _base.Operator.EQ,
                True,
            ),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000050",
            "Nu transforma prezența +k și -k în serie în dovada unei personalități scindate, a inconsecvenței globale, a două Euri separate sau a unui diagnostic. Termenul istoric Realitätsprüfung din sursă nu autorizează concluzii moderne despre reality testing intact/deficitar, psihoză sau contact cu realitatea. Nu deduce Verdrängung din simplul -k și nu atribui cauză, ritm ori succesiune psihodinamică fără date suplimentare."
        ),
    ),
    inference_rationale=(
        "The source establishes the k polarity itself. The implementation inference consists only in "
        "promoting the observed occurrence of at least one positive and one negative k foreground reaction "
        "to a series-level statement that both poles of that source-defined k pair were sampled."
    ),
    reversal_condition=(
        "Retire or narrow this trigger if source review requires additional conditions before repeated +k/-k "
        "occurrence may be described at series level as sampling both poles of Egosystole."
    ),
    pathodiagnostic_content=True,
)


_CLAIM_000051 = _base.ClaimDefinition(
    schema_version=1,
    claim_id="IC_SZONDI_PRIMARY_000051",
    rule_version=1,
    status=_base.STATUS,
    source_layer=_base.PRIMARY,
    doctrine_ids=(
        "DR_SZ_IA_1956_A_000040",
        "DR_SZ_IA_1956_A_000043",
        "DR_SZ_IA_1956_A_000045",
    ),
    source_ids=("SZ_IA_1956_A",),
    epistemic_class=_base.EpistemicClass.IMPLEMENTATION_INFERRED_TRIGGER,
    assertion_mode=_base.AssertionMode.POSSIBLE,
    source_strength_note=(
        "Ich-Analyse I maps p to Egodiastole/Ich-Erweiterung and, with the explicit qualifier "
        "'nehmen wir an', treats primordial projection/participation, inflation and secondary projection "
        "as phases/forms of that same process. The source also states that inflation/projection phases may "
        "alternate and that their exact individual order is not always determinable. Runtime therefore "
        "records only the presence of both -p and +p directions in the foreground series; it does not infer a phase order."
    ),
    claim=(
        "În seria de Vordergrundprofile apar atât -p, cât și +p. În modelul lui Szondi, "
        "Projektion și Inflation aparțin aceleiași dinamici supraordonate de Egodiastole/" 
        "Ich-Erweiterung. Prezența ambelor direcții p în serie este compatibilă cu participarea "
        "mai multor forme ale acestei funcții de extindere a Eului; nu trebuie tratată ca o "
        "contradicție între două descrieri incompatibile ale persoanei."
    ),
    trigger=_base.TriggerDefinition(
        kind=_base.TriggerKind.EXACT_STRUCTURAL,
        predicates=(
            _base.Predicate(
                "series.sch.p_opposed_signs_present",
                _base.Operator.EQ,
                True,
            ),
        ),
    ),
    anti_inferences=(
        _base.AntiInference(
            "AI_SZONDI_000051",
            "Nu transforma ordinea testelor cu -p și +p într-o cronologie demonstrată primordiale Projektion → Inflation → sekundäre Projektion și nu decide din semne care formă de proiecție este prezentă. Nu deduce progresie, regresie, decompensare, psihoză, manie, disociere ori prognostic din schimbarea de semn p. Sursa însăși califică această schemă ca presupunere și spune că ordinea individuală Inflation versus sekundäre Projektion nu este întotdeauna stabilibilă."
        ),
    ),
    inference_rationale=(
        "The source establishes that projection and inflation belong under Egodiastole. The implementation "
        "inference is restricted to recognizing that a foreground series containing both negative and positive p "
        "has directly sampled both source-defined p directions; no temporal phase assignment is added."
    ),
    reversal_condition=(
        "Retire or narrow this trigger if source review shows that simple repeated -p/+p occurrence is insufficient "
        "even for the limited series-level statement that both p directions within Egodiastole were observed."
    ),
    pathodiagnostic_content=True,
)


INITIAL_CLAIMS = _previous.INITIAL_CLAIMS + (
    _CLAIM_000044,
    _CLAIM_000045,
    _CLAIM_000046,
    _CLAIM_000047,
    _CLAIM_000048,
    _CLAIM_000049,
    _CLAIM_000050,
    _CLAIM_000051,
)
CLAIMS_BY_ID = {claim.claim_id: claim for claim in INITIAL_CLAIMS}
