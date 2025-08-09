# backend/app/schemas/social.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PageOut(BaseModel):
    id: int
    page_id: str
    name: str
    category: Optional[str] = None
    connected: bool
    class Config: from_attributes = True

class AccountOut(BaseModel):
    id: int
    provider: str
    provider_user_id: str
    name: str
    pages: List[PageOut] = []
    class Config: from_attributes = True

class PostCreate(BaseModel):
    page_id: int
    message: str
    media_url: Optional[str] = None
    link_url: Optional[str] = None
    scheduled_for: Optional[datetime] = None
