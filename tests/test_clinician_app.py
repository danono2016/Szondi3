import unittest
from urllib.parse import urlencode

from szondi3 import clinical_release
from szondi3.administration import complete_foreground, record_foreground
from szondi3.clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from szondi3.clinical_archive import SQLiteClinicalArchive
from szondi3.clinical_case_runner import run_clinical_case
from szondi3.clinical_pipeline import AdministeredTestRecord
from szondi3.clinician_app import ClinicianApp, make_local_clinician_server
from szondi3.clinician_workspace import build_clinician_workspace
from szondi3.longitudinal_comparison import LongitudinalCaseRef
from szondi3.stimuli import SERIES, presentation_rows


def _card_ids(series):
    return [card.card_id for row in presentation_rows(series) for card in row]


def _foreground(offset):
    choices = []
    for series in SERIES:
        cards = _card_ids(series)
        shift = offset % len(cards)
        rotated = cards[shift:] + cards[:shift]
        choices.append(record_foreground(series, rotated[:2], rotated[2:4]))
    return complete_foreground(choices)


def _run(offset=0):
    records = tuple(
        AdministeredTestRecord(_foreground(offset + index))
        for index in range(8)
    )
    return run_clinical_case(
        records,
        git_commit_sha=clinical_release._verified_checkout_sha(),
        synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
        synthesis_model=DEFAULT_PREVIEW_MODEL,
    )


def _workspace():
    return build_clinician_workspace(
        LongitudinalCaseRef(case_id="CASE-002", run=_run(1)),
        prior_cases=(LongitudinalCaseRef(case_id="CASE-001", run=_run(0)),),
    )


def _request(app, path, query="", method="GET"):
    captured = {}

    def start_response(status, headers):
        captured["status"] = status
        captured["headers"] = dict(headers)

    payload = b"".join(
        app(
            {
                "REQUEST_METHOD": method,
                "PATH_INFO": path,
                "QUERY_STRING": query,
            },
            start_response,
        )
    ).decode("utf-8")
    return captured, payload


class ClinicianAppTests(unittest.TestCase):
    def test_core_clinician_routes_compose_existing_surfaces(self):
        app = ClinicianApp(_workspace())
        expectations = {
            "/": "Caz curent",
            "/current": "Profil Szondi — caz curent",
            "/findings": "Constatări Szondiene autorizate",
            "/longitudinal": "Comparație longitudinală",
            "/integration": "Integrare clinică manuală",
            "/report": "raport clinic de lucru",
            "/archive": "Arhivă locală pseudonimizată",
        }
        for route, phrase in expectations.items():
            captured, html = _request(app, route)
            self.assertEqual(captured["status"], "200 OK")
            self.assertIn(phrase, html)
            self.assertEqual(captured["headers"]["Cache-Control"], "no-store")
            self.assertEqual(captured["headers"]["Referrer-Policy"], "no-referrer")

    def test_finding_route_uses_exact_drilldown_identity(self):
        workspace = _workspace()
        app = ClinicianApp(workspace)
        finding = workspace.report.findings[0]
        query = urlencode(
            {
                "claim_id": finding.claim_id,
                "scope": finding.scope,
                "profile_number": "" if finding.profile_number is None else finding.profile_number,
            }
        )
        captured, html = _request(app, "/finding", query)
        self.assertEqual(captured["status"], "200 OK")
        self.assertIn("De ce apare?", html)
        self.assertIn(finding.claim_id, html)
        self.assertIn(finding.statement, html)

    def test_bad_finding_identity_and_non_get_fail_closed(self):
        app = ClinicianApp(_workspace())
        captured, _ = _request(
            app,
            "/finding",
            urlencode({"claim_id": "IC_MISSING", "scope": "SERIES"}),
        )
        self.assertEqual(captured["status"], "404 Not Found")

        captured, html = _request(app, "/current", method="POST")
        self.assertEqual(captured["status"], "405 Method Not Allowed")
        self.assertIn("read-oriented", html)

    def test_archive_route_can_use_configured_local_archive(self):
        workspace = _workspace()
        with SQLiteClinicalArchive(":memory:") as archive:
            app = ClinicianApp(workspace, archive=archive)
            captured, html = _request(app, "/archive")
            self.assertEqual(captured["status"], "200 OK")
            self.assertIn("Arhiva este goală", html)

    def test_server_factory_refuses_network_exposure_and_accepts_loopback(self):
        app = ClinicianApp(_workspace())
        with self.assertRaises(ValueError):
            make_local_clinician_server(app, host="0.0.0.0", port=8765)
        server = make_local_clinician_server(app, host="127.0.0.1", port=0)
        try:
            self.assertEqual(server.server_address[0], "127.0.0.1")
        finally:
            server.server_close()

    def test_wrong_app_inputs_fail_closed(self):
        with self.assertRaises(TypeError):
            ClinicianApp(object())
        with self.assertRaises(TypeError):
            make_local_clinician_server(object())


if __name__ == "__main__":
    unittest.main()
