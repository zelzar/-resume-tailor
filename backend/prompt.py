def build_prompt(original_data, job_description):
    return f"""
You are an expert resume writer specializing in ATS optimization. Transform resume content to align with the job description while maintaining technical accuracy.

CRITICAL REQUIREMENTS:

**CANDIDATE EDUCATION: Bachelor of Science in Computer Science, Arizona State University (GPA: 4.0/4.0), already graduated in May 2025. Do NOT mention or imply any graduate degrees (Master's/PhD).**

1. BULLET LENGTH: Each bullet MUST be 195-207 characters including space. This is STRICTLY ENFORCED. Maximize space with technical details.

2. TECHNICAL DEPTH: Pack each bullet with:
   - Specific technologies, frameworks, and tools (APIs, protocols, architecture patterns). Or vaguely fit along if job description is vague.
   - Concrete features built (authentication, payments, real-time features, data pipelines)
   - Infrastructure details (containerization, cloud services, CI/CD, databases)/Related info to job description.

3.If job is very different from original content, adapt skills/technologies to match job description while staying truthful but dont change it 100%.

4. NOT Very VAGUE METRICS: Avoid fake-sounding percentages ("35% improvement"), big claims, or buzzwords like "spearheaded/revolutionized". Can use believable, metrics.

5. KEYWORD INTEGRATION: Incorporate job description technologies. Swap equivalent tools if relevant (AWS/Azure, PostgreSQL/MySQL) while staying truthful and little deviation.

6. ACTION VERBS: Built, Developed, Implemented, Architected, Deployed, Designed, Integrated, Configured

7. NO SPECIAL CHARACTERS: # $ % & _ {{ }} \\ ^ ~
Job Description:
{job_description}

Original Content:
Summary: {original_data['summary']}
(Note: I only speak English/Hindi so dont add languages in summary unless necessity of these 2.)

FitKind Bullets:
{chr(10).join(f'{i+1}. {b}' for i, b in enumerate(original_data['fitkind_bullets']))}

Cmindset Bullets:
{chr(10).join(f'{i+1}. {b}' for i, b in enumerate(original_data['cmindset_bullets']))}

Skills: Languages: {original_data['skills_languages']} | Backend: {original_data['skills_backend']} | DevOps: {original_data['skills_devops']}

EXAMPLES:

Bad (vague, 98 chars): "Built REST APIs using Python Flask and PostgreSQL for authentication and payments"

Good (technical, 207 chars): "Built RESTful APIs using Node.js and Prisma ORM for trainer-user matching, session scheduling, real-time chat via WebSockets, progress tracking, and PostgreSQL database schema design with indexing optimization."

Bad (fake metrics, 187 chars): "Engineered scalable microservices on AWS, improving performance by 45% and reducing costs by 30% while enhancing user experience across the platform."

Good (factual, 198 chars): "Deployed containerized microservices on AWS using Docker, Elastic Beanstalk for auto-scaling, S3 for media storage, CloudFront CDN, RDS for database hosting, and CI/CD pipelines via GitHub Actions."

Return JSON:
{{
  "summary": "<250-280 char(incl spaces) summary which might sound good for job but not direct copy-paste of company JD>",
  "fitkind_bullets": ["<198-207 chars>", "<198-207 chars>", "<198-207 chars>"],
  "cmindset_bullets": ["<198-207 chars>", "<198-207 chars>", "<198-207 chars>"],
  "skills_languages": "<max 80 chars - comma separated. Must fit on ONE line>",
  "skills_backend": "<comma separated with keywords - no limit>",
  "skills_devops": "<max 180 chars - comma separated. Must fit on TWO lines>"
}}

SKILL LENGTH CONSTRAINTS (CRITICAL - One Page Resume):
- skills_languages: MAX 80 characters (includes spaces) - Must fit on single line (e.g., Python, SQL, JavaScript, TypeScript, Java, C++)
- skills_backend: MAX 300 char (includes spaces)
- skills_devops: MAX 180 characters (includes spaces) - Must fit on TWO lines maximum. PRIORITIZE: Docker, Kubernetes, CI/CD, Git, AWS, GCP, monitoring tools

CHECK: Every bullet must be 190-210 characters. Pack with technical details!
SKILL SECTIONS MUST RESPECT CHARACTER LIMITS TO MAINTAIN ONE-PAGE FORMAT!
"""