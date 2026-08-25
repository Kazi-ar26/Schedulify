"""
Schedulify Auth API Service

Desktop-side auth operations via HTTP to the backend.
"""

from api_client.client import get_client, save_token


def register(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    role: str,
    school_name: str = None,
    grade_level: str = None,
) -> dict:
    """Register a new account via the API."""
    client = get_client()

    data = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "role": role,
    }
    if school_name:
        data["school_name"] = school_name
    if grade_level:
        data["grade_level"] = grade_level

    result = client.post("/api/auth/register", data)

    # Save token to disk AND update the in-memory singleton
    if result and "access_token" in result:
        save_token(result["access_token"], result.get("user", {}))
        client.set_token(result["access_token"])

    return result


def login(email: str, password: str) -> dict:
    """Login via the API."""
    client = get_client()

    result = client.post("/api/auth/login", {
        "email": email,
        "password": password,
    })

    # Save token to disk AND update the in-memory singleton
    if result and "access_token" in result:
        save_token(result["access_token"], result.get("user", {}))
        client.set_token(result["access_token"])

    return result


def logout():
    """Clear local auth state."""
    from api_client.client import clear_token
    client = get_client()
    client.clear_auth()
    clear_token()


def get_me() -> dict:
    """Get current user profile."""
    client = get_client()
    return client.get("/api/auth/me")
