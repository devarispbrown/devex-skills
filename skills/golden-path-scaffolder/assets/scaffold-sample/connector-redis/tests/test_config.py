import os
import unittest

from config import load_config


class TestLoadConfig(unittest.TestCase):
    def test_defaults(self):
        cfg = load_config()
        self.assertEqual(cfg["host"], "localhost")
        self.assertEqual(cfg["port"], 6379)
        self.assertEqual(cfg["ssl_mode"], "require")

    def test_environment_overrides(self):
        os.environ["REDIS_HOST"] = "cache.internal"
        try:
            cfg = load_config()
            self.assertEqual(cfg["host"], "cache.internal")
        finally:
            os.environ.pop("REDIS_HOST", None)


if __name__ == "__main__":
    unittest.main()
