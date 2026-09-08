"""Alpha clinician shell with concise report and explicit AI formulation.

The existing archive-enabled application remains the authoritative administration,
calculation, integration and archive shell. This subclass changes only the current
report surface and adds one explicit, CSRF-protected AI formulation action.

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
    make_local_clinician_server,
)
from .clinician_archive_browser import ArchiveBrowsingClinicianApp
from .clinician_working_report_renderer import render_clinician_working_report_html
from .clinician_workspace import ClinicianWorkspace


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

    @property
    def ai_available(self) -> bool:
        return self._ai_report_runner is not None

    def _current_ai_result(self, workspace: ClinicianWorkspace) -> ClinicalReportAIResult | None:
        if self._ai_result_case_id != workspace.current.case_id:
            return None
        return self._ai_result

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        if path in {"/report", "/report/audit"}:
            try:
                workspace = self._workspace_required()
            except LookupError:
                return super()._resolve(path, query_string)
            if path == "/report/audit":
                return "200 OK", render_clinician_working_report_html(workspace.report)
            return (
                "200 OK",
                render_clinician_alpha_report_html(
                    workspace,
                    ai_result=self._current_ai_result(workspace),
                    ai_available=self.ai_available,
                    csrf_token=self.csrf_token if self.ai_available else None,
                    ai_error=self._ai_error,
                ),
            )
        return super()._resolve(path, query_string)

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
