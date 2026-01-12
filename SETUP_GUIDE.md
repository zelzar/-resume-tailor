# Resume Tailor - Setup and Usage Guide

## Quick Start

### 1. Set up your Gemini API Key

Edit `backend/.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

Get your API key from: https://makersuite.google.com/app/apikey

### 2. Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 3. Run the Application

#### Easy way (uses start.sh):
```bash
./start.sh
```

#### Manual way:
```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 4. Use the App

1. Open http://localhost:5173
2. Enter job title (e.g., "Software Engineer at Google")
3. Paste the job description
4. Click "Generate Resume & Cover Letter"
5. Download the ZIP file with both PDFs

## How It Works

### The Flow:
```
User Input → Frontend → FastAPI → Gemini AI → LaTeX → PDFs → ZIP Download
```

### What Gemini Does:
- Takes your ORIGINAL resume content (in `main.py`)
- Analyzes the job description
- Rephrases bullets to match job keywords
- Emphasizes relevant skills
- **NEVER invents experience** - only rewrites existing content

### Original Data Location:
All your original resume content is in `backend/main.py` in the `ORIGINAL_DATA` dictionary:
- `summary`: Your professional summary
- `skills_languages`: Programming languages
- `skills_backend`: Backend technologies
- `skills_devops`: DevOps/Cloud skills
- `fitkind_bullets`: 3 bullets for FitKind job
- `cmindset_bullets`: 3 bullets for Cmindset job

### LaTeX Templates:
- `backend/latex/resume_template.tex` - Main resume layout
- `backend/latex/cover_letter_template.tex` - Cover letter layout

These use `{{ placeholders }}` that get replaced with AI-tailored content.

## Customization

### Change Your Info:
1. Edit `ORIGINAL_DATA` in `backend/main.py`
2. Update personal info in cover letter template

### Change Styling:
1. Frontend colors: `frontend/src/App.css` (search for gradient colors)
2. LaTeX formatting: Edit the `.tex` files

### Change AI Behavior:
Edit `backend/prompt.py` to modify how Gemini tailors content.

## File Structure Explained

```
backend/
├── main.py           # FastAPI server, ORIGINAL_DATA, API endpoints
├── llm.py            # Gemini AI integration
├── prompt.py         # AI prompt engineering
├── utils.py          # LaTeX rendering utilities
├── latex/
│   ├── resume_template.tex       # Resume LaTeX template
│   └── cover_letter_template.tex # Cover letter template
└── output/           # Generated files go here

frontend/
├── src/
│   ├── App.jsx      # React UI component
│   ├── App.css      # Glassmorphism styles
│   └── index.css    # Base dark theme
```

## Troubleshooting

### "LaTeX not found"
Install LaTeX:
- macOS: `brew install --cask mactex`
- Ubuntu: `sudo apt-get install texlive-full`

### "Gemini API error"
- Check your API key in `.env`
- Verify it's valid at Google AI Studio

### "Port already in use"
Change ports:
- Backend: `uvicorn main:app --reload --port 8001`
- Frontend: `npm run dev -- --port 5174`

### "Resume looks wrong"
- Check `backend/output/` folder for generated .tex files
- Review for any LaTeX compilation errors
- Ensure placeholders `{{ bullet }}` match count in template

## Tips

1. **Be specific with job titles**: Use format "Role at Company" for better results
2. **Paste full job description**: More detail = better tailoring
3. **Review before sending**: Always review the generated PDFs
4. **Keep original data updated**: Update `ORIGINAL_DATA` as you gain experience

## Features

✅ Professional glassmorphism UI with dark theme  
✅ Real-time AI tailoring with Gemini 1.5 Pro  
✅ LaTeX PDF generation  
✅ ZIP download with both resume and cover letter  
✅ Privacy-focused (no data storage)  
✅ Mobile-responsive design  
✅ Loading states and error handling  

Enjoy your tailored resumes! 🚀
