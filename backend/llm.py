import os
import json
from google.generativeai import GenerativeModel, configure
from utils import sanitize_latex
from prompt import build_prompt

configure(api_key=os.getenv("GEMINI_API_KEY"))

model = GenerativeModel("gemini-1.5-pro")

def tweak_resume_sections(original_data: dict, job_description: str):
    """
    original_data = {
        "summary": "...",
        "skills_languages": "...",
        "skills_backend": "...",
        "skills_devops": "...",
        "fitkind_bullets": [...],
        "cmindset_bullets": [...]
    }
    """

    prompt = build_prompt(original_data, job_description)

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    try:
        data = json.loads(raw_text)
    except Exception:
        raise ValueError("Gemini did not return valid JSON:\n" + raw_text)

    # Sanitize for LaTeX
    data["summary"] = sanitize_latex(data["summary"])
    data["skills_languages"] = sanitize_latex(data["skills_languages"])
    data["skills_backend"] = sanitize_latex(data["skills_backend"])
    data["skills_devops"] = sanitize_latex(data["skills_devops"])

    data["fitkind_bullets"] = [sanitize_latex(b) for b in data["fitkind_bullets"]]
    data["cmindset_bullets"] = [sanitize_latex(b) for b in data["cmindset_bullets"]]

    return data
