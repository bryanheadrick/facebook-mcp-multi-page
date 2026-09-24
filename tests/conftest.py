"""Shared fixtures. Every test runs against a stubbed ``requests`` — no real Graph
API calls, no real token, no network."""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config  # noqa: E402
import facebook_api  # noqa: E402
from _fakes import FakeResponse  # noqa: E402

# A realistic-looking (fake) Page token so scrub assertions are meaningful.
FAKE_TOKEN = "EAAsecrettoken1234567890abcdefGHIJ"
FAKE_CLIENT_ID = "acme"
FAKE_PAGE_ID = "PAGE123"


@pytest.fixture
def clients_file(tmp_path, monkeypatch):
    """Point config.CLIENTS_FILE at a temp clients.json with one fake client."""
    path = tmp_path / "clients.json"
    path.write_text(json.dumps({
        FAKE_CLIENT_ID: {"access_token": FAKE_TOKEN, "page_id": FAKE_PAGE_ID},
    }))
    monkeypatch.setattr(config, "CLIENTS_FILE", str(path))
    return path


@pytest.fixture
def api(clients_file):
    return facebook_api.FacebookAPI(FAKE_CLIENT_ID, timeout=5, max_retries=2)


@pytest.fixture
def stub(monkeypatch):
    """Records calls and returns queued responses. Queue items may be a FakeResponse
    or an Exception (raised to simulate a network failure). Empty queue → generic OK.
    ``time.sleep`` is patched out so retry tests never actually wait."""
    calls: list[dict] = []
    queue: list = []

    def fake_request(method, url, params=None, json=None, timeout=None):
        calls.append({"method": method, "url": url, "params": params,
                      "json": json, "timeout": timeout})
        if not queue:
            return FakeResponse({"id": "ok"})
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item

    monkeypatch.setattr(facebook_api.requests, "request", fake_request)
    monkeypatch.setattr(facebook_api.time, "sleep", lambda *_a, **_k: None)
    return {"calls": calls, "queue": queue}
