"""Multi-client credential resolution: clients.json loading and lookup."""
import json

import pytest

import config
from conftest import FAKE_CLIENT_ID, FAKE_PAGE_ID, FAKE_TOKEN


def test_load_clients_returns_configured_clients(clients_file):
    clients = config.load_clients()
    assert clients == {FAKE_CLIENT_ID: {"access_token": FAKE_TOKEN, "page_id": FAKE_PAGE_ID}}


def test_load_clients_missing_file_raises(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "CLIENTS_FILE", str(tmp_path / "does-not-exist.json"))
    with pytest.raises(FileNotFoundError):
        config.load_clients()


def test_get_client_credentials_known_client(clients_file):
    access_token, page_id = config.get_client_credentials(FAKE_CLIENT_ID)
    assert access_token == FAKE_TOKEN
    assert page_id == FAKE_PAGE_ID


def test_get_client_credentials_unknown_client_raises(clients_file):
    with pytest.raises(config.UnknownClientError) as ei:
        config.get_client_credentials("nonexistent")
    assert FAKE_CLIENT_ID in str(ei.value)  # known clients are listed to help debugging


def test_get_client_credentials_unknown_client_with_no_clients_configured(tmp_path, monkeypatch):
    path = tmp_path / "clients.json"
    path.write_text(json.dumps({}))
    monkeypatch.setattr(config, "CLIENTS_FILE", str(path))
    with pytest.raises(config.UnknownClientError) as ei:
        config.get_client_credentials("anything")
    assert "(none configured)" in str(ei.value)
