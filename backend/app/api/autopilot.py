# backend/app/api/autopilot.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.core.database import get_db
from app.models.social import SocialPost, SocialPage
import requests, os

GRAPH = os.getenv("META_GRAPH_VERSION", "v20.0")
router = APIRouter(prefix="/autopilot", tags=["autopilot"])

@router.post("/run")
def run_autopilot(db: Session = Depends(get_db)):
    # find due posts
    now = datetime.utcnow()
    queue = db.query(SocialPost).filter(
        SocialPost.status=="queued",
        SocialPost.scheduled_for != None,
        SocialPost.scheduled_for <= now
    ).all()

    published = 0
    for p in queue:
        page = db.query(SocialPage).filter_by(id=p.page_id).first()
        if not page:
            p.status="failed"; p.error="Page not found"; continue

        payload = {"message": p.message, "access_token": page.page_access_token}
        url = f"https://graph.facebook.com/{GRAPH}/{page.page_id}/feed"
        if p.media_url:
            url = f"https://graph.facebook.com/{GRAPH}/{page.page_id}/photos"
            payload = {"url": p.media_url, "caption": p.message, "access_token": page.page_access_token}
        if p.link_url and not p.media_url:
            payload["link"] = p.link_url

        res = requests.post(url, data=payload, timeout=20).json()
        if "error" in res:
            p.status = "failed"; p.error = str(res["error"])
        else:
            p.status = "posted"; p.external_post_id = res.get("id")
            published += 1

    db.commit()
    return {"published": published, "checked": len(queue)}
