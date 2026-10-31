import re
from typing import List, Dict, Set, Tuple

class NLPExtractorService:
    # Standard Canonical Taxonomy mapping aliases to standard canonical names
    SKILL_TAXONOMY = {
        # Programming Languages
        "python": "Python",
        "typescript": "TypeScript",
        "javascript": "JavaScript",
        "golang": "Go",
        "go": "Go",
        "rust": "Rust",
        "java": "Java",
        "c++": "C++",
        "cpp": "C++",
        "c#": "C#",
        "csharp": "C#",
        "sql": "SQL",
        "r": "R",
        "ruby": "Ruby",
        "php": "PHP",
        "html": "HTML/CSS",
        "css": "HTML/CSS",
        "bash": "Bash/Shell",
        "shell": "Bash/Shell",

        # Frameworks & Libraries
        "next.js": "Next.js",
        "nextjs": "Next.js",
        "react": "React",
        "react.js": "React",
        "reactjs": "React",
        "fastapi": "FastAPI",
        "fast api": "FastAPI",
        "node.js": "Node.js",
        "nodejs": "Node.js",
        "node": "Node.js",
        "express": "Express.js",
        "express.js": "Express.js",
        "django": "Django",
        "flask": "Flask",
        "vue": "Vue.js",
        "vue.js": "Vue.js",
        "angular": "Angular",
        "spring boot": "Spring Boot",
        "springboot": "Spring Boot",
        "tailwind": "Tailwind CSS",
        "tailwindcss": "Tailwind CSS",

        # Databases & Storage
        "postgresql": "PostgreSQL",
        "postgres": "PostgreSQL",
        "mysql": "MySQL",
        "mongodb": "MongoDB",
        "mongo": "MongoDB",
        "redis": "Redis",
        "dynamodb": "DynamoDB",
        "cassandra": "Cassandra",
        "elasticsearch": "Elasticsearch",
        "sqlite": "SQLite",
        "snowflake": "Snowflake",
        "bigquery": "BigQuery",

        # Cloud & DevOps
        "aws": "AWS",
        "amazon web services": "AWS",
        "gcp": "Google Cloud (GCP)",
        "google cloud": "Google Cloud (GCP)",
        "azure": "Microsoft Azure",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "k8s": "Kubernetes",
        "terraform": "Terraform",
        "ci/cd": "CI/CD",
        "github actions": "GitHub Actions",
        "gitlab ci": "GitLab CI",
        "linux": "Linux",
        "helm": "Helm",
        "ansible": "Ansible",

        # AI, Data & ML
        "nlp": "Natural Language Processing (NLP)",
        "natural language processing": "Natural Language Processing (NLP)",
        "machine learning": "Machine Learning",
        "deep learning": "Deep Learning",
        "llm": "LLMs & Generative AI",
        "llms": "LLMs & Generative AI",
        "large language models": "LLMs & Generative AI",
        "generative ai": "LLMs & Generative AI",
        "genai": "LLMs & Generative AI",
        "langchain": "LangChain",
        "llamaindex": "LlamaIndex",
        "pytorch": "PyTorch",
        "tensorflow": "TensorFlow",
        "scikit-learn": "Scikit-Learn",
        "sklearn": "Scikit-Learn",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "vector database": "Vector Databases",
        "vector search": "Vector Search",
        "rag": "RAG (Retrieval-Augmented Generation)",

        # Architecture & Concepts
        "rest": "RESTful APIs",
        "restful": "RESTful APIs",
        "graphql": "GraphQL",
        "microservices": "Microservices",
        "event-driven": "Event-Driven Architecture",
        "kafka": "Apache Kafka",
        "rabbitmq": "RabbitMQ",
        "system design": "System Design",
        "distributed systems": "Distributed Systems",
        "unit testing": "Unit Testing",
        "tdd": "Test-Driven Development (TDD)",
        "agile": "Agile / Scrum",
        "scrum": "Agile / Scrum",

        # Soft Skills
        "leadership": "Technical Leadership",
        "mentorship": "Mentorship",
        "communication": "Effective Communication",
        "problem solving": "Problem Solving",
        "cross-functional": "Cross-Functional Collaboration",
        "project management": "Project Management"
    }

    @classmethod
    def extract_skills(cls, text: str) -> List[str]:
        """
        Extracts and normalizes skills from text using word boundary patterns.
        """
        if not text:
            return []
            
        found_skills: Set[str] = set()
        lowered_text = f" {text.lower()} "

        # Sort keys by length descending to match multi-word phrases first (e.g. 'google cloud' before 'go')
        sorted_patterns = sorted(cls.SKILL_TAXONOMY.keys(), key=lambda k: len(k), reverse=True)

        for pattern in sorted_patterns:
            canonical = cls.SKILL_TAXONOMY[pattern]
            # Escape regex characters
            escaped = re.escape(pattern)
            # Match with boundary check
            regex = rf"(?:^|[^\w#+]){escaped}(?:[^\w#+]|$)"
            if re.search(regex, lowered_text):
                found_skills.add(canonical)
                # Remove matched phrase to prevent double matching substring words
                lowered_text = re.sub(regex, " ", lowered_text)

        return sorted(list(found_skills))

    @classmethod
    def categorize_skills(cls, skills: List[str]) -> Dict[str, List[str]]:
        """Group canonical skills into high-level domains for reporting."""
        categories = {
            "Languages": ["Python", "TypeScript", "JavaScript", "Go", "Rust", "Java", "C++", "C#", "SQL", "R", "Ruby", "PHP", "HTML/CSS", "Bash/Shell"],
            "Frameworks": ["Next.js", "React", "FastAPI", "Node.js", "Express.js", "Django", "Flask", "Vue.js", "Angular", "Spring Boot", "Tailwind CSS"],
            "Databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "DynamoDB", "Cassandra", "Elasticsearch", "SQLite", "Snowflake", "BigQuery"],
            "Cloud & Infrastructure": ["AWS", "Google Cloud (GCP)", "Microsoft Azure", "Docker", "Kubernetes", "Terraform", "CI/CD", "GitHub Actions", "GitLab CI", "Linux", "Helm", "Ansible"],
            "AI / Data Science": ["Natural Language Processing (NLP)", "Machine Learning", "Deep Learning", "LLMs & Generative AI", "LangChain", "LlamaIndex", "PyTorch", "TensorFlow", "Scikit-Learn", "Pandas", "NumPy", "Vector Databases", "Vector Search", "RAG (Retrieval-Augmented Generation)"],
            "Architecture & Practices": ["RESTful APIs", "GraphQL", "Microservices", "Event-Driven Architecture", "Apache Kafka", "RabbitMQ", "System Design", "Distributed Systems", "Unit Testing", "Test-Driven Development (TDD)", "Agile / Scrum"],
            "Soft Skills": ["Technical Leadership", "Mentorship", "Effective Communication", "Problem Solving", "Cross-Functional Collaboration", "Project Management"]
        }
        
        result: Dict[str, List[str]] = {k: [] for k in categories}
        result["Other"] = []

        for skill in skills:
            assigned = False
            for cat, member_skills in categories.items():
                if skill in member_skills:
                    result[cat].append(skill)
                    assigned = True
                    break
            if not assigned:
                result["Other"].append(skill)

        return {k: v for k, v in result.items() if v}

nlp_extractor = NLPExtractorService()

