import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

if not os.getenv("GEMINI_API_KEY"):
    print("WARNING: GEMINI_API_KEY not found in environment!")
    print(f"Looking for .env at: {env_path}")

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
from llm import tweak_resume_sections, generate_cover_letter_content
from utils import render_latex_template
import tempfile
import zipfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "latex")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

ORIGINAL_DATA = {
    "summary": "Full stack engineer with experience building production web and mobile applications, integrating cloud architectures, APIs, and databases. Skilled in React Native Expo, Node.js, Python, and distributed systems. Experienced in designing scalable features, optimizing performance, delivering reliable products, and thriving in fast-paced collaborative environments.",
    "skills_languages": "Python, SQL, JavaScript, TypeScript, Java, C++, C#, Go",
    "skills_backend": "Python (Flask, Django, FastAPI), .NET Core, Angular, RESTful APIs, SOA/Microservices, OAuth 2.0/JWT, PostgreSQL, MySQL, Redis, MongoDB, Message Queues (RabbitMQ, Kafka), WebSockets, Stripe/Payment APIs, unit testing (pytest, unittest)",
    "skills_devops": "Docker, Kubernetes, CI/CD (GitHub Actions, Jenkins), Git, AWS (EC2, S3, RDS, Lambda, Elastic Beanstalk), GCP (Cloud Run, Cloud SQL), monitoring (Prometheus, Grafana, ELK), performance optimization",
    "fitkind_bullets": [
        "Developed a full-stack fitness platform using Node.js and Prisma ORM with React Native (Expo/EAS), collaborating with clients to deliver a scalable trainer-user marketplace",
        "Architected microservices on Azure (App Service, Blob Storage, SQL Database) with CI/CD, implementing secure authentication (OAuth+JWT), scalable APIs (Health, Stripe Payments), and seamless communication features to enable interactive fitness communities and progress monitoring.",
        "Collaborated in fast-paced, cross-functional environment to ensure scalability, reliability, and timely delivery"
    ],
    "cmindset_bullets": [
        "Architected a RAG system on AWS using Pinecone and OpenSearch, defining requirements and managing project plans for an AI career platform across 100+ data sources.",
        "Built Python FastAPI microservices with Docker and Kubernetes, integrating REST endpoints with error handling and managing MLOps pipelines for automated deployment.",
        "Developed generative services via LangChain and OpenAI API, collaborating with stakeholders to deliver products and perform Ragas evaluation in agile environments."
    ]
}

@app.post("/generate")
async def generate_resume(
    job_title: str = Form(...), 
    job_description: str = Form(...),
    type: str = Form("both")  # "resume", "cover_letter", or "both"
):
    try:
        print(f"Received request for job: {job_title}")
        print(f"Job description length: {len(job_description)} characters")
        print(f"Generation type: {type}")
        
        folder_name = job_title.replace(" ", "_").replace("/", "_")
        
        # Create temporary directory for generated files
        temp_dir = tempfile.mkdtemp()
        output_folder = os.path.join(temp_dir, folder_name)
        os.makedirs(output_folder, exist_ok=True)
        print(f"Created temporary folder: {output_folder}")
        
        files_to_zip = []
        
        if type in ["resume", "both"]:
            tweaked_data = tweak_resume_sections(ORIGINAL_DATA, job_description)
            print("Resume AI tailoring completed successfully")
            
            resume_context = {
                "summary": tweaked_data["summary"],
                "skillslanguages": tweaked_data["skills_languages"],
                "skillsbackend": tweaked_data["skills_backend"],
                "skillsdevops": tweaked_data["skills_devops"],
                "fitkind_bullets": tweaked_data["fitkind_bullets"],
                "cmindset_bullets": tweaked_data["cmindset_bullets"]
            }
            
            print("Rendering resume PDF...")
            resume_pdf = render_latex_template(
                os.path.join(TEMPLATE_DIR, "resume_template.tex"),
                resume_context,
                output_folder,
                "resume_Singh"
            )
            print(f"Resume PDF created: {resume_pdf}")
            files_to_zip.append(("resume_Singh.pdf", resume_pdf))
        
        if type in ["cover_letter", "both"]:
            company_name = job_title.split(" at ")[-1] if " at " in job_title else "your company"
            role_title = job_title.split(" at ")[0] if " at " in job_title else job_title
            
            cl_content = generate_cover_letter_content(ORIGINAL_DATA, job_description, role_title, company_name)
            print("Cover letter AI generation completed successfully")
            
            cover_letter_context = {
                "phone": "(623) 297 7664",
                "email": "shreyashsingh26@gmail.com",
                "portfolio_url": "www.shreyashsingh.com",
                "linkedin": "shreyazh",
                "company_name": company_name,
                "role_title": role_title,
                "opening_paragraph": cl_content["opening_paragraph"],
                "experience_paragraph_1": cl_content["experience_paragraph_1"],
                "experience_paragraph_2": cl_content["experience_paragraph_2"],
                "closing_paragraph": cl_content["closing_paragraph"]
            }
            
            print("Rendering cover letter PDF...")
            cover_letter_pdf = render_latex_template(
                os.path.join(TEMPLATE_DIR, "cover_letter_template.tex"),
                cover_letter_context,
                output_folder,
                "cl_Singh"
            )
            print(f"Cover letter PDF created: {cover_letter_pdf}")
            files_to_zip.append(("cl_Singh.pdf", cover_letter_pdf))
        
        # Create ZIP file in temporary directory
        zip_path = os.path.join(temp_dir, f"{folder_name}.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for filename, file_path in files_to_zip:
                # Add files within the folder structure in the ZIP
                zipf.write(file_path, os.path.join(folder_name, filename))
        print(f"ZIP file created: {zip_path}")
        
        return FileResponse(
            path=zip_path,
            filename=f"{folder_name}.zip",
            media_type="application/zip",
            background=lambda: shutil.rmtree(temp_dir)  # Cleanup temp directory after response
        )
        
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"ERROR: {str(e)}")
        print(f"Full traceback:\n{error_detail}")
        raise HTTPException(status_code=500, detail=str(e))
