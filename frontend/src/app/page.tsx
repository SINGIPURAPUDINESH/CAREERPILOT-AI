"use client";

import React, { useState, useEffect } from "react";
import {
  Upload,
  FileText,
  Briefcase,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  Award,
  Zap,
  Target,
  ArrowRight,
  Server,
  RefreshCw,
} from "lucide-react";
import {
  analyzeFullPipeline,
  uploadResumeFile,
  checkBackendHealth,
  MatchAnalysisResponse,
} from "@/lib/api";

const SAMPLE_RESUME = `Alex Rivera
San Francisco, CA | alex.rivera@email.com | github.com/alexrivera

PROFESSIONAL SUMMARY
Senior Full Stack Engineer with 5+ years of experience building scalable distributed web applications, high-throughput REST APIs, and microservices. Proven track record leading frontend and backend teams, implementing CI/CD pipelines, and reducing system latency.

WORK EXPERIENCE
Senior Full Stack Engineer — CloudScale Technologies (2022 – Present)
• Architected and deployed microservices backend using FastAPI, Python, and PostgreSQL, reducing endpoint response times by 42%.
• Built dynamic frontends using Next.js, React, and TypeScript with Tailwind CSS for 100k+ monthly active users.
• Containerized microservices using Docker and orchestrated deployments via GitHub Actions CI/CD.
• Implemented caching strategies using Redis, improving database query efficiency by 65%.

Software Engineer — Apex Systems (2019 – 2022)
• Developed responsive web components in React and Node.js with Express.js and MongoDB.
• Implemented automated unit testing with Jest and PyTest, reaching 88% code coverage.
• Participated in Agile / Scrum rituals and mentored 3 junior developers.

TECHNICAL SKILLS
• Languages: Python, TypeScript, JavaScript, SQL, HTML/CSS, Bash/Shell
• Frameworks: Next.js, React, FastAPI, Node.js, Express.js, Tailwind CSS
• Databases: PostgreSQL, MongoDB, Redis
• Cloud & DevOps: Docker, CI/CD, GitHub Actions, Linux
• Concepts: RESTful APIs, Microservices, Agile / Scrum, Unit Testing`;

const SAMPLE_JD = `Role: Senior Full Stack AI & Cloud Engineer
Company: InnovateTech AI Solutions

About the Role:
We are looking for a Senior Full Stack Engineer to join our high-growth product team building AI-native workflow automation platforms. In this role, you will design scalable web systems, integrate large language models, and deploy reliable cloud infrastructure.

Key Qualifications & Requirements:
• 4+ years of professional software engineering experience.
• Strong proficiency in Python, FastAPI, TypeScript, and Next.js / React.
• Deep experience with relational databases, specifically PostgreSQL and query optimization.
• Hands-on experience with Cloud & DevOps: Amazon Web Services (AWS) and Kubernetes (k8s) container orchestration.
• Familiarity with Generative AI / LLMs, Natural Language Processing (NLP), or vector databases is strongly preferred.
• Experience with message streaming architectures (Apache Kafka) is a plus.
• Strong communication, problem-solving, and cross-functional leadership skills.`;

export default function Home() {
  const [resumeText, setResumeText] = useState("");
  const [jdText, setJdText] = useState("");
  const [roleTitle, setRoleTitle] = useState("Senior Full Stack AI & Cloud Engineer");
  const [company, setCompany] = useState("InnovateTech AI");
  const [isLoading, setIsLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [results, setResults] = useState<MatchAnalysisResponse | null>(null);
  const [activeTab, setActiveTab] = useState<string>("All");
  const [expandedQuestions, setExpandedQuestions] = useState<Record<number, boolean>>({});
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);

  const checkHealth = async () => {
    const ok = await checkBackendHealth();
    setBackendOnline(ok);
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 6000);
    return () => clearInterval(interval);
  }, []);

  const handleLoadSample = () => {
    setResumeText(SAMPLE_RESUME);
    setJdText(SAMPLE_JD);
    setRoleTitle("Senior Full Stack AI & Cloud Engineer");
    setCompany("InnovateTech AI");
    setErrorMsg(null);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      setIsLoading(true);
      setErrorMsg(null);

      // If user uploaded a plain text file, we can read it client-side immediately
      if (file.name.endsWith(".txt") || file.name.endsWith(".md") || file.type.startsWith("text/")) {
        const text = await file.text();
        if (text.trim()) {
          setResumeText(text);
          setIsLoading(false);
          return;
        }
      }

      const parsed = await uploadResumeFile(file);
      const fullText = Object.values(parsed.sections).join("\n\n");
      setResumeText(fullText || `Uploaded file: ${file.name}`);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to parse uploaded resume.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      setErrorMsg("Please upload or paste your resume.");
      return;
    }
    if (!jdText.trim()) {
      setErrorMsg("Please provide the target job description.");
      return;
    }

    try {
      setIsLoading(true);
      setErrorMsg(null);
      const data = await analyzeFullPipeline(resumeText, jdText, roleTitle, company);
      setResults(data);
      // Auto-expand the first question
      setExpandedQuestions({ 0: true });
    } catch (err: any) {
      setErrorMsg(err.message || "Error running match analysis.");
    } finally {
      setIsLoading(false);
    }
  };

  const toggleQuestion = (idx: number) => {
    setExpandedQuestions((prev) => ({
      ...prev,
      [idx]: !prev[idx],
    }));
  };

  const filteredQuestions =
    activeTab === "All"
      ? results?.interview_questions || []
      : (results?.interview_questions || []).filter((q) => q.category.includes(activeTab));

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-emerald-600 bg-emerald-50 border-emerald-200";
    if (score >= 60) return "text-amber-600 bg-amber-50 border-amber-200";
    return "text-rose-600 bg-rose-50 border-rose-200";
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      {/* Hero Section */}
      <div className="text-center max-w-3xl mx-auto mb-10">
        <div className="flex flex-wrap items-center justify-center gap-2 mb-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Resume Analyzer & Job Matcher</span>
          </div>

          {backendOnline === true && (
            <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Backend Online (FastAPI)</span>
            </div>
          )}

          {backendOnline === false && (
            <div className="inline-flex items-center space-x-1.5 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-rose-500" />
              <span>Backend Offline — Run `run-backend.bat`</span>
            </div>
          )}
        </div>

        <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight text-slate-900 mb-4">
          Land Interviews with <span className="text-indigo-600">Precision Matching</span>
        </h1>
        <p className="text-base sm:text-lg text-slate-600 mb-6">
          Compare your resume against any job posting, uncover critical skill gaps, and practice
          tailored behavioral & technical interview questions designed for the role.
        </p>
        <button
          onClick={handleLoadSample}
          className="inline-flex items-center space-x-2 text-xs font-semibold px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition border border-slate-300"
        >
          <Zap className="w-3.5 h-3.5 text-indigo-600" />
          <span>Load Sample Fullstack Resume & Job Description</span>
        </button>
      </div>

      {/* Error Banner */}
      {errorMsg && (
        <div className="mb-6 p-4 rounded-xl bg-rose-50 border border-rose-200 flex items-center space-x-3 text-rose-700 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Inputs Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
        {/* Resume Input Card */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <FileText className="w-5 h-5 text-indigo-600" />
                <h2 className="font-bold text-lg text-slate-900">Your Resume</h2>
              </div>
              <label className="cursor-pointer inline-flex items-center space-x-1.5 text-xs font-semibold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-lg border border-indigo-200 transition">
                <Upload className="w-3.5 h-3.5" />
                <span>Upload PDF / DOCX</span>
                <input
                  type="file"
                  accept=".pdf,.docx,.txt"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </label>
            </div>
            <textarea
              rows={14}
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              placeholder="Paste plain resume text or upload your PDF/DOCX resume file above..."
              className="w-full text-xs font-mono p-3.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-slate-50/50"
            />
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
            <span>Supports PDF, DOCX, TXT</span>
            <span>{resumeText.split(/\s+/).filter(Boolean).length} words</span>
          </div>
        </div>

        {/* Job Description Card */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <Briefcase className="w-5 h-5 text-indigo-600" />
              <h2 className="font-bold text-lg text-slate-900">Target Job Description</h2>
            </div>
            <div className="grid grid-cols-2 gap-3 mb-3">
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Target Role</label>
                <input
                  type="text"
                  value={roleTitle}
                  onChange={(e) => setRoleTitle(e.target.value)}
                  placeholder="e.g. Senior Software Engineer"
                  className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label className="block text-xs font-semibold text-slate-600 mb-1">Company</label>
                <input
                  type="text"
                  value={company}
                  onChange={(e) => setCompany(e.target.value)}
                  placeholder="e.g. InnovateTech"
                  className="w-full text-xs px-3 py-2 rounded-lg border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>
            <textarea
              rows={12}
              value={jdText}
              onChange={(e) => setJdText(e.target.value)}
              placeholder="Paste the full job description here (requirements, qualifications, tech stack)..."
              className="w-full text-xs font-mono p-3.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-slate-50/50"
            />
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
            <span>Paste from LinkedIn, Indeed, Greenhouse</span>
            <span>{jdText.split(/\s+/).filter(Boolean).length} words</span>
          </div>
        </div>
      </div>

      {/* CTA Button */}
      <div className="text-center mb-12">
        <button
          onClick={handleAnalyze}
          disabled={isLoading}
          className="inline-flex items-center space-x-2.5 px-8 py-3.5 rounded-xl bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-base shadow-lg shadow-indigo-200 transition disabled:opacity-50"
        >
          {isLoading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              <span>Analyzing Resume & Synthesizing Questions...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5" />
              <span>Analyze Match & Generate Interview Prep</span>
              <ArrowRight className="w-4 h-4 ml-1" />
            </>
          )}
        </button>
      </div>

      {/* Results Dashboard */}
      {results && (
        <div className="space-y-8 animate-fadeIn">
          {/* Top Score Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {/* Overall Score */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col items-center justify-center text-center">
              <span className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                Overall Match Score
              </span>
              <div className="text-5xl font-extrabold text-indigo-600 mb-2">
                {results.overall_score}%
              </div>
              <div
                className={`text-xs font-semibold px-3 py-1 rounded-full border ${getScoreColor(
                  results.overall_score
                )}`}
              >
                {results.overall_score >= 80
                  ? "High Match Alignment"
                  : results.overall_score >= 60
                  ? "Strong Potential Candidate"
                  : "Moderate Fit / Gaps Identified"}
              </div>
            </div>

            {/* Sub-Score 1: Skill Coverage */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                  Skill Coverage
                </span>
                <div className="text-3xl font-extrabold text-slate-900 mt-2 mb-1">
                  {results.skill_coverage_score}%
                </div>
                <p className="text-xs text-slate-500">
                  {results.matched_skills.length} matched out of{" "}
                  {results.matched_skills.length + results.missing_skills.length} required skills.
                </p>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 mt-4">
                <div
                  className="bg-emerald-500 h-2 rounded-full"
                  style={{ width: `${Math.min(100, results.skill_coverage_score)}%` }}
                />
              </div>
            </div>

            {/* Sub-Score 2: Semantic Relevance */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                  Semantic Alignment
                </span>
                <div className="text-3xl font-extrabold text-slate-900 mt-2 mb-1">
                  {results.semantic_score}%
                </div>
                <p className="text-xs text-slate-500">
                  Vector cosine similarity between work history and role responsibilities.
                </p>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 mt-4">
                <div
                  className="bg-indigo-500 h-2 rounded-full"
                  style={{ width: `${Math.min(100, results.semantic_score)}%` }}
                />
              </div>
            </div>

            {/* Sub-Score 3: Experience Fit */}
            <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col justify-between">
              <div>
                <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                  Experience Fit
                </span>
                <div className="text-3xl font-extrabold text-slate-900 mt-2 mb-1">
                  {results.experience_score}%
                </div>
                <p className="text-xs text-slate-500">
                  Years of experience and seniority level match for {roleTitle}.
                </p>
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 mt-4">
                <div
                  className="bg-sky-500 h-2 rounded-full"
                  style={{ width: `${Math.min(100, results.experience_score)}%` }}
                />
              </div>
            </div>
          </div>

          {/* Skills Breakdown Matrix */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <h3 className="font-bold text-lg text-slate-900 mb-6 flex items-center space-x-2">
              <Target className="w-5 h-5 text-indigo-600" />
              <span>Skills Gap & Alignment Matrix</span>
            </h3>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Matched Skills */}
              <div className="p-4 rounded-xl bg-emerald-50/50 border border-emerald-200">
                <div className="flex items-center space-x-2 text-emerald-800 font-bold text-sm mb-3">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  <span>Matched Skills ({results.matched_skills.length})</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {results.matched_skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2.5 py-1 bg-white text-emerald-800 text-xs font-semibold rounded-lg border border-emerald-200 shadow-xs"
                    >
                      {skill}
                    </span>
                  ))}
                  {results.matched_skills.length === 0 && (
                    <span className="text-xs text-emerald-600">No direct skills matched.</span>
                  )}
                </div>
              </div>

              {/* Missing Skills */}
              <div className="p-4 rounded-xl bg-rose-50/50 border border-rose-200">
                <div className="flex items-center space-x-2 text-rose-800 font-bold text-sm mb-3">
                  <AlertCircle className="w-4 h-4 text-rose-600" />
                  <span>Missing Skills ({results.missing_skills.length})</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {results.missing_skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2.5 py-1 bg-white text-rose-800 text-xs font-semibold rounded-lg border border-rose-200 shadow-xs"
                    >
                      {skill}
                    </span>
                  ))}
                  {results.missing_skills.length === 0 && (
                    <span className="text-xs text-rose-600">No missing skills detected!</span>
                  )}
                </div>
              </div>

              {/* Bonus Skills */}
              <div className="p-4 rounded-xl bg-indigo-50/50 border border-indigo-200">
                <div className="flex items-center space-x-2 text-indigo-800 font-bold text-sm mb-3">
                  <Award className="w-4 h-4 text-indigo-600" />
                  <span>Bonus Resume Skills ({results.bonus_skills.length})</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {results.bonus_skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2.5 py-1 bg-white text-indigo-800 text-xs font-semibold rounded-lg border border-indigo-200 shadow-xs"
                    >
                      {skill}
                    </span>
                  ))}
                  {results.bonus_skills.length === 0 && (
                    <span className="text-xs text-indigo-600">No additional skills noted.</span>
                  )}
                </div>
              </div>
            </div>

            {/* Recommendations */}
            {results.gap_recommendations.length > 0 && (
              <div className="mt-6 p-4 rounded-xl bg-slate-50 border border-slate-200">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2 flex items-center space-x-1.5">
                  <Zap className="w-3.5 h-3.5 text-amber-500" />
                  <span>Actionable Upskilling Recommendations</span>
                </h4>
                <ul className="space-y-1.5 text-xs text-slate-600 list-disc list-inside">
                  {results.gap_recommendations.map((rec, i) => (
                    <li key={i}>{rec}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* Tailored Interview Questions Arena */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm">
            <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 pb-4 border-b border-slate-100 gap-4">
              <div>
                <h3 className="font-bold text-xl text-slate-900 flex items-center space-x-2">
                  <HelpCircle className="w-5 h-5 text-indigo-600" />
                  <span>Tailored Interview Preparation Arena</span>
                </h3>
                <p className="text-xs text-slate-500 mt-1">
                  Questions generated specifically based on your matched strengths and identified skill gaps for {roleTitle}.
                </p>
              </div>

              {/* Category Filter Tabs */}
              <div className="flex items-center space-x-1 bg-slate-100 p-1 rounded-xl text-xs font-semibold">
                {["All", "Behavioral", "Technical", "Skill Gap"].map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-3 py-1.5 rounded-lg transition ${
                      activeTab === tab
                        ? "bg-white text-indigo-700 shadow-xs"
                        : "text-slate-600 hover:text-slate-900"
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>
            </div>

            {/* Questions List */}
            <div className="space-y-4">
              {filteredQuestions.map((q, idx) => {
                const isExpanded = !!expandedQuestions[idx];
                return (
                  <div
                    key={idx}
                    className="border border-slate-200 rounded-xl overflow-hidden hover:border-indigo-200 transition"
                  >
                    <div
                      onClick={() => toggleQuestion(idx)}
                      className="p-4 sm:p-5 cursor-pointer bg-slate-50/50 hover:bg-slate-50 flex items-start justify-between gap-4 select-none"
                    >
                      <div className="space-y-2">
                        <div className="flex items-center space-x-2">
                          <span
                            className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md ${
                              q.category.includes("Behavioral")
                                ? "bg-amber-100 text-amber-800"
                                : q.category.includes("Technical")
                                ? "bg-indigo-100 text-indigo-800"
                                : "bg-rose-100 text-rose-800"
                            }`}
                          >
                            {q.category}
                          </span>
                          <span className="text-[10px] font-semibold text-slate-500 bg-slate-200 px-2 py-0.5 rounded-md">
                            {q.difficulty}
                          </span>
                        </div>
                        <h4 className="font-semibold text-sm sm:text-base text-slate-900 leading-snug">
                          {q.question}
                        </h4>
                      </div>
                      <button className="text-slate-400 hover:text-slate-600 mt-1 flex-shrink-0">
                        {isExpanded ? (
                          <ChevronUp className="w-5 h-5" />
                        ) : (
                          <ChevronDown className="w-5 h-5" />
                        )}
                      </button>
                    </div>

                    {isExpanded && (
                      <div className="p-4 sm:p-5 border-t border-slate-200 bg-white space-y-4 text-xs">
                        <div>
                          <span className="font-bold text-slate-700 uppercase tracking-wider text-[11px] block mb-1">
                            Why Interviewers Ask This:
                          </span>
                          <p className="text-slate-600 leading-relaxed">{q.rationale}</p>
                        </div>
                        <div className="p-3.5 rounded-xl bg-indigo-50/60 border border-indigo-100">
                          <span className="font-bold text-indigo-900 uppercase tracking-wider text-[11px] block mb-1">
                            Sample Answer Guide & Key Points to Hit:
                          </span>
                          <p className="text-indigo-800 leading-relaxed font-mono text-[11.5px]">
                            {q.sample_answer_guide}
                          </p>
                        </div>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

