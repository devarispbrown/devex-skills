"""Configuration for the MySQL connector.

Loads connection settings from environment variables with safe defaults.
"""
import os

DEFAULT_PORT = 3306
DEFAULT_TIMEOUT_SECONDS = 30


def load_config(env_prefix="MYSQL"):
    return {
        "host": os.environ.get(f"{env_prefix}_HOST", "localhost"),
        "port": int(os.environ.get(f"{env_prefix}_PORT", DEFAULT_PORT)),
        "database": os.environ.get(f"{env_prefix}_DATABASE", "app"),
        "user": os.environ.get(f"{env_prefix}_USER", "app"),
        "password": os.environ.get(f"{env_prefix}_PASSWORD", ""),
        "ssl_mode": os.environ.get(f"{env_prefix}_SSL_MODE", "require"),
        "charset": os.environ.get(f"{env_prefix}_CHARSET", "utf8mb4"),
        "pool_size": int(os.environ.get(f"{env_prefix}_POOL_SIZE", 10)),
        "timeout_seconds": int(
            os.environ.get(f"{env_prefix}_TIMEOUT", DEFAULT_TIMEOUT_SECONDS)
        ),
    }
