"""Dependency-free local-first web shell for the clinician product surfaces.

The first app shell intentionally uses Python's WSGI standard library and binds only
to loopback. It composes already-existing clinician projections/renderers and adds no
clinical meaning. The shell is replaceable; the epistemic core remains independent of
web technology.
"""

from __future__ import annotations

from html import escape
from typing import Callable, Iterable
from urllib.parse import parse_qs, urlencode
from wsgiref.simple_server import WSGIServer, make_server

from .clinical_archive import SQLiteClinicalArchive
from .clinician_current_case_view import build_current_case_view, render_current_case_view_html
from .clinician_finding_drilldown import build_finding_drilldown, render_finding_drilldown_html
from .clinician_input_editor import build_clinician_input_editor, render_clinician_input_editor_html
from .clinician_longitudinal_panel import (
    build_clinician_longitudinal_panel,
    render_clinician_longitudinal_panel_html,
)
from .clinician_working_report_renderer import render_clinician_working_report_html
from .clinician_workspace import ClinicianWorkspace


_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}


def _page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title, quote=True)}</title><style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width:1000px; margin:0 auto; padding:1.5rem; color:#1f2328; line-height:1.45; }}
a {{ color:inherit; }} nav a {{ margin-right:1rem; }} .card {{ border:1px solid #d0d7de; border-radius:.5rem; padding:.8rem 1rem; margin:.7rem 0; }}
.meta {{ color:#57606a; font-size:.88rem; }} code {{ word-break:break-all; }}
</style></head><body>{body}</body></html>"""


def _navigation() -> str:
    return (
        '<nav><a href="/current">Profil</a><a href="/findings">Interpretare</a>'
        '<a href="/longitudinal">Longitudinal</a><a href="/integration">Integrare</a>'
        '<a href="/report">Raport</a><a href="/archive">Arhivă</a></nav>'
    )


def _finding_list(workspace: ClinicianWorkspace) -> str:
    items = []
    for finding in workspace.report.findings:
        query = urlencode(
            {
                "claim_id": finding.claim_id,
                "scope": finding.scope,
                "profile_number": "" if finding.profile_number is None else finding.profile_number,
            }
        )
        location = finding.scope + (
            f" {finding.profile_number}" if finding.profile_number is not None else ""
        )
        anti = (
            f'<p class="meta">Anti-inferențe: {len(finding.anti_inferences)}</p>'
            if finding.anti_inferences
            else ""
        )
        items.append(
            '<article class="card">'
            f'<p class="meta">{escape(location)} · {escape(finding.assertion_mode)} · {escape(finding.source_strength_note)}</p>'
            f'<p>{escape(finding.statement)}</p>{anti}'
            f'<a href="/finding?{escape(query, quote=True)}">De ce apare?</a>'
            "</article>"
        )
    content = "".join(items) or '<p class="meta">Nicio constatare activă.</p>'
    return _page(
        "Szondi3 — interpretare",
        _navigation()
        + '<h1>Constatări Szondiene autorizate</h1>'
        + '<p class="meta">Afirmația este primară; identitățile tehnice și sursa sunt accesibile prin „De ce apare?”.</p>'
        + content,
    )


def _archive_page(archive: SQLiteClinicalArchive | None) -> str:
    if archive is None:
        content = (
            '<p class="meta">Arhiva durabilă nu este configurată pentru această sesiune. '
            'App shell-ul poate funcționa complet în memorie.</p>'
        )
    else:
        rows = "".join(
            '<article class="card">'
            f'<strong>{escape(item.assessment_id)}</strong>'
            f'<p class="meta">Git <code>{escape(item.git_commit_sha)}</code><br>'
            f'Doctrină <code>{escape(item.doctrine_snapshot_id)}</code><br>'
            f'P2B <code>{escape(item.p2b_release_id)}</code></p>'
            '<p class="meta">Textul manual al clinicianului nu este persistat de acest store necriptat.</p>'
            "</article>"
            for item in archive.list()
        )
        content = rows or '<p class="meta">Arhiva este goală.</p>'
    return _page("Szondi3 — arhivă", _navigation() + "<h1>Arhivă locală pseudonimizată</h1>" + content)


class ClinicianApp:
    """Read-oriented WSGI composition shell over one live clinician workspace."""

    def __init__(
        self,
        workspace: ClinicianWorkspace,
        *,
        archive: SQLiteClinicalArchive | None = None,
    ) -> None:
        if not isinstance(workspace, ClinicianWorkspace):
            raise TypeError("ClinicianApp requires a ClinicianWorkspace")
        if archive is not None and not isinstance(archive, SQLiteClinicalArchive):
            raise TypeError("archive must be a SQLiteClinicalArchive or None")
        self.workspace = workspace
        self.archive = archive

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        if path == "/":
            return "200 OK", _page(
                "Szondi3",
                _navigation()
                + f"<h1>Szondi3</h1><p><strong>Caz curent:</strong> {escape(self.workspace.current.case_id)}</p>"
                + '<p class="meta">Instrument clinic local; motorul determinist și proveniența rămân separate de shell-ul web.</p>',
            )
        if path == "/current":
            return "200 OK", render_current_case_view_html(build_current_case_view(self.workspace))
        if path == "/findings":
            return "200 OK", _finding_list(self.workspace)
        if path == "/longitudinal":
            return "200 OK", render_clinician_longitudinal_panel_html(
                build_clinician_longitudinal_panel(self.workspace)
            )
        if path == "/integration":
            return "200 OK", render_clinician_input_editor_html(
                build_clinician_input_editor(self.workspace)
            )
        if path == "/report":
            return "200 OK", render_clinician_working_report_html(self.workspace.report)
        if path == "/archive":
            return "200 OK", _archive_page(self.archive)
        if path == "/finding":
            query = parse_qs(query_string, keep_blank_values=True)
            claim_id = query.get("claim_id", [""])[0]
            scope = query.get("scope", [""])[0]
            raw_profile = query.get("profile_number", [""])[0]
            profile_number = None
            if raw_profile:
                try:
                    profile_number = int(raw_profile)
                except ValueError:
                    return "400 Bad Request", _page("Cerere invalidă", "<h1>profile_number invalid</h1>")
            try:
                drilldown = build_finding_drilldown(
                    self.workspace,
                    claim_id=claim_id,
                    scope=scope,
                    profile_number=profile_number,
                )
            except (KeyError, TypeError, ValueError) as exc:
                return "404 Not Found", _page("Constatare indisponibilă", f"<h1>Constatare indisponibilă</h1><p>{escape(str(exc))}</p>")
            return "200 OK", render_finding_drilldown_html(drilldown)
        return "404 Not Found", _page("Nu există", "<h1>404</h1>")

    def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:
        method = environ.get("REQUEST_METHOD", "GET").upper()
        if method != "GET":
            status, html = "405 Method Not Allowed", _page(
                "Metodă indisponibilă",
                "<h1>405</h1><p>Primul shell este read-oriented; mutațiile sunt încă gestionate explicit de contractele Python.</p>",
            )
        else:
            status, html = self._resolve(
                environ.get("PATH_INFO", "/"),
                environ.get("QUERY_STRING", ""),
            )
        payload = html.encode("utf-8")
        start_response(
            status,
            [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Content-Length", str(len(payload))),
                ("Cache-Control", "no-store"),
                ("X-Content-Type-Options", "nosniff"),
                ("Referrer-Policy", "no-referrer"),
            ],
        )
        return [payload]


def make_local_clinician_server(
    app: ClinicianApp,
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
) -> WSGIServer:
    """Create a loopback-only server; network exposure is deliberately refused."""
    if not isinstance(app, ClinicianApp):
        raise TypeError("app must be a ClinicianApp")
    if host not in _LOOPBACK_HOSTS:
        raise ValueError("First clinician app shell may bind only to loopback")
    if not isinstance(port, int) or isinstance(port, bool) or not 0 <= port <= 65535:
        raise ValueError("port must be an integer from 0 to 65535")
    return make_server(host, port, app)
