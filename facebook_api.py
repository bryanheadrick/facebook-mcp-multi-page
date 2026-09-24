"""Thin, hardened wrapper over the Facebook Graph API.

Hardening added on top of the original single-tenant client:
- HTTP status is checked; a Graph API error is raised as ``FacebookAPIError``
  instead of being returned as if it were a successful payload.
- Every request has a timeout; rate-limit / transient errors are retried with
  backoff.
- The Page access token is never leaked: error text is passed through ``scrub``.
- Credentials are resolved per ``client_id`` from ``clients.json`` (multi-Page
  support), not from a single pair of module-level constants.
- The unsolicited-DM tool was removed (Meta policy risk).
"""
from __future__ import annotations

import time
from typing import Any

import requests

from config import GRAPH_API_BASE_URL, MAX_RETRIES, REQUEST_TIMEOUT_SECONDS, get_client_credentials
from sanitize import scrub

# Meta error codes that are transient / rate-limit related and worth retrying.
_RETRYABLE_ERROR_CODES = {4, 17, 32, 341, 613}


class FacebookAPIError(Exception):
    """A Graph API call failed. Carries only scrubbed, safe context."""

    def __init__(self, message: str, *, status_code: int | None = None, error_code: int | None = None):
        self.status_code = status_code
        self.error_code = error_code
        self.safe_message = scrub(message)
        super().__init__(self.safe_message)


def _safe_json(response: requests.Response) -> dict[str, Any]:
    try:
        data = response.json()
    except ValueError:
        return {"error": {"message": scrub(response.text)[:300]}}
    return data if isinstance(data, dict) else {"data": data}


class FacebookAPI:
    def __init__(self, client_id: str, *, base_url: str | None = None,
                 timeout: float | None = None, max_retries: int | None = None):
        self.client_id = client_id
        self.access_token, self.page_id = get_client_credentials(client_id)
        self.base_url = base_url or GRAPH_API_BASE_URL
        self.timeout = timeout if timeout is not None else REQUEST_TIMEOUT_SECONDS
        self.max_retries = max_retries if max_retries is not None else MAX_RETRIES

    # Generic Graph API request method (hardened)
    def _request(self, method: str, endpoint: str, params: dict[str, Any], json: dict[str, Any] = None) -> dict[str, Any]:
        if not self.access_token or not self.page_id:
            raise FacebookAPIError(
                f"Facebook credentials are not configured for client_id '{self.client_id}'."
            )

        url = f"{self.base_url}/{endpoint}"
        call_params = dict(params or {})
        call_params["access_token"] = self.access_token

        attempt = 0
        while True:
            attempt += 1
            try:
                response = requests.request(method, url, params=call_params, json=json, timeout=self.timeout)
            except requests.RequestException as exc:
                raise FacebookAPIError(f"HTTP request to Facebook failed: {exc}") from None

            data = _safe_json(response)
            error = data.get("error") if isinstance(data, dict) else None
            if response.ok and not error:
                return data

            code = (error or {}).get("code")
            if attempt <= self.max_retries and (response.status_code == 429 or code in _RETRYABLE_ERROR_CODES):
                time.sleep(min(2.0, 0.5 * (2 ** (attempt - 1))))
                continue

            message = (error or {}).get("message") or f"HTTP {response.status_code}"
            raise FacebookAPIError(message, status_code=response.status_code, error_code=code)

    def post_message(self, message: str) -> dict[str, Any]:
        return self._request("POST", f"{self.page_id}/feed", {"message": message})

    def reply_to_comment(self, comment_id: str, message: str) -> dict[str, Any]:
        return self._request("POST", f"{comment_id}/comments", {"message": message})

    def get_posts(self) -> dict[str, Any]:
        return self._request("GET", f"{self.page_id}/posts", {"fields": "id,message,created_time"})

    def get_comments(self, post_id: str) -> dict[str, Any]:
        return self._request("GET", f"{post_id}/comments", {"fields": "id,message,from,created_time"})

    def delete_post(self, post_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"{post_id}", {})

    def delete_comment(self, comment_id: str) -> dict[str, Any]:
        return self._request("DELETE", f"{comment_id}", {})

    def hide_comment(self, comment_id: str) -> dict[str, Any]:
        """Hide a comment from the Page."""
        return self._request("POST", f"{comment_id}", {"is_hidden": True})

    def unhide_comment(self, comment_id: str) -> dict[str, Any]:
        """Unhide a previously hidden comment."""
        return self._request("POST", f"{comment_id}", {"is_hidden": False})

    def get_insights(self, post_id: str, metric: str, period: str = "lifetime") -> dict[str, Any]:
        return self._request("GET", f"{post_id}/insights", {"metric": metric, "period": period})

    def get_bulk_insights(self, post_id: str, metrics: list[str], period: str = "lifetime") -> dict[str, Any]:
        metric_str = ",".join(metrics)
        return self.get_insights(post_id, metric_str, period)

    def post_image_to_facebook(self, image_url: str, caption: str) -> dict[str, Any]:
        params = {
            "url": image_url,
            "caption": caption
        }
        return self._request("POST", f"{self.page_id}/photos", params)

    def update_post(self, post_id: str, new_message: str) -> dict[str, Any]:
        return self._request("POST", f"{post_id}", {"message": new_message})

    def schedule_post(self, message: str, publish_time: int) -> dict[str, Any]:
        params = {
            "message": message,
            "published": False,
            "scheduled_publish_time": publish_time,
        }
        return self._request("POST", f"{self.page_id}/feed", params)

    def get_page_fan_count(self) -> int:
        data = self._request("GET", f"{self.page_id}", {"fields": "fan_count"})
        return data.get("fan_count", 0)

    def get_post_share_count(self, post_id: str) -> int:
        data = self._request("GET", f"{post_id}", {"fields": "shares"})
        return data.get("shares", {}).get("count", 0)

    def get_comment_replies(self, comment_id: str) -> dict[str, Any]:
        return self._request("GET", f"{comment_id}/comments", {"fields": "id,message,from,created_time"})

    def get_post_permalink(self, post_id: str) -> dict[str, Any]:
        return self._request("GET", f"{post_id}", {"fields": "permalink_url"})

    def get_scheduled_posts(self) -> dict[str, Any]:
        return self._request("GET", f"{self.page_id}/scheduled_posts", {"fields": "id,message,scheduled_publish_time"})

    def get_page_info(self) -> dict[str, Any]:
        fields = "name,about,category,website,emails,phone,description,location"
        return self._request("GET", f"{self.page_id}", {"fields": fields})
