"""Instructions for the generative clinical integration layer.

These rules are intentionally small.  They correct failure modes observed when an
AI was asked to interpret the same Szondi Zehnerserie independently several times:
good global synthesis, but factor-first flattening, automatic modernization of
Szondi's vocabulary, and unsafe assumptions that a null reaction means absence.

The policy does not create doctrine.  Source-authorized meanings still have to
come from P2B claims and traceable doctrine records.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ClinicalSynthesisPolicy:
    configuration_first: bool = True
    deterministic_counts_only: bool = True
    preserve_source_vocabulary: bool = True
    null_is_not_absence: bool = True
    frequency_is_not_sole_weight: bool = True
    consolidate_caveats: bool = True
    avoid_generic_balancing_template: bool = True

    @property
    def instructions(self) -> tuple[str, ...]:
        return (
            "Pornește de la morfologia deterministă a seriei și de la configurațiile vectoriale; "
            "abia apoi folosește factorii pentru diferențiere și integrare.",
            "Nu număra reacțiile din ochi. Folosește exclusiv frecvențele, tensiunile și "
            "configurațiile furnizate de stratul determinist.",
            "Păstrează termenii autorizați de sursa szondiană (de ex. Projektion, Inflation, "
            "Introjektion, Negation, Sadismus, Entfremdung, Desintegration, kainitisch) când "
            "sunt relevanți. Nu îi înlocui automat cu eufemisme psihologice contemporane.",
            "Protecția se aplică inferenței, nu vocabularului: prezintă termenul ca denumire "
            "testologică/doctrinară și nu îl transforma fără suport în fapt biografic, diagnostic "
            "sau conduită efectivă.",
            "Nu interpreta reacția 0 ca absență a trebuinței pulsionale. Sensul ei trebuie decis "
            "din doctrina autorizată, profilul întreg și seria; o Nullreaktion poate marca o "
            "Triebmanifestation, nu lipsa pulsiunii.",
            "Nu acorda prioritate automată numai semnelor frecvente. O configurație rară poate "
            "avea greutate doctrinară mare dacă sursa o autorizează; păstrează distinct frecvența "
            "de semnificația configurativă.",
            "Nu impune secțiuni compensatorii de tip «resurse», «vulnerabilități», «reglare», "
            "«autonomie» sau «atașament» dacă ele nu rezultă din doctrina autorizată ori din "
            "contextul clinic furnizat.",
            "Evită avertismentele standard repetate după fiecare afirmație. Formulează limita "
            "epistemică precis acolo unde schimbă ce poate fi inferat și păstrează raportul clinic "
            "dens, direct și terminologic fidel.",
            "AI-ul integrează configurațiile și relațiile dintre ele; nu inventează doctrină și "
            "nu corectează rezultatele deterministe.",
        )


DEFAULT_CLINICAL_SYNTHESIS_POLICY = ClinicalSynthesisPolicy()
