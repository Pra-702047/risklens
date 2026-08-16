from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

db_url = os.getenv("DATABASE_URL")
if not db_url or db_url.strip() == "":
    db_url = os.getenv("POSTGRES_URL")

if not db_url or db_url.strip() == "":
    db_url = "postgresql://postgres:postgres@localhost:5432/risklens"

# SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

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
