from szondi3.profile import build_profile
from szondi3.scoring import FactorReaction
from szondi3.series import ProfileSeries
from szondi3.series_morphology import series_morphology_facts


_FACTORS = ("h", "s", "e", "hy", "k", "p", "d", "m")
_KIND = {"0": "null", "+": "positive", "-": "negative", "±": "ambivalent"}


def _reaction(factor: str, symbol: str) -> FactorReaction:
    base = "±" if symbol.startswith("±") else symbol[0]
    quantum = symbol.count("!")
    return FactorReaction(
        factor=factor,
        sympathetic=0,
        unsympathetic=0,
        kind=_KIND[base],
        symbol=symbol,
        quantum_level=quantum,
        forced_null=False,
    )


def _profile(*symbols: str):
    return build_profile(_reaction(factor, symbol) for factor, symbol in zip(_FACTORS, symbols))


def _facts_by_key(series: ProfileSeries):
    return {fact.key: fact.value for fact in series_morphology_facts(series)}


def test_ten_profile_morphology_counts_factor_tension_and_vector_gestalts():
    series = ProfileSeries(
        (
            _profile("+!", "0", "0", "-", "-", "±", "+", "-"),
            _profile("+!", "0", "-", "-", "-", "+", "+", "-"),
            _profile("+", "0", "-", "-", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-"),
            _profile("+", "0", "0", "-", "+", "±", "+", "-!!"),
            _profile("+!", "0", "-", "-!", "+", "±", "+", "-!"),
            _profile("+!", "-", "-", "0", "+", "+", "+", "-!"),
            _profile("+!", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "-", "+", "±", "+", "-!"),
            _profile("+", "0", "-", "0", "±", "±", "+", "-!"),
        )
    )
    facts = _facts_by_key(series)

    assert facts["series.profile_count"] == 10
    assert facts["series.factor.h.base_symbol.positive.count"] == 10
    assert facts["series.factor.h.quantum_level.1.count"] == 6
    assert facts["series.factor.s.base_symbol.null.count"] == 9
    assert facts["series.factor.e.base_symbol.negative.count"] == 8
    assert facts["series.factor.hy.base_symbol.negative.count"] == 8
    assert facts["series.factor.k.base_symbol.negative.count"] == 2
    assert facts["series.factor.k.base_symbol.positive.count"] == 7
    assert facts["series.factor.k.base_symbol.ambivalent.count"] == 1
    assert facts["series.factor.p.base_symbol.positive.count"] == 3
    assert facts["series.factor.p.base_symbol.ambivalent.count"] == 7
    assert facts["series.factor.d.base_symbol.positive.count"] == 10
    assert facts["series.factor.m.base_symbol.negative.count"] == 10
    assert facts["series.factor.m.tensioned.count"] == 7
    assert facts["series.factor.m.quantum_level.2.count"] == 1

    assert facts["series.vector.P.configuration.negative_negative.count"] == 6
    assert facts["series.vector.P.configuration.null_negative.count"] == 2
    assert facts["series.vector.P.configuration.negative_null.count"] == 2

    assert facts["series.vector.Sch.configuration.negative_ambivalent.count"] == 1
    assert facts["series.vector.Sch.configuration.negative_positive.count"] == 1
    assert facts["series.vector.Sch.configuration.positive_positive.count"] == 2
    assert facts["series.vector.Sch.configuration.positive_ambivalent.count"] == 5
    assert facts["series.vector.Sch.configuration.ambivalent_ambivalent.count"] == 1

    assert facts["series.vector.C.configuration.positive_negative.count"] == 10


def test_forced_null_is_not_counted_as_real_zero_or_vector_zero():
    profile = _profile("+", "0", "-", "-", "+", "±", "+", "-")
    factors = list(profile.factors)
    s_index = _FACTORS.index("s")
    s = factors[s_index]
    factors[s_index] = FactorReaction(
        factor=s.factor,
        sympathetic=s.sympathetic,
        unsympathetic=s.unsympathetic,
        kind=s.kind,
        symbol="ø",
        quantum_level=s.quantum_level,
        forced_null=True,
    )
    series = ProfileSeries((build_profile(factors),))
    facts = _facts_by_key(series)

    assert facts["series.factor.s.base_symbol.null.count"] == 0
    assert facts["series.factor.s.forced_null.count"] == 1
    assert facts["series.vector.S.undefined_configuration.count"] == 1
    assert facts["series.vector.S.configuration.positive_null.count"] == 0
