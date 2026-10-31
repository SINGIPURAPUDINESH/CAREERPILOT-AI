from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class ResumeParseRequest(BaseModel):
    raw_text: Optional[str] = None

class ParsedResumeResponse(BaseModel):
    id: Optional[str] = None
    filename: Optional[str] = None
    sections: Dict[str, str] = Field(default_factory=dict)
    extracted_skills: List[str] = Field(default_factory=list)
    word_count: int = 0
    estimated_experience_years: Optional[float] = None

class JobDescriptionParseRequest(BaseModel):
    title: Optional[str] = "Target Role"
    company: Optional[str] = "Target Company"
    raw_text: str

class ParsedJobDescriptionResponse(BaseModel):
    id: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    key_responsibilities: List[str] = Field(default_factory=list)

class SkillMatchDetail(BaseModel):
    skill: str
    category: str
    status: str  # "matched", "missing_required", "missing_preferred", "bonus"

class MatchAnalysisRequest(BaseModel):
    resume_id: Optional[str] = None
    resume_text: Optional[str] = None
    jd_id: Optional[str] = None
    jd_text: Optional[str] = None

class InterviewQuestionItem(BaseModel):
    category: str  # "Behavioral (STAR)", "Technical Deep Dive", "Skill Gap Probing"
    question: str
    rationale: str
    sample_answer_guide: str
    difficulty: str

class MatchAnalysisResponse(BaseModel):
    analysis_id: Optional[str] = None
    overall_score: float
    skill_coverage_score: float
    semantic_score: float
    experience_score: float
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    bonus_skills: List[str] = Field(default_factory=list)
    gap_recommendations: List[str] = Field(default_factory=list)
    interview_questions: List[InterviewQuestionItem] = Field(default_factory=list)

class FullAnalysisRequest(BaseModel):
    resume_text: Optional[str] = None
    jd_text: str
    role_title: Optional[str] = "Software Engineer"
    company: Optional[str] = "Tech Company"

