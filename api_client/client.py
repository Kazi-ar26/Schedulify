"""
Schedulify Desktop API Client

HTTP client for communicating with the FastAPI backend.
Stores the JWT token for authentication.
Provides methods matching the service interfaces.
"""

import json
import os
import logging
from pathlib import Path
from typing import Optional

import httpx


# -------------------------------------------------
# Configuration
# -------------------------------------------------

CONFIG_DIR = Path.home() / ".schedulify"
TOKEN_FILE = CONFIG_DIR / "auth_token"
USER_FILE = CONFIG_DIR / "auth_user"


def _get_base_url() -> str:
    """Get the API base URL from environment or config."""
    url = os.environ.get("SCHEDULIFY_API_URL")
    if url:
        return url.rstrip("/")

    # Check config file
    config_path = Path(__file__).resolve().parent.parent / "config.json"
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
            api_url = config.get("api", {}).get("base_url", "")
            if api_url:
                return api_url.rstrip("/")
        except Exception:
            pass

    return "http://localhost:8000"


BASE_URL = _get_base_url()


# -------------------------------------------------
# Token Management
# -------------------------------------------------

def save_token(token: str, user_data: dict):
    """Persist auth token and user data to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token)
    USER_FILE.write_text(json.dumps(user_data))


def load_token() -> Optional[str]:
    """Load saved auth token from disk."""
    try:
        if TOKEN_FILE.exists():
            return TOKEN_FILE.read_text().strip()
    except Exception:
        pass
    return None


def load_user_data() -> Optional[dict]:
    """Load saved user data from disk."""
    try:
        if USER_FILE.exists():
            return json.loads(USER_FILE.read_text())
    except Exception:
        pass
    return None


def clear_token():
    """Remove saved auth token."""
    try:
        if TOKEN_FILE.exists():
            TOKEN_FILE.unlink()
        if USER_FILE.exists():
            USER_FILE.unlink()
    except Exception:
        pass


# -------------------------------------------------
# HTTP Client
# -------------------------------------------------

class APIClient:
    """
    HTTP client for making authenticated requests
    to the Schedulify backend.
    """

    def __init__(self, base_url: str | None = None):
        self.base_url = (base_url or BASE_URL).rstrip("/")
        self._token: str | None = load_token()
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=30.0,
        )

    @property
    def token(self) -> str | None:
        return self._token

    def set_token(self, token: str):
        self._token = token
        save_token(token, {})

    def clear_auth(self):
        self._token = None
        clear_token()

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def request(
        self,
        method: str,
        path: str,
        json_data: dict | None = None,
    ) -> dict | list | None:
        """
        Make an authenticated HTTP request.

        Returns parsed JSON response, or None for 204.
        Raises APIError on non-2xx responses.
        """
        try:
            response = self._client.request(
                method,
                path,
                json=json_data,
                headers=self._headers(),
            )

            if response.status_code == 204:
                return None

            data = response.json()

            if response.status_code >= 400:
                detail = data.get("detail", "Unknown error")
                raise APIError(
                    status_code=response.status_code,
                    detail=detail,
                )

            return data

        except httpx.ConnectError:
            raise APIError(
                status_code=0,
                detail=(
                    "Cannot connect to server. "
                    f"Ensure the backend is running at {self.base_url}"
                ),
            )
        except httpx.TimeoutException:
            raise APIError(
                status_code=0,
                detail="Request timed out. Please try again.",
            )
        except APIError:
            raise
        except Exception as e:
            raise APIError(
                status_code=0,
                detail=f"Network error: {str(e)}",
            )

    def get(self, path: str) -> dict | list | None:
        return self.request("GET", path)

    def post(self, path: str, data: dict | None = None) -> dict | list | None:
        return self.request("POST", path, data)

    def put(self, path: str, data: dict | None = None) -> dict | list | None:
        return self.request("PUT", path, data)

    def delete(self, path: str) -> dict | list | None:
        return self.request("DELETE", path)


class APIError(Exception):
    """Error from API call."""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


# -------------------------------------------------
# Singleton instance
# -------------------------------------------------

_client: APIClient | None = None


def get_client() -> APIClient:
    """Returns the singleton API client."""
    global _client
    if _client is None:
        _client = APIClient()
    return _client
