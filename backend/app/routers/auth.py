"""
Authentication & Google SSO API Router
Handles Google OAuth 2.0 / OIDC SSO, token verification, session lifecycle, and profile management.
"""

import os
import urllib.parse
from fastapi import APIRouter, Depends, HTTPException, Request, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
import httpx

from app.database import get_db
from app.models.user import User
from app.models.session import UserSession
from app.schemas import GoogleAuthRequest, AuthResponse, UserResponse, SessionResponse
from app.auth import (
    verify_google_id_token,
    authenticate_or_register_google_user,
    get_current_user,
    decode_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    GOOGLE_CLIENT_ID,
)

from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Auth"])

GOOGLE_CLIENT_SECRET = settings.GOOGLE_CLIENT_SECRET
FRONTEND_URL = settings.FRONTEND_URL
BACKEND_URL = settings.BACKEND_URL


@router.get("/google/login")
def google_sso_login_redirect(request: Request, return_to: Optional[str] = Query(None)):
    """
    Initiate Google SSO redirect.
    If GOOGLE_CLIENT_ID is configured, redirects to Google's live OAuth screen.
    Preserves return_to origin (e.g. Cloudflare tunnel or localhost) via OAuth state.
    """
    target_origin = return_to or request.headers.get("referer") or FRONTEND_URL
    if target_origin and target_origin.startswith("http"):
        parsed = urllib.parse.urlparse(target_origin)
        target_origin = f"{parsed.scheme}://{parsed.netloc}"
    else:
        target_origin = FRONTEND_URL

    if GOOGLE_CLIENT_ID:
        redirect_uri = f"{BACKEND_URL}/api/auth/google/callback"
        params = {
            "client_id": GOOGLE_CLIENT_ID,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "select_account",
            "state": target_origin,
        }
        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        return RedirectResponse(url=auth_url)
    else:
        # Development fallback: redirect to frontend Google SSO interface
        return RedirectResponse(url=f"{target_origin}/login?sso=prompt")


@router.get("/google/callback")
async def google_sso_callback(
    code: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    Handle Google OAuth 2.0 authorization code callback.
    Exchanges code for access & ID tokens and redirects to the origin frontend with sso_token.
    """
    target_frontend = state if state and state.startswith("http") else FRONTEND_URL

    if error:
        return RedirectResponse(
            url=f"{target_frontend}/login?error={urllib.parse.quote(error)}"
        )

    if not code:
        raise HTTPException(
            status_code=400, detail="Missing authorization code from Google"
        )

    redirect_uri = f"{BACKEND_URL}/api/auth/google/callback"

    # Exchange code for tokens with Google OAuth
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(token_url, data=token_data)
            if resp.status_code != 200:
                return RedirectResponse(
                    url=f"{target_frontend}/login?error=Google+token+exchange+failed"
                )
            token_json = resp.json()
            id_token = token_json.get("id_token")

        if not id_token:
            return RedirectResponse(
                url=f"{target_frontend}/login?error=Missing+Google+id_token"
            )

        profile = await verify_google_id_token(id_token)
        user, session, access_token = authenticate_or_register_google_user(
            db=db,
            profile=profile,
        )

        return RedirectResponse(url=f"{target_frontend}/?sso_token={access_token}")
    except Exception as e:
        return RedirectResponse(
            url=f"{target_frontend}/login?error={urllib.parse.quote(str(e))}"
        )


@router.post("/google", response_model=AuthResponse)
async def google_auth(
    auth_req: GoogleAuthRequest, request: Request, db: Session = Depends(get_db)
):
    """
    Sign up or log in using Google OAuth credentials or verified SSO token.
    Separates User entity, OAuth provider account, and active UserSession.
    """
    client_ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    profile = {}
    if auth_req.credential:
        profile = await verify_google_id_token(auth_req.credential)
    else:
        if not auth_req.email:
            raise HTTPException(
                status_code=400,
                detail="Either Google credential token or email must be provided",
            )
        profile = {
            "sub": auth_req.sub or f"google_{auth_req.email}",
            "email": auth_req.email,
            "name": auth_req.full_name
            or auth_req.email.split("@")[0].replace(".", " ").title(),
            "picture": auth_req.avatar_url
            or f"https://api.dicebear.com/7.x/avataaars/svg?seed={auth_req.email}",
            "email_verified": True,
            "raw": {"source": "google_sso"},
        }

    user, session, token = authenticate_or_register_google_user(
        db=db,
        profile=profile,
        role_preference=auth_req.role,
        ip_address=client_ip,
        user_agent=user_agent,
    )

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user profile from Bearer token."""
    return UserResponse.model_validate(current_user)


@router.post("/logout")
def logout_current_user(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Log out current user and revoke their active session."""
    raw_header = request.headers.get("Authorization", "")
    token = raw_header[7:].strip() if raw_header.startswith("Bearer ") else None

    if token:
        payload = decode_access_token(token)
        if payload and "session_id" in payload:
            session = (
                db.query(UserSession)
                .filter(UserSession.id == payload["session_id"])
                .first()
            )
            if session:
                session.is_revoked = True
                db.commit()

    return {"message": "Successfully logged out", "status": "success"}


@router.get("/sessions", response_model=List[SessionResponse])
def get_user_sessions(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Get all active sessions for the authenticated user."""
    sessions = (
        db.query(UserSession)
        .filter(UserSession.user_id == current_user.id, UserSession.is_revoked == False)
        .order_by(desc(UserSession.last_active_at))
        .all()
    )
    return [SessionResponse.model_validate(s) for s in sessions]


@router.get("/demo-accounts")
def list_demo_accounts(db: Session = Depends(get_db)):
    """List available pre-seeded Google accounts for one-click testing."""
    users = db.query(User).filter(User.is_active == True).limit(5).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "avatar_url": u.avatar_url,
            "role": u.role,
        }
        for u in users
    ]
