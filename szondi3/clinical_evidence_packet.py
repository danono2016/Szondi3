"""Minimal closed-world handoff from Szondi3 to a future narrative model.

The packet deliberately adds no Szondian meaning. It compiles deterministic
whole-series morphology together with the findings, calculations and unresolved
states already exposed by ``ClinicalReport``. A future generative layer should
receive this object instead of recounting the raw Zehnerserie or inventing missing
interpretation from model knowledge.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

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
class ClinicalEvidencePacket:
    """Finite case-specific evidence boundary for downstream AI synthesis."""

    schema_version: int
    report: ClinicalReport
    factor_series: tuple[FactorSeriesEvidence, ...]
    vector_series: tuple[VectorSeriesEvidence, ...]

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

    def to_dict(self) -> dict[str, Any]:
        """Return the intended narrative-model payload.

        Therapist synthesis is deliberately excluded: it is manual clinician input,
        not evidence supplied to a generative model.
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
            "uncertainties": report["uncertainties"],
        }


def _base_symbol(reaction) -> str:
    if reaction.forced_null:
        return "ø"
    return _BASE_SYMBOL_BY_KIND[reaction.kind]


def _factor_series(evaluation: ClinicalProtocolEvaluation) -> tuple[FactorSeriesEvidence, ...]:
    result = []
    for factor in FACTORS:
        reactions = tuple(
            next(item for item in profile.factors if item.factor == factor)
            for profile in evaluation.series.profiles
        )
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


def _vector_series(evaluation: ClinicalProtocolEvaluation) -> tuple[VectorSeriesEvidence, ...]:
    result = []
    for vector_name, factors in VECTOR_FACTORS:
        exact_pairs = []
        base_pairs = []
        for profile in evaluation.series.profiles:
            by_factor = {item.factor: item for item in profile.factors}
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


def build_clinical_evidence_packet(
    evaluation: ClinicalProtocolEvaluation,
) -> ClinicalEvidencePacket:
    """Compile the smallest complete handoff needed for grounded narrative work."""
    if not isinstance(evaluation, ClinicalProtocolEvaluation):
        raise TypeError("Clinical evidence packet requires a ClinicalProtocolEvaluation")

    return ClinicalEvidencePacket(
        schema_version=1,
        report=build_clinical_report(evaluation),
        factor_series=_factor_series(evaluation),
        vector_series=_vector_series(evaluation),
    )
