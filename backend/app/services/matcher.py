import re
import math
from typing import List, Dict, Set, Tuple
from collections import Counter

class MatcherService:
    @staticmethod
    def _compute_cosine_similarity(text1: str, text2: str) -> float:
        """
        Computes cosine similarity between two text corpuses using word frequency vectors.
        """
        def tokenize(text: str) -> List[str]:
            return [w for w in re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower()) if len(w) > 2]

        tokens1 = tokenize(text1)
        tokens2 = tokenize(text2)

        if not tokens1 or not tokens2:
            return 0.0

        vec1 = Counter(tokens1)
        vec2 = Counter(tokens2)

        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([val ** 2 for val in vec1.values()])
        sum2 = sum([val ** 2 for val in vec2.values()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        return float(numerator) / denominator

    @classmethod
    def analyze_match(
        cls, 
        resume_text: str, 
        resume_skills: List[str], 
        jd_text: str, 
        jd_skills: List[str],
        resume_exp_years: float = 0.0
    ) -> Dict:
        """
        Performs holistic match scoring and skill gap identification.
        """
        resume_skill_set = set(resume_skills)
        jd_skill_set = set(jd_skills)

        # 1. Skill overlap calculation
        matched_skills = sorted(list(resume_skill_set & jd_skill_set))
        missing_skills = sorted(list(jd_skill_set - resume_skill_set))
        bonus_skills = sorted(list(resume_skill_set - jd_skill_set))

        # Skill coverage score (0 - 100)
        if jd_skill_set:
            skill_coverage_score = round((len(matched_skills) / len(jd_skill_set)) * 100, 1)
        else:
            skill_coverage_score = 75.0  # fallback when JD has generic skill definitions

        # 2. Semantic text similarity (0 - 100)
        raw_semantic = cls._compute_cosine_similarity(resume_text, jd_text)
        # Scaled up because raw cosine on different document lengths typically ranges from 0.2 to 0.7
        semantic_score = min(100.0, round(raw_semantic * 160.0, 1))

        # 3. Experience alignment score (0 - 100)
        # Check if JD mentions minimum years (e.g., "5+ years", "3 years of experience")
        exp_match = re.search(r"(\d+)\+?\s*years(?:\s*of)?\s*experience", jd_text.lower())
        required_years = float(exp_match.group(1)) if exp_match else 3.0

        if resume_exp_years >= required_years:
            experience_score = 100.0
        elif resume_exp_years > 0:
            experience_score = round((resume_exp_years / required_years) * 90.0, 1)
        else:
            experience_score = 70.0  # reasonable neutral default

        # 4. Composite overall score
        # 50% Skill Coverage, 35% Semantic Similarity, 15% Experience Fit
        overall_score = round(
            (skill_coverage_score * 0.50) + 
            (semantic_score * 0.35) + 
            (experience_score * 0.15), 
            1
        )
        overall_score = max(0.0, min(100.0, overall_score))

        # 5. Generate tailored gap recommendations
        recommendations = cls.generate_recommendations(missing_skills, bonus_skills)

        return {
            "overall_score": overall_score,
            "skill_coverage_score": skill_coverage_score,
            "semantic_score": semantic_score,
            "experience_score": experience_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "bonus_skills": bonus_skills[:8],  # limit top bonus skills
            "gap_recommendations": recommendations
        }

    @staticmethod
    def generate_recommendations(missing_skills: List[str], bonus_skills: List[str]) -> List[str]:
        recommendations = []
        if not missing_skills:
            recommendations.append("Your resume aligns closely with all critical requirements in this job posting.")
            return recommendations

        for skill in missing_skills[:4]:
            if skill in ["AWS", "Google Cloud (GCP)", "Microsoft Azure"]:
                recommendations.append(f"Consider deploying a portfolio capstone on {skill} using free-tier services to demonstrate hands-on cloud experience.")
            elif skill in ["Docker", "Kubernetes", "CI/CD", "Terraform"]:
                recommendations.append(f"Add a containerized build pipeline or IaC configuration using {skill} in one of your public GitHub projects.")
            elif skill in ["PostgreSQL", "Redis", "MongoDB", "Elasticsearch"]:
                recommendations.append(f"Highlight data modeling, indexing, or caching architectures involving {skill} in your project bullet points.")
            elif skill in ["LLMs & Generative AI", "Natural Language Processing (NLP)", "LangChain", "Vector Databases"]:
                recommendations.append(f"Incorporate an AI/LLM integration feature (e.g. RAG, embeddings search) using {skill} to showcase practical AI engineering.")
            else:
                recommendations.append(f"Review core concepts for {skill} and highlight any related or transferable tool experience on your resume.")

        if bonus_skills:
            top_bonus = ", ".join(bonus_skills[:3])
            recommendations.append(f"Leverage your proficiency in {top_bonus} as a competitive differentiator during your introductory pitch.")

        return recommendations

matcher_service = MatcherService()

