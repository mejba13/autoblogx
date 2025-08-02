from sqlalchemy import create_engine

# Adjust if needed: add password or use .env
DATABASE_URL = "postgresql://root@localhost:5432/autoblogx"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        print("✅ Connected successfully:", conn)
except Exception as e:
    print("❌ Connection failed:", e)