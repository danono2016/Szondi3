"""Minimal closed-world handoff from Szondi3 to a future narrative model.

The packet deliberately adds no Szondian meaning. It compiles deterministic
whole-series morphology together with the findings, calculations and unresolved
states already exposed by ``ClinicalReport``. For every active finding it also
resolves the already-linked SOURCE_VERIFIED doctrine objects from the local
Doctrine Registry, so a future generative layer receives the exact canonical
support instead of searching freely or restoring missing meaning from pretraining.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import json
from pathlib import Path
from typing import Any, Iterable

from .clinical_protocol import ClinicalProtocolEvaluation
from .clinical_report import ClinicalReport, build_clinical_report
from .profile import VECTOR_FACTORS
from .stimuli import FACTORS


_BASE_SYMBOL_BY_KIND = {
    "null": "0",
    "positive": "+",
    "negative": "-",
    "ambivalent": "±",
}

_REGISTRY_ROOT = Path(__file__).resolve().parents[1] / "doctrine" / "registry"


@dataclass(frozen=True, slots=True)
class FactorSeriesEvidence:
    factor: str
    symbols: tuple[str, ...]
    base_symbols: tuple[str, ...]
    positive_count: int
    negative_count: int
    null_count: int
    ambivalent_count: int
    forced_null_count: int
    tensioned_profiles: tuple[int, ...]
    quantum_total: int


@dataclass(frozen=True, slots=True)
class VectorConfigurationFrequency:
    symbols: tuple[str, str]
    count: int


@dataclass(frozen=True, slots=True)
class VectorSeriesEvidence:
    vector: str
    factors: tuple[str, str]
    symbols: tuple[tuple[str, str], ...]
    base_symbols: tuple[tuple[str, str], ...]
    configuration_frequencies: tuple[VectorConfigurationFrequency, ...]


@dataclass(frozen=True, slots=True)
class CanonicalSourceAnchor:
    stream: str
    unit_start: str
    unit_end: str
    pdf_path: str | None
    printed_page: str | int | None
    visual_arbitration_note: str | None


@dataclass(frozen=True, slots=True)
class CanonicalDoctrineEvidence:
    doctrine_id: str
    source_id: str
    source_layer: str
    source_language: str
    review_status: str
    source_anchors: tuple[CanonicalSourceAnchor, ...]
    source_excerpt: str
    romanian_rendering: str | None
    doctrinal_statement: str | None
    assertion_strength: str | None
    scope_notes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ClinicalEvidencePacket:
    """Finite case-specific evidence boundary for downstream AI synthesis."""

    schema_version: int
    report: ClinicalReport
    factor_series: tuple[FactorSeriesEvidence, ...]
    vector_series: tuple[VectorSeriesEvidence, ...]
    canonical_evidence: tuple[CanonicalDoctrineEvidence, ...]

    def factor(self, factor: str) -> FactorSeriesEvidence:
        matches = tuple(item for item in self.factor_series if item.factor == factor)
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate factor series: {factor}")
        return matches[0]

    def vector(self, vector: str) -> VectorSeriesEvidence:
        matches = tuple(item for item in self.vector_series if item.vector == vector)
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate vector series: {vector}")
        return matches[0]

    def doctrine(self, doctrine_id: str) -> CanonicalDoctrineEvidence:
        matches = tuple(
            item for item in self.canonical_evidence if item.doctrine_id == doctrine_id
        )
        if len(matches) != 1:
            raise KeyError(f"Unknown or duplicate canonical doctrine evidence: {doctrine_id}")
        return matches[0]

    def to_dict(self) -> dict[str, Any]:
        """Return the intended narrative-model payload.

        Therapist synthesis is deliberately excluded: it is manual clinician input,
        not evidence supplied to a generative model. Canonical doctrine evidence is
        contextual support for existing findings; its presence does not authorize a
        downstream model to create additional person-specific claims.
        """
        report = self.report.to_dict()
        return {
            "schema_version": self.schema_version,
            "profile_count": self.report.header.profile_count,
            "production_mode": self.report.header.production_mode,
            "interpretation_release_state": self.report.header.interpretation_release_state,
            "factor_series": [
                {
                    "factor": item.factor,
                    "symbols": list(item.symbols),
                    "base_symbols": list(item.base_symbols),
                    "positive_count": item.positive_count,
                    "negative_count": item.negative_count,
                    "null_count": item.null_count,
                    "ambivalent_count": item.ambivalent_count,
                    "forced_null_count": item.forced_null_count,
                    "tensioned_profiles": list(item.tensioned_profiles),
                    "quantum_total": item.quantum_total,
                }
                for item in self.factor_series
            ],
            "vector_series": [
                {
                    "vector": item.vector,
                    "factors": list(item.factors),
                    "symbols": [list(pair) for pair in item.symbols],
                    "base_symbols": [list(pair) for pair in item.base_symbols],
                    "configuration_frequencies": [
                        {"symbols": list(frequency.symbols), "count": frequency.count}
                        for frequency in item.configuration_frequencies
                    ],
                }
                for item in self.vector_series
            ],
            "calculations": report["calculations"],
            "findings": report["findings"],
            "canonical_evidence": [
                {
                    "doctrine_id": item.doctrine_id,
                    "source_id": item.source_id,
                    "source_layer": item.source_layer,
                    "source_language": item.source_language,
                    "review_status": item.review_status,
                    "source_anchors": [
                        {
                            "stream": anchor.stream,
                            "unit_start": anchor.unit_start,
                            "unit_end": anchor.unit_end,
                            "pdf_path": anchor.pdf_path,
                            "printed_page": anchor.printed_page,
                            "visual_arbitration_note": anchor.visual_arbitration_note,
                        }
                        for anchor in item.source_anchors
                    ],
                    "source_excerpt": item.source_excerpt,
                    "romanian_rendering": item.romanian_rendering,
                    "doctrinal_statement": item.doctrinal_statement,
                    "assertion_strength": item.assertion_strength,
                    "scope_notes": list(item.scope_notes),
                }
                for item in self.canonical_evidence
            ],
            "uncertainties": report["uncertainties"],
        }


def _base_symbol(reaction) -> str:
    if reaction.forced_null:
        return "ø"
    return _BASE_SYMBOL_BY_KIND[reaction.kind]


def _profile_factor_maps(
    evaluation: ClinicalProtocolEvaluation,
) -> tuple[dict[str, Any], ...]:
    """Index each profile once for all factor/vector evidence extraction."""
    return tuple(
        {item.factor: item for item in profile.factors}
        for profile in evaluation.series.profiles
    )


def _factor_series(
    factor_maps: tuple[dict[str, Any], ...],
) -> tuple[FactorSeriesEvidence, ...]:
    result = []
    for factor in FACTORS:
        reactions = tuple(by_factor[factor] for by_factor in factor_maps)
        base_symbols = tuple(_base_symbol(item) for item in reactions)
        result.append(
            FactorSeriesEvidence(
                factor=factor,
                symbols=tuple(item.symbol for item in reactions),
                base_symbols=base_symbols,
                positive_count=base_symbols.count("+"),
                negative_count=base_symbols.count("-"),
                null_count=base_symbols.count("0"),
                ambivalent_count=base_symbols.count("±"),
                forced_null_count=base_symbols.count("ø"),
                tensioned_profiles=tuple(
                    index
                    for index, item in enumerate(reactions, start=1)
                    if item.quantum_level > 0
                ),
                quantum_total=sum(item.quantum_level for item in reactions),
            )
        )
    return tuple(result)


def _vector_series(
    factor_maps: tuple[dict[str, Any], ...],
) -> tuple[VectorSeriesEvidence, ...]:
    result = []
    for vector_name, factors in VECTOR_FACTORS:
        exact_pairs = []
        base_pairs = []
        for by_factor in factor_maps:
            first, second = (by_factor[factor] for factor in factors)
            exact_pairs.append((first.symbol, second.symbol))
            base_pairs.append((_base_symbol(first), _base_symbol(second)))

        counts = Counter(base_pairs)
        frequencies = tuple(
            VectorConfigurationFrequency(symbols=pair, count=count)
            for pair, count in counts.items()
        )
        result.append(
            VectorSeriesEvidence(
                vector=vector_name,
                factors=factors,
                symbols=tuple(exact_pairs),
                base_symbols=tuple(base_pairs),
                configuration_frequencies=frequencies,
            )
        )
    return tuple(result)


def _registry_index(registry_root: Path) -> dict[str, dict[str, Any]]:
    if not registry_root.is_dir():
        raise ValueError(f"Doctrine registry is unavailable: {registry_root}")

    index: dict[str, dict[str, Any]] = {}
    for path in sorted(registry_root.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid doctrine registry JSON at {path.name}:{line_number}"
                    ) from exc
                doctrine_id = record.get("doctrineId")
                if not doctrine_id:
                    continue
                if doctrine_id in index:
                    raise ValueError(f"Duplicate doctrine registry identity: {doctrine_id}")
                index[doctrine_id] = record
    return index


@lru_cache(maxsize=1)
def _default_registry_index() -> dict[str, dict[str, Any]]:
    """Load the immutable packaged doctrine registry once per process."""
    return _registry_index(_REGISTRY_ROOT)


def _canonical_evidence(record: dict[str, Any]) -> CanonicalDoctrineEvidence:
    doctrine_id = record["doctrineId"]
    if record.get("reviewStatus") != "SOURCE_VERIFIED":
        raise ValueError(f"Doctrine is not SOURCE_VERIFIED: {doctrine_id}")

    raw_anchors = record.get("sourceAnchors") or ()
    if not raw_anchors:
        raise ValueError(f"Doctrine lacks canonical source anchors: {doctrine_id}")
    source_excerpt = record.get("sourceExcerpt")
    if not isinstance(source_excerpt, str) or not source_excerpt.strip():
        raise ValueError(f"Doctrine lacks canonical source excerpt: {doctrine_id}")

    anchors = tuple(
        CanonicalSourceAnchor(
            stream=anchor["stream"],
            unit_start=anchor["unitStart"],
            unit_end=anchor["unitEnd"],
            pdf_path=anchor.get("pdfPath"),
            printed_page=anchor.get("printedPage"),
            visual_arbitration_note=anchor.get("visualArbitrationNote"),
        )
        for anchor in raw_anchors
    )
    return CanonicalDoctrineEvidence(
        doctrine_id=doctrine_id,
        source_id=record["sourceId"],
        source_layer=record["sourceLayer"],
        source_language=record["sourceLanguage"],
        review_status=record["reviewStatus"],
        source_anchors=anchors,
        source_excerpt=source_excerpt,
        romanian_rendering=record.get("romanianRendering"),
        doctrinal_statement=record.get("doctrinalStatement"),
        assertion_strength=record.get("assertionStrength"),
        scope_notes=tuple(record.get("scopeNotes") or ()),
    )


def resolve_canonical_evidence(
    doctrine_ids: Iterable[str],
    *,
    registry_root: Path | None = None,
) -> tuple[CanonicalDoctrineEvidence, ...]:
    """Resolve exact local canonical support by doctrine identity, never by similarity."""
    ordered_ids = tuple(dict.fromkeys(doctrine_ids))
    if not ordered_ids:
        return ()

    index = _default_registry_index() if registry_root is None else _registry_index(registry_root)
    resolved = []
    for doctrine_id in ordered_ids:
        try:
            record = index[doctrine_id]
        except KeyError as exc:
            raise ValueError(f"Unknown doctrine evidence identity: {doctrine_id}") from exc
        resolved.append(_canonical_evidence(record))
    return tuple(resolved)


def _required_doctrine(report: ClinicalReport) -> tuple[tuple[str, ...], dict[str, set[str]]]:
    ordered_ids: list[str] = []
    allowed_sources: dict[str, set[str]] = {}
    for finding in report.findings:
        for doctrine_id in finding.doctrine_ids:
            if doctrine_id not in allowed_sources:
                ordered_ids.append(doctrine_id)
                allowed_sources[doctrine_id] = set()
            allowed_sources[doctrine_id].update(finding.source_ids)
    return tuple(ordered_ids), allowed_sources


def build_clinical_evidence_packet(
    evaluation: ClinicalProtocolEvaluation,
) -> ClinicalEvidencePacket:
    """Compile the smallest complete handoff needed for grounded narrative work."""
    if not isinstance(evaluation, ClinicalProtocolEvaluation):
        raise TypeError("Clinical evidence packet requires a ClinicalProtocolEvaluation")

    report = build_clinical_report(evaluation)
    doctrine_ids, allowed_sources = _required_doctrine(report)
    canonical_evidence = resolve_canonical_evidence(doctrine_ids)
    for evidence in canonical_evidence:
        if evidence.source_id not in allowed_sources[evidence.doctrine_id]:
            raise ValueError(
                "Canonical doctrine source does not match executable claim provenance: "
                f"{evidence.doctrine_id} -> {evidence.source_id}"
            )

    factor_maps = _profile_factor_maps(evaluation)
    return ClinicalEvidencePacket(
        schema_version=2,
        report=report,
        factor_series=_factor_series(factor_maps),
        vector_series=_vector_series(factor_maps),
        canonical_evidence=canonical_evidence,
    )
