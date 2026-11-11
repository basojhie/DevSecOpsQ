import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/validate_scope.py"

class ScopeRules(unittest.TestCase):
    def test_domain_validation(self):
        spec = importlib.util.spec_from_file_location("scope", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(module.valid_domain("example.com"))
        self.assertFalse(module.valid_domain("*.example.com"))
        self.assertFalse(module.valid_domain("https://example.com"))
        self.assertFalse(module.valid_domain("127.0.0.1"))
        self.assertFalse(module.valid_domain("example.com/path"))

if __name__ == "__main__":
    unittest.main()
