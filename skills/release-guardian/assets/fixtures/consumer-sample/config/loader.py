"""Fixture: a config parser consumer."""
import configparser
import os

parser = configparser.ConfigParser()
parser.read(os.environ.get("APP_CONFIG", "app.ini"))
timeout = parser.getfloat("client", "timeout")
retries = parser.getint("client", "retries", fallback=3)
