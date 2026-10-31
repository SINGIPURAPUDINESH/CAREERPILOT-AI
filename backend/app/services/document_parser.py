import re
import io
from typing import Dict, Tuple, Optional

class DocumentParserService:
    SECTION_HEADERS = {
        "summary": [r"summary", r"professional summary", r"profile", r"about me", r"objective"],
        "experience": [r"experience", r"work experience", r"employment history", r"professional experience", r"work history"],
        "skills": [r"skills", r"technical skills", r"competencies", r"core competencies", r"technologies"],
        "education": [r"education", r"academic background", r"qualifications", r"degrees"],
        "projects": [r"projects", r"personal projects", r"key projects", r"portfolio"],
        "certifications": [r"certifications", r"licenses", r"certificates", r"achievements"]
    }

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extracts text from PDF bytes using pypdf with fallback."""
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            return "\n".join(text_parts).strip()
        except ImportError:
            raise ImportError("pypdf is required for PDF parsing. Install it with: pip install pypdf")
        except Exception as e:
            raise ValueError(f"Failed to parse PDF document: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """Extracts text from DOCX bytes using python-docx."""
        try:
            import docx
            doc = docx.Document(io.BytesIO(file_bytes))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            return "\n".join(paragraphs).strip()
        except ImportError:
            raise ImportError("python-docx is required for DOCX parsing. Install it with: pip install python-docx")
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX document: {str(e)}")

    @classmethod
    def segment_sections(cls, raw_text: str) -> Dict[str, str]:
        """
        Segments plain resume text into semantic sections using regex heuristics.
        """
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        sections: Dict[str, list] = {
            "summary": [],
            "experience": [],
            "skills": [],
            "education": [],
            "projects": [],
            "certifications": [],
            "other": []
        }
        
        current_section = "other"

        for line in lines:
            normalized_line = line.lower().strip(" :#\t*-_")
            
            # Check if this line is a section header
            matched_header = None
            for section_name, patterns in cls.SECTION_HEADERS.items():
                for pat in patterns:
                    if re.fullmatch(pat, normalized_line):
                        matched_header = section_name
                        break
                if matched_header:
                    break
            
            if matched_header:
                current_section = matched_header
            else:
                sections[current_section].append(line)

        # Join lists into clean multiline strings
        return {
            sec: "\n".join(content_lines).strip()
            for sec, content_lines in sections.items()
            if content_lines
        }

    @staticmethod
    def estimate_experience_years(text: str) -> float:
        """
        Scans for date ranges (e.g., 2019 - 2023, 2021 - Present) to estimate total working years.
        """
        year_pattern = r"(20\d{2}|19\d{2})\s*(?:-|–|to)\s*(20\d{2}|present|current|now)"
        matches = re.findall(year_pattern, text.lower())
        
        total_years = 0.0
        current_year = 2026

        for start_str, end_str in matches:
            try:
                start = int(start_str)
                end = current_year if end_str in ["present", "current", "now"] else int(end_str)
                diff = max(0, end - start)
                if diff <= 40:  # Sanity check
                    total_years += diff
            except ValueError:
                continue

        # If date ranges aren't explicit, check for phrases like "5+ years of experience"
        if total_years == 0:
            exp_phrase = re.search(r"(\d+)\+?\s*years(?:\s*of)?\s*experience", text.lower())
            if exp_phrase:
                total_years = float(exp_phrase.group(1))

        return min(total_years, 30.0)

document_parser = DocumentParserService()
