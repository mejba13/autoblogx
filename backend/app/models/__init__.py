# backend/app/models/__init__.py
from app.core.database import Base

# Import models so Alembic sees them
from .user import User           # noqa: F401
from .social import SocialAccount, SocialPage, SocialPost  # noqa: F401

__all__ = [
    "Base",
    "User",
    "SocialAccount",
    "SocialPage",
    "SocialPost",
]
