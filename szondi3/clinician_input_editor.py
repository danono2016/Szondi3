"""Clinician-owned context and synthesis editor over ``ClinicianWorkspace``.

This layer edits only explicit clinician-authored material. Applying an edit rebuilds
integration/report composition from the same canonical case runs; it never writes
clinician text into P1 facts, P2B activation, canonical evidence, or release
provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Sequence

from .clinical_integration import ClinicianContextItem
from .clinician_workspace import ClinicianWorkspace, build_clinician_workspace
from .longitudinal_comparison import LongitudinalCaseRef


@dataclass(frozen=True, slots=True)
class ClinicianInputEditorState:
    clinician_context: tuple[ClinicianContextItem, ...]
    clinician_synthesis: str | None
    context_epistemic_role: str = "EXTERNAL_CASE_CONTEXT_NOT_SZONDI_EVIDENCE"
    synthesis_authorship: str = "MANUAL_CLINICIAN_INPUT_ONLY"


def build_clinician_input_editor(
    workspace: ClinicianWorkspace,
) -> ClinicianInputEditorState:
    """Read the current clinician-owned input into an immutable editor state."""
    if not isinstance(workspace, ClinicianWorkspace):
        raise TypeError("Clinician input editor requires a ClinicianWorkspace")
    return ClinicianInputEditorState(
        clinician_context=workspace.report.clinician_context,
        clinician_synthesis=workspace.report.clinician_synthesis.text,
    )


def update_clinician_input_editor(
    state: ClinicianInputEditorState,
    *,
    clinician_context: Sequence[ClinicianContextItem] | None = None,
    clinician_synthesis: str | None = None,
    clear_synthesis: bool = False,
) -> ClinicianInputEditorState:
    """Return a validated draft state without touching any case runtime.

    ``clinician_context=None`` means keep the current context. ``clear_synthesis`` is
    explicit because ``clinician_synthesis=None`` otherwise means keep the current
    synthesis.
    """
    if not isinstance(state, ClinicianInputEditorState):
        raise TypeError("state must be a ClinicianInputEditorState")
    if clear_synthesis and clinician_synthesis is not None:
        raise ValueError("Cannot set and clear clinician_synthesis simultaneously")

    context = state.clinician_context
    if clinician_context is not None:
        context = tuple(clinician_context)
        if any(not isinstance(item, ClinicianContextItem) for item in context):
            raise TypeError("clinician_context must contain only ClinicianContextItem objects")

    synthesis = state.clinician_synthesis
    if clear_synthesis:
        synthesis = None
    elif clinician_synthesis is not None:
        if not isinstance(clinician_synthesis, str):
            raise TypeError("clinician_synthesis must be a string")
        if not clinician_synthesis.strip():
            raise ValueError("clinician_synthesis cannot be blank")
        synthesis = clinician_synthesis

    return ClinicianInputEditorState(
        clinician_context=context,
        clinician_synthesis=synthesis,
    )


def apply_clinician_input_editor(
    workspace: ClinicianWorkspace,
    state: ClinicianInputEditorState,
) -> ClinicianWorkspace:
    """Apply clinician-owned text by rebuilding composition over identical runs."""
    if not isinstance(workspace, ClinicianWorkspace):
        raise TypeError("Clinician input application requires a ClinicianWorkspace")
    if not isinstance(state, ClinicianInputEditorState):
        raise TypeError("state must be a ClinicianInputEditorState")

    history_refs = tuple(
        LongitudinalCaseRef(case_id=item.case_id, run=item.run)
        for item in workspace.history
    )
    current_ref = LongitudinalCaseRef(
        case_id=workspace.current.case_id,
        run=workspace.current.run,
    )
    updated = build_clinician_workspace(
        current_ref,
        prior_cases=history_refs,
        clinician_context=state.clinician_context,
        clinician_synthesis=state.clinician_synthesis,
    )

    if tuple(item.run for item in updated.history) != tuple(item.run for item in workspace.history):
        raise ValueError("Clinician input edit changed historical case runs")
    if updated.current.run is not workspace.current.run:
        raise ValueError("Clinician input edit changed current case run")
    return updated


def _text(value: object) -> str:
    return escape("" if value is None else str(value), quote=True)


def render_clinician_input_editor_html(state: ClinicianInputEditorState) -> str:
    """Render the clinician-owned text area; submission/persistence belongs to app shell."""
    if not isinstance(state, ClinicianInputEditorState):
        raise TypeError("Clinician input renderer requires a ClinicianInputEditorState")

    context_blocks = "".join(
        '<fieldset class="context-item">'
        f'<legend>{_text(item.label)}</legend>'
        f'<p class="boundary">{_text(item.authorship)} · {_text(item.epistemic_role)}</p>'
        f'<label>Etichetă<input name="context_label_{index}" value="{_text(item.label)}"></label>'
        f'<label>Context<textarea name="context_text_{index}" rows="5">{_text(item.text)}</textarea></label>'
        "</fieldset>"
        for index, item in enumerate(state.clinician_context, start=1)
    )
    if not context_blocks:
        context_blocks = '<p class="empty">Nu există încă elemente de context introduse de clinician.</p>'

    synthesis = _text(state.clinician_synthesis)
    return f"""<!doctype html>
<html lang="ro"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Szondi3 — integrare clinică manuală</title><style>
:root {{ font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
body {{ max-width: 900px; margin:0 auto; padding:1.5rem; color:#1f2328; line-height:1.45; }}
.boundary {{ color:#57606a; font-size:.88rem; }} .notice {{ border-left:4px solid #57606a; background:#f6f8fa; padding:.7rem 1rem; }}
fieldset {{ margin:1rem 0; border:1px solid #d0d7de; }} label {{ display:block; font-weight:650; margin:.6rem 0; }}
input, textarea {{ display:block; width:100%; box-sizing:border-box; margin-top:.3rem; padding:.55rem; font:inherit; }} textarea {{ resize:vertical; }}
.empty {{ color:#57606a; font-style:italic; }}
</style></head><body>
<h1>Integrare clinică manuală</h1>
<div class="notice"><strong>Separare epistemică</strong><p>Contextul și sinteza de aici aparțin clinicianului. Ele nu devin fapte Szondi, nu activează claims P2B și nu modifică proveniența doctrinară.</p></div>
<form>
<section><h2>Context extern</h2><p class="boundary">{_text(state.context_epistemic_role)}</p>{context_blocks}</section>
<section><h2>Sinteza clinicianului</h2><p class="boundary">{_text(state.synthesis_authorship)}</p>
<label>Sinteză<textarea name="clinician_synthesis" rows="12">{synthesis}</textarea></label></section>
<p class="boundary">Acest renderer este doar suprafața editorului. Salvarea și persistența vor aparține app shell-ului; motorul clinic rămâne neschimbat.</p>
</form></body></html>"""
