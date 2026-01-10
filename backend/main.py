from fastapi import FastAPI, Form
import os, json
from utils import sanitize_latex, render_latex
import openai  # replace with your Gemini client if different

app = FastAPI()

TEMPLATE_PATH = "backend/templates/resume.tex.jinja"
OUTPUT_DIR = "backend/output"
COVER_LETTER_TEMPLATE = "backend/templates/cl.tex"

# --- Gemini helper ---
def gemini_generate(prompt: str) -> dict:
    """Call Gemini to get JSON output for resume"""
    response = openai.chat.completions.create(
        model="gemini-1",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    out = response.choices[0].message.content
    return json.loads(out)  # expects {"summary":"...", "skills":"...", "bullets":["...",...]} 

@app.post("/generate")
def generate_resume(job_title: str = Form(...), job_description: str = Form(...)):

    # --- prompt Gemini ---
    prompt = f"""
Update my resume for this job description:
{job_description}

Output JSON with keys:
- "summary": 1 short paragraph (max 50 words):Similar to this: ""
- "skills": comma separated skills line
- "bullets": 3-5 resume bullet points for experience sections

Use only plain text, no LaTeX special characters (# _ % & {{}} \), commas and slashes are allowed.
"""
    gemini_output = gemini_generate(prompt)

    # --- sanitize ---
    summary = sanitize_latex(gemini_output["summary"])
    skills = sanitize_latex(gemini_output["skills"])
    bullets = [sanitize_latex(b) for b in gemini_output["bullets"]]

    # --- context for Jinja ---
    context = {
        "summary": summary,
        "skillslanguages": skills,
        "skillsbackend": skills,
        "skillsdevops": skills,
        "fitkind_bullets": bullets,
        "cmindset_bullets": bullets
    }

    # --- create job folder ---
    folder_name = job_title.replace(" ", "_")
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    # --- render resume PDF ---
    resume_pdf = render_latex(TEMPLATE_PATH, context, folder_path, "resume_Singh")

    # --- render cover letter PDF ---
    cl_pdf = render_latex(COVER_LETTER_TEMPLATE, context, folder_path, "cl_Singh")

    return {
        "folder": folder_path,
        "resume_pdf": os.path.basename(resume_pdf),
        "cover_letter_pdf": os.path.basename(cl_pdf)
    }
