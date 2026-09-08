"""Clinician-facing Alpha report surface.

Unlike the exhaustive working-report renderer, this projection deliberately keeps
technical provenance, inactive claims and release metadata out of the ordinary
clinical reading flow. Nothing is deleted from Szondi3: the exhaustive renderer
remains available as a separate audit surface.
"""

from __future__ import annotations

from html import escape
from urllib.parse import urlencode

from .clinical_report_ai import ClinicalReportAIResult
from .clinician_workspace import ClinicianWorkspace


def _e(value: object) -> str:
    return escape(str(value), quote=True)


def _case_findings(workspace: ClinicianWorkspace):
    return tuple(
        item for item in workspace.report.findings
        if item.assertion_mode != "LIMITATION"
    )


def _matrix(workspace: ClinicianWorkspace) -> str:
    rows: list[str] = []
    for profile in workspace.report.formal.observations:
        factor_by_name = {item.factor: item for item in profile.factors}
        vector_by_name = {item.vector: item for item in profile.vectors}
        factor_cells = "".join(
            f"<td><strong>{_e(factor_by_name[name].symbol)}</strong></td>"
            for name in ("h", "s", "e", "hy", "k", "p", "d", "m")
        )
        vector_cells = "".join(
            f"<td>{_e(' '.join(vector_by_name[name].symbols))}</td>"
            for name in ("S", "P", "Sch", "C")
        )
        rows.append(
            f"<tr><th>{profile.profile_number}</th>{factor_cells}{vector_cells}</tr>"
        )
    return (
        '<div class="table-wrap"><table class="matrix"><thead><tr>'
        '<th>Profil</th><th>h</th><th>s</th><th>e</th><th>hy</th>'
        '<th>k</th><th>p</th><th>d</th><th>m</th>'
        '<th>S</th><th>P</th><th>Sch</th><th>C</th>'
        '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"
    )


def _source_links(block) -> str:
    links: list[str] = []
    for index, claim_id in enumerate(block.support_claim_ids, start=1):
        query = urlencode(
            {
                "claim_id": claim_id,
                "scope": block.scope,
                "profile_number": "" if block.profile_number is None else block.profile_number,
            }
        )
        label = "Sursa și justificarea" if len(block.support_claim_ids) == 1 else f"Sursa și justificarea {index}"
        links.append(f'<a href="/finding?{escape(query, quote=True)}">{label}</a>')
    return '<p class="source-links screen-only">' + " · ".join(links) + "</p>"


def _ai_blocks(ai_result: ClinicalReportAIResult | None) -> str:
    if ai_result is None:
        return ""
    if not ai_result.blocks:
        return '<p class="quiet">Nu a fost autorizată nicio formulare clinică AI pentru datele curente.</p>'

    rendered: list[str] = []
    for block in ai_result.blocks:
        questions = "".join(f"<li>{_e(item)}</li>" for item in block.exploration_questions)
        limit = (
            '<div class="limit"><strong>Limită relevantă</strong><p>'
            + _e(block.relevant_limit)
            + "</p></div>"
            if block.relevant_limit
            else ""
        )
        location = (
            f"Profil {block.profile_number}"
            if block.scope == "PROFILE"
            else "Serie" if block.scope == "SERIES"
            else f"Complement experimental {block.profile_number}"
        )
        rendered.append(
            '<article class="interpretation">'
            f'<div class="location">{_e(location)}</div>'
            f'<h3>{_e(block.title)}</h3>'
            '<h4>În termenii lui Szondi</h4>'
            f'<p>{_e(block.szondi_reading)}</p>'
            '<h4>Formulare clinică</h4>'
            f'<p>{_e(block.clinical_formulation)}</p>'
            '<h4>De explorat clinic</h4>'
            f'<ul>{questions}</ul>'
            f'{limit}{_source_links(block)}'
            '</article>'
        )
    return "".join(rendered)


def _experimental_complement(workspace: ClinicianWorkspace) -> str:
    section = workspace.report.experimental_complement
    if not section.evidence:
        return ""
    blocks: list[str] = []
    for item in section.evidence:
        reactions = " · ".join(
            f"{factor} {symbol}" for factor, symbol in item.factor_symbols
        )
        blocks.append(
            f'<p><strong>E.K.P. {item.test_number}:</strong> {_e(reactions)}</p>'
        )
    return (
        '<section><h2>Complement experimental (E.K.P.)</h2>'
        + "".join(blocks)
        + '<p class="quiet">Complementul rămâne separat de seria de prim-plan. În această versiune Alpha, formularea clinică AI nu extinde automat interpretarea asupra E.K.P.; această separare previne amestecarea celor două niveluri.</p>'
        + '</section>'
    )


def _clinician_integration(workspace: ClinicianWorkspace) -> str:
    context = workspace.report.clinician_context
    synthesis = workspace.report.clinician_synthesis
    context_html = "".join(
        f'<article class="clinician-item"><strong>{_e(item.label)}</strong><p>{_e(item.text)}</p></article>'
        for item in context
    )
    synthesis_html = (
        f'<p>{_e(synthesis.text)}</p>'
        if synthesis.text
        else '<p class="quiet">Sinteza clinicianului nu a fost completată.</p>'
    )
    return (
        '<section><h2>Integrarea clinicianului</h2>'
        '<h3>Context clinic</h3>'
        + (context_html or '<p class="quiet">Nu a fost introdus context clinic extern.</p>')
        + '<h3>Sinteza clinicianului</h3>'
        + synthesis_html
        + '<p class="screen-only"><a href="/integration">Editează integrarea clinică</a></p>'
        + '</section>'
    )


def render_clinician_alpha_report_html(
    workspace: ClinicianWorkspace,
    *,
    ai_result: ClinicalReportAIResult | None = None,
    ai_available: bool = False,
    csrf_token: str | None = None,
    ai_error: str | None = None,
) -> str:
    """Render the concise clinical surface without exposing audit vocabulary."""
    if not isinstance(workspace, ClinicianWorkspace):
        raise TypeError("Alpha clinician report requires a ClinicianWorkspace")
    if ai_result is not None and not isinstance(ai_result, ClinicalReportAIResult):
        raise TypeError("ai_result must be a ClinicalReportAIResult or None")
    if ai_available and (not isinstance(csrf_token, str) or not csrf_token):
        raise ValueError("AI-enabled report rendering requires a CSRF token")

    report = workspace.report
    case_findings = _case_findings(workspace)
    ai_section = _ai_blocks(ai_result)

    if ai_result is None:
        if ai_available:
            action = (
                '<form class="screen-only" method="post" action="/report/ai">'
                f'<input type="hidden" name="_csrf" value="{escape(csrf_token or "", quote=True)}">'
                '<button type="submit">Generează formularea clinică AI</button>'
                '</form>'
            )
            ai_notice = (
                '<p class="quiet">Programul a identificat semnificațiile autorizate ale cazului. '
                'Formularea clinică AI se generează explicit, la cererea clinicianului.</p>'
            )
        else:
            action = ""
            ai_notice = (
                '<p class="quiet screen-only">Formularea clinică AI nu este configurată în această sesiune. '
                'Raportul determinist și sursele rămân disponibile.</p>'
            )
    else:
        action = (
            '<form class="screen-only" method="post" action="/report/ai">'
            f'<input type="hidden" name="_csrf" value="{escape(csrf_token or "", quote=True)}">'
            '<button type="submit">Regenerează formularea clinică AI</button>'
            '</form>'
            if ai_available else ""
        )
        ai_notice = (
            '<div class="ai-boundary"><strong>Formulare asistată de AI.</strong> '
            'Textul de mai jos organizează numai semnificații deja autorizate de motor și surse. '
            'Nu este verdict clinic și rămâne supus judecății clinicianului.</div>'
        )

    error_html = (
        f'<div class="error screen-only"><strong>Formularea AI nu a putut fi generată.</strong> {_e(ai_error)}</div>'
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
<title>Szondi3 — raport clinic Alpha — {_e(report.summary.current_case_id)}</title>
<style>
:root{{font-family:Georgia,"Times New Roman",serif;color:#1f2328;line-height:1.55}}
body{{max-width:980px;margin:0 auto;padding:2rem;background:#fff}}
nav{{font-family:system-ui,sans-serif;margin-bottom:2rem}}nav a{{margin-right:1rem;color:inherit}}
h1{{margin-bottom:.2rem}}h2{{border-bottom:1px solid #d8dee4;padding-bottom:.35rem;margin-top:2.2rem}}
h3{{margin-bottom:.35rem}}h4{{font-size:.92rem;text-transform:uppercase;letter-spacing:.04em;margin:.9rem 0 .2rem;color:#57606a}}
.subtitle,.quiet,.location{{color:#57606a}}.location{{font-family:system-ui,sans-serif;font-size:.82rem;text-transform:uppercase;letter-spacing:.04em}}
.table-wrap{{overflow-x:auto}}table{{border-collapse:collapse;width:100%;font-family:system-ui,sans-serif}}th,td{{border:1px solid #d0d7de;padding:.45rem;text-align:center}}th{{background:#f6f8fa}}
.interpretation{{border:1px solid #d0d7de;border-radius:.65rem;padding:1rem 1.2rem;margin:1rem 0;break-inside:avoid}}
.interpretation h3{{font-size:1.18rem}}.limit{{border-left:4px solid #bf8700;background:#fff8c5;padding:.55rem .8rem;margin-top:1rem}}
.limit p{{margin:.25rem 0}}.source-links{{font-family:system-ui,sans-serif;font-size:.85rem}}
.ai-boundary{{border-left:4px solid #8250df;background:#f6f3ff;padding:.7rem 1rem;margin:1rem 0}}
.warning,.error{{border-left:4px solid #cf222e;background:#fff1f0;padding:.7rem 1rem;margin:1rem 0}}
.clinician-item{{border-left:3px solid #57606a;padding-left:.8rem;margin:.8rem 0}}
.actions{{display:flex;gap:.7rem;align-items:center;flex-wrap:wrap}}button{{font:inherit;padding:.55rem .9rem;cursor:pointer}}
.meta-strip{{font-family:system-ui,sans-serif;display:flex;gap:1rem;flex-wrap:wrap;color:#57606a;font-size:.9rem;margin:1rem 0}}
@media print{{body{{max-width:none;padding:0}}nav,.screen-only{{display:none!important}}a{{text-decoration:none;color:inherit}}.interpretation{{page-break-inside:avoid}}}}
</style></head><body>
<nav class="screen-only"><a href="/">Acasă</a><a href="/current">Profil</a><a href="/findings">Interpretare</a><a href="/integration">Integrare</a><a href="/report">Raport</a><a href="/report/audit">Audit</a></nav>
<header><h1>Raport clinic de lucru</h1><p class="subtitle">Caz pseudonimizat: <strong>{_e(report.summary.current_case_id)}</strong></p>
<div class="meta-strip"><span>{report.summary.profile_count} profil(uri)</span><span>{len(case_findings)} interpretări specifice cazului</span><span>{len(report.experimental_complement.evidence)} E.K.P.</span></div></header>
{status_note}
<section><h2>Profilul Szondi</h2>{_matrix(workspace)}</section>
<section><h2>Lectura clinică</h2>{ai_notice}{error_html}<div class="actions">{action}</div>{ai_section}</section>
{_experimental_complement(workspace)}
{_clinician_integration(workspace)}
<section class="screen-only"><h2>Surse și control</h2><p><a href="/findings">Deschide constatările și traseul „De ce apare?”</a></p><p><a href="/report/audit">Deschide raportul tehnic complet / auditul</a></p></section>
</body></html>"""
