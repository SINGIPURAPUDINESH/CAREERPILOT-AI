from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.schemas.resume import InterviewQuestionItem
from app.services.interview_generator import interview_generator

router = APIRouter()

class DirectInterviewRequest(BaseModel):
    role_title: str = "Senior Full Stack Engineer"
    matched_skills: List[str]
    missing_skills: List[str]
    candidate_summary: Optional[str] = ""

@router.post("/generate", response_model=List[InterviewQuestionItem])
def generate_interview_questions(payload: DirectInterviewRequest):
    """Generates tailored interview questions based on candidate profile and skill gaps."""
    questions_raw = interview_generator.generate_interview_questions(
        role_title=payload.role_title,
        matched_skills=payload.matched_skills,
        missing_skills=payload.missing_skills,
        resume_summary=payload.candidate_summary or ""
    )

    return [
        InterviewQuestionItem(
            category=q.get("category", "General"),
            question=q.get("question", ""),
            rationale=q.get("rationale", ""),
            sample_answer_guide=q.get("sample_answer_guide", ""),
            difficulty=q.get("difficulty", "Intermediate")
        )
        for q in questions_raw
    ]

