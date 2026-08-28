"""Environment-driven settings with safe defaults. Stdlib only."""
import os


class Settings:
    def __init__(self):
        self.host = os.getenv("REFAPP_HOST", "127.0.0.1")
        self.port = int(os.getenv("REFAPP_PORT", "8000"))
        self.log_level = os.getenv("REFAPP_LOG_LEVEL", "INFO")
        self.auth_token = os.environ.get("REFAPP_AUTH_TOKEN", "")
        self.db_url = os.getenv("REFAPP_DB_URL", "")


settings = Settings()
