"""Fixture: a JSON response consumer."""
import json

import requests


def fetch_user(user_id):
    resp = requests.get(f"https://api.example.test/users/{user_id}")
    data = json.loads(resp.text)
    return data["name"], data["role"]
