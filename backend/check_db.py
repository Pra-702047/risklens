from sqlalchemy import create_engine, text

engine = create_engine("postgresql://postgres:admin123@localhost:5432/risklens")
try:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        conn.commit()
        print("PostGIS installed successfully.")
except Exception as e:
    print(f"Error: {e}")
