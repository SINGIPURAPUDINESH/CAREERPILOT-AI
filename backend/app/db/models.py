import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = Column(String, nullable=True)
    raw_text = Column(Text, nullable=False)
    parsed_sections = Column(JSON, default=dict)
    extracted_skills = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship("AnalysisResult", back_populates="resume", cascade="all, delete-orphan")


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    raw_text = Column(Text, nullable=False)
    required_skills = Column(JSON, default=list)
    preferred_skills = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    analyses = relationship("AnalysisResult", back_populates="job_description", cascade="all, delete-orphan")


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    resume_id = Column(String, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=False)
    jd_id = Column(String, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False)
    
    overall_score = Column(Float, nullable=False)
    skill_coverage_score = Column(Float, nullable=False)
    semantic_score = Column(Float, nullable=False)
    experience_score = Column(Float, nullable=False)
    
    matched_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    gap_recommendations = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    resume = relationship("Resume", back_populates="analyses")
    job_description = relationship("JobDescription", back_populates="analyses")
    interview_questions = relationship("InterviewQuestion", back_populates="analysis", cascade="all, delete-orphan")


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    analysis_id = Column(String, ForeignKey("analysis_results.id", ondelete="CASCADE"), nullable=False)
    category = Column(String, nullable=False)  # Behavioral (STAR), Technical, Skill Gap
    question = Column(Text, nullable=False)
    rationale = Column(Text, nullable=True)
    sample_answer_guide = Column(Text, nullable=True)
    difficulty = Column(String, default="Intermediate")

    analysis = relationship("AnalysisResult", back_populates="interview_questions")

