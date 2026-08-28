"""Unit tests for the reference stub, including failure paths. Stdlib only."""
import unittest

from app.auth import require_token
from app.config import settings
from app.errors import AppError
from app.retries import retry


class AuthTests(unittest.TestCase):
    def test_fails_closed_without_configured_token(self):
        settings.auth_token = ""
        self.assertFalse(require_token("anything"))

    def test_accepts_configured_token(self):
        settings.auth_token = "s3cret-token"
        self.assertTrue(require_token("Bearer s3cret-token"))

    def test_rejects_wrong_token(self):
        settings.auth_token = "s3cret-token"
        self.assertFalse(require_token("Bearer wrong"))


class RetryTests(unittest.TestCase):
    def test_retries_then_succeeds(self):
        calls = {"n": 0}

        @retry(times=3, base_delay=0)
        def flaky():
            calls["n"] += 1
            if calls["n"] < 2:
                raise AppError("not yet")
            return "ok"

        self.assertEqual(flaky(), "ok")
        self.assertEqual(calls["n"], 2)

    def test_gives_up_after_bounded_attempts(self):
        @retry(times=2, base_delay=0)
        def always_fails():
            raise AppError("boom")

        with self.assertRaises(AppError):
            always_fails()


if __name__ == "__main__":
    unittest.main()
