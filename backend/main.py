import sys
import os
import traceback
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from dotenv import load_dotenv

# Load .env file
load_dotenv()

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
    from app.modules.sla.models import SLAStatus, SLAPolicy
    from app.modules.geo.models import Zone, Ward
    from app.modules.incidents.models import Incident
    from app.modules.routing.models import RoutingRule, Department
    from app.modules.notifications.models import Notification
    from app.modules.assignments.models import Assignment
    from app.modules.audit.models import ComplaintEvent
    from app.modules.feedback.models import ComplaintFeedback
    from app.modules.field_actions.models import FieldAction
    from app.modules.severity.models import ComplaintSeverity
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
        allow_origins=[
            "http://localhost:3000",
            "https://risklens-alpha.vercel.app",
            "https://risklens-git-main-prathmesh-uttarwars-projects.vercel.app"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from app.modules.geo.routes import router as geo_router
    from app.modules.notifications.routes import router as notifications_router
    from app.modules.admin.routes import router as admin_router
    from apscheduler.schedulers.background import BackgroundScheduler
    from app.modules.sla.monitor import check_sla_breaches

    # Start APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_sla_breaches, 'interval', minutes=1)
    scheduler.start()

    # Shut down scheduler on exit
    import atexit
    atexit.register(lambda: scheduler.shutdown())

    app.include_router(users_router)
    app.include_router(complaints_router)
    app.include_router(officer_router)
    app.include_router(analytics_router)
    app.include_router(geo_router)
    app.include_router(notifications_router)
    app.include_router(admin_router)

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
