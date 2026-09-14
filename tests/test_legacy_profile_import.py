from __future__ import annotations

import unittest

from szondi3.clinical_protocol import evaluate_clinical_protocol
from szondi3.clinical_report import build_clinical_report
from szondi3.legacy_profile_import import profile_series_from_legacy_text


class LegacyProfileImportTests(unittest.TestCase):
    def test_imports_unlabelled_profile_in_factor_order(self) -> None:
        series = profile_series_from_legacy_text("- + + 0 + + - -")
        self.assertEqual(series.profile_count, 1)
        profile = series.profiles[0]
        self.assertEqual(
            tuple((item.factor, item.symbol) for item in profile.factors),
            (
                ("h", "-"),
                ("s", "+"),
                ("e", "+"),
                ("hy", "0"),
                ("k", "+"),
                ("p", "+"),
                ("d", "-"),
                ("m", "-"),
            ),
        )
        self.assertTrue(all(item.sympathetic is None for item in profile.factors))
        self.assertTrue(all(item.unsympathetic is None for item in profile.factors))

    def test_imports_labelled_profiles_and_preserves_quantum(self) -> None:
        series = profile_series_from_legacy_text(
            "h- s+! e+ hy0 k+ p+ d- m-\n"
            "h0 s- e± hy+ k-! p0 d+ m±!"
        )
        self.assertEqual(series.profile_count, 2)
        first = {item.factor: item for item in series.profiles[0].factors}
        second = {item.factor: item for item in series.profiles[1].factors}
        self.assertEqual(first["s"].symbol, "+!")
        self.assertEqual(first["s"].quantum_level, 1)
        self.assertEqual(second["k"].symbol, "-!")
        self.assertEqual(second["m"].symbol, "±!")
        self.assertEqual(second["m"].quantum_level, 1)

    def test_manual_profile_can_enter_existing_clinical_protocol_pipeline(self) -> None:
        series = profile_series_from_legacy_text("- + + 0 + + - -")
        evaluation = evaluate_clinical_protocol(series, production=True)
        report = build_clinical_report(evaluation)
        self.assertEqual(report.header.profile_count, 1)
        self.assertEqual(
            tuple(item.symbol for item in report.observations[0].factors),
            ("-", "+", "+", "0", "+", "+", "-", "-"),
        )
        self.assertGreater(len(report.findings), 0)

    def test_rejects_missing_factor(self) -> None:
        with self.assertRaisesRegex(ValueError, "exact cei 8 factori"):
            profile_series_from_legacy_text("h- s+ e+ hy0 k+ p+ d-")

    def test_rejects_forced_null_in_foreground_import(self) -> None:
        with self.assertRaisesRegex(ValueError, "token invalid"):
            profile_series_from_legacy_text("h- s+ e+ hy0 k+ p+ d- mø")

    def test_rejects_more_than_ten_profiles(self) -> None:
        text = "\n".join(["- + + 0 + + - -"] * 11)
        with self.assertRaisesRegex(ValueError, "între 1 și 10"):
            profile_series_from_legacy_text(text)


if __name__ == "__main__":
    unittest.main()
