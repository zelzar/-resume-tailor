# Resume Tailor 

AI-powered tool that tailors your resume and cover letter to any job description in seconds using Ninja and Latex 

## What It Does

- Enter a job title and paste the job description
- Click a button (Resume, Cover Letter, or Both)
- Download professionally formatted PDFs tailored to that specific job
- Uses AI to integrate keywords and emphasize relevant experience

## Quick Start

### 1. Install Prerequisites

**Python 3.8+**
```bash
python3 --version
```

**Node.js 16+**
```bash
node --version
```

**LaTeX** (for PDF generation)
- **macOS**: `brew install --cask mactex`
- **Ubuntu/Debian**: `sudo apt-get install texlive-full`
- **Windows**: Download from [miktex.org](https://miktex.org/)

### 2. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a free API key
3. Copy it for the next step

### 3. Configure API Key

Create a file `backend/.env` with your API key:
```bash
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Application

**Easy Way (Recommended):**
```bash
chmod +x start.sh
./start.sh
```

This script will:
- Install all Python dependencies
- Install all Node.js dependencies
- Start the backend server (port 8000)
- Start the frontend server (port 5173)

**Manual Way:**

*Terminal 1 - Backend:*
```bash
cd backend
pip3 install -r requirements.txt
PYTHONPATH=$(pwd) python3 -m uvicorn main:app --reload --port 8000
```

*Terminal 2 - Frontend:*
```bash
cd frontend
npm install
npm run dev
```

### 5. Use the App

1. Open **http://localhost:5173** in your browser
2. Enter the job title (e.g., "Software Engineer at Google")
3. Paste the full job description
4. Click one of three buttons:
   - **📄 Resume Only** - Just the tailored resume
   - **✉️ Cover Letter Only** - Just the tailored cover letter
   - **🎯 Both** - Resume + Cover Letter (recommended)
5. Download the ZIP file with your PDFs

## How to Customize Your Content

Your resume data is stored in `backend/main.py` in the `ORIGINAL_DATA` dictionary. Update it with your real information:

```python
ORIGINAL_DATA = {
    "summary": "Your professional summary...",
    "skills_languages": "Python, JavaScript, Java...",
    "skills_backend": "Django, FastAPI, Node.js...",
    "skills_devops": "Docker, AWS, Kubernetes...",
    "fitkind_bullets": [
        "Your first job bullet point...",
        "Your second job bullet point...",
        "Your third job bullet point..."
    ],
    "cmindset_bullets": [
        "Your other job bullet point...",
        # ... etc
    ]
}
```

The AI will rephrase this content to match each job description you apply to.

## Troubleshooting

### "LaTeX not found" error
Install LaTeX using the commands in step 1 above.

### "GEMINI_API_KEY not found" error
Make sure you created `backend/.env` with your API key (step 3).

### Port already in use
Kill existing processes:
```bash
lsof -ti:8000 | xargs kill  # Backend
lsof -ti:5173 | xargs kill  # Frontend
```

### PDFs don't look right
Check `backend/output/` folder for `.tex` files to see what LaTeX generated.

## What Gets Generated

- **resume_Singh.pdf** - Your tailored resume with job-specific keywords
- **cl_Singh.pdf** - A personalized cover letter referencing the job
- Both are formatted professionally using LaTeX templates

## Tech Stack

- **Frontend**: React + Vite (glassmorphism dark theme)
- **Backend**: FastAPI (Python)
- **AI**: Google Gemini 2.0 Flash
- **PDF Generation**: LaTeX

## License

MIT

---

Made by Shreyash Singh
