"""Alpha clinician shell with concise report and explicit AI formulation.

The existing archive-enabled application remains the authoritative administration,
calculation, integration and archive shell. This subclass changes only the current
report surface, adds one explicit CSRF-protected AI formulation action, and exposes
a bounded legacy-import path for already-scored historical foreground profiles.

AI output is ephemeral process memory. It is not written into the immutable SQLite
assessment snapshot and it never mutates ``ClinicalCaseRun``.
"""

from __future__ import annotations

import argparse
from functools import partial
from html import escape
import os
from pathlib import Path
from typing import Callable

from .clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from .clinical_archive import SQLiteClinicalArchive
from .clinical_evidence_packet import ClinicalEvidencePacket
from .clinical_report_ai import (
    ClinicalReportAIResult,
    run_openai_clinical_report,
)
from .clinician_alpha_report_renderer import render_clinician_alpha_report_html
from .clinician_app import (
    _navigation,
    _page,
    _parse_form,
    _redirect,
    _single_form_value,
    make_local_clinician_server,
)
from .clinician_archive_browser import ArchiveBrowsingClinicianApp
from .clinician_assessment_session import require_pseudonymous_assessment_id
from .clinician_working_report_renderer import render_clinician_working_report_html
from .clinician_workspace import ClinicianWorkspace, build_clinician_workspace
from .legacy_profile_import import (
    profile_series_from_legacy_text,
    run_legacy_profile_case_from_verified_checkout,
)
from .longitudinal_comparison import LongitudinalCaseRef


ClinicalReportAIRunner = Callable[[ClinicalEvidencePacket], ClinicalReportAIResult]


class AlphaClinicianApp(ArchiveBrowsingClinicianApp):
    """Archive-enabled app with the Alpha-1 clinical report as the default report."""

    def __init__(
        self,
        workspace: ClinicianWorkspace | None = None,
        *,
        archive: SQLiteClinicalArchive | None = None,
        ai_report_runner: ClinicalReportAIRunner | None = None,
    ) -> None:
        super().__init__(workspace, archive=archive)
        if ai_report_runner is not None and not callable(ai_report_runner):
            raise TypeError("ai_report_runner must be callable or None")
        self._ai_report_runner = ai_report_runner
        self._ai_result: ClinicalReportAIResult | None = None
        self._ai_result_case_id: str | None = None
        self._ai_error: str | None = None
        self._legacy_case_ids: set[str] = set()

    @property
    def ai_available(self) -> bool:
        return self._ai_report_runner is not None

    def _current_ai_result(self, workspace: ClinicianWorkspace) -> ClinicalReportAIResult | None:
        if self._ai_result_case_id != workspace.current.case_id:
            return None
        return self._ai_result

    def _home_page(self) -> str:
        html = super()._home_page()
        legacy = (
            '<div class="notice"><strong>Cazuri istorice:</strong> '
            'dacă ai deja profilul Szondi calculat, îl poți introduce direct fără '
            'a reconstrui alegerile fotografiilor. '
            '<a href="/legacy"><strong>Introdu profiluri manual</strong></a>.</div>'
        )
        return html.replace("</body>", legacy + "</body>", 1)

    def _legacy_import_page(
        self,
        *,
        error: str | None = None,
        assessment_id: str = "",
        profiles_text: str = "",
    ) -> str:
        error_html = (
            f'<div class="notice error"><strong>Eroare:</strong> {escape(error)}</div>'
            if error
            else ""
        )
        archive_note = (
            '<p class="meta"><strong>Notă de persistență:</strong> această primă '
            'suprafață de import istoric păstrează cazul în sesiunea curentă și îl '
            'poate trimite în raportul/AI-ul clinic, dar nu îl scrie în arhiva '
            'card-by-card. Nu sunt fabricate alegeri de fotografii pentru a forța '
            'compatibilitatea cu arhiva.</p>'
        )
        return _page(
            "Szondi3 — import profiluri istorice",
            _navigation(self.workspace is not None)
            + '<h1>Introducere manuală a profilurilor Szondi</h1>'
            + '<div class="notice"><strong>Pentru protocoale vechi deja calculate.</strong> '
            'Introdu numai reacțiile factoriale pe care le ai în fișa istorică. '
            'Aplicația nu inventează numărul de alegeri simpatice/antipatice și nu '
            'reconstruiește fotografiile lipsă.</div>'
            + error_html
            + '<form method="post" action="/legacy/import">'
            + self._csrf_field()
            + '<p><label>ID evaluare <input required maxlength="80" name="assessment_id" '
            + f'value="{escape(assessment_id, quote=True)}" '
            + 'pattern="[A-Za-z0-9][A-Za-z0-9._-]{0,79}" placeholder="OLD-CASE-001"></label></p>'
            + '<p><label>Profiluri (1–10; un profil pe linie)'
            + f'<textarea required name="profiles" rows="10" spellcheck="false" '
            + 'placeholder="- + + 0 + + - -&#10;h0 s+! e- hy± k+ p0 d- m+">'
            + escape(profiles_text)
            + '</textarea></label></p>'
            + '<p class="meta">Ordinea neetichetată este <code>h s e hy k p d m</code>. '
            'Poți folosi fie opt simboluri, fie forme etichetate precum '
            '<code>h- s+ e+ hy0 k+ p+ d- m-</code>. Simboluri admise: '
            '<code>0 + +! +!! +!!! - -! -!! -!!! ± ±!</code>.</p>'
            + '<button type="submit"><strong>Calculează și deschide raportul</strong></button>'
            + '</form>'
            + archive_note,
        )

    def _legacy_notice(self, html: str, case_id: str) -> str:
        if case_id not in self._legacy_case_ids:
            return html
        notice = (
            '<div class="notice"><strong>Import istoric manual.</strong> '
            'Profilurile factoriale au fost introduse direct; alegerile fotografiilor '
            'și numărătorile simpatice/antipatice nu sunt cunoscute și nu au fost '
            'reconstruite. P2B și raportul folosesc numai morfologia formală furnizată.</div>'
        )
        return html.replace("<body>", "<body>" + notice, 1)

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        if path == "/legacy":
            return "200 OK", self._legacy_import_page()
        if path in {"/report", "/report/audit"}:
            try:
                workspace = self._workspace_required()
            except LookupError:
                return super()._resolve(path, query_string)
            if path == "/report/audit":
                html = render_clinician_working_report_html(workspace.report)
                return "200 OK", self._legacy_notice(html, workspace.current.case_id)
            html = render_clinician_alpha_report_html(
                workspace,
                ai_result=self._current_ai_result(workspace),
                ai_available=self.ai_available,
                csrf_token=self.csrf_token if self.ai_available else None,
                ai_error=self._ai_error,
            )
            return "200 OK", self._legacy_notice(html, workspace.current.case_id)
        return super()._resolve(path, query_string)

    def _handle_legacy_import(self, environ: dict):
        assessment_id = ""
        profiles_text = ""
        try:
            form = _parse_form(environ)
            self._require_csrf(form)
            assessment_id = require_pseudonymous_assessment_id(
                _single_form_value(form, "assessment_id")
            )
            profiles_text = _single_form_value(form, "profiles")
            series = profile_series_from_legacy_text(profiles_text)
            run = run_legacy_profile_case_from_verified_checkout(
                series,
                synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
                synthesis_model=DEFAULT_PREVIEW_MODEL,
            )
            workspace = build_clinician_workspace(
                LongitudinalCaseRef(case_id=assessment_id, run=run)
            )
            self._live_runs[assessment_id] = run
            self.workspace = workspace
            self._legacy_case_ids.add(assessment_id)
            self._ai_result = None
            self._ai_result_case_id = None
            self._ai_error = None
            return _redirect("/report")
        except PermissionError as exc:
            return (
                "403 Forbidden",
                _page("Cerere refuzată", f'<h1>403</h1><p>{escape(str(exc))}</p>'),
                (),
            )
        except (RuntimeError, TypeError, ValueError) as exc:
            return (
                "400 Bad Request",
                self._legacy_import_page(
                    error=str(exc),
                    assessment_id=assessment_id,
                    profiles_text=profiles_text,
                ),
                (),
            )

    def _handle_report_ai(self, environ: dict):
        if self._ai_report_runner is None:
            return (
                "409 Conflict",
                _page(
                    "Szondi3 — AI neconfigurat",
                    _navigation(self.workspace is not None)
                    + '<h1>Formularea clinică AI nu este configurată</h1>'
                    + '<p>Raportul determinist și auditul rămân disponibile. Pentru sesiunea locală Alpha, cheia furnizorului trebuie configurată în afara aplicației.</p>'
                    + '<p><a href="/report">Înapoi la raport</a></p>',
                ),
                (),
            )
        try:
            form = _parse_form(environ)
            self._require_csrf(form)
            workspace = self._workspace_required()
            result = self._ai_report_runner(workspace.current.run.evidence_packet)
            if not isinstance(result, ClinicalReportAIResult):
                raise TypeError("AI report runner returned an unexpected result type")
            self._ai_result = result
            self._ai_result_case_id = workspace.current.case_id
            self._ai_error = None
            return _redirect("/report")
        except PermissionError as exc:
            return (
                "403 Forbidden",
                _page("Cerere refuzată", f'<h1>403</h1><p>{escape(str(exc))}</p>'),
                (),
            )
        except LookupError as exc:
            return (
                "409 Conflict",
                _page(
                    "Evaluare necesară",
                    _navigation(False)
                    + f'<h1>Evaluare necesară</h1><p>{escape(str(exc))}</p>',
                ),
                (),
            )
        except (RuntimeError, TypeError, ValueError) as exc:
            self._ai_result = None
            self._ai_result_case_id = None
            self._ai_error = str(exc)
            return _redirect("/report")

    def _handle_post(self, path: str, environ: dict):
        if path == "/legacy/import":
            return self._handle_legacy_import(environ)
        if path == "/report/ai":
            return self._handle_report_ai(environ)
        return super()._handle_post(path, environ)


def _configured_ai_runner() -> ClinicalReportAIRunner | None:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        return None
    return partial(run_openai_clinical_report, api_key=api_key)


def main(argv: list[str] | None = None) -> int:
    """Launch the current Alpha clinician product surface."""
    parser = argparse.ArgumentParser(description="Szondi3 Alpha clinician application")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--archive",
        default=str(Path.home() / ".szondi3" / "clinical_archive.sqlite3"),
        help="SQLite archive path outside the repository",
    )
    parser.add_argument(
        "--no-archive",
        action="store_true",
        help="Run without durable local assessment persistence",
    )
    args = parser.parse_args(argv)

    archive = None if args.no_archive else SQLiteClinicalArchive(args.archive)
    ai_runner = _configured_ai_runner()
    app = AlphaClinicianApp(None, archive=archive, ai_report_runner=ai_runner)
    server = make_local_clinician_server(app, host="127.0.0.1", port=args.port)
    ai_state = "AI clinic configurat" if ai_runner is not None else "AI clinic neconfigurat"
    print(
        f"Szondi3 Alpha: http://127.0.0.1:{server.server_port}/ "
        f"({ai_state})"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if archive is not None:
            archive.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
