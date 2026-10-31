from fastapi import APIRouter
from app.api.endpoints import resume, match, interview

api_router = APIRouter()

api_router.include_router(resume.router, prefix="/resumes", tags=["Resumes"])
api_router.include_router(match.router, prefix="/match", tags=["Matching & Analysis"])
api_router.include_router(interview.router, prefix="/interview", tags=["Interview Prep"])

