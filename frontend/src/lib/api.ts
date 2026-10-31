export interface InterviewQuestionItem {
  category: string;
  question: string;
  rationale: string;
  sample_answer_guide: string;
  difficulty: string;
}

export interface MatchAnalysisResponse {
  analysis_id?: string;
  overall_score: number;
  skill_coverage_score: number;
  semantic_score: number;
  experience_score: number;
  matched_skills: string[];
  missing_skills: string[];
  bonus_skills: string[];
  gap_recommendations: string[];
  interview_questions: InterviewQuestionItem[];
}

export interface ParsedResumeResponse {
  id?: string;
  filename?: string;
  sections: Record<string, string>;
  extracted_skills: string[];
  word_count: number;
  estimated_experience_years?: number;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function safeFetch(url: string, options: RequestInit): Promise<Response> {
  try {
    const res = await fetch(url, options);
    return res;
  } catch (err: any) {
    if (err.name === "TypeError" && err.message.toLowerCase().includes("fetch")) {
      throw new Error(
        "Could not connect to the CareerPilot backend at http://localhost:8000. " +
        "Please ensure the FastAPI backend is running! " +
        "(Run 'run-backend.bat' or 'python -m uvicorn app.main:app --reload --port 8000' in the backend folder)."
      );
    }
    throw err;
  }
}

export async function uploadResumeFile(file: File): Promise<ParsedResumeResponse> {
  // If it's a plain text file, we can also read it directly as fallback
  const formData = new FormData();
  formData.append("file", file);

  const res = await safeFetch(`${API_BASE_URL}/resumes/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Failed to upload and parse resume file.");
  }

  return res.json();
}

export async function analyzeFullPipeline(
  resumeText: string,
  jdText: string,
  roleTitle = "Senior Full Stack Engineer",
  company = "Tech Company"
): Promise<MatchAnalysisResponse> {
  const res = await safeFetch(`${API_BASE_URL}/match/full-pipeline`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      resume_text: resumeText,
      jd_text: jdText,
      role_title: roleTitle,
      company: company,
    }),
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Match analysis request failed.");
  }

  return res.json();
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const res = await fetch("http://localhost:8000/health", { method: "GET" });
    return res.ok;
  } catch {
    return false;
  }
}
