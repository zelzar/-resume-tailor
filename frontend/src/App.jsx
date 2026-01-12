import { useState } from 'react'
import { FiFileText, FiMail, FiBriefcase, FiDownload } from 'react-icons/fi'
import './App.css'

function App() {
  const [jobTitle, setJobTitle] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [loadingType, setLoadingType] = useState('')

  const handleGenerate = async (type) => {
    if (!jobTitle.trim() || !jobDescription.trim()) {
      setError('Please fill in all fields')
      return
    }

    setIsLoading(true)
    setLoadingType(type)
    setError('')

    try {
      const formData = new FormData()
      formData.append('job_title', jobTitle)
      formData.append('job_description', jobDescription)
      formData.append('type', type)

      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error('Failed to generate documents')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `${jobTitle.replace(/\s+/g, '_')}_${type}.zip`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setIsLoading(false)
      setLoadingType('')
    }
  }

  return (
    <div className="app">
      <div className="background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      <div className="container">
        <div className="glass-card">
          <div className="header">
            <h1 className="title">Resume Tailor</h1>
          </div>

          <div className="form">
            <div className="input-group">
              <label htmlFor="job-title">Job Title / Role</label>
              <input
                id="job-title"
                type="text"
                placeholder="e.g., Software Engineer at Google"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                disabled={isLoading}
              />
            </div>

            <div className="input-group">
              <label htmlFor="job-description">Job Description</label>
              <textarea
                id="job-description"
                placeholder="Paste the full job description here..."
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                disabled={isLoading}
                rows={12}
              />
            </div>

            {error && <div className="error-message">{error}</div>}

            <div className="button-group">
              <button
                className="generate-btn btn-resume"
                onClick={() => handleGenerate('resume')}
                disabled={isLoading}
              >
                {isLoading && loadingType === 'resume' ? (
                  <>
                    <span className="spinner"></span>
                    Generating...
                  </>
                ) : (
                  <>
                    <FiFileText />
                    Resume
                    <FiDownload />
                  </>
                )}
              </button>

              <button
                className="generate-btn btn-cover-letter"
                onClick={() => handleGenerate('cover_letter')}
                disabled={isLoading}
              >
                {isLoading && loadingType === 'cover_letter' ? (
                  <>
                    <span className="spinner"></span>
                    Generating...
                  </>
                ) : (
                  <>
                    <FiMail />
                    CoverLetter
                    <FiDownload />
                  </>
                )}
              </button>

              <button
                className="generate-btn btn-both"
                onClick={() => handleGenerate('both')}
                disabled={isLoading}
              >
                {isLoading && loadingType === 'both' ? (
                  <>
                    <span className="spinner"></span>
                    Generating...
                  </>
                ) : (
                  <>
                    <FiBriefcase />
                    Both
                    <FiDownload />
                  </>
                )}
              </button>
            </div>

            <p className="info-text">
              Your tailored documents will be downloaded as a ZIP file.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
