import json
import logging
from typing import List, Dict
from app.config import settings

logger = logging.getLogger(__name__)

class InterviewGeneratorService:
    @classmethod
    def generate_interview_questions(
        cls,
        role_title: str,
        matched_skills: List[str],
        missing_skills: List[str],
        resume_summary: str = "",
        jd_text: str = ""
    ) -> List[Dict[str, str]]:
        """
        Generates tailored interview questions. Uses Gemini API if configured,
        otherwise uses a deterministic dynamic question generator.
        """
        if settings.GEMINI_API_KEY:
            try:
                return cls._generate_with_gemini(
                    role_title=role_title,
                    matched_skills=matched_skills,
                    missing_skills=missing_skills,
                    resume_summary=resume_summary,
                    jd_text=jd_text
                )
            except Exception as e:
                logger.warning(f"Gemini API call failed, falling back to rule-based generator: {e}")

        return cls._generate_fallback_questions(
            role_title=role_title,
            matched_skills=matched_skills,
            missing_skills=missing_skills
        )

    @classmethod
    def _generate_with_gemini(
        cls,
        role_title: str,
        matched_skills: List[str],
        missing_skills: List[str],
        resume_summary: str,
        jd_text: str
    ) -> List[Dict[str, str]]:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        prompt = f"""
You are an expert technical interviewer and hiring manager for the role of {role_title}.
Analyze the candidate's profile against the job requirements:
- Matched Skills: {', '.join(matched_skills) if matched_skills else 'General software engineering skills'}
- Missing Skills from Job Description: {', '.join(missing_skills) if missing_skills else 'None identified'}
- Candidate Background: {resume_summary[:400] if resume_summary else 'Software Engineering'}

Generate exactly 5 tailored interview questions structured as JSON list:
1. Two Behavioral (STAR) questions that probe leadership, handling complexity, or resolving production incidents.
2. Two Technical Deep Dive questions specifically focused on the matched skills ({', '.join(matched_skills[:3])}).
3. One Skill Gap Probing question assessing how the candidate learns or bridges gaps in {missing_skills[0] if missing_skills else 'new emerging technologies'}.

Return ONLY a valid JSON array of objects with the exact schema:
[
  {{
    "category": "Behavioral (STAR)" | "Technical Deep Dive" | "Skill Gap Probing",
    "question": "The interview question",
    "rationale": "Why hiring managers ask this question for this role",
    "sample_answer_guide": "Structured bullet points on how to answer effectively using STAR or technical architecture principles",
    "difficulty": "Intermediate" | "Advanced"
  }}
]
"""
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.3
            )
        )
        
        parsed = json.loads(response.text)
        if isinstance(parsed, list):
            return parsed
        return cls._generate_fallback_questions(role_title, matched_skills, missing_skills)

    @classmethod
    def _generate_fallback_questions(
        cls,
        role_title: str,
        matched_skills: List[str],
        missing_skills: List[str]
    ) -> List[Dict[str, str]]:
        """High quality, realistic interview questions tailored to the matched & missing skills."""
        primary_skill = matched_skills[0] if matched_skills else "Python/Fullstack"
        second_skill = matched_skills[1] if len(matched_skills) > 1 else "REST APIs"
        gap_skill = missing_skills[0] if missing_skills else "Cloud Architecture / CI/CD"

        return [
            {
                "category": "Behavioral (STAR)",
                "question": f"Can you describe a challenging project where you utilized {primary_skill} to solve a critical business bottleneck or performance issue under tight deadlines?",
                "rationale": "Hiring managers ask this to evaluate your problem-solving depth, ownership under pressure, and ability to deliver measurable business impact.",
                "sample_answer_guide": "Structure your response with STAR: Situation (high traffic/latency issue), Task (your specific deliverable), Action (architectural redesign or optimization in " + primary_skill + "), Result (quantifiable metric like 40% latency reduction).",
                "difficulty": "Intermediate"
            },
            {
                "category": "Behavioral (STAR)",
                "question": "Tell me about a time you had a technical disagreement with a teammate or stakeholder over system design or implementation choices. How did you resolve it?",
                "rationale": "Assesses emotional intelligence, cross-functional collaboration, and objective decision-making based on trade-offs rather than ego.",
                "sample_answer_guide": "Highlight how you gathered benchmark data, created a proof-of-concept (POC), weighed latency vs complexity trade-offs, and maintained team cohesion.",
                "difficulty": "Intermediate"
            },
            {
                "category": "Technical Deep Dive",
                "question": f"When scaling an application built with {primary_skill} and {second_skill}, what are the most common concurrency, memory, or database connection bottlenecks, and how do you mitigate them?",
                "rationale": "Tests whether you understand production-level operational realities beyond standard tutorial code.",
                "sample_answer_guide": "Discuss connection pooling, asynchronous I/O loops, caching layers (e.g. Redis), database indexing strategies, and horizontal autoscaling.",
                "difficulty": "Advanced"
            },
            {
                "category": "Technical Deep Dive",
                "question": f"How do you design and structure secure, high-throughput interfaces between {primary_skill} services and upstream consumers, including authentication and rate limiting?",
                "rationale": "Evaluates hands-on knowledge of API gateway patterns, JWT/OAuth2 token validation, and distributed rate limiting (e.g., token bucket algorithms).",
                "sample_answer_guide": "Explain token verification at API gateway level, idempotency keys for mutable operations, and structured logging for observability.",
                "difficulty": "Advanced"
            },
            {
                "category": "Skill Gap Probing",
                "question": f"This role frequently requires working with {gap_skill}. While your resume highlights strong expertise in {primary_skill}, how would you approach ramping up quickly on {gap_skill} within your first 30 days?",
                "rationale": "Tests intellectual curiosity, learning velocity, and ability to transfer conceptual knowledge across differing frameworks or stacks.",
                "sample_answer_guide": "Mention parallel concepts between your existing stack and " + gap_skill + ", your methodology for reading official docs and building a sandbox POC, and how you leverage senior code reviews.",
                "difficulty": "Intermediate"
            }
        ]

interview_generator = InterviewGeneratorService()

