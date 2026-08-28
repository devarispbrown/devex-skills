"""Sample app: reads the same keys from env vars and a YAML config file."""
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

load_dotenv()

with open("config.yaml") as fh:
    cfg = yaml.safe_load(fh)

api_key = os.getenv("API_KEY", "changeme") or cfg["api_key"]
timeout = int(os.getenv("TIMEOUT", "30") or cfg["timeout"])
db_password = os.environ.get("DB_PASSWORD", "postgres")
