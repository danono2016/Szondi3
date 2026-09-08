"""Dependency-free local-first web shell for the clinician product surfaces.

The shell now supports the first complete local clinical loop:

new pseudonymous assessment -> visual source-defined administration -> deterministic
clinical run -> clinician workspace -> optional immutable local archive snapshot.

HTTP remains a presentation/orchestration boundary. Card recording, P1 calculation,
P2B activation, doctrine, provenance and report composition stay in their existing
authoritative modules.
"""

from __future__ import annotations

import argparse
from html import escape
import hmac
from io import BytesIO
from pathlib import Path
import secrets
from typing import Callable, Iterable
from urllib.parse import parse_qs, urlencode
from wsgiref.simple_server import WSGIServer, make_server

from .clinical_ai_preview import DEFAULT_PREVIEW_MODEL, PREVIEW_CONTRACT_VERSION
from .clinical_archive import SQLiteClinicalArchive
from .clinical_case_runner import ClinicalCaseRun, run_clinical_case_from_verified_checkout
from .clinical_integration import ClinicianContextItem
from .clinician_assessment_session import (
    AssessmentAdministrationSession,
    require_pseudonymous_assessment_id,
    start_assessment_administration,
)
from .clinician_current_case_view import build_current_case_view, render_current_case_view_html
from .clinician_finding_drilldown import build_finding_drilldown, render_finding_drilldown_html
from .clinician_input_editor import (
    apply_clinician_input_editor,
    build_clinician_input_editor,
    render_clinician_input_editor_fragment,
    update_clinician_input_editor,
)
from .clinician_longitudinal_panel import (
    build_clinician_longitudinal_panel,
    render_clinician_longitudinal_panel_html,
)
from .clinician_working_report_renderer import render_clinician_working_report_html
from .clinician_workspace import ClinicianWorkspace, build_clinician_workspace
from .longitudinal_comparison import LongitudinalCaseRef
from .stimuli import catalog


_LOOPBACK_HOSTS = {"127.0.0.1", "localhost", "::1"}
_MAX_FORM_BYTES = 64 * 1024
_MAX_CONTEXT_ITEMS = 32
_REPO_ROOT = Path(__file__).resolve().parents[1]
_STIMULUS_ROUTE_TO_FILE = {
    f"/stimulus/{card.card_id}.webp": _REPO_ROOT / card.image_path
    for card in catalog()
}
_SECURITY_HEADERS = (
    ("Cache-Control", "no-store"),
    ("X-Content-Type-Options", "nosniff"),
    ("Referrer-Policy", "no-referrer"),
    ("X-Frame-Options", "DENY"),
    (
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'",
    ),
)


def _page(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title, quote=True)}</title><style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width:1100px; margin:0 auto; padding:1.5rem; color:#1f2328; line-height:1.45; }}
a {{ color:inherit; }} nav {{ margin-bottom:1.25rem; }} nav a {{ margin-right:1rem; }}
.card {{ border:1px solid #d0d7de; border-radius:.5rem; padding:.8rem 1rem; margin:.7rem 0; }}
.meta, .boundary {{ color:#57606a; font-size:.88rem; }} code {{ word-break:break-all; }}
button, input, select, textarea {{ font:inherit; }} button {{ padding:.55rem .9rem; cursor:pointer; }}
.notice {{ border-left:4px solid #57606a; background:#f6f8fa; padding:.7rem 1rem; margin:1rem 0; }}
.error {{ border-left-color:#cf222e; background:#fff1f0; }} .saved {{ border-left-color:#1a7f37; background:#dafbe1; }}
fieldset {{ margin:1rem 0; border:1px solid #d0d7de; }} label {{ display:block; font-weight:650; margin:.6rem 0; }}
textarea {{ display:block; width:100%; box-sizing:border-box; margin-top:.3rem; padding:.55rem; resize:vertical; }}
.context-item input[type="text"], .context-item input:not([type]) {{ display:block; width:100%; box-sizing:border-box; margin-top:.3rem; padding:.55rem; }}
.remove input {{ display:inline-block; width:auto; margin-right:.35rem; }} .empty {{ color:#57606a; font-style:italic; }}
</style></head><body>{body}</body></html>"""


def _navigation(has_workspace: bool) -> str:
    links = ['<a href="/">Acasă</a>', '<a href="/new">Evaluare nouă</a>']
    if has_workspace:
        links.extend(
            [
                '<a href="/current">Profil</a>',
                '<a href="/findings">Interpretare</a>',
                '<a href="/longitudinal">Longitudinal</a>',
                '<a href="/integration">Integrare</a>',
                '<a href="/report">Raport</a>',
            ]
        )
    links.append('<a href="/archive">Arhivă</a>')
    return "<nav>" + "".join(links) + "</nav>"


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
        _navigation(True)
        + '<h1>Constatări Szondiene autorizate</h1>'
        + '<p class="meta">Afirmația este primară; identitățile tehnice și sursa sunt accesibile prin „De ce apare?”.</p>'
        + content,
    )


def _archive_page(archive: SQLiteClinicalArchive | None, *, has_workspace: bool) -> str:
    if archive is None:
        content = (
            '<p class="meta">Arhiva durabilă nu este configurată pentru această sesiune. '
            'Evaluările finalizate rămân numai în memoria procesului.</p>'
        )
    else:
        rows = "".join(
            '<article class="card">'
            f'<strong>{escape(item.assessment_id)}</strong>'
            f'<p class="meta">Git <code>{escape(item.git_commit_sha)}</code><br>'
            f'Doctrină <code>{escape(item.doctrine_snapshot_id)}</code><br>'
            f'P2B <code>{escape(item.p2b_release_id)}</code></p>'
            '<p class="meta">Snapshot istoric imuabil. Textul manual al clinicianului nu este persistat de acest store necriptat.</p>'
            "</article>"
            for item in archive.list()
        )
        content = rows or '<p class="meta">Arhiva este goală.</p>'
    return _page(
        "Szondi3 — arhivă",
        _navigation(has_workspace) + "<h1>Arhivă locală pseudonimizată</h1>" + content,
    )


def _parse_form(environ: dict) -> dict[str, list[str]]:
    content_type = environ.get("CONTENT_TYPE", "").split(";", 1)[0].strip().lower()
    if content_type != "application/x-www-form-urlencoded":
        raise ValueError("Formularul trebuie trimis ca application/x-www-form-urlencoded")
    raw_length = environ.get("CONTENT_LENGTH", "")
    try:
        length = int(raw_length)
    except (TypeError, ValueError) as exc:
        raise ValueError("CONTENT_LENGTH invalid") from exc
    if not 0 <= length <= _MAX_FORM_BYTES:
        raise ValueError("Formular prea mare")
    stream = environ.get("wsgi.input")
    if stream is None or not hasattr(stream, "read"):
        raise ValueError("Lipsește corpul formularului")
    raw = stream.read(length)
    if len(raw) != length:
        raise ValueError("Corpul formularului este incomplet")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("Formularul nu este UTF-8 valid") from exc
    return parse_qs(text, keep_blank_values=True)


def _single_form_value(
    form: dict[str, list[str]],
    name: str,
    *,
    default: str | None = None,
) -> str:
    values = form.get(name)
    if values is None:
        if default is None:
            raise ValueError(f"Lipsește câmpul formularului: {name}")
        return default
    if len(values) != 1:
        raise ValueError(f"Câmpul {name} trebuie trimis o singură dată")
    return values[0]


def _redirect(location: str) -> tuple[str, str, tuple[tuple[str, str], ...]]:
    return (
        "303 See Other",
        _page("Redirecționare", f'<p><a href="{escape(location, quote=True)}">Continuă</a></p>'),
        (("Location", location),),
    )


class ClinicianApp:
    """Local WSGI clinician application with explicit in-memory mutation boundaries."""

    def __init__(
        self,
        workspace: ClinicianWorkspace | None = None,
        *,
        archive: SQLiteClinicalArchive | None = None,
    ) -> None:
        if workspace is not None and not isinstance(workspace, ClinicianWorkspace):
            raise TypeError("workspace must be a ClinicianWorkspace or None")
        if archive is not None and not isinstance(archive, SQLiteClinicalArchive):
            raise TypeError("archive must be a SQLiteClinicalArchive or None")
        self.workspace = workspace
        self.archive = archive
        self._draft: AssessmentAdministrationSession | None = None
        self._csrf_token = secrets.token_urlsafe(32)
        self._live_runs: dict[str, ClinicalCaseRun] = {}
        if workspace is not None:
            for item in workspace.history + (workspace.current,):
                self._live_runs[item.case_id] = item.run

    @property
    def csrf_token(self) -> str:
        """Expose the per-process form token for deterministic shell tests/clients."""
        return self._csrf_token

    @property
    def draft(self) -> AssessmentAdministrationSession | None:
        return self._draft

    def _csrf_field(self) -> str:
        return f'<input type="hidden" name="_csrf" value="{escape(self._csrf_token, quote=True)}">'

    def _require_csrf(self, form: dict[str, list[str]]) -> None:
        supplied = form.get("_csrf", [""])[0]
        if not hmac.compare_digest(supplied, self._csrf_token):
            raise PermissionError("Token CSRF invalid")

    def _workspace_required(self) -> ClinicianWorkspace:
        if self.workspace is None:
            raise LookupError("Nu există încă o evaluare clinică finalizată")
        return self.workspace

    def _home_page(self) -> str:
        if self.workspace is None:
            state = (
                '<h1>Szondi3</h1><p>Nu există o evaluare curentă.</p>'
                '<p><a href="/new"><strong>Începe o evaluare nouă</strong></a></p>'
            )
        else:
            state = (
                f"<h1>Szondi3</h1><p><strong>Caz curent:</strong> {escape(self.workspace.current.case_id)}</p>"
                '<p><a href="/current"><strong>Deschide profilul curent</strong></a></p>'
            )
        if self._draft is not None:
            state += (
                '<div class="notice"><strong>Administrare în curs:</strong> '
                f'{escape(self._draft.assessment_id)} · '
                f'{self._draft.completed_profile_count}/{self._draft.target_profile_count} profiluri închise. '
                '<a href="/admin">Continuă administrarea</a></div>'
            )
        return _page(
            "Szondi3",
            _navigation(self.workspace is not None)
            + state
            + '<p class="meta">Instrument clinic local; shell-ul nu recalculează și nu reinterpretă ieșirile motorului Szondi3.</p>',
        )

    def _new_assessment_page(self) -> str:
        if self._draft is not None:
            return _page(
                "Szondi3 — administrare în curs",
                _navigation(self.workspace is not None)
                + '<h1>Există deja o administrare în curs</h1>'
                + f'<p><strong>{escape(self._draft.assessment_id)}</strong></p>'
                + '<p><a href="/admin">Continuă administrarea</a></p>'
                + '<form method="post" action="/assessment/cancel">'
                + self._csrf_field()
                + '<button type="submit">Anulează administrarea curentă</button></form>',
            )

        prior = ""
        if self._live_runs:
            prior = '<fieldset><legend>Comparație longitudinală opțională</legend><p class="meta">Sunt disponibile numai evaluările încărcate în sesiunea locală curentă; arhiva istorică nu este rerulată automat.</p>'
            for case_id in self._live_runs:
                prior += (
                    '<label style="display:block;margin:.35rem 0">'
                    f'<input type="checkbox" name="prior_case_id" value="{escape(case_id, quote=True)}"> '
                    f'{escape(case_id)}</label>'
                )
            prior += "</fieldset>"

        persistence = (
            "La final, protocolul și snapshot-ul raportului vor fi salvate automat în arhiva locală pseudonimizată."
            if self.archive is not None
            else "Arhiva durabilă nu este configurată; evaluarea finalizată va rămâne numai în memoria procesului."
        )
        return _page(
            "Szondi3 — evaluare nouă",
            _navigation(self.workspace is not None)
            + '<h1>Evaluare nouă</h1>'
            + '<div class="notice"><strong>Identitate pseudonimizată.</strong> Nu introduce numele pacientului, CNP, e-mail sau alte date direct identificabile în ID-ul evaluării.</div>'
            + '<form method="post" action="/assessment/start">'
            + self._csrf_field()
            + '<p><label>ID evaluare <input required maxlength="80" name="assessment_id" pattern="[A-Za-z0-9][A-Za-z0-9._-]{0,79}" placeholder="CASE-2026-001"></label></p>'
            + '<p><label>Număr de profiluri <input required type="number" name="profile_count" min="1" max="10" value="10"></label></p>'
            + '<p><label><input type="checkbox" name="include_complement" value="1"> Administrează și E.K.P. pentru fiecare profil</label></p>'
            + prior
            + f'<p class="meta">{escape(persistence)}</p>'
            + '<button type="submit">Începe administrarea</button></form>',
        )

    def _admin_page(self) -> str:
        if self._draft is None:
            return _page(
                "Szondi3 — fără administrare",
                _navigation(self.workspace is not None)
                + '<h1>Nu există o administrare în curs</h1><p><a href="/new">Începe o evaluare nouă</a></p>',
            )
        draft = self._draft
        if draft.is_complete:
            return _page(
                "Szondi3 — administrare completă",
                _navigation(self.workspace is not None)
                + f'<h1>Administrare completă — {escape(draft.assessment_id)}</h1>'
                + '<p>Toate alegerile canonice au fost înregistrate. Finalizarea clinică nu a fost încă închisă.</p>'
                + '<form method="post" action="/assessment/finalize">'
                + self._csrf_field()
                + '<button type="submit">Calculează și deschide workspace-ul</button></form>',
            )

        step = draft.current_step
        progress = draft.workflow.progress
        phase_label = "Prim-plan (V.G.P.)" if step.phase == "FOREGROUND" else "Complement experimental (E.K.P.)"
        card_blocks: list[str] = []
        if step.phase == "FOREGROUND":
            rows = step.presentation_rows or ()
            for row in rows:
                cards = "".join(
                    '<label class="stimulus">'
                    f'<span class="position">{card.position}</span>'
                    f'<img src="/stimulus/{escape(card.card_id, quote=True)}.webp" alt="Cartela {card.position}">'
                    f'<select name="choice_{escape(card.card_id, quote=True)}" aria-label="Alegere cartela {card.position}">'
                    '<option value="">—</option><option value="sympathetic">simpatică</option><option value="unsympathetic">antipatică</option>'
                    '</select></label>'
                    for card in row
                )
                card_blocks.append(f'<div class="stimulus-row">{cards}</div>')
            instruction = "Marchează exact două cartele ca simpatice și exact două ca antipatice. Celelalte patru rămân nealese."
        else:
            cards = "".join(
                '<label class="stimulus">'
                f'<span class="position">{card.position}</span>'
                f'<img src="/stimulus/{escape(card.card_id, quote=True)}.webp" alt="Cartela {card.position}">'
                f'<span><input type="checkbox" name="selected" value="{escape(card.card_id, quote=True)}"> selectată</span>'
                '</label>'
                for card in step.cards
            )
            card_blocks.append(f'<div class="stimulus-row complement">{cards}</div>')
            instruction = "Alege exact două dintre cele patru cartele rămase și indică sensul selecției relative."

        complement_direction = ""
        if step.phase == "COMPLEMENT":
            complement_direction = (
                '<p><label>Sensul celor două selectate <select name="selected_as">'
                '<option value="unsympathetic">relativ mai antipatice</option>'
                '<option value="sympathetic">relativ mai simpatice</option>'
                '</select></label></p>'
            )

        return _page(
            f"Szondi3 — administrare {draft.assessment_id}",
            _navigation(self.workspace is not None)
            + f'<h1>Administrare — {escape(draft.assessment_id)}</h1>'
            + f'<p><strong>Profil {draft.current_profile_number}/{draft.target_profile_count}</strong> · {escape(phase_label)} · seria {escape(step.series)}</p>'
            + f'<p class="meta">Pas {progress.completed_steps + 1}/{progress.total_steps} în profilul curent.</p>'
            + f'<div class="notice">{escape(instruction)}</div>'
            + '<style>.stimulus-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1rem;margin:1rem 0}.stimulus{display:flex;flex-direction:column;gap:.45rem;border:1px solid #d0d7de;border-radius:.5rem;padding:.5rem}.stimulus img{width:100%;height:auto;aspect-ratio:3/4;object-fit:cover;background:#f6f8fa}.position{font-weight:700}.stimulus select{width:100%}@media(max-width:700px){.stimulus-row{grid-template-columns:repeat(2,minmax(0,1fr))}}</style>'
            + '<form method="post" action="/admin/submit">'
            + self._csrf_field()
            + "".join(card_blocks)
            + complement_direction
            + '<button type="submit">Înregistrează seria și continuă</button></form>',
        )

    def _integration_page(self, workspace: ClinicianWorkspace, *, saved: bool = False) -> str:
        persistence_notice = (
            "Arhiva SQLite păstrează snapshot-ul clinic inițial fără textul manual al clinicianului. Modificările de aici rămân numai în memoria procesului și nu rescriu snapshot-ul istoric."
            if self.archive is not None
            else "Nu este configurată o arhivă durabilă; textul manual rămâne numai în memoria procesului curent."
        )
        fragment = render_clinician_input_editor_fragment(
            build_clinician_input_editor(workspace),
            form_action="/integration/update",
            csrf_token=self._csrf_token,
            saved=saved,
            persistence_notice=persistence_notice,
        )
        return _page(
            "Szondi3 — integrare clinică manuală",
            _navigation(True) + fragment,
        )

    def _resolve(self, path: str, query_string: str) -> tuple[str, str]:
        if path == "/":
            return "200 OK", self._home_page()
        if path == "/new":
            return "200 OK", self._new_assessment_page()
        if path == "/admin":
            return "200 OK", self._admin_page()
        if path == "/archive":
            return "200 OK", _archive_page(self.archive, has_workspace=self.workspace is not None)

        try:
            workspace = self._workspace_required()
        except LookupError as exc:
            return "409 Conflict", _page(
                "Szondi3 — evaluare necesară",
                _navigation(False) + f'<h1>Evaluare necesară</h1><p>{escape(str(exc))}</p><p><a href="/new">Începe o evaluare</a></p>',
            )

        if path == "/current":
            return "200 OK", render_current_case_view_html(build_current_case_view(workspace))
        if path == "/findings":
            return "200 OK", _finding_list(workspace)
        if path == "/longitudinal":
            return "200 OK", render_clinician_longitudinal_panel_html(
                build_clinician_longitudinal_panel(workspace)
            )
        if path == "/integration":
            query = parse_qs(query_string, keep_blank_values=True)
            saved = query.get("saved", [""])[0] == "1"
            return "200 OK", self._integration_page(workspace, saved=saved)
        if path == "/report":
            return "200 OK", render_clinician_working_report_html(workspace.report)
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
                    workspace,
                    claim_id=claim_id,
                    scope=scope,
                    profile_number=profile_number,
                )
            except (KeyError, TypeError, ValueError) as exc:
                return "404 Not Found", _page("Constatare indisponibilă", f"<h1>Constatare indisponibilă</h1><p>{escape(str(exc))}</p>")
            return "200 OK", render_finding_drilldown_html(drilldown)
        return "404 Not Found", _page("Nu există", "<h1>404</h1>")

    def _existing_assessment_ids(self) -> set[str]:
        ids = set(self._live_runs)
        if self.archive is not None:
            ids.update(item.assessment_id for item in self.archive.list())
        return ids

    def _start_assessment(self, form: dict[str, list[str]]) -> tuple[str, str, tuple[tuple[str, str], ...]]:
        if self._draft is not None:
            return "409 Conflict", self._new_assessment_page(), ()
        assessment_id = require_pseudonymous_assessment_id(form.get("assessment_id", [""])[0])
        if assessment_id in self._existing_assessment_ids():
            raise ValueError(f"assessment_id există deja și nu poate fi suprascris: {assessment_id}")
        try:
            profile_count = int(form.get("profile_count", [""])[0])
        except ValueError as exc:
            raise ValueError("profile_count invalid") from exc
        include_complement = form.get("include_complement", [""])[0] == "1"
        prior_case_ids = tuple(form.get("prior_case_id", []))
        missing = tuple(case_id for case_id in prior_case_ids if case_id not in self._live_runs)
        if missing:
            raise ValueError(f"Evaluări longitudinale indisponibile în sesiunea curentă: {', '.join(missing)}")
        self._draft = start_assessment_administration(
            assessment_id=assessment_id,
            target_profile_count=profile_count,
            include_complement=include_complement,
            prior_case_ids=prior_case_ids,
        )
        return _redirect("/admin")

    def _submit_admin(self, form: dict[str, list[str]]) -> tuple[str, str, tuple[tuple[str, str], ...]]:
        if self._draft is None:
            raise RuntimeError("Nu există o administrare în curs")
        draft = self._draft
        if draft.is_complete or draft.current_step is None or draft.workflow is None:
            raise RuntimeError("Administrarea este deja completă")
        step = draft.current_step
        if step.phase == "FOREGROUND":
            sympathetic: list[str] = []
            unsympathetic: list[str] = []
            for card_id in step.card_ids:
                value = form.get(f"choice_{card_id}", [""])[0]
                if value == "sympathetic":
                    sympathetic.append(card_id)
                elif value == "unsympathetic":
                    unsympathetic.append(card_id)
                elif value != "":
                    raise ValueError(f"Alegere invalidă pentru {card_id}")
            updated = draft.submit_foreground(
                sympathetic=sympathetic,
                unsympathetic=unsympathetic,
            )
        else:
            selected = tuple(form.get("selected", []))
            selected_as = form.get("selected_as", [""])[0]
            updated = draft.submit_complement(
                selected=selected,
                selected_as=selected_as,
            )
        self._draft = updated
        if updated.is_complete:
            return self._finalize_assessment()
        return _redirect("/admin")

    def _finalize_assessment(self) -> tuple[str, str, tuple[tuple[str, str], ...]]:
        if self._draft is None or not self._draft.is_complete:
            raise RuntimeError("Administrarea trebuie închisă înainte de calcul")
        draft = self._draft
        records = draft.records()
        run = run_clinical_case_from_verified_checkout(
            records,
            synthesis_contract_version=PREVIEW_CONTRACT_VERSION,
            synthesis_model=DEFAULT_PREVIEW_MODEL,
        )
        prior_refs = tuple(
            LongitudinalCaseRef(case_id=case_id, run=self._live_runs[case_id])
            for case_id in draft.prior_case_ids
        )
        workspace = build_clinician_workspace(
            LongitudinalCaseRef(case_id=draft.assessment_id, run=run),
            prior_cases=prior_refs,
        )
        if self.archive is not None:
            self.archive.save(
                assessment_id=draft.assessment_id,
                records=records,
                workspace=workspace,
            )
        self._live_runs[draft.assessment_id] = run
        self.workspace = workspace
        self._draft = None
        return _redirect("/current")

    def _update_integration(self, form: dict[str, list[str]]) -> tuple[str, str, tuple[tuple[str, str], ...]]:
        workspace = self._workspace_required()
        before = build_clinician_input_editor(workspace)
        if len(before.clinician_context) > _MAX_CONTEXT_ITEMS:
            raise ValueError("Prea multe elemente de context pentru editorul browser")

        context: list[ClinicianContextItem] = []
        for index, item in enumerate(before.clinician_context, start=1):
            remove = _single_form_value(form, f"remove_context_{index}", default="")
            if remove not in {"", "1"}:
                raise ValueError(f"Valoare invalidă pentru remove_context_{index}")
            if remove == "1":
                continue
            label = _single_form_value(form, f"context_label_{index}")
            text = _single_form_value(form, f"context_text_{index}")
            if len(label) > 160 or len(text) > 16000:
                raise ValueError("Un element de context depășește limita editorului")
            context.append(ClinicianContextItem(label=label, text=text))

        new_label = _single_form_value(form, "new_context_label", default="")
        new_text = _single_form_value(form, "new_context_text", default="")
        if bool(new_label.strip()) != bool(new_text.strip()):
            raise ValueError("Pentru un context nou sunt necesare atât eticheta, cât și textul")
        if new_label.strip():
            if len(context) >= _MAX_CONTEXT_ITEMS:
                raise ValueError("Numărul maxim de elemente de context a fost atins")
            if len(new_label) > 160 or len(new_text) > 16000:
                raise ValueError("Noul element de context depășește limita editorului")
            context.append(ClinicianContextItem(label=new_label, text=new_text))

        synthesis = _single_form_value(form, "clinician_synthesis", default="")
        if len(synthesis) > 32000:
            raise ValueError("Sinteza clinicianului depășește limita editorului")
        state = update_clinician_input_editor(
            before,
            clinician_context=tuple(context),
            clinician_synthesis=synthesis if synthesis.strip() else None,
            clear_synthesis=not synthesis.strip(),
        )
        updated = apply_clinician_input_editor(workspace, state)

        if updated.current.run is not workspace.current.run:
            raise ValueError("Editarea integrării a schimbat runtime-ul cazului curent")
        if updated.report.findings != workspace.report.findings:
            raise ValueError("Editarea integrării a schimbat constatările Szondi")
        if updated.report.provenance != workspace.report.provenance:
            raise ValueError("Editarea integrării a schimbat proveniența doctrinară")
        if updated.report.release != workspace.report.release:
            raise ValueError("Editarea integrării a schimbat manifestul de release")

        self.workspace = updated
        return _redirect("/integration?saved=1")

    def _handle_post(self, path: str, environ: dict) -> tuple[str, str, tuple[tuple[str, str], ...]]:
        allowed = {
            "/assessment/start",
            "/assessment/cancel",
            "/assessment/finalize",
            "/admin/submit",
            "/integration/update",
        }
        if path not in allowed:
            return (
                "405 Method Not Allowed",
                _page(
                    "Metodă indisponibilă",
                    "<h1>405</h1><p>Shell-ul acceptă POST numai pentru mutații explicite de administrare sau integrare clinică manuală.</p>",
                ),
                (),
            )
        try:
            form = _parse_form(environ)
            self._require_csrf(form)
            if path == "/assessment/start":
                return self._start_assessment(form)
            if path == "/assessment/cancel":
                self._draft = None
                return _redirect("/new")
            if path == "/assessment/finalize":
                return self._finalize_assessment()
            if path == "/integration/update":
                return self._update_integration(form)
            return self._submit_admin(form)
        except PermissionError as exc:
            return "403 Forbidden", _page("Cerere refuzată", f'<h1>403</h1><p>{escape(str(exc))}</p>'), ()
        except LookupError as exc:
            return (
                "409 Conflict",
                _page(
                    "Evaluare necesară",
                    _navigation(False) + f'<h1>Evaluare necesară</h1><div class="notice error">{escape(str(exc))}</div><p><a href="/new">Începe o evaluare</a></p>',
                ),
                (),
            )
        except (KeyError, TypeError, ValueError, RuntimeError) as exc:
            if path == "/integration/update" and self.workspace is not None:
                back = '<p><a href="/integration">Înapoi la integrarea clinică</a></p>'
                title = "Date de integrare invalide"
            elif self._draft is not None:
                back = '<p><a href="/admin">Înapoi la administrare</a></p>'
                title = "Date de administrare invalide"
            else:
                back = '<p><a href="/new">Înapoi</a></p>'
                title = "Date invalide"
            return (
                "400 Bad Request",
                _page(
                    title,
                    _navigation(self.workspace is not None)
                    + f'<h1>Date invalide</h1><div class="notice error">{escape(str(exc))}</div>'
                    + back,
                ),
                (),
            )

    def _send(
        self,
        start_response: Callable,
        status: str,
        payload: bytes,
        *,
        content_type: str,
        extra_headers: tuple[tuple[str, str], ...] = (),
    ) -> Iterable[bytes]:
        start_response(
            status,
            [
                ("Content-Type", content_type),
                ("Content-Length", str(len(payload))),
                *_SECURITY_HEADERS,
                *extra_headers,
            ],
        )
        return [payload]

    def __call__(self, environ: dict, start_response: Callable) -> Iterable[bytes]:
        method = environ.get("REQUEST_METHOD", "GET").upper()
        path = environ.get("PATH_INFO", "/")

        if method == "GET" and path in _STIMULUS_ROUTE_TO_FILE:
            asset = _STIMULUS_ROUTE_TO_FILE[path]
            try:
                payload = asset.read_bytes()
            except OSError:
                html = _page("Stimulus indisponibil", "<h1>404</h1><p>Fișierul stimulus nu este disponibil.</p>")
                return self._send(
                    start_response,
                    "404 Not Found",
                    html.encode("utf-8"),
                    content_type="text/html; charset=utf-8",
                )
            return self._send(
                start_response,
                "200 OK",
                payload,
                content_type="image/webp",
            )

        if method == "GET":
            status, html = self._resolve(path, environ.get("QUERY_STRING", ""))
            extra_headers: tuple[tuple[str, str], ...] = ()
        elif method == "POST":
            status, html, extra_headers = self._handle_post(path, environ)
        else:
            status, html, extra_headers = (
                "405 Method Not Allowed",
                _page("Metodă indisponibilă", "<h1>405</h1>"),
                (),
            )
        return self._send(
            start_response,
            status,
            html.encode("utf-8"),
            content_type="text/html; charset=utf-8",
            extra_headers=extra_headers,
        )


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


def main(argv: list[str] | None = None) -> int:
    """Launch the local clinician app from a clean Szondi3 checkout."""
    parser = argparse.ArgumentParser(description="Szondi3 local clinician application")
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
    app = ClinicianApp(None, archive=archive)
    server = make_local_clinician_server(app, host="127.0.0.1", port=args.port)
    print(f"Szondi3 clinician app: http://127.0.0.1:{server.server_port}/")
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