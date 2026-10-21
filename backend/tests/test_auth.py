"""
Unit Tests for Authentication and Google Sign-In
Verifies user registration, OAuth provider linkage, session management, and JWT validation.
"""

from app.models.user import User
from app.models.oauth import OAuthAccount
from app.models.session import UserSession


def test_google_auth_signup_new_user(client, db_session):
    """Verify Google sign-up creates User, OAuthAccount, and UserSession tables."""
    payload = {
        "email": "marcus.vance@techlead.com",
        "full_name": "Marcus Vance",
        "avatar_url": "https://api.dicebear.com/7.x/avataaars/svg?seed=Marcus",
        "sub": "google_sub_998877",
        "role": "sales_rep"
    }

    response = client.post("/api/auth/google", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "marcus.vance@techlead.com"
    assert data["user"]["full_name"] == "Marcus Vance"
    assert data["user"]["is_verified"] is True

    # Verify tables in database
    user = db_session.query(User).filter(User.email == "marcus.vance@techlead.com").first()
    assert user is not None
    assert user.full_name == "Marcus Vance"

    oauth_account = db_session.query(OAuthAccount).filter(OAuthAccount.user_id == user.id).first()
    assert oauth_account is not None
    assert oauth_account.provider == "google"
    assert oauth_account.provider_user_id == "google_sub_998877"

    session = db_session.query(UserSession).filter(UserSession.user_id == user.id).first()
    assert session is not None
    assert session.is_revoked is False


def test_google_auth_login_existing_user(client, db_session):
    """Verify repeated Google sign-in logs in existing user without duplication."""
    payload = {
        "email": "sarah.crm@enterprise.io",
        "full_name": "Sarah Connor",
        "sub": "google_sub_112233",
    }

    # First attempt: Sign up
    resp1 = client.post("/api/auth/google", json=payload)
    assert resp1.status_code == 200

    # Second attempt: Log in
    resp2 = client.post("/api/auth/google", json=payload)
    assert resp2.status_code == 200
    data2 = resp2.json()

    assert data2["user"]["email"] == "sarah.crm@enterprise.io"

    # Verify only 1 User record exists
    user_count = db_session.query(User).filter(User.email == "sarah.crm@enterprise.io").count()
    assert user_count == 1

    oauth_count = db_session.query(OAuthAccount).filter(OAuthAccount.provider_user_id == "google_sub_112233").count()
    assert oauth_count == 1


def test_get_current_user_profile(client):
    """Verify /api/auth/me returns profile for valid Bearer token."""
    # Register/login
    auth_resp = client.post("/api/auth/google", json={
        "email": "alex.test@neuronforce.ai",
        "full_name": "Alex Test",
        "sub": "google_sub_554433"
    })
    token = auth_resp.json()["access_token"]

    # Access protected route
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["email"] == "alex.test@neuronforce.ai"
    assert me_data["full_name"] == "Alex Test"


def test_get_current_user_unauthorized(client):
    """Verify /api/auth/me rejects missing or invalid token."""
    # No header
    resp1 = client.get("/api/auth/me")
    assert resp1.status_code == 401

    # Invalid header
    resp2 = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.jwt.token"})
    assert resp2.status_code == 401


def test_logout_and_session_revocation(client, db_session):
    """Verify logout revokes active user session."""
    auth_resp = client.post("/api/auth/google", json={
        "email": "jordan.ops@neuronforce.ai",
        "full_name": "Jordan Ops",
        "sub": "google_sub_776655"
    })
    token = auth_resp.json()["access_token"]

    # Logout
    logout_resp = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {token}"})
    assert logout_resp.status_code == 200
    assert logout_resp.json()["status"] == "success"

    # Subsequent call with revoked session fails
    me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 401
    assert "revoked" in me_resp.json()["detail"].lower()


def test_list_user_sessions(client):
    """Verify listing active sessions for current user."""
    auth_resp = client.post("/api/auth/google", json={
        "email": "elena.dev@neuronforce.ai",
        "full_name": "Elena Dev",
        "sub": "google_sub_332211"
    })
    token = auth_resp.json()["access_token"]

    sessions_resp = client.get("/api/auth/sessions", headers={"Authorization": f"Bearer {token}"})
    assert sessions_resp.status_code == 200
    sessions = sessions_resp.json()
    assert len(sessions) >= 1
    assert "session_token" in sessions[0]
