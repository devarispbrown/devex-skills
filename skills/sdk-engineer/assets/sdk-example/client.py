"""Minimal fixture client for the Widgets API (subset only)."""

class Widget:
    def __init__(self, widget_id, name):
        self.id = widget_id
        self.name = name

class WidgetsClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def list_widgets(self):
        return [Widget("w-1", "alpha")]
