def build_prompt(jd, current):
    return f"""
You are tailoring an existing resume.

STRICT RULES:
- Do not invent experience
- Do not add new technologies
- Only rephrase and emphasize alignment
- Keep length within plus minus five to six words
- Maintain original meaning
- Output valid JSON only

Job Description:
{jd}

Current Content:
{current}

Return JSON exactly matching:
summary
fitkind_bullets (3)
cmindset_bullets (3)
skills_languages
skills_backend
skills_devops
"""