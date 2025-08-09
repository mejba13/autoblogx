# backend/app/api/social_facebook.py
import os, requests, datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.social import SocialAccount, SocialPage, SocialPost
from app.schemas.social import AccountOut, PageOut, PostCreate

GRAPH = os.getenv("META_GRAPH_VERSION", "v20.0")
APP_ID = os.getenv("META_APP_ID")
APP_SECRET = os.getenv("META_APP_SECRET")
REDIRECT_URI = os.getenv("META_REDIRECT_URI")

router = APIRouter(prefix="/social/facebook", tags=["facebook"])

SCOPES = [
    "public_profile",
    "pages_show_list",
    "pages_read_engagement",
    "pages_manage_posts",
    "pages_manage_metadata",
]

@router.get("/login-url")
def login_url():
    url = (
        f"https://www.facebook.com/{GRAPH}/dialog/oauth"
        f"?client_id={APP_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={','.join(SCOPES)}"
        f"&response_type=code"
    )
    return {"url": url}

def exchange_code_for_token(code: str):
    token_url = (
        f"https://graph.facebook.com/{GRAPH}/oauth/access_token"
        f"?client_id={APP_ID}&redirect_uri={REDIRECT_URI}"
        f"&client_secret={APP_SECRET}&code={code}"
    )
    r = requests.get(token_url, timeout=15)
    r.raise_for_status()
    data = r.json()
    # upgrade to long‑lived user token
    ll_url = (
        f"https://graph.facebook.com/{GRAPH}/oauth/access_token"
        f"?grant_type=fb_exchange_token&client_id={APP_ID}"
        f"&client_secret={APP_SECRET}&fb_exchange_token={data['access_token']}"
    )
    ll = requests.get(ll_url, timeout=15).json()
    return ll  # {access_token, token_type, expires_in}

@router.get("/callback")
def callback(code: str, db: Session = Depends(get_db), request: Request = None):
    try:
        token_data = exchange_code_for_token(code)
    except Exception as e:
        raise HTTPException(400, f"OAuth error: {e}")

    user_r = requests.get(
        f"https://graph.facebook.com/{GRAPH}/me",
        params={"access_token": token_data["access_token"], "fields": "id,name,picture"},
        timeout=15,
    )
    user_r.raise_for_status()
    me = user_r.json()

    # upsert SocialAccount (assuming request.user.id available—replace with your auth)
    platform_user_id = 1  # TODO: get from session/JWT
    account = db.query(SocialAccount).filter_by(
        user_id=platform_user_id,
        provider="facebook",
        provider_user_id=me["id"],
    ).first()
    expires_at = datetime.datetime.utcnow() + datetime.timedelta(seconds=int(token_data.get("expires_in", 0)))

    if account:
        account.name = me.get("name")
        account.picture_url = me.get("picture", {}).get("data", {}).get("url")
        account.access_token = token_data["access_token"]
        account.token_expires_at = expires_at
    else:
        account = SocialAccount(
            user_id=platform_user_id,
            provider="facebook",
            provider_user_id=me["id"],
            name=me.get("name"),
            picture_url=me.get("picture", {}).get("data", {}).get("url"),
            access_token=token_data["access_token"],
            token_expires_at=expires_at,
        )
        db.add(account)
        db.flush()

    # fetch pages the user manages
    pages_r = requests.get(
        f"https://graph.facebook.com/{GRAPH}/me/accounts",
        params={"access_token": token_data["access_token"]},
        timeout=15,
    )
    pages_r.raise_for_status()
    pages = pages_r.json().get("data", [])

    # upsert pages + their page access tokens
    existing = {p.page_id: p for p in db.query(SocialPage).filter_by(account_id=account.id).all()}
    for p in pages:
        page = existing.get(p["id"])
        if page:
            page.name = p.get("name")
            page.category = p.get("category")
            page.page_access_token = p.get("access_token")
            page.connected = True
        else:
            db.add(SocialPage(
                account_id=account.id,
                page_id=p["id"],
                name=p.get("name"),
                category=p.get("category"),
                page_access_token=p.get("access_token"),
                connected=True,
            ))
    db.commit()
    return {"message": "Facebook connected", "account_id": account.id}

@router.get("/accounts", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    accounts = db.query(SocialAccount).all()
    return accounts

@router.get("/pages", response_model=list[PageOut])
def list_pages(account_id: int, db: Session = Depends(get_db)):
    return db.query(SocialPage).filter_by(account_id=account_id, connected=True).all()

@router.post("/pages/{page_pk}/post")
def post_to_page(page_pk: int, body: PostCreate, db: Session = Depends(get_db)):
    page = db.query(SocialPage).filter_by(id=page_pk).first()
    if not page or not page.page_access_token:
        raise HTTPException(400, "Page not found or not connected")

    # immediate publish (text/link)
    if not body.media_url:
        r = requests.post(
            f"https://graph.facebook.com/{GRAPH}/{page.page_id}/feed",
            data={
                "message": body.message,
                **({"link": body.link_url} if body.link_url else {}),
                "access_token": page.page_access_token,
            },
            timeout=15,
        )
        data = r.json()
    else:
        # photo upload then publish
        r = requests.post(
            f"https://graph.facebook.com/{GRAPH}/{page.page_id}/photos",
            data={"url": body.media_url, "caption": body.message, "access_token": page.page_access_token},
            timeout=20,
        )
        data = r.json()

    if "error" in data:
        post = SocialPost(
            account_id=page.account_id, page_id=page.id, message=body.message,
            media_url=body.media_url, link_url=body.link_url, status="failed", error=str(data["error"])
        )
        db.add(post); db.commit()
        raise HTTPException(400, f"Facebook error: {data['error']}")

    post = SocialPost(
        account_id=page.account_id, page_id=page.id, message=body.message,
        media_url=body.media_url, link_url=body.link_url, status="posted",
        external_post_id=data.get("id"),
    )
    db.add(post); db.commit()
    return {"ok": True, "post_id": post.id, "facebook_id": data.get("id")}
