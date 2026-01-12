import os
import json
import re
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

from google import generativeai as genai
from utils import sanitize_latex
from prompt import build_prompt

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash-exp")

def tweak_resume_sections(original_data: dict, job_description: str):
    prompt = build_prompt(original_data, job_description)
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            response_mime_type="application/json"
        )
    )
    
    raw_text = response.text.strip()
    raw_text = re.sub(r'^```json\s*', '', raw_text)
    raw_text = re.sub(r'\s*```$', '', raw_text)
    
    try:
        data = json.loads(raw_text)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON from Gemini response: {str(e)}\nRaw response: {raw_text}")
    
    data["summary"] = sanitize_latex(data["summary"])
    data["skills_languages"] = sanitize_latex(data["skills_languages"])
    data["skills_backend"] = sanitize_latex(data["skills_backend"])
    data["skills_devops"] = sanitize_latex(data["skills_devops"])
    data["fitkind_bullets"] = [sanitize_latex(b) for b in data["fitkind_bullets"]]
    data["cmindset_bullets"] = [sanitize_latex(b) for b in data["cmindset_bullets"]]
    
    return data

def generate_cover_letter_content(original_data: dict, job_description: str, job_title: str, company_name: str):
    prompt = f"""
You are a professional cover letter writer. Create a compelling, personalized cover letter for this job.

**CANDIDATE EDUCATION: Bachelor of Science in Computer Science, Arizona State University (GPA: 4.0/4.0), graduated May 2025. Do NOT mention or imply any graduate degrees (Master's/PhD).**

STRICT RULES:
1. Write 3-4 substantial paragraphs (not the generic template)
2. Reference SPECIFIC experiences from the resume that match the job requirements
3. Show genuine enthusiasm and understanding of the role
4. Use concrete examples and achievements
5. Make it personal and engaging, not robotic
6. Output ONLY valid JSON with no markdown formatting
7. Do not use special LaTeX characters: # $ % & _ {{{{ }}}} \\ ^ ~


Job Title: {job_title}
Company: {company_name}

Job Description:
{job_description}

Resume Summary: {original_data['summary']}

Key Experiences:
- FitKind: {original_data['fitkind_bullets'][0]}
- Cmindset: {original_data['cmindset_bullets'][0]}

Skills: {original_data['skills_languages']}, {original_data['skills_backend'][:100]}...

Return JSON with these EXACT keys:
{{
  "opening_paragraph": "<strong opening that shows you understand the role and company>",
  "experience_paragraph_1": "<paragraph highlighting relevant experience with specific examples>",
  "experience_paragraph_2": "<paragraph about additional relevant skills and achievements>",
  "closing_paragraph": "<compelling closing that reiterates interest and calls to action>"
}}
"""
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.8,
            response_mime_type="application/json"
        )
    )
    
    raw_text = response.text.strip()
    raw_text = re.sub(r'^```json\s*', '', raw_text)
    raw_text = re.sub(r'\s*```$', '', raw_text)
    
    try:
        data = json.loads(raw_text)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON: {str(e)}\nRaw: {raw_text}")
    
    for key in data:
        data[key] = sanitize_latex(data[key])
    
    return data
