"""Clinician-facing exact trace for one active Szondi finding.

The drill-down is a projection over ``ClinicalExploration.trace_finding``. It uses
explicit runtime/support/doctrine identities only: no textual similarity, search,
AI reconstruction, or new interpretation is allowed.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Any

from .clinician_workspace import ClinicianWorkspace


@dataclass(frozen=True, slots=True)
class FindingDrilldownKey:
    scope: str
    profile_number: int | None
    claim_id: str


@dataclass(frozen=True, slots=True)
class FindingSupportFact:
    fact_id: str
    key: str
    value: Any
    scope: str
    input_state: str
    calculation_version: str | None


@dataclass(frozen=True, slots=True)
class FindingSourceAnchor:
    stream: str
    unit_start: str
    unit_end: str
    pdf_path: str | None
    printed_page: str | int | None
    visual_arbitration_note: str | None


@dataclass(frozen=True, slots=True)
class FindingDoctrineSupport:
    doctrine_id: str
    source_id: str
    source_layer: str
    source_language: str
    review_status: str
    assertion_strength: str | None
    doctrinal_statement: str | None
    romanian_rendering: str | None
    source_excerpt: str
    anchors: tuple[FindingSourceAnchor, ...]
    scope_notes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class FindingDrilldown:
    key: FindingDrilldownKey
    statement: str
    assertion_mode: str
    lifecycle_status: str
    source_strength_note: str
    sensitive_domains: tuple[str, ...]
    support_facts: tuple[FindingSupportFact, ...]
    doctrine_support: tuple[FindingDoctrineSupport, ...]
    anti_inference_ids: tuple[str, ...]
    anti_inferences: tuple[str, ...]


def build_finding_drilldown(
    workspace: ClinicianWorkspace,
    *,
    claim_id: str,
    scope: str,
    profile_number: int | None = None,
) -> FindingDrilldown:
    """Resolve one active current-case finding through the existing exact trace."""
    if not isinstance(workspace, ClinicianWorkspace):
        raise TypeError("Finding drill-down requires a ClinicianWorkspace")

    trace = workspace.trace_current_finding(
        claim_id,
        scope=scope,
        profile_number=profile_number,
    )
    finding = trace.finding

    support_facts: list[FindingSupportFact] = []
    for fact in trace.support_facts:
        if fact.fact_id is None:
            raise ValueError("Active finding support fact lacks fact_id")
        support_facts.append(
            FindingSupportFact(
                fact_id=fact.fact_id,
                key=fact.key,
                value=fact.value,
                scope=fact.scope,
                input_state=fact.input_state.value,
                calculation_version=fact.calculation_version,
            )
        )

    doctrine_support = tuple(
        FindingDoctrineSupport(
            doctrine_id=item.doctrine_id,
            source_id=item.source_id,
            source_layer=item.source_layer,
            source_language=item.source_language,
            review_status=item.review_status,
            assertion_strength=item.assertion_strength,
            doctrinal_statement=item.doctrinal_statement,
            romanian_rendering=item.romanian_rendering,
            source_excerpt=item.source_excerpt,
            anchors=tuple(
                FindingSourceAnchor(
                    stream=anchor.stream,
                    unit_start=anchor.unit_start,
                    unit_end=anchor.unit_end,
                    pdf_path=anchor.pdf_path,
                    printed_page=anchor.printed_page,
                    visual_arbitration_note=anchor.visual_arbitration_note,
                )
                for anchor in item.source_anchors
            ),
            scope_notes=item.scope_notes,
        )
        for item in trace.doctrine_evidence
    )

    result = FindingDrilldown(
        key=FindingDrilldownKey(
            scope=finding.scope,
            profile_number=finding.profile_number,
            claim_id=finding.claim_id,
        ),
        statement=finding.statement,
        assertion_mode=finding.assertion_mode,
        lifecycle_status=finding.lifecycle_status,
        source_strength_note=finding.source_strength_note,
        sensitive_domains=finding.sensitive_domains,
        support_facts=tuple(support_facts),
        doctrine_support=doctrine_support,
        anti_inference_ids=finding.anti_inference_ids,
        anti_inferences=finding.anti_inferences,
    )

    if tuple(item.fact_id for item in result.support_facts) != finding.support_fact_ids:
        raise ValueError("Finding drill-down support fact ordering diverges from finding")
    if tuple(item.doctrine_id for item in result.doctrine_support) != finding.doctrine_ids:
        raise ValueError("Finding drill-down doctrine ordering diverges from finding")
    return result


def _text(value: Any) -> str:
    return escape("—" if value is None else str(value), quote=True)


def render_finding_drilldown_html(drilldown: FindingDrilldown) -> str:
    """Render the exact 'De ce apare?' path for clinician inspection."""
    if not isinstance(drilldown, FindingDrilldown):
        raise TypeError("Finding drill-down renderer requires a FindingDrilldown")

    location = drilldown.key.scope
    if drilldown.key.profile_number is not None:
        location += f" {drilldown.key.profile_number}"

    fact_rows = "".join(
        "<tr>"
        f"<td>{_text(item.fact_id)}</td><td>{_text(item.key)}</td>"
        f"<td>{_text(item.value)}</td><td>{_text(item.scope)}</td>"
        f"<td>{_text(item.input_state)}</td><td>{_text(item.calculation_version)}</td>"
        "</tr>"
        for item in drilldown.support_facts
    )

    doctrine_blocks: list[str] = []
    for item in drilldown.doctrine_support:
        anchors = "".join(
            "<li>"
            f"{_text(anchor.stream)} · {_text(anchor.unit_start)}–{_text(anchor.unit_end)}"
            f" · pagina tipărită {_text(anchor.printed_page)}"
            + (f" · {_text(anchor.pdf_path)}" if anchor.pdf_path else "")
            + (
                f"<br><em>{_text(anchor.visual_arbitration_note)}</em>"
                if anchor.visual_arbitration_note
                else ""
            )
            + "</li>"
            for anchor in item.anchors
        )
        scope_notes = "".join(f"<li>{_text(note)}</li>" for note in item.scope_notes)
        doctrine_blocks.append(
            '<article class="doctrine">'
            f"<h3>{_text(item.doctrine_id)}</h3>"
            f'<p class="meta">{_text(item.source_id)} · {_text(item.source_layer)} · '
            f'{_text(item.review_status)} · forță {_text(item.assertion_strength)}</p>'
            f"<p><strong>Doctrină:</strong> {_text(item.doctrinal_statement)}</p>"
            f"<p><strong>Redare română:</strong> {_text(item.romanian_rendering)}</p>"
            f"<blockquote>{_text(item.source_excerpt)}</blockquote>"
            f"<ul>{anchors}</ul>"
            + (f"<p><strong>Note de scop</strong></p><ul>{scope_notes}</ul>" if scope_notes else "")
            + "</article>"
        )

    anti = "".join(f"<li>{_text(item)}</li>" for item in drilldown.anti_inferences)
    domains = ", ".join(drilldown.sensitive_domains) or "—"

    return f"""<!doctype html>
<html lang="ro">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Szondi3 — de ce apare? — {_text(drilldown.key.claim_id)}</title>
<style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width: 1050px; margin: 0 auto; padding: 1.5rem; line-height: 1.45; color: #1f2328; }}
.meta {{ color: #57606a; font-size: .88rem; }}
.finding {{ border-left: 4px solid #57606a; padding: .7rem 1rem; background: #f6f8fa; }}
.anti {{ border-left: 4px solid #8c6d1f; padding: .7rem 1rem; background: #fff8c5; }}
table {{ width: 100%; border-collapse: collapse; font-size: .9rem; }}
th, td {{ border: 1px solid #d0d7de; padding: .4rem .5rem; text-align: left; vertical-align: top; }}
th {{ background: #f6f8fa; }}
.doctrine {{ margin: 1rem 0; padding-top: .5rem; border-top: 1px solid #d0d7de; }}
blockquote {{ margin-left: 0; padding-left: 1rem; border-left: 3px solid #d0d7de; white-space: pre-wrap; }}
</style>
</head>
<body>
<h1>De ce apare?</h1>
<section class="finding">
<p class="meta">{_text(location)} · {_text(drilldown.key.claim_id)} · {_text(drilldown.assertion_mode)} · {_text(drilldown.lifecycle_status)}</p>
<p>{_text(drilldown.statement)}</p>
<p class="meta">Forța sursei: {_text(drilldown.source_strength_note)} · domenii sensibile: {_text(domains)}</p>
</section>
<section>
<h2>Faptele care au activat constatarea</h2>
<table><thead><tr><th>Fact ID</th><th>Cheie</th><th>Valoare</th><th>Scop</th><th>Stare</th><th>Versiune calcul</th></tr></thead>
<tbody>{fact_rows}</tbody></table>
</section>
<section>
<h2>Doctrina și sursa</h2>
{"".join(doctrine_blocks)}
</section>
<section class="anti">
<h2>Ce nu autorizează constatarea</h2>
{f'<ul>{anti}</ul>' if anti else '<p>Nicio anti-inferență suplimentară înregistrată pentru această constatare.</p>'}
</section>
</body>
</html>
"""
