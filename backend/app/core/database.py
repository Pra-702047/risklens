from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

db_url = os.getenv("DATABASE_URL")
if not db_url or db_url.strip() == "" or db_url.strip() == "POSTGRES_URL":
    db_url = os.getenv("POSTGRES_URL")

if not db_url or db_url.strip() == "" or db_url.strip() == "POSTGRES_URL":
    db_url = os.getenv("STORAGE_URL")

if not db_url or db_url.strip() == "" or db_url.strip() == "POSTGRES_URL":
    db_url = "postgresql://postgres:postgres@localhost:5432/risklens"

# Strip surrounding quotes if the user accidentally added them
db_url = db_url.strip().strip("'").strip('"')

# SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if not db_url.startswith("postgresql://"):
    raise ValueError(f"CRITICAL ERROR: The Database URL is totally invalid. Value found: {db_url[:20]}...")

DATABASE_URL = db_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
