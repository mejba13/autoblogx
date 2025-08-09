# backend/alembic/env.py
from logging.config import fileConfig
import os
import sys
import pathlib

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# ——— Path + env ———
# Ensure "backend/" is on sys.path so `import app...` works when Alembic runs
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

# Load .env for DATABASE_URL
load_dotenv()

config = context.config

database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("❌ DATABASE_URL not found in .env file")
config.set_main_option("sqlalchemy.url", database_url)

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ——— Import metadata and force-load model modules ———
from app.models import Base  # Base.metadata used by Alembic

# IMPORTANT: import modules so tables are registered on Base.metadata
import app.models.user    # noqa: F401
import app.models.social  # noqa: F401

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
