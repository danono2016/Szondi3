"""Clinician-facing renderer for the global V4 narrative writer.

The clinical reading comes before the deterministic support appendix. V4 provenance
atoms remain invisible metadata; the clinician sees one report, not one card per
report-plan unit.
"""

from __future__ import annotations

from html import escape

from .clinical_report_ai_v4 import ClinicalReportAIV4Result
from .clinician_alpha_report_renderer import (
    _case_findings,
    _clinician_integration,
    _deterministic_findings,
    _e,
    _experimental_complement,
    _matrix,
)
from .clinician_workspace import ClinicianWorkspace


def _global_ai_narrative(result: ClinicalReportAIV4Result) -> str:
    summary = "".join(f"<p>{_e(item.text)}</p>" for item in result.summary)
    sections: list[str] = []
    for section in result.sections:
        passages = "".join(
            f'<p class="narrative-{escape(item.kind.lower())}">{_e(item.text)}</p>'
            for item in section.passages
        )
        sections.append(
            '<section class="narrative-section">'
            f'<h3>{_e(section.title)}</h3>{passages}</section>'
        )
    questions = "".join(f"<li>{_e(item.text)}</li>" for item in result.global_questions)
    limits = ""
    if result.closing_limits:
        limits = (
            '<section class="narrative-limits"><h3>Ce rămâne deschis</h3>'
            + "".join(f"<p>{_e(item.text)}</p>" for item in result.closing_limits)
            + "</section>"
        )
    return (
        '<section class="global-reading">'
        '<h2>Lectura clinică</h2>'
        '<div class="clinical-summary"><h3>Sinteză</h3>' + summary + "</div>"
        + "".join(sections)
        + '<section class="interview-questions"><h3>De explorat în interviu</h3><ul>'
        + questions
        + "</ul></section>"
        + limits
        + "</section>"
    )


def render_clinician_alpha_report_v4_html(
    workspace: ClinicianWorkspace,
    *,
    ai_result: ClinicalReportAIV4Result,
    ai_available: bool = False,
    csrf_token: str | None = None,
    ai_error: str | None = None,
) -> str:
    if not isinstance(workspace, ClinicianWorkspace):
        raise TypeError("V4 clinician report requires a ClinicianWorkspace")
    if not isinstance(ai_result, ClinicalReportAIV4Result):
        raise TypeError("V4 clinician report requires a ClinicalReportAIV4Result")
    if ai_available and (not isinstance(csrf_token, str) or not csrf_token):
        raise ValueError("AI-enabled V4 rendering requires a CSRF token")

    report = workspace.report
    case_findings = _case_findings(workspace)
    deterministic = _deterministic_findings(workspace)
    action = (
        '<form class="screen-only" method="post" action="/report/ai">'
        f'<input type="hidden" name="_csrf" value="{escape(csrf_token or "", quote=True)}">'
        '<button type="submit">Regenerează lectura clinică</button></form>'
        if ai_available else ""
    )
    error_html = (
        '<div class="error"><strong>Lectura AI nu a putut fi regenerată.</strong>'
        f'<span class="screen-only"> {_e(ai_error)}</span></div>'
        if ai_error else ""
    )
    unresolved = len(report.status.unresolved)
    blocked = len(report.status.blocked)
    status_note = ""
    if unresolved or blocked:
        status_note = (
            '<div class="warning"><strong>Atenție:</strong> există '
            f'{unresolved} stări nerezolvate și {blocked} stări blocate. '
            'Raportul nu le transformă în interpretări.</div>'
        )

    return f"""<!doctype html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Szondi3 — raport clinic — {_e(report.summary.current_case_id)}</title>
<style>
:root{{font-family:Georgia,"Times New Roman",serif;color:#1f2328;line-height:1.68}}
body{{max-width:900px;margin:0 auto;padding:2rem;background:#fff}}
nav{{font-family:system-ui,sans-serif;margin-bottom:2rem}}nav a{{margin-right:1rem;color:inherit}}
h1{{margin-bottom:.2rem}}h2{{border-bottom:1px solid #d8dee4;padding-bottom:.35rem;margin-top:2.4rem}}
h3{{margin-top:1.5rem;margin-bottom:.45rem}}.subtitle,.quiet,.location{{color:#57606a}}
.location{{font-family:system-ui,sans-serif;font-size:.82rem;text-transform:uppercase;letter-spacing:.04em}}
.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-family:system-ui,sans-serif}}
th,td{{border:1px solid #d0d7de;padding:.45rem;text-align:center}}th{{background:#f6f8fa}}
.meta-strip{{font-family:system-ui,sans-serif;display:flex;gap:1rem;flex-wrap:wrap;color:#57606a;font-size:.9rem;margin:1rem 0}}
.ai-boundary{{border-left:4px solid #8250df;background:#f6f3ff;padding:.7rem 1rem;margin:1rem 0}}
.warning,.error{{border-left:4px solid #cf222e;background:#fff1f0;padding:.7rem 1rem;margin:1rem 0}}
.global-reading{{font-size:1.04rem}}.clinical-summary{{font-size:1.08rem}}
.narrative-section{{margin:1.6rem 0}}.narrative-section p{{margin:.72rem 0}}
.narrative-example,.narrative-contrast,.narrative-bifurcation{{margin-left:1rem}}
.interview-questions li{{margin:.45rem 0}}
.narrative-limits{{border-left:4px solid #bf8700;background:#fff8c5;padding:.3rem 1rem 1rem;margin-top:1.4rem}}
.deterministic-appendix{{margin-top:3rem}}.deterministic-finding{{border-left:3px solid #57606a;padding:.25rem 0 .25rem 1rem;margin:1rem 0}}
.deterministic-finding p{{margin:.35rem 0}}.source-links{{font-family:system-ui,sans-serif;font-size:.85rem}}
.clinician-item{{border-left:3px solid #57606a;padding-left:.8rem;margin:.8rem 0}}
.actions{{display:flex;gap:.7rem;align-items:center;flex-wrap:wrap}}button{{font:inherit;padding:.55rem .9rem;cursor:pointer}}
@media print{{body{{max-width:none;padding:0}}nav,.screen-only{{display:none!important}}a{{text-decoration:none;color:inherit}}
.narrative-section,.deterministic-finding{{page-break-inside:avoid;break-inside:avoid}}}}
</style></head><body>
<nav class="screen-only"><a href="/">Acasă</a><a href="/current">Profil</a><a href="/findings">Interpretare</a><a href="/integration">Integrare</a><a href="/report">Raport</a><a href="/report/audit">Audit</a></nav>
<header><h1>Raport clinic de lucru</h1><p class="subtitle">Caz pseudonimizat: <strong>{_e(report.summary.current_case_id)}</strong></p>
<div class="meta-strip"><span>{report.summary.profile_count} profil(uri)</span><span>{len(case_findings)} sensuri active</span><span>{len(report.experimental_complement.evidence)} E.K.P.</span></div></header>
{status_note}
<section><h2>Profilul Szondi</h2>{_matrix(workspace)}</section>
<div class="ai-boundary"><strong>Lectură formulată cu AI.</strong> Narațiunea dezvoltă numai sensurile deja autorizate. Exemplele rămân ipotetice și trebuie confruntate cu materialul clinic.</div>
{error_html}<div class="actions">{action}</div>
{_global_ai_narrative(ai_result)}
{_experimental_complement(workspace)}
{_clinician_integration(workspace)}
<section class="deterministic-appendix"><h2>Anexă: baza interpretativă</h2><p class="quiet">Aici sunt păstrate sensurile deterministe și legăturile către justificarea lor. Ele preced redactarea AI și nu sunt create de aceasta.</p>{deterministic}</section>
<section class="screen-only"><h2>Surse și control</h2><p><a href="/findings">Deschide constatările și traseul „De ce apare?”</a></p><p><a href="/report/audit">Deschide raportul tehnic complet / auditul</a></p></section>
</body></html>"""


__all__ = ["render_clinician_alpha_report_v4_html"]
