import json
import unittest

from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_report_ai_v4 import parse_openai_clinical_report_response_v4
from szondi3.clinical_report_plan import build_clinical_report_plan
from szondi3.clinician_alpha_report_renderer_v4 import render_clinician_alpha_report_v4_html
from szondi3.clinician_workspace import build_clinician_workspace
from szondi3.legacy_profile_import import (
    profile_series_from_legacy_text,
    run_legacy_profile_case_from_verified_checkout,
)
from szondi3.longitudinal_comparison import LongitudinalCaseRef


REFERENCE_PROFILE = "h- s+ e+ hy0 k+ p+ d- m-"


def _run():
    series = profile_series_from_legacy_text(REFERENCE_PROFILE)
    return run_legacy_profile_case_from_verified_checkout(
        series,
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


def _decoded(packet):
    plan = build_clinical_report_plan(packet)
    inflation = next(u for u in plan.units if any("+p" in s and "Inflation" in s for s in u.authorized_statements))
    introjection = next(u for u in plan.units if any("+k" in s and "Introjektion" in s for s in u.authorized_statements))
    identification = next(u for u in plan.units if any("−m" in s and "+k" in s for s in u.authorized_statements))
    sch = next(u for u in plan.units if len(u.support_claim_ids) == 2)
    contact = next(u for u in plan.units if any("Kontaktsperre" in s for s in u.authorized_statements))
    return {
        "summary": [
            {"item_id": "S1", "unit_id": sch.unit_id, "kind": "SYNTHESIS", "text": "Centrul lecturii este introinflația și problema limitei realiste."},
            {"item_id": "S2", "unit_id": contact.unit_id, "kind": "SYNTHESIS", "text": "Blocarea contactului apare în doctrină ca formă narcisică de protecție a Eului."},
        ],
        "sections": [
            {
                "section_id": "A",
                "title": "Însușire și expansiune",
                "lead_unit_id": sch.unit_id,
                "passages": [
                    {"item_id": "A1", "unit_id": introjection.unit_id, "kind": "EXPLANATION", "text": "Introiecția înseamnă încorporare, luare în posesie și a face propriu."},
                    {"item_id": "A2", "unit_id": inflation.unit_id, "kind": "EXPLANATION", "text": "Inflația împinge către dublare, perfecțiune și totalitate."},
                    {"item_id": "A3", "unit_id": sch.unit_id, "kind": "BIFURCATION", "text": "Două ramuri rămân deschise: limitarea realistă poate reuși sau poate rămâne dificilă; profilul nu decide între ele."},
                ],
            },
            {
                "section_id": "B",
                "title": "Identificarea prin preluare",
                "lead_unit_id": identification.unit_id,
                "passages": [
                    {"item_id": "B1", "unit_id": identification.unit_id, "kind": "CONTRAST", "text": "A admira nu este încă același lucru cu a prelua o calitate și a o face parte din propriul mod de a proceda; identificarea nu este identitate."},
                ],
            },
            {
                "section_id": "C",
                "title": "Blocarea contactului",
                "lead_unit_id": contact.unit_id,
                "passages": [
                    {"item_id": "C1", "unit_id": contact.unit_id, "kind": "EXPLANATION", "text": "Szondi păstrează aici termenul narcisic și enumeră doctrinar primejdia incestuoasă, bisexualitate, inversiune sau perversiune, fără a atribui automat persoanei una dintre ele."},
                    {"item_id": "C2", "unit_id": contact.unit_id, "kind": "EXAMPLE", "text": "De pildă, contactul ar putea fi întrerupt într-un moment dificil, fără ca scena să precizeze cauza sau natura primejdiei pulsionale."},
                ],
            },
        ],
        "global_questions": [
            {"question_id": "Q1", "unit_id": sch.unit_id, "text": "Cum decideți unde să vă opriți când ceva important tinde să crească?"},
            {"question_id": "Q2", "unit_id": contact.unit_id, "text": "Ce se întâmplă concret înainte ca dialogul să se închidă?"},
        ],
        "closing_limits": [
            {"item_id": "L1", "unit_id": contact.unit_id, "kind": "LIMIT", "text": "Această terminologie doctrinară nu stabilește orientarea, conduita sau diagnosticul persoanei."},
        ],
        "appendix_only_unit_ids": [],
    }


class ClinicianAlphaReportV4Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case_run = _run()
        cls.packet = cls.case_run.evidence_packet
        response = {
            "id": "resp_v4_renderer",
            "model": "gpt-5.6-sol",
            "status": "completed",
            "output_text": json.dumps(_decoded(cls.packet), ensure_ascii=False),
        }
        cls.result = parse_openai_clinical_report_response_v4(cls.packet, response)
        cls.workspace = build_clinician_workspace(LongitudinalCaseRef(case_id="test-v4", run=cls.case_run))

    def test_global_clinical_reading_precedes_deterministic_appendix(self):
        html = render_clinician_alpha_report_v4_html(
            self.workspace,
            ai_result=self.result,
            ai_available=True,
            csrf_token="csrf-test",
        )
        self.assertLess(html.index("Lectura clinică"), html.index("Anexă: baza interpretativă"))
        self.assertIn("Sinteză", html)
        self.assertIn("Însușire și expansiune", html)
        self.assertIn("De explorat în interviu", html)

    def test_v4_surface_does_not_render_plan_unit_template_headings(self):
        html = render_clinician_alpha_report_v4_html(
            self.workspace,
            ai_result=self.result,
            ai_available=False,
        )
        self.assertNotIn("Sensul szondian", html)
        self.assertNotIn("Explicație clinică", html)
        self.assertNotIn("Exemple ilustrative", html)
        self.assertNotIn("Ce nu rezultă de aici", html)
        self.assertNotIn("RPU-", html)


if __name__ == "__main__":
    unittest.main()
