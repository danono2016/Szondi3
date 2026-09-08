"""Deterministic, print-friendly HTML rendering for ``ClinicianWorkingReport``.

The renderer is a presentation-only layer over the existing working-report contract.
It preserves report wording, provenance, unresolved states, longitudinal structural
Differences, clinician-authored context, and release metadata without recalculating
P1, activating P2B claims, adding clinical meaning, or using AI.
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
from fractions import Fraction
from html import escape
import json
from typing import Any

from .clinician_working_report import ClinicianWorkingReport


def _json_safe(value: Any) -> Any:
    if isinstance(value, Fraction):
        return {"numerator": value.numerator, "denominator": value.denominator, "exact": str(value)}
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value) and not isinstance(value, type):
        return {field.name: _json_safe(getattr(value, field.name)) for field in fields(value)}
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, (set, frozenset)):
        return [_json_safe(item) for item in sorted(value, key=repr)]
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return repr(value)


def _display(value: Any) -> str:
    if value is None:
        return "—"
    if isinstance(value, Fraction):
        return str(value)
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float, bool)):
        return str(value)
    return json.dumps(_json_safe(value), ensure_ascii=False, sort_keys=True, separators=(", ", ": "))


def _text(value: Any) -> str:
    return escape(_display(value), quote=True)


def _join(values: Any, separator: str = ", ") -> str:
    return separator.join(_display(value) for value in values)


def _scope_label(scope: str, profile_number: int | None) -> str:
    return scope if profile_number is None else f"{scope} {profile_number}"


def _finding_block(finding: Any) -> str:
    meta = " · ".join(
        (
            _scope_label(finding.scope, finding.profile_number),
            finding.claim_id,
            finding.assertion_mode,
            finding.lifecycle_status,
        )
    )
    source_strength = (
        f'<p class="source-strength"><strong>Forța sursei:</strong> {_text(finding.source_strength_note)}</p>'
        if finding.source_strength_note
        else ""
    )
    anti = ""
    if finding.anti_inferences:
        anti = '<div class="anti"><strong>Anti-inferențe:</strong><ul>' + "".join(
            f"<li>{_text(item)}</li>" for item in finding.anti_inferences
        ) + "</ul></div>"
    return (
        '<article class="finding">'
        f'<div class="meta">{_text(meta)}</div>'
        f"<p>{_text(finding.statement)}</p>{source_strength}{anti}</article>"
    )


def _uncertainty_block(item: Any) -> str:
    identity = _scope_label(item.scope, item.profile_number)
    qualifiers: list[str] = []
    if item.claim_id:
        qualifiers.append(f"claim {item.claim_id}")
    if item.calculation_name:
        qualifiers.append(f"calcul {item.calculation_name}")
    suffix = f" · {' · '.join(qualifiers)}" if qualifiers else ""
    return (
        '<article class="uncertainty">'
        f'<div class="meta">{_text(identity + " · " + item.kind + suffix)}</div>'
        f"<p>{_text(item.message)}</p></article>"
    )


def _render_profile_observations(report: ClinicianWorkingReport) -> str:
    blocks: list[str] = []
    for profile in report.formal.observations:
        factor_rows = "".join(
            "<tr>"
            f"<td>{_text(item.factor)}</td><td>{_text(item.symbol)}</td>"
            f"<td>{item.sympathetic}</td><td>{item.unsympathetic}</td>"
            f"<td>{item.quantum_level}</td><td>{_text(item.forced_null)}</td>"
            "</tr>"
            for item in profile.factors
        )
        vector_rows = "".join(
            f"<tr><td>{_text(item.vector)}</td><td>{_text(_join(item.symbols, ' '))}</td></tr>"
            for item in profile.vectors
        )
        blocks.append(
            f"<h3>Profil {profile.profile_number}</h3>"
            '<div class="grid"><div><table><thead><tr><th>Factor</th><th>Reacție</th>'
            '<th>+</th><th>-</th><th>Quantum</th><th>Null forțat</th></tr></thead>'
            f"<tbody>{factor_rows}</tbody></table></div>"
            '<div><table><thead><tr><th>Vector</th><th>Configurație</th></tr></thead>'
            f"<tbody>{vector_rows}</tbody></table></div></div>"
        )
    return "".join(blocks) or '<p class="empty">Nicio observație formală.</p>'


def _render_series_morphology(report: ClinicianWorkingReport) -> str:
    factor_rows = "".join(
        "<tr>"
        f"<td>{_text(item.factor)}</td><td>{_text(_join(item.symbols, ' '))}</td>"
        f"<td>{_text(_join(item.base_symbols, ' '))}</td><td>{item.positive_count}</td>"
        f"<td>{item.negative_count}</td><td>{item.null_count}</td>"
        f"<td>{item.ambivalent_count}</td><td>{item.forced_null_count}</td>"
        f"<td>{_text(_join(item.tensioned_profiles))}</td><td>{item.quantum_total}</td>"
        "</tr>"
        for item in report.formal.factor_series
    )
    vector_rows = "".join(
        "<tr>"
        f"<td>{_text(item.vector)}</td><td>{_text(_join(item.factors, ' / '))}</td>"
        f"<td>{_text(' | '.join(' '.join(pair) for pair in item.symbols))}</td>"
        f"<td>{_text(' | '.join(' '.join(pair) for pair in item.base_symbols))}</td>"
        f"<td>{_text('; '.join(' '.join(freq.symbols) + '=' + str(freq.count) for freq in item.configuration_frequencies))}</td>"
        "</tr>"
        for item in report.formal.vector_series
    )
    return (
        '<h3>Factori în serie</h3><table><thead><tr><th>Factor</th><th>Secvență</th>'
        '<th>Secvență bază</th><th>+</th><th>-</th><th>0</th><th>±</th>'
        '<th>Null forțat</th><th>Profile tensionate</th><th>Quantum total</th></tr></thead>'
        f"<tbody>{factor_rows}</tbody></table>"
        '<h3>Vectori în serie</h3><table><thead><tr><th>Vector</th><th>Factori</th>'
        '<th>Secvență</th><th>Secvență bază</th><th>Frecvențe configurații</th></tr></thead>'
        f"<tbody>{vector_rows}</tbody></table>"
    )


def _render_calculations(report: ClinicianWorkingReport) -> str:
    rows = "".join(
        f"<tr><td>{_text(item.name)}</td><td>{_text(item.state)}</td>"
        f"<td>{_text(item.value)}</td><td>{_text(item.note)}</td></tr>"
        for item in report.formal.calculations
    )
    if not rows:
        return '<p class="empty">Niciun calcul de serie.</p>'
    return (
        '<table><thead><tr><th>Calcul</th><th>Stare</th><th>Valoare</th><th>Notă</th></tr></thead>'
        f"<tbody>{rows}</tbody></table>"
    )


def _render_boundaries(report: ClinicianWorkingReport) -> str:
    if not report.limits_and_anti_inferences:
        return '<p class="empty">Nicio limită suplimentară în proiecția curentă.</p>'
    blocks: list[str] = []
    for item in report.limits_and_anti_inferences:
        anti = "".join(f"<li>{_text(value)}</li>" for value in item.anti_inferences)
        blocks.append(
            '<article class="boundary">'
            f'<div class="meta">{_text(_scope_label(item.scope, item.profile_number))} · '
            f'{_text(item.claim_id)} · {_text(item.assertion_mode)}</div>'
            f"<p>{_text(item.statement)}</p><ul>{anti}</ul></article>"
        )
    return "".join(blocks)


def _render_status(report: ClinicianWorkingReport) -> str:
    unresolved = "".join(_uncertainty_block(item) for item in report.status.unresolved)
    blocked = "".join(_uncertainty_block(item) for item in report.status.blocked)
    suppressed_rows = "".join(
        "<tr>"
        f"<td>{_text(_scope_label(item.scope, item.profile_number))}</td>"
        f"<td>{_text(item.claim_id)}</td><td>{_text(item.activation_status)}</td>"
        f"<td>{_text(_join(item.missing_facts))}</td><td>{_text(_join(item.missing_context))}</td>"
        f"<td>{_text(_join(item.qualifications, ' | '))}</td></tr>"
        for item in report.status.suppressed
    )
    suppressed = (
        '<details open><summary>Claim-uri neactivate păstrate pentru audit '
        f"({len(report.status.suppressed)})</summary>"
        '<table><thead><tr><th>Scop</th><th>Claim</th><th>Stare</th><th>Fapte lipsă</th>'
        '<th>Context lipsă</th><th>Calificări</th></tr></thead>'
        f"<tbody>{suppressed_rows}</tbody></table></details>"
        if report.status.suppressed
        else '<p class="empty">Niciun claim neactivat păstrat în această proiecție.</p>'
    )
    return (
        '<h3>Nerezolvat</h3>'
        f"{unresolved or '<p class=\"empty\">Nicio stare nerezolvată.</p>'}"
        '<h3>Blocat</h3>'
        f"{blocked or '<p class=\"empty\">Nicio stare blocată.</p>'}"
        f"<h3>Audit de activare</h3>{suppressed}"
    )


def _render_experimental_complement(report: ClinicianWorkingReport) -> str:
    section = report.experimental_complement
    if not section.findings and not section.uncertainties and not section.evidence:
        return '<p class="empty">Nu există material E.K.P. în cazul curent.</p>'
    findings = "".join(_finding_block(item) for item in section.findings)
    uncertainties = "".join(_uncertainty_block(item) for item in section.uncertainties)
    evidence_blocks: list[str] = []
    for item in section.evidence:
        factor_symbols = ", ".join(f"{factor} {symbol}" for factor, symbol in item.factor_symbols)
        fact_rows = "".join(
            f"<tr><td>{_text(fact.key)}</td><td>{_text(fact.value)}</td>"
            f"<td>{_text(fact.input_state)}</td><td>{_text(fact.fact_id)}</td></tr>"
            for fact in item.facts
        )
        evidence_blocks.append(
            f"<h3>E.K.P. test {item.test_number}</h3><p><strong>Reacții:</strong> {_text(factor_symbols)}</p>"
            '<table><thead><tr><th>Cheie</th><th>Valoare</th><th>Stare input</th><th>Fact ID</th></tr></thead>'
            f"<tbody>{fact_rows}</tbody></table>"
        )
    return (
        '<h3>Constatări E.K.P.</h3>'
        f"{findings or '<p class=\"empty\">Nicio constatare E.K.P. activă.</p>'}"
        '<h3>Stări E.K.P. nerezolvate/blocate</h3>'
        f"{uncertainties or '<p class=\"empty\">Nicio incertitudine E.K.P.</p>'}"
        '<h3>Dovezi E.K.P.</h3>'
        f"{''.join(evidence_blocks) or '<p class=\"empty\">Nicio dovadă E.K.P.</p>'}"
    )


def _render_field_diff_rows(items: Any) -> str:
    return "".join(
        f"<tr><td>{_text(item.label)}</td><td>{_text(item.value_a)}</td>"
        f"<td>{_text(item.value_b)}</td><td>{_text(item.note)}</td></tr>"
        for item in items
        if not item.is_identical
    )


def _render_longitudinal(report: ClinicianWorkingReport) -> str:
    if not report.longitudinal:
        return '<p class="empty">Nu există comparație longitudinală.</p>'

    blocks: list[str] = []
    for comparison in report.longitudinal:
        issues = "".join(
            f"<li><strong>{_text(item.code)}</strong>: {_text(item.detail)}</li>"
            for item in comparison.comparability_issues
        )
        header_rows = _render_field_diff_rows(comparison.header_diffs)
        calculation_rows = _render_field_diff_rows(comparison.series_calculation_diffs)
        factor_sequence_rows = "".join(
            f"<tr><td>{_text(item.factor)}</td>"
            f"<td>{_text(_join(item.symbol_sequence_a or (), ' '))}</td>"
            f"<td>{_text(_join(item.symbol_sequence_b or (), ' '))}</td></tr>"
            for item in comparison.factor_comparisons
            if not item.sequences_identical
        )
        factor_detail_rows: list[str] = []
        for item in comparison.factor_comparisons:
            detailed = list(item.field_diffs)
            if item.quantum_total_diff is not None:
                detailed.append(item.quantum_total_diff)
            for diff in detailed:
                if diff.is_identical:
                    continue
                factor_detail_rows.append(
                    f"<tr><td>{_text(item.factor)}</td><td>{_text(diff.label)}</td>"
                    f"<td>{_text(diff.value_a)}</td><td>{_text(diff.value_b)}</td>"
                    f"<td>{_text(diff.note)}</td></tr>"
                )
        vector_rows = "".join(
            f"<tr><td>{_text(item.vector)}</td>"
            f"<td>{_text(' | '.join(' '.join(pair) for pair in (item.symbol_sequence_a or ())))}</td>"
            f"<td>{_text(' | '.join(' '.join(pair) for pair in (item.symbol_sequence_b or ())))}</td></tr>"
            for item in comparison.vector_comparisons
            if not item.is_identical
        )
        claim_rows = "".join(
            f"<tr><td>{_text(_scope_label(item.key.scope, item.key.profile_number))}</td>"
            f"<td>{_text(item.key.claim_id)}</td><td>{_text(item.state_a)}</td>"
            f"<td>{_text(item.state_b)}</td></tr>"
            for item in comparison.claim_comparisons
            if item.state_changed or item.present_in_a != item.present_in_b
        )

        blocks.append(
            f"<h3>{_text(comparison.case_id_a)} → {_text(comparison.case_id_b)}</h3>"
            '<p class="boundary-note">Comparație structurală; sensul clinic al schimbării nu este inferat de renderer.</p>'
            + (f"<ul>{issues}</ul>" if issues else "")
        )
        if header_rows:
            blocks.append(
                '<h4>Diferențe de antet</h4><table><thead><tr><th>Câmp</th><th>A</th><th>B</th><th>Notă</th></tr></thead>'
                f"<tbody>{header_rows}</tbody></table>"
            )
        if factor_sequence_rows:
            blocks.append(
                '<h4>Diferențe factoriale de secvență</h4><table><thead><tr><th>Factor</th><th>A</th><th>B</th></tr></thead>'
                f"<tbody>{factor_sequence_rows}</tbody></table>"
            )
        if factor_detail_rows:
            blocks.append(
                '<h4>Diferențe factoriale detaliate</h4><table><thead><tr><th>Factor</th><th>Câmp</th><th>A</th><th>B</th><th>Notă</th></tr></thead>'
                f"<tbody>{''.join(factor_detail_rows)}</tbody></table>"
            )
        if vector_rows:
            blocks.append(
                '<h4>Diferențe vectoriale</h4><table><thead><tr><th>Vector</th><th>A</th><th>B</th></tr></thead>'
                f"<tbody>{vector_rows}</tbody></table>"
            )
        if calculation_rows:
            blocks.append(
                '<h4>Diferențe de calcul</h4><table><thead><tr><th>Calcul</th><th>A</th><th>B</th><th>Notă</th></tr></thead>'
                f"<tbody>{calculation_rows}</tbody></table>"
            )
        if claim_rows:
            blocks.append(
                '<h4>Diferențe de stare P2B</h4><table><thead><tr><th>Scop</th><th>Claim</th><th>A</th><th>B</th></tr></thead>'
                f"<tbody>{claim_rows}</tbody></table>"
            )
        if not any((issues, header_rows, factor_sequence_rows, factor_detail_rows, vector_rows, calculation_rows, claim_rows)):
            blocks.append('<p class="empty">Nicio diferență structurală expusă pentru această pereche.</p>')
    return "".join(blocks)


def _render_clinician_input(report: ClinicianWorkingReport) -> str:
    context = "".join(
        '<article class="context">'
        f"<h3>{_text(item.label)}</h3>"
        f'<div class="meta">{_text(item.authorship)} · {_text(item.epistemic_role)}</div>'
        f"<p>{_text(item.text)}</p></article>"
        for item in report.clinician_context
    )
    synthesis = (
        '<article class="synthesis">'
        f'<div class="meta">{_text(report.clinician_synthesis.authorship)}</div>'
        f"<p>{_text(report.clinician_synthesis.text)}</p></article>"
        if report.clinician_synthesis.text is not None
        else '<p class="empty">Sinteza clinicianului nu a fost completată.</p>'
    )
    return (
        '<h3>Context extern introdus de clinician</h3>'
        f"{context or '<p class=\"empty\">Niciun context extern introdus.</p>'}"
        f"<h3>Sinteza clinicianului</h3>{synthesis}"
    )


def _render_provenance(report: ClinicianWorkingReport) -> str:
    if not report.provenance:
        return '<p class="empty">Nicio dovadă doctrinară asociată constatărilor active.</p>'
    blocks: list[str] = []
    for item in report.provenance:
        anchors = "".join(
            "<li>"
            f"{_text(anchor.stream)} · {_text(anchor.unit_start)}–{_text(anchor.unit_end)}"
            f" · pagina tipărită {_text(anchor.printed_page)}"
            + (f" · {_text(anchor.pdf_path)}" if anchor.pdf_path else "")
            + (f"<br><em>{_text(anchor.visual_arbitration_note)}</em>" if anchor.visual_arbitration_note else "")
            + "</li>"
            for anchor in item.source_anchors
        )
        scope_notes = "".join(f"<li>{_text(note)}</li>" for note in item.scope_notes)
        blocks.append(
            '<details class="provenance" open><summary>'
            f"{_text(item.doctrine_id)} · {_text(item.source_id)} · {_text(item.review_status)}"
            "</summary>"
            f"<p><strong>Forță:</strong> {_text(item.assertion_strength)}</p>"
            f"<p><strong>Doctrină:</strong> {_text(item.doctrinal_statement)}</p>"
            f"<p><strong>Redare română:</strong> {_text(item.romanian_rendering)}</p>"
            f"<blockquote>{_text(item.source_excerpt)}</blockquote><ul>{anchors}</ul>"
            + (f"<p><strong>Note de scop:</strong></p><ul>{scope_notes}</ul>" if scope_notes else "")
            + "</details>"
        )
    return "".join(blocks)


def _render_technical(report: ClinicianWorkingReport) -> str:
    release = report.release
    audit = report.technical_audit
    release_rows = "".join(
        f"<tr><th>{_text(label)}</th><td>{_text(value)}</td></tr>"
        for label, value in (
            ("schema_version", release.schema_version),
            ("git_commit_sha", release.git_commit_sha),
            ("doctrine_snapshot_id", release.doctrine_snapshot_id),
            ("doctrine_registry_sha256", release.doctrine_registry_sha256),
            ("p2b_release_id", release.p2b_release_id),
            ("p2b_catalogue_sha256", release.p2b_catalogue_sha256),
            ("evidence_packet_sha256", release.evidence_packet_sha256),
            ("synthesis_contract_version", release.synthesis_contract_version),
            ("synthesis_model", release.synthesis_model),
            ("synthesis_release_policy", release.synthesis_release_policy),
            ("autonomous_ai_release", release.autonomous_ai_release),
        )
    )
    audit_rows = "".join(
        f"<tr><th>{_text(label)}</th><td>{_text(value)}</td></tr>"
        for label, value in (
            ("profile_count", audit.profile_count),
            ("complement_count", audit.complement_count),
            ("finding_count", audit.finding_count),
            ("traced_finding_count", audit.traced_finding_count),
            ("routed_claim_count", audit.routed_claim_count),
            ("nonactive_occurrence_count", audit.nonactive_occurrence_count),
            ("uncertainty_count", audit.uncertainty_count),
        )
    )
    return (
        '<details open><summary>Manifest de release</summary><table class="kv">'
        f"{release_rows}</table></details>"
        '<details open><summary>Audit structural</summary><table class="kv">'
        f"{audit_rows}</table></details>"
    )


def render_clinician_working_report_html(report: ClinicianWorkingReport) -> str:
    """Render a complete clinician working report as deterministic standalone HTML."""
    if not isinstance(report, ClinicianWorkingReport):
        raise TypeError("HTML renderer requires a ClinicianWorkingReport")

    summary = report.summary
    history = ", ".join(item.case_id for item in report.historical_assessments) or "—"
    findings = "".join(_finding_block(item) for item in report.findings)

    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Szondi3 — raport clinic de lucru — {_text(summary.current_case_id)}</title>
<style>
:root {{ color-scheme: light; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width: 1180px; margin: 0 auto; padding: 2rem; line-height: 1.45; color: #1f2328; }}
h1, h2, h3, h4 {{ line-height: 1.2; }}
h2 {{ margin-top: 2.4rem; border-bottom: 1px solid #d0d7de; padding-bottom: .35rem; }}
table {{ width: 100%; border-collapse: collapse; margin: .75rem 0 1.25rem; font-size: .92rem; }}
th, td {{ border: 1px solid #d0d7de; padding: .45rem .55rem; vertical-align: top; text-align: left; }}
th {{ background: #f6f8fa; }}
.grid {{ display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 1rem; }}
.meta {{ color: #57606a; font-size: .84rem; margin-bottom: .25rem; }}
.finding, .boundary, .uncertainty, .context, .synthesis {{ border-left: 4px solid #d0d7de; padding: .55rem .85rem; margin: .75rem 0; background: #f6f8fa; }}
.anti, .boundary-note {{ color: #424a53; }}
.source-strength {{ font-size: .92rem; }}
.empty {{ color: #57606a; font-style: italic; }}
details {{ margin: .75rem 0; }}
summary {{ cursor: pointer; font-weight: 650; }}
blockquote {{ border-left: 3px solid #d0d7de; margin-left: 0; padding-left: 1rem; white-space: pre-wrap; }}
.kv th {{ width: 28%; }}
@media (max-width: 780px) {{ .grid {{ grid-template-columns: 1fr; }} body {{ padding: 1rem; }} }}
@media print {{ body {{ max-width: none; padding: 0; }} details {{ display: block; }} summary {{ list-style: none; }} }}
</style>
</head>
<body>
<header>
<h1>Szondi3 — raport clinic de lucru</h1>
<p><strong>Caz curent:</strong> {_text(summary.current_case_id)}</p>
<p class="meta">Acest document organizează exclusiv rezultate și limite deja autorizate în pipeline. Judecata clinică și sinteza rămân ale clinicianului.</p>
</header>
<section id="summary"><h2>Rezumat</h2><table class="kv">
<tr><th>Evaluări</th><td>{_text(_join(summary.assessment_ids, " → "))}</td></tr>
<tr><th>Istoric</th><td>{_text(history)}</td></tr>
<tr><th>Profile</th><td>{summary.profile_count}</td></tr>
<tr><th>Constatări active</th><td>{summary.finding_count}</td></tr>
<tr><th>Nerezolvate</th><td>{summary.unresolved_count}</td></tr>
<tr><th>Blocate</th><td>{summary.blocked_count}</td></tr>
<tr><th>Comparații longitudinale</th><td>{summary.longitudinal_comparison_count}</td></tr>
<tr><th>Probleme de comparabilitate</th><td>{summary.comparability_issue_count}</td></tr>
<tr><th>Stare interpretare</th><td>{_text(summary.interpretation_release_state)}</td></tr>
<tr><th>Elemente context clinician</th><td>{summary.clinician_context_count}</td></tr>
<tr><th>Autor sinteză</th><td>{_text(summary.clinician_synthesis_authorship)}</td></tr>
</table></section>
<section id="formal"><h2>Structura formală actuală</h2>{_render_profile_observations(report)}
<h3>Morfologia seriei</h3>{_render_series_morphology(report)}
<h3>Calcule deterministe</h3>{_render_calculations(report)}</section>
<section id="findings"><h2>Constatări Szondiene autorizate</h2>{findings or '<p class="empty">Nicio constatare activă în proiecția curentă.</p>'}</section>
<section id="boundaries"><h2>Limite și anti-inferențe</h2>{_render_boundaries(report)}</section>
<section id="status"><h2>Stări nerezolvate, blocate și neactivate</h2>{_render_status(report)}</section>
<section id="complement"><h2>Complement experimental (E.K.P.)</h2>{_render_experimental_complement(report)}</section>
<section id="longitudinal"><h2>Comparație longitudinală</h2>{_render_longitudinal(report)}</section>
<section id="clinician-input"><h2>Integrare clinică manuală</h2>{_render_clinician_input(report)}</section>
<section id="provenance"><h2>Trasabilitate doctrinară</h2>{_render_provenance(report)}</section>
<section id="technical"><h2>Trasabilitate tehnică</h2>{_render_technical(report)}</section>
</body>
</html>
"""
