# CareerPilot AI 🚀

> **AI Resume Analyzer & Job Matcher for Job Seekers**  
> *Upload a resume, match it against target job descriptions, uncover critical skill gaps, and practice role-tailored interview questions.*

---

## 🌟 Overview & Portfolio Value

**CareerPilot AI** bridges the preparation gap between applying for a role and succeeding in interviews. By coupling document processing and NLP skill extraction with semantic relevance scoring and LLM prompt engineering, CareerPilot AI gives job seekers quantifiable feedback on how closely their experience aligns with any target role.

### Why This Project Stands Out in a Portfolio:
- **Production-Grade Hybrid NLP:** Combines fast, deterministic taxonomy-based entity matching with neural vector similarity instead of relying purely on expensive or slow LLM calls.
- **Robust Document Ingestion:** Handles raw PDF and DOCX files, normalizing whitespace and segmenting documents into semantic sections (Experience, Skills, Education, Projects).
- **Tailored Interview Prep Arena:** Synthesizes realistic Behavioral (STAR), Technical Deep Dive, and Skill Gap Probing questions with sample answers and interviewer rationale.
- **Clean Full-Stack Architecture:** Separation of concerns between a reactive Next.js 14 frontend and an asynchronous FastAPI backend backed by PostgreSQL.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | [Next.js 14](https://nextjs.org/) (App Router), [TypeScript](https://www.typescriptlang.org/), [Tailwind CSS](https://tailwindcss.com/), [Lucide React](https://lucide.dev/) |
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/), Python 3.11+, [Pydantic v2](https://docs.pydantic.dev/) |
| **Document Processing** | `pypdf`, `python-docx` |
| **NLP & Scoring** | Custom Canonical Taxonomy (200+ skills), Cosine Similarity, Section Segmentation |
| **AI / LLM Integration** | [Google Gemini API](https://ai.google.dev/) (`gemini-2.5-flash` via `google-genai` SDK) with deterministic fallback |
| **Database** | [PostgreSQL](https://www.postgresql.org/) (via [SQLAlchemy 2.0](https://www.sqlalchemy.org/)) with automatic local SQLite fallback |
| **DevOps** | Docker, Docker Compose |

---

## 🏗️ Architecture & Workflow

```
[Resume PDF/DOCX] ──► [Document Parser] ──► [Section Segmentation]
                                                    │
                                                    ▼
[Job Description] ──► [NLP Extractor]    ──► [Skills Matrix]
                            │                       │
                            ▼                       ▼
                     [Taxonomy Match]    ──► [Hybrid Match Scorer]
                                                    │
                                                    ▼
                                            [Skill Gap Analysis]
                                                    │
                                                    ▼
                                            [Tailored Interview Q&A]
                                                    │
                                                    ▼
                                       [Next.js Interactive Arena]
```

### 1. Document Parsing & Section Segmentation
- Parses multi-page PDF and DOCX files.
- Heuristic regex boundaries segment raw text into `Summary`, `Experience`, `Education`, and `Skills`.
- Extracts estimated working years from chronological dates.

### 2. Hybrid NLP Skill Extraction
- Normalizes variations and aliases (e.g., `Postgres` ➔ `PostgreSQL`, `k8s` ➔ `Kubernetes`, `React.js` ➔ `React`).
- Categorizes identified competencies across:
  - Languages
  - Frameworks
  - Databases
  - Cloud & DevOps
  - AI / ML & Data Science
  - Architecture & Soft Skills

### 3. Multidimensional Match Scoring
- **Skill Coverage (50%):** Direct intersection between required JD competencies and candidate resume.
- **Semantic Alignment (35%):** N-gram vector cosine similarity between candidate experience bullet points and job responsibilities.
- **Experience Level Fit (15%):** Comparison between candidate tenure and target role seniority requirements.

### 4. Tailored Interview Question Generation
Generates targeted mock interview prompts categorized into:
- **Behavioral (STAR):** Probing real-world leadership, production incident resolution, and collaboration.
- **Technical Deep Dives:** Testing architectural understanding of the candidate's core strengths.
- **Skill Gap Probing:** Evaluating how the candidate handles technologies specified in the JD that are absent from their resume.

---

## 🚀 Quick Start Guide

### Option 1: Run with Docker Compose (Recommended)

1. Clone or navigate to the project directory:
   ```bash
   cd careerpilot-ai
   ```

2. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```
   *(Optional: Add your `GEMINI_API_KEY` in `.env` for AI-powered question synthesis. The app includes a dynamic fallback engine if no key is provided.)*

3. Launch all services:
   ```bash
   docker compose up --build
   ```

4. Open:
   - **Frontend:** [http://localhost:3000](http://localhost:3000)
   - **Backend API & Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Run Locally (Without Docker)

#### 1. Backend Setup
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
*Note: If no PostgreSQL instance is configured, CareerPilot automatically creates a local SQLite database (`careerpilot.db`) for immediate zero-config testing.*

#### 2. Frontend Setup
```bash
cd ../frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧪 Running Automated Tests

Run the test suite verifying skill extraction, document segmentation, match scoring, and interview question generation:
```bash
cd backend
python tests/test_nlp_and_matcher.py
```

---

## 💬 Portfolio Interview Talking Points

When presenting this project in engineering interviews:
1. **Explain the Hybrid NLP Design:** Discuss why you chose deterministic taxonomy extraction combined with vector similarity rather than prompting an LLM for everything (faster latency, sub-50ms execution, lower API cost, deterministic repeatability).
2. **Discuss Document Parsing Edge Cases:** Mention handling non-standard section headers, multi-column resumes, and date formats across different applicant backgrounds.
3. **Address Skill Gap Actionability:** Explain how the tool doesn't just score candidates negatively for missing skills, but categorizes transferable skills and suggests practical portfolio projects to close the gap.

