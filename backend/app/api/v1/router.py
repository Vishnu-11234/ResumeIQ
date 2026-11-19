from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.resumes import resume_router
from app.api.v1.analysis import analysis_router

api_router = APIRouter()

api_router.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"]
)

api_router.include_router(
    resume_router,
    prefix="/resumes",
    tags=["Resumes"]
)

api_router.include_router(
    analysis_router,
    prefix="/analysis",
    tags=["Resume Analysis"]
)