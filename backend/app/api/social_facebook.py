# backend/app/api/social_facebook.py

from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import List, Optional
from urllib.parse import quote_plus

import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from requests.exceptions import RequestException
from sqlalchemy.orm import Session
# prefer a central get_db() helper (recommended)
try:
    from app.core.database import get_db  # your helper that yields a Session
except Exception:
    # fallback if you don't have get_db in core.database
    from app.core.database import SessionLocal

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

from app.models.social import SocialAccount, SocialPage, SocialPost
from app.schemas.social import AccountOut, PageOut, PostCreate

# --- Config ---
GRAPH = os.getenv("META_GRAPH_VERSION", "v20.0").strip()  # e.g., "v20.0"
APP_ID = os.getenv("META_APP_ID", "").strip()
APP_SECRET = os.getenv("META_APP_SECRET", "").strip()
REDIRECT_URI = os.getenv("META_REDIRECT_URI", "").strip()

# Validate at runtime (not import time) to avoid crashing the app on boot
def _require_env():
    missing = [k for k, v in {
        "META_APP_ID": APP_ID,
        "META_APP_SECRET": APP_SECRET,
        "META_REDIRECT_URI": REDIRECT_URI,
    }.items() if not v]
    if missing:
        raise HTTPException(
            status_code=500,
            detail=f"Facebook config missing: {', '.join(missing)}"
        )

router = APIRouter(prefix="/social/facebook", tags=["facebook"])

SCOPES = [
    "public_profile",
    "pages_show_list",
    "pages_read_engagement",
    "pages_manage_posts",
    "pages_manage_metadata",
]

# Helper to wrap requests with consistent error handling
def _get(url: str, **kwargs):
    try:
        r = requests.get(url, timeout=kwargs.pop("timeout", 15), **kwargs)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise HTTPException(400, f"Facebook error: {data['error']}")
        return data
    except RequestException as e:
        raise HTTPException(502, f"Facebook network error: {e}")

def _post(url: str, **kwargs):
    try:
        r = requests.post(url, timeout=kwargs.pop("timeout", 20), **kwargs)
        r.raise_for_status()
        data = r.json()
        if "error" in data:
            raise HTTPException(400, f"Facebook error: {data['error']}")
        return data
    except RequestException as e:
        raise HTTPException(502, f"Facebook network error: {e}")

@router.get("/login-url")
def login_url(state: Optional[str] = None):
    """
    Returns the Facebook OAuth dialog URL.
    You should pass a CSRF-protected `state` from your frontend.
    """
    _require_env()
    scope = ",".join(SCOPES)
    redirect = quote_plus(REDIRECT_URI)
    url = (
        f"https://www.facebook.com/{GRAPH}/dialog/oauth"
        f"?client_id={APP_ID}"
        f"&redirect_uri={redirect}"
        f"&scope={scope}"
        f"&response_type=code"
        f"{f'&state={quote_plus(state)}' if state else ''}"
    )
    return {"url": url}

def exchange_code_for_token(code: str) -> dict:
    """
    Exchange authorization code for a short-lived token,
    then upgrade to a long-lived user token.
    """
    _require_env()

    token_url = (
        f"https://graph.facebook.com/{GRAPH}/oauth/access_token"
        f"?client_id={APP_ID}&redirect_uri={quote_plus(REDIRECT_URI)}"
        f"&client_secret={APP_SECRET}&code={quote_plus(code)}"
    )
    short = _get(token_url)

    ll_url = (
        f"https://graph.facebook.com/{GRAPH}/oauth/access_token"
        f"?grant_type=fb_exchange_token&client_id={APP_ID}"
        f"&client_secret={APP_SECRET}&fb_exchange_token={short['access_token']}"
    )
    long_lived = _get(ll_url)
    return long_lived  # {access_token, token_type, expires_in}

@router.get("/callback")
def callback(code: str, db: Session = Depends(get_db), request: Request = None):
    """
    OAuth callback endpoint. Exchanges `code` for a long-lived user token,
    fetches user info and managed pages, and upserts them into DB.
    """
    token_data = exchange_code_for_token(code)

    me = _get(
        f"https://graph.facebook.com/{GRAPH}/me",
        params={
            "access_token": token_data["access_token"],
            "fields": "id,name,picture"
        },
    )

    # TODO: swap this with your authenticated platform user ID (from JWT/session)
    platform_user_id = 1

    expires_at = datetime.utcnow() + timedelta(
        seconds=int(token_data.get("expires_in") or 0)
    )

    # Upsert account
    account = (
        db.query(SocialAccount)
        .filter_by(user_id=platform_user_id, provider="facebook", provider_user_id=me["id"])
        .first()
    )

    picture_url = (me.get("picture") or {}).get("data", {}).get("url")

    if account:
        account.name = me.get("name")
        account.picture_url = picture_url
        account.access_token = token_data["access_token"]
        account.token_expires_at = expires_at
    else:
        account = SocialAccount(
            user_id=platform_user_id,
            provider="facebook",
            provider_user_id=me["id"],
            name=me.get("name"),
            picture_url=picture_url,
            access_token=token_data["access_token"],
            token_expires_at=expires_at,
        )
        db.add(account)
        db.flush()  # so account.id is available

    # Fetch managed pages
    pages_data = _get(
        f"https://graph.facebook.com/{GRAPH}/me/accounts",
        params={"access_token": token_data["access_token"]},
    ).get("data", [])

    existing = {
        p.page_id: p for p in db.query(SocialPage).filter_by(account_id=account.id).all()
    }

    for p in pages_data:
        page = existing.get(p["id"])
        if page:
            page.name = p.get("name")
            page.category = p.get("category")
            page.page_access_token = p.get("access_token")
            page.connected = True
        else:
            db.add(
                SocialPage(
                    account_id=account.id,
                    page_id=p["id"],
                    name=p.get("name"),
                    category=p.get("category"),
                    page_access_token=p.get("access_token"),
                    connected=True,
                )
            )

    db.commit()
    return {"message": "Facebook connected", "account_id": account.id}

@router.get("/accounts", response_model=List[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return db.query(SocialAccount).all()

@router.get("/pages", response_model=List[PageOut])
def list_pages(account_id: int, db: Session = Depends(get_db)):
    return db.query(SocialPage).filter_by(account_id=account_id, connected=True).all()

@router.post("/pages/{page_pk}/post")
def post_to_page(page_pk: int, body: PostCreate, db: Session = Depends(get_db)):
    """
    Publishes a post to a connected page. If `media_url` is provided, it will be posted as a photo.
    Otherwise, it posts a standard feed message, optionally with a link.
    """
    page = db.query(SocialPage).filter_by(id=page_pk).first()
    if not page or not page.page_access_token:
        raise HTTPException(400, "Page not found or not connected")

    if not body.media_url:
        # simple feed post
        data = _post(
            f"https://graph.facebook.com/{GRAPH}/{page.page_id}/feed",
            data={
                "message": body.message,
                **({"link": body.link_url} if body.link_url else {}),
                "access_token": page.page_access_token,
            },
        )
    else:
        # photo upload
        data = _post(
            f"https://graph.facebook.com/{GRAPH}/{page.page_id}/photos",
            data={
                "url": body.media_url,
                "caption": body.message,
                "access_token": page.page_access_token,
            },
        )

    post = SocialPost(
        account_id=page.account_id,
        page_id=page.id,
        message=body.message,
        media_url=body.media_url,
        link_url=body.link_url,
        status="posted",
        external_post_id=data.get("id"),
    )
    db.add(post)
    db.commit()
    return {"ok": True, "post_id": post.id, "facebook_id": data.get("id")}
