import unittest
from unittest.mock import patch

from szondi3 import __main__ as package_entrypoint


class PackageEntrypointTests(unittest.TestCase):
    def test_default_package_entrypoint_delegates_to_archive_enabled_clinician_shell(self):
        argv = ["--port", "0", "--no-archive"]
        with patch.object(package_entrypoint, "archive_browser_main", return_value=17) as delegated:
            result = package_entrypoint.main(argv)

        self.assertEqual(result, 17)
        delegated.assert_called_once_with(argv)


if __name__ == "__main__":
    unittest.main()
