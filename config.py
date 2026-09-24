import json
import os

GRAPH_API_VERSION = "v22.0"
GRAPH_API_BASE_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}"

CLIENTS_FILE = os.getenv("FACEBOOK_CLIENTS_FILE", os.path.join(os.path.dirname(__file__), "clients.json"))


class UnknownClientError(Exception):
    pass


def load_clients() -> dict[str, dict[str, str]]:
    if not os.path.exists(CLIENTS_FILE):
        raise FileNotFoundError(
            f"Clients file not found at {CLIENTS_FILE}. "
            "Copy clients.example.json to clients.json and fill in each client's "
            "access_token and page_id."
        )

    with open(CLIENTS_FILE) as f:
        return json.load(f)


def get_client_credentials(client_id: str) -> tuple[str, str]:
    """Return (access_token, page_id) for a client slug."""
    clients = load_clients()

    if client_id not in clients:
        raise UnknownClientError(
            f"Unknown client_id '{client_id}'. Known clients: {', '.join(sorted(clients)) or '(none configured)'}"
        )

    client = clients[client_id]
    return client["access_token"], client["page_id"]
