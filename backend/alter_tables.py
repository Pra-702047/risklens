import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from app.core.database import engine
from sqlalchemy import text

def alter_tables():
    with engine.begin() as conn:
        try:
            conn.execute(text("ALTER TABLE officers ADD COLUMN password_hash VARCHAR;"))
            print("Added password_hash to officers")
        except Exception as e:
            print(e)
            
if __name__ == "__main__":
    alter_tables()
