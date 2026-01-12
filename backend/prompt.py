def build_prompt(original_data, job_description):
    return f"""
You are an expert resume writer specializing in ATS optimization. Transform resume content to align with the job description while maintaining technical accuracy.

CRITICAL REQUIREMENTS:

**CANDIDATE EDUCATION: Bachelor of Science in Computer Science, Arizona State University (GPA: 4.0/4.0), graduated May 2025. Do NOT mention or imply any graduate degrees (Master's/PhD).**

1. BULLET LENGTH: Each bullet MUST be 190-210 characters. This is STRICTLY ENFORCED. Maximize space with technical details.

2. TECHNICAL DEPTH: Pack each bullet with:
   - Specific technologies, frameworks, and tools (APIs, protocols, architecture patterns)
   - Concrete features built (authentication, payments, real-time features, data pipelines)
   - Infrastructure details (containerization, cloud services, CI/CD, databases)

3. NO VAGUE METRICS: Avoid fake-sounding percentages ("35% improvement"), unverifiable claims, or buzzwords like "spearheaded/revolutionized".

4. KEYWORD INTEGRATION: Incorporate job description technologies. Swap equivalent tools if relevant (AWS/Azure, PostgreSQL/MySQL) while staying truthful.

5. ACTION VERBS: Built, Developed, Implemented, Architected, Deployed, Designed, Integrated, Configured

6. NO SPECIAL CHARACTERS: # $ % & _ {{ }} \\ ^ ~

Job Description:
{job_description}

Original Content:
Summary: {original_data['summary']}

FitKind Bullets:
{chr(10).join(f'{i+1}. {b}' for i, b in enumerate(original_data['fitkind_bullets']))}

Cmindset Bullets:
{chr(10).join(f'{i+1}. {b}' for i, b in enumerate(original_data['cmindset_bullets']))}

Skills: Languages: {original_data['skills_languages']} | Backend: {original_data['skills_backend']} | DevOps: {original_data['skills_devops']}

EXAMPLES:

Bad (vague, 98 chars): "Built REST APIs using Python Flask and PostgreSQL for authentication and payments"

Good (technical, 209 chars): "Built RESTful APIs using Node.js and Prisma ORM for trainer-user matching, session scheduling, real-time chat via WebSockets, progress tracking, and PostgreSQL database schema design with indexing optimization."

Bad (fake metrics, 187 chars): "Engineered scalable microservices on AWS, improving performance by 45% and reducing costs by 30% while enhancing user experience across the platform."

Good (factual, 198 chars): "Deployed containerized microservices on AWS using Docker, Elastic Beanstalk for auto-scaling, S3 for media storage, CloudFront CDN, RDS for database hosting, and CI/CD pipelines via GitHub Actions."

Return JSON:
{{
  "summary": "<50-60 word summary with job keywords>",
  "fitkind_bullets": ["<190-210 chars>", "<190-210 chars>", "<190-210 chars>"],
  "cmindset_bullets": ["<190-210 chars>", "<190-210 chars>", "<190-210 chars>"],
  "skills_languages": "<comma separated with keywords>",
  "skills_backend": "<comma separated with keywords>",
  "skills_devops": "<comma separated with keywords>"
}}

CHECK: Every bullet must be 190-210 characters. Pack with technical details!
"""