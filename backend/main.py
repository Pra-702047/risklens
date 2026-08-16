import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

app = FastAPI()

try:
    from app.modules.users.routes import router as users_router
    from app.modules.complaints.routes import router as complaints_router
    from app.modules.officer.routes import router as officer_router
    from app.modules.analytics.routes import router as analytics_router
    from app.core.database import Base, engine
    from fastapi.middleware.cors import CORSMiddleware

    try:
        Base.metadata.create_all(bind=engine)
    except Exception as db_err:
        print(f"Warning: Could not create tables. Database might be offline: {db_err}")

    app.title = "RiskLens API"
    app.description = "Backend API for RiskLens platform"
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users_router)
    app.include_router(complaints_router)
    app.include_router(officer_router)
    app.include_router(analytics_router)

    @app.get("/")
    def read_root():
        return {"status": "ok", "message": "Welcome to RiskLens API"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

except Exception as e:
    err_msg = traceback.format_exc()
    @app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"])
    def catch_all(path: str):
        return PlainTextResponse(f"Initialization Error:\n\n{err_msg}", status_code=500)
