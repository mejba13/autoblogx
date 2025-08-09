# backend/app/models/social.py
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    provider = Column(String(32), default="facebook")
    provider_user_id = Column(String(64), index=True)
    name = Column(String(255))
    picture_url = Column(String(1024))
    access_token = Column(Text)
    token_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    pages = relationship("SocialPage", back_populates="account", cascade="all, delete-orphan")

class SocialPage(Base):
    __tablename__ = "social_pages"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    page_id = Column(String(64), index=True)
    name = Column(String(255))
    category = Column(String(255), nullable=True)
    picture_url = Column(String(1024), nullable=True)
    connected = Column(Boolean, default=True)
    perms = Column(JSON, nullable=True)
    page_access_token = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship("SocialAccount", back_populates="pages")

class SocialPost(Base):
    __tablename__ = "social_posts"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    page_id = Column(Integer, ForeignKey("social_pages.id"))
    status = Column(String(32), default="queued")
    message = Column(Text, nullable=False)
    media_url = Column(String(1024), nullable=True)
    link_url = Column(String(1024), nullable=True)
    scheduled_for = Column(DateTime, nullable=True)
    external_post_id = Column(String(128), nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
