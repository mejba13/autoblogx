from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 👇 Import all models here so Alembic detects them during autogenerate
from app.models.user import User
