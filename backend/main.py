from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.modules.users.routes import router as users_router
from app.modules.complaints.routes import router as complaints_router
from app.modules.officer.routes import router as officer_router
from app.modules.analytics.routes import router as analytics_router
from app.core.database import Base, engine

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RiskLens API",
    description="Backend API for RiskLens platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
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
