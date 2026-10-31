import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.nlp_extractor import nlp_extractor
from app.services.document_parser import document_parser
from app.services.matcher import matcher_service
from app.services.interview_generator import interview_generator

def test_skill_extraction():
    sample_text = """
    Senior Full Stack Engineer with 5+ years of experience building scalable applications.
    Proficient in Python, FastAPI, TypeScript, React, PostgreSQL, Docker, and AWS.
    Experience with Machine Learning and Natural Language Processing (NLP) models.
    """
    skills = nlp_extractor.extract_skills(sample_text)
    
    assert "Python" in skills
    assert "FastAPI" in skills
    assert "TypeScript" in skills
    assert "React" in skills
    assert "PostgreSQL" in skills
    assert "Docker" in skills
    assert "AWS" in skills
    assert "Natural Language Processing (NLP)" in skills

def test_document_segmentation():
    sample_resume = """
    Professional Summary
    Senior Developer with expertise in web systems.

    Work Experience
    Google - Software Engineer (2021 - Present)
    Built high-throughput distributed microservices.

    Education
    BS in Computer Science, Stanford University

    Technical Skills
    Python, Next.js, Kubernetes, Redis
    """
    sections = document_parser.segment_sections(sample_resume)
    assert "summary" in sections
    assert "experience" in sections
    assert "education" in sections
    assert "skills" in sections

def test_matcher_and_skill_gap():
    resume_skills = ["Python", "FastAPI", "React", "PostgreSQL", "Docker"]
    jd_skills = ["Python", "FastAPI", "PostgreSQL", "Kubernetes", "AWS", "Kafka"]
    
    match_result = matcher_service.analyze_match(
        resume_text="Experienced engineer working with Python and FastAPI on Docker containers.",
        resume_skills=resume_skills,
        jd_text="Looking for an engineer with Python, FastAPI, PostgreSQL, Kubernetes, AWS, and Kafka.",
        jd_skills=jd_skills,
        resume_exp_years=4.0
    )

    assert "Python" in match_result["matched_skills"]
    assert "FastAPI" in match_result["matched_skills"]
    assert "PostgreSQL" in match_result["matched_skills"]
    assert "Kubernetes" in match_result["missing_skills"]
    assert "AWS" in match_result["missing_skills"]
    assert match_result["overall_score"] > 40.0
    assert len(match_result["gap_recommendations"]) > 0

def test_interview_question_generation():
    questions = interview_generator.generate_interview_questions(
        role_title="Backend Engineer",
        matched_skills=["Python", "FastAPI", "PostgreSQL"],
        missing_skills=["Kubernetes", "AWS"]
    )

    assert len(questions) >= 5
    categories = [q["category"] for q in questions]
    assert "Behavioral (STAR)" in categories
    assert "Technical Deep Dive" in categories
    assert "Skill Gap Probing" in categories

if __name__ == "__main__":
    test_skill_extraction()
    test_document_segmentation()
    test_matcher_and_skill_gap()
    test_interview_question_generation()
    print("All unit tests passed successfully!")

