from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.modules.auth.service import seed_roles_and_admin
from app.modules.auth.router import router as auth_router
from app.modules.crm.router import router as crm_router
from app.modules.projects.router import router as projects_router
from app.modules.events.router import router as events_router
from app.modules.tasks.router import router as tasks_router
from app.modules.documents.router import router as documents_router
from app.modules.finance.router import router as finance_router
from app.modules.dashboard.router import router as dashboard_router
from app.modules.imports.router import router as imports_router
from app.modules.event_sources.router import router as event_sources_router

# Make sure models are registered on Base
from app.modules.auth.models import User, Role
from app.modules.crm.models import Customer, Contact
from app.modules.projects.models import Project, ProjectStatusLog, ProjectActivityLog
from app.modules.events.models import EventSchedule
from app.modules.tasks.models import Task
from app.modules.documents.models import Document
from app.modules.finance.models import Invoice, Payment
from app.modules.event_sources.models import EventSource
from app.models.activity import ActivityLog

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    # 1. Create tables automatically (highly robust for immediate startup)
    Base.metadata.create_all(bind=engine)
    
    # 2. Seed database roles and default admin user
    db = SessionLocal()
    try:
        seed_roles_and_admin(db)
    finally:
        db.close()

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(crm_router, prefix=settings.API_V1_STR)
app.include_router(projects_router, prefix=settings.API_V1_STR)
app.include_router(events_router, prefix=settings.API_V1_STR)
app.include_router(tasks_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)
app.include_router(finance_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(imports_router, prefix=settings.API_V1_STR)
app.include_router(event_sources_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "onespirit-backend"
    }

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": f"Welcome to {settings.PROJECT_NAME} API. Access documentation at /docs"
    }
