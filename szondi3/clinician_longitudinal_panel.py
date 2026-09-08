"""Clinician-facing structural longitudinal panel.

The panel projects existing ``CaseComparisonResult`` objects into visual differences.
It never assigns improvement, deterioration, therapeutic direction, or other clinical
meaning to change. All comparability warnings and detailed factor diffs remain visible.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Any

from .clinician_workspace import ClinicianWorkspace


@dataclass(frozen=True, slots=True)
class LongitudinalReactionChange:
    profile_number: int
    symbol_a: str | None
    symbol_b: str | None
    changed: bool


@dataclass(frozen=True, slots=True)
class LongitudinalFieldChange:
    label: str
    value_a: Any
    value_b: Any
    note: str | None


@dataclass(frozen=True, slots=True)
class LongitudinalFactorRow:
    factor: str
    reactions: tuple[LongitudinalReactionChange, ...]
    base_sequence_a: tuple[str, ...] | None
    base_sequence_b: tuple[str, ...] | None
    detailed_changes: tuple[LongitudinalFieldChange, ...]


@dataclass(frozen=True, slots=True)
class LongitudinalClaimTransition:
    scope: str
    profile_number: int | None
    claim_id: str
    transition_kind: str
    state_a: str | None
    state_b: str | None


@dataclass(frozen=True, slots=True)
class LongitudinalPairPanel:
    case_id_a: str
    case_id_b: str
    comparability_issues: tuple[tuple[str, str], ...]
    factor_rows: tuple[LongitudinalFactorRow, ...]
    header_changes: tuple[LongitudinalFieldChange, ...]
    calculation_changes: tuple[LongitudinalFieldChange, ...]
    claim_transitions: tuple[LongitudinalClaimTransition, ...]
    experimental_complement_present_a: bool
    experimental_complement_present_b: bool


@dataclass(frozen=True, slots=True)
class ClinicianLongitudinalPanel:
    assessment_ids: tuple[str, ...]
    pairs: tuple[LongitudinalPairPanel, ...]
    interpretation_boundary: str = (
        "STRUCTURAL_COMPARISON_ONLY_NO_IMPROVEMENT_OR_WORSENING_INFERENCE"
    )


def _field_change(item: Any) -> LongitudinalFieldChange:
    return LongitudinalFieldChange(
        label=item.label,
        value_a=item.value_a,
        value_b=item.value_b,
        note=item.note,
    )


def _state(value: Any) -> str | None:
    return None if value is None else value.value


def build_clinician_longitudinal_panel(
    workspace: ClinicianWorkspace,
) -> ClinicianLongitudinalPanel:
    """Project the existing adjacent comparisons without re-comparing case data."""
    if not isinstance(workspace, ClinicianWorkspace):
        raise TypeError("Longitudinal panel requires a ClinicianWorkspace")

    pair_panels: list[LongitudinalPairPanel] = []
    for comparison in workspace.integration.longitudinal:
        factor_rows: list[LongitudinalFactorRow] = []
        for factor in comparison.factor_comparisons:
            sequence_a = factor.symbol_sequence_a
            sequence_b = factor.symbol_sequence_b
            width = max(len(sequence_a or ()), len(sequence_b or ()))
            reactions = tuple(
                LongitudinalReactionChange(
                    profile_number=index + 1,
                    symbol_a=(sequence_a[index] if sequence_a is not None and index < len(sequence_a) else None),
                    symbol_b=(sequence_b[index] if sequence_b is not None and index < len(sequence_b) else None),
                    changed=(
                        (sequence_a[index] if sequence_a is not None and index < len(sequence_a) else None)
                        != (sequence_b[index] if sequence_b is not None and index < len(sequence_b) else None)
                    ),
                )
                for index in range(width)
            )
            detailed = tuple(
                _field_change(item)
                for item in factor.field_diffs
                if not item.is_identical
            )
            if factor.quantum_total_diff is not None and not factor.quantum_total_diff.is_identical:
                detailed += (_field_change(factor.quantum_total_diff),)
            factor_rows.append(
                LongitudinalFactorRow(
                    factor=factor.factor,
                    reactions=reactions,
                    base_sequence_a=factor.base_symbol_sequence_a,
                    base_sequence_b=factor.base_symbol_sequence_b,
                    detailed_changes=detailed,
                )
            )

        transitions: list[LongitudinalClaimTransition] = []
        for item in comparison.claim_comparisons:
            if not (item.state_changed or item.present_in_a != item.present_in_b):
                continue
            if not item.present_in_a and item.present_in_b:
                kind = "APPEARED"
            elif item.present_in_a and not item.present_in_b:
                kind = "DISAPPEARED"
            else:
                kind = "STATE_CHANGED"
            transitions.append(
                LongitudinalClaimTransition(
                    scope=item.key.scope,
                    profile_number=item.key.profile_number,
                    claim_id=item.key.claim_id,
                    transition_kind=kind,
                    state_a=_state(item.state_a),
                    state_b=_state(item.state_b),
                )
            )

        pair_panels.append(
            LongitudinalPairPanel(
                case_id_a=comparison.case_id_a,
                case_id_b=comparison.case_id_b,
                comparability_issues=tuple(
                    (item.code, item.detail) for item in comparison.comparability_issues
                ),
                factor_rows=tuple(factor_rows),
                header_changes=tuple(
                    _field_change(item) for item in comparison.header_diffs if not item.is_identical
                ),
                calculation_changes=tuple(
                    _field_change(item)
                    for item in comparison.series_calculation_diffs
                    if not item.is_identical
                ),
                claim_transitions=tuple(transitions),
                experimental_complement_present_a=comparison.experimental_complement_present_a,
                experimental_complement_present_b=comparison.experimental_complement_present_b,
            )
        )

    return ClinicianLongitudinalPanel(
        assessment_ids=workspace.assessment_ids,
        pairs=tuple(pair_panels),
    )


def _text(value: Any) -> str:
    return escape("—" if value is None else str(value), quote=True)


def render_clinician_longitudinal_panel_html(panel: ClinicianLongitudinalPanel) -> str:
    """Render structural longitudinal differences with changed cells emphasized."""
    if not isinstance(panel, ClinicianLongitudinalPanel):
        raise TypeError("Longitudinal renderer requires a ClinicianLongitudinalPanel")

    pair_blocks: list[str] = []
    for pair in panel.pairs:
        profile_numbers = sorted(
            {change.profile_number for row in pair.factor_rows for change in row.reactions}
        )
        header = "".join(f"<th>P{number}</th>" for number in profile_numbers)
        factor_rows = []
        for row in pair.factor_rows:
            by_profile = {item.profile_number: item for item in row.reactions}
            cells = []
            for number in profile_numbers:
                item = by_profile.get(number)
                if item is None:
                    cells.append("<td>—</td>")
                    continue
                cls = ' class="changed"' if item.changed else ""
                cells.append(
                    f"<td{cls}><span>{_text(item.symbol_a)}</span> → <span>{_text(item.symbol_b)}</span></td>"
                )
            factor_rows.append(f"<tr><th>{_text(row.factor)}</th>{''.join(cells)}</tr>")

        issues = "".join(
            f"<li><strong>{_text(code)}</strong>: {_text(detail)}</li>"
            for code, detail in pair.comparability_issues
        )
        detail_rows = "".join(
            f"<tr><td>{_text(row.factor)}</td><td>{_text(change.label)}</td>"
            f"<td>{_text(change.value_a)}</td><td>{_text(change.value_b)}</td></tr>"
            for row in pair.factor_rows
            for change in row.detailed_changes
        )
        transition_rows = "".join(
            f"<tr><td>{_text(item.scope)} {_text(item.profile_number) if item.profile_number is not None else ''}</td>"
            f"<td>{_text(item.claim_id)}</td><td>{_text(item.transition_kind)}</td>"
            f"<td>{_text(item.state_a)}</td><td>{_text(item.state_b)}</td></tr>"
            for item in pair.claim_transitions
        )
        pair_blocks.append(
            f"<section><h2>{_text(pair.case_id_a)} → {_text(pair.case_id_b)}</h2>"
            '<p class="boundary">Diferențele sunt structurale. Interfața nu le califică drept ameliorare, agravare sau efect terapeutic.</p>'
            + (f"<div class=\"warning\"><strong>Comparabilitate</strong><ul>{issues}</ul></div>" if issues else "")
            + '<div class="matrix-wrap"><table><thead><tr><th>Factor</th>' + header + "</tr></thead>"
            + f"<tbody>{''.join(factor_rows)}</tbody></table></div>"
            + (
                '<details><summary>Diferențe factoriale detaliate</summary><table><thead><tr><th>Factor</th><th>Câmp</th><th>A</th><th>B</th></tr></thead>'
                f"<tbody>{detail_rows}</tbody></table></details>"
                if detail_rows else ""
            )
            + (
                '<details open><summary>Tranziții P2B</summary><table><thead><tr><th>Scop</th><th>Claim</th><th>Tranziție</th><th>A</th><th>B</th></tr></thead>'
                f"<tbody>{transition_rows}</tbody></table></details>"
                if transition_rows else '<p class="meta">Nicio tranziție P2B între aceste evaluări.</p>'
            )
            + f'<p class="meta">E.K.P.: A={_text(pair.experimental_complement_present_a)}, B={_text(pair.experimental_complement_present_b)}</p></section>'
        )

    empty = '<p class="meta">Nu există încă două evaluări pentru comparație longitudinală.</p>'
    return f"""<!doctype html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Szondi3 — longitudinal</title><style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width: 1180px; margin: 0 auto; padding: 1.5rem; color: #1f2328; line-height: 1.4; }}
table {{ border-collapse: collapse; width: 100%; font-size: .9rem; }} th, td {{ border:1px solid #d0d7de; padding:.4rem; text-align:center; }} th {{ background:#f6f8fa; }}
.changed {{ font-weight:700; outline:2px solid currentColor; outline-offset:-2px; }} .warning {{ border-left:4px solid #8c6d1f; padding:.6rem 1rem; background:#fff8c5; }}
.boundary, .meta {{ color:#57606a; }} details {{ margin:1rem 0; }} summary {{ cursor:pointer; font-weight:650; }} .matrix-wrap {{ overflow-x:auto; }}
</style></head><body><h1>Comparație longitudinală</h1>
<p class="boundary">{_text(panel.interpretation_boundary)}</p>
{''.join(pair_blocks) if pair_blocks else empty}</body></html>"""
