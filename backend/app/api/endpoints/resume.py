from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.db.session import get_db
from app.db.models import Resume
from app.schemas.resume import ParsedResumeResponse, ResumeParseRequest
from app.services.document_parser import document_parser
from app.services.nlp_extractor import nlp_extractor

router = APIRouter()

@router.post("/parse", response_model=ParsedResumeResponse)
def parse_resume_text(
    payload: ResumeParseRequest,
    db: Session = Depends(get_db)
):
    """Parses raw text resume, segments sections, and extracts normalized skills."""
    if not payload.raw_text or not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="Resume text cannot be empty.")

    raw_text = payload.raw_text
    sections = document_parser.segment_sections(raw_text)
    skills = nlp_extractor.extract_skills(raw_text)
    exp_years = document_parser.estimate_experience_years(raw_text)

    resume_record = Resume(
        filename="pasted_text.txt",
        raw_text=raw_text,
        parsed_sections=sections,
        extracted_skills=skills
    )
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    return ParsedResumeResponse(
        id=resume_record.id,
        filename=resume_record.filename,
        sections=sections,
        extracted_skills=skills,
        word_count=len(raw_text.split()),
        estimated_experience_years=exp_years
    )

@router.post("/upload", response_model=ParsedResumeResponse)
def upload_resume_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Uploads a PDF or DOCX file, extracts text, sections, and skills."""
    filename = file.filename or "resume"
    extension = filename.lower().split(".")[-1] if "." in filename else "txt"
    content = file.file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if extension == "pdf":
        raw_text = document_parser.extract_text_from_pdf(content)
    elif extension in ["docx", "doc"]:
        raw_text = document_parser.extract_text_from_docx(content)
    elif extension in ["txt", "md", "rtf"]:
        raw_text = content.decode("utf-8", errors="ignore")
    else:
        # Fallback: try decoding as text
        try:
            raw_text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format (.{extension}). Please upload a PDF (.pdf), Word Document (.docx), or plain text file (.txt)."
            )

    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract readable text from the uploaded file.")

    sections = document_parser.segment_sections(raw_text)
    skills = nlp_extractor.extract_skills(raw_text)
    exp_years = document_parser.estimate_experience_years(raw_text)

    resume_record = Resume(
        filename=filename,
        raw_text=raw_text,
        parsed_sections=sections,
        extracted_skills=skills
    )
    db.add(resume_record)
    db.commit()
    db.refresh(resume_record)

    return ParsedResumeResponse(
        id=resume_record.id,
        filename=filename,
        sections=sections,
        extracted_skills=skills,
        word_count=len(raw_text.split()),
        estimated_experience_years=exp_years
    )

