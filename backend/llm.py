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
    # Determine which experiences are most relevant to the job
    jd_lower = job_description.lower()
    
    # Analyze which projects are relevant
    fitkind_relevant = any(keyword in jd_lower for keyword in ['mobile', 'react native', 'nodejs', 'node.js', 'full-stack', 'fullstack', 'marketplace', 'fitness', 'wellness', 'health'])
    cmindset_relevant = any(keyword in jd_lower for keyword in ['ai', 'rag', 'aws', 'cloud', 'backend', 'microservices', 'python', 'fastapi', 'kubernetes', 'docker', 'llm', 'ml', 'machine learning'])
    
    # Build relevant experiences section
    relevant_experiences = []
    if fitkind_relevant:
        relevant_experiences.append(f"FitKind Project: {original_data['fitkind_bullets'][0]}")
    if cmindset_relevant:
        relevant_experiences.append(f"Cmindset Project: {original_data['cmindset_bullets'][0]}")
    
    # If no specific match, include both but prioritize based on job type
    if not relevant_experiences:
        if any(keyword in jd_lower for keyword in ['backend', 'python', 'java', 'devops', 'cloud']):
            relevant_experiences.append(f"Cmindset Project: {original_data['cmindset_bullets'][0]}")
            relevant_experiences.append(f"FitKind Project: {original_data['fitkind_bullets'][0]}")
        else:
            relevant_experiences.append(f"FitKind Project: {original_data['fitkind_bullets'][0]}")
            relevant_experiences.append(f"Cmindset Project: {original_data['cmindset_bullets'][0]}")
    
    experiences_text = "\n".join(relevant_experiences)
    
    # Filter skills based on job relevance
    relevant_skills = []
    base_skills = original_data['skills_languages']
    
    if any(keyword in jd_lower for keyword in ['frontend', 'react', 'javascript', 'typescript', 'ui', 'ux', 'mobile', 'ios', 'android']):
        relevant_skills.append(original_data['skills_languages'])
    if any(keyword in jd_lower for keyword in ['backend', 'api', 'database', 'sql', 'mongodb', 'python', 'java']):
        relevant_skills.append(original_data['skills_backend'][:150])
    if any(keyword in jd_lower for keyword in ['devops', 'docker', 'kubernetes', 'aws', 'gcp', 'azure', 'ci/cd']):
        relevant_skills.append(original_data['skills_devops'][:150])
    
    if not relevant_skills:
        relevant_skills = [original_data['skills_languages'], original_data['skills_backend'][:100]]
    
    skills_text = ", ".join(relevant_skills)
    
    prompt = f"""
You are writing a FINAL, PRODUCTION-READY cover letter that will be submitted immediately. This is NOT a template.

**CANDIDATE EDUCATION: Bachelor of Science in Computer Science, Arizona State University (GPA: 4.0/4.0), graduated May 2025.**

ABSOLUTE REQUIREMENTS:
1. THIS IS A FINAL COVER LETTER, NOT A TEMPLATE. Generate complete, specific content for every sentence.
2. DO NOT GENERATE ANY PLACEHOLDER TEXT. No [brackets], no "mention something", no "your research", NOTHING.
3. Use the job description to research and understand what the company values and does.
4. Infer company details from the job description (technology stack, company focus, values).
5. Generate a cover letter that could be sent immediately without any edits.
6. Every sentence must be original and specific to THIS job and company.
7. Use the contact information provided - do not ask for it.
8. Output ONLY valid JSON. No markdown, no code blocks, no explanations.
9. Do not use special LaTeX characters: # $ % & _ {{{{ }}}} \\ ^ ~

Job Title: {job_title}
Company: {company_name}

Job Description:
{job_description}

Your Resume Summary: {original_data['summary']}

Your Relevant Experience:
{experiences_text}

Your Relevant Skills: {skills_text}

Your Contact Info (use in closing):
Phone: (623) 297-7664
Email: shreyashsingh26@gmail.com
Portfolio: www.shreyashsingh.com

GENERATE A FINAL, COMPLETE COVER LETTER. Fill in ALL details based on the job description. Make it specific to {company_name} and the {job_title} role. Do not write anything that starts with "mention", "research", "based on", or any other instruction-like text.

Return ONLY this JSON - every field will be a paragraph of a final, submittable cover letter:
{{
  "opening_paragraph": "First paragraph with specific enthusiasm about {company_name} and the {job_title} role based on what you learned from the job description",
  "experience_paragraph_1": "Second paragraph describing your relevant experience with specific examples that match this job",
  "experience_paragraph_2": "Third paragraph discussing your skills and how they solve problems mentioned in the job description",
  "closing_paragraph": "Final paragraph with your availability, gratitude, and contact information: (623) 297-7664, shreyashsingh26@gmail.com"
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
