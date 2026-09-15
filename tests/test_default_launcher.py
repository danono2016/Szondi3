import unittest

import szondi3.__main__ as default_launcher
from szondi3 import clinician_alpha_app_v3, clinician_alpha_app_v4


class DefaultLauncherTests(unittest.TestCase):
    def test_python_m_szondi3_uses_stable_v3_launcher(self):
        self.assertIs(default_launcher.alpha_clinician_main, clinician_alpha_app_v3.main)
        self.assertIsNot(default_launcher.alpha_clinician_main, clinician_alpha_app_v4.main)

    def test_experimental_v4_remains_explicitly_invokable(self):
        self.assertTrue(callable(clinician_alpha_app_v4.main))


if __name__ == "__main__":
    unittest.main()
