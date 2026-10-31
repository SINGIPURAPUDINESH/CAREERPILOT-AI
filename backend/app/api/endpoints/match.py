from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Resume, JobDescription, AnalysisResult, InterviewQuestion
from app.schemas.resume import (
    JobDescriptionParseRequest,
    ParsedJobDescriptionResponse,
    MatchAnalysisRequest,
    MatchAnalysisResponse,
    FullAnalysisRequest,
    InterviewQuestionItem
)
from app.services.nlp_extractor import nlp_extractor
from app.services.document_parser import document_parser
from app.services.matcher import matcher_service
from app.services.interview_generator import interview_generator

router = APIRouter()

@router.post("/parse-job", response_model=ParsedJobDescriptionResponse)
def parse_job_description(
    payload: JobDescriptionParseRequest,
    db: Session = Depends(get_db)
):
    """Extracts required and preferred skills from a job description."""
    if not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="Job description text cannot be empty.")

    skills = nlp_extractor.extract_skills(payload.raw_text)
    
    # Store JD
    jd_record = JobDescription(
        title=payload.title or "Target Role",
        company=payload.company or "Target Company",
        raw_text=payload.raw_text,
        required_skills=skills
    )
    db.add(jd_record)
    db.commit()
    db.refresh(jd_record)

    return ParsedJobDescriptionResponse(
        id=jd_record.id,
        title=jd_record.title,
        company=jd_record.company,
        required_skills=skills,
        preferred_skills=[],
        key_responsibilities=[]
    )

@router.post("/analyze", response_model=MatchAnalysisResponse)
def run_match_analysis(
    payload: MatchAnalysisRequest,
    db: Session = Depends(get_db)
):
    """Calculates match score, identifies skill gaps, and generates tailored interview prep."""
    # Resolve resume
    resume_text = payload.resume_text or ""
    resume_skills = []
    exp_years = 0.0

    if payload.resume_id:
        resume_record = db.query(Resume).filter(Resume.id == payload.resume_id).first()
        if resume_record:
            resume_text = resume_record.raw_text
            resume_skills = resume_record.extracted_skills
            exp_years = document_parser.estimate_experience_years(resume_text)

    if not resume_skills and resume_text:
        resume_skills = nlp_extractor.extract_skills(resume_text)
        exp_years = document_parser.estimate_experience_years(resume_text)

    # Resolve JD
    jd_text = payload.jd_text or ""
    jd_skills = []
    role_title = "Software Engineer"

    if payload.jd_id:
        jd_record = db.query(JobDescription).filter(JobDescription.id == payload.jd_id).first()
        if jd_record:
            jd_text = jd_record.raw_text
            jd_skills = jd_record.required_skills
            role_title = jd_record.title or "Software Engineer"

    if not jd_skills and jd_text:
        jd_skills = nlp_extractor.extract_skills(jd_text)

    if not resume_text:
        raise HTTPException(status_code=400, detail="Resume content is required.")
    if not jd_text:
        raise HTTPException(status_code=400, detail="Job description content is required.")

    # Run match scoring
    match_result = matcher_service.analyze_match(
        resume_text=resume_text,
        resume_skills=resume_skills,
        jd_text=jd_text,
        jd_skills=jd_skills,
        resume_exp_years=exp_years
    )

    # Generate interview questions
    questions_raw = interview_generator.generate_interview_questions(
        role_title=role_title,
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        resume_summary=resume_text[:300],
        jd_text=jd_text[:500]
    )

    questions_formatted = [
        InterviewQuestionItem(
            category=q.get("category", "General"),
            question=q.get("question", ""),
            rationale=q.get("rationale", ""),
            sample_answer_guide=q.get("sample_answer_guide", ""),
            difficulty=q.get("difficulty", "Intermediate")
        )
        for q in questions_raw
    ]

    return MatchAnalysisResponse(
        overall_score=match_result["overall_score"],
        skill_coverage_score=match_result["skill_coverage_score"],
        semantic_score=match_result["semantic_score"],
        experience_score=match_result["experience_score"],
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        bonus_skills=match_result["bonus_skills"],
        gap_recommendations=match_result["gap_recommendations"],
        interview_questions=questions_formatted
    )

@router.post("/full-pipeline", response_model=MatchAnalysisResponse)
def run_full_pipeline(
    payload: FullAnalysisRequest,
    db: Session = Depends(get_db)
):
    """
    Direct all-in-one endpoint: Takes raw resume text + job description text,
    parses both, computes match scores, identifies skill gaps, and returns interview prep.
    """
    if not payload.resume_text or not payload.resume_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")
    if not payload.jd_text or not payload.jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    resume_skills = nlp_extractor.extract_skills(payload.resume_text)
    exp_years = document_parser.estimate_experience_years(payload.resume_text)
    jd_skills = nlp_extractor.extract_skills(payload.jd_text)

    match_result = matcher_service.analyze_match(
        resume_text=payload.resume_text,
        resume_skills=resume_skills,
        jd_text=payload.jd_text,
        jd_skills=jd_skills,
        resume_exp_years=exp_years
    )

    questions_raw = interview_generator.generate_interview_questions(
        role_title=payload.role_title or "Software Engineer",
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        resume_summary=payload.resume_text[:400],
        jd_text=payload.jd_text[:600]
    )

    questions_formatted = [
        InterviewQuestionItem(
            category=q.get("category", "General"),
            question=q.get("question", ""),
            rationale=q.get("rationale", ""),
            sample_answer_guide=q.get("sample_answer_guide", ""),
            difficulty=q.get("difficulty", "Intermediate")
        )
        for q in questions_raw
    ]

    return MatchAnalysisResponse(
        overall_score=match_result["overall_score"],
        skill_coverage_score=match_result["skill_coverage_score"],
        semantic_score=match_result["semantic_score"],
        experience_score=match_result["experience_score"],
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"],
        bonus_skills=match_result["bonus_skills"],
        gap_recommendations=match_result["gap_recommendations"],
        interview_questions=questions_formatted
    )

