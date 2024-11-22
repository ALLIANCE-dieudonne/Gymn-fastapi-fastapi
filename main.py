from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth,
    contact,
    enroll,
    attendance,
    profile,
    gallery,
    trainer
)
from app.models import models
from app.db.session import engine

# Create FastAPI app instance
app = FastAPI(
    title="Gym Management System",
    description="API for Gym Management System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Include all routers with their prefixes and tags
app.include_router(
    auth.router,
    prefix="/api",
    tags=["Authentication"]
)

app.include_router(
    contact.router,
    prefix="/api/contact",
    tags=["Contact"]
)

app.include_router(
    enroll.router,
    prefix="/api/enroll",
    tags=["Enrollment"]
)

app.include_router(
    attendance.router,
    prefix="/api/attendance",
    tags=["Attendance"]
)

app.include_router(
    profile.router,
    prefix="/api/profile",
    tags=["Profile"]
)

app.include_router(
    gallery.router,
    prefix="/api/gallery",
    tags=["Gallery"]
)

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Gym Management System API",
        "documentation": "/docs",
        "alternative_documentation": "/redoc"
    }

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

