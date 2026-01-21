import { useState, useEffect } from 'react'
import { FiFileText, FiMail, FiBriefcase, FiDownload, FiGithub, FiLinkedin, FiGlobe } from 'react-icons/fi'
import { BsLayoutSidebarInset } from 'react-icons/bs'
import { HiOutlineAtSymbol } from 'react-icons/hi'
import './App.css'

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [jobTitle, setJobTitle] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [loadingType, setLoadingType] = useState('')
  const [todayApplications, setTodayApplications] = useState([])
  const [copiedItem, setCopiedItem] = useState('')

  const contactInfo = {
    linkedin: 'https://linkedin.com/in/yourprofile',
    github: 'https://github.com/yourusername',
    website: 'https://yourwebsite.com',
    email: 'your.email@example.com'
  }

  useEffect(() => {
    loadTodayApplications()
  }, [])

  const getTodayKey = () => {
    const today = new Date().toDateString()
    return `resume-tailor-apps-${today}`
  }

  const loadTodayApplications = () => {
    const saved = localStorage.getItem(getTodayKey())
    if (saved) {
      setTodayApplications(JSON.parse(saved))
    }
  }

  const addApplicationToToday = (title, type) => {
    const newApp = {
      id: Date.now(),
      title,
      type,
      timestamp: new Date().toLocaleTimeString()
    }
    const updated = [newApp, ...todayApplications]
    setTodayApplications(updated)
    localStorage.setItem(getTodayKey(), JSON.stringify(updated))
  }

  const copyToClipboard = async (text, type) => {
    try {
      await navigator.clipboard.writeText(text)
      setCopiedItem(type)
      setTimeout(() => setCopiedItem(''), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

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

      addApplicationToToday(jobTitle, type)
      setJobTitle('')
      setJobDescription('')
    } catch (err) {
      setError(err.message || 'Something went wrong')
    } finally {
      setIsLoading(false)
      setLoadingType('')
    }
  }

  return (
    <div className={`app ${sidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      <div className="background">
        <div className="gradient-orb orb-1"></div>
        <div className="gradient-orb orb-2"></div>
        <div className="gradient-orb orb-3"></div>
      </div>

      <button 
        className={`sidebar-toggle sidebar-toggle-outside ${sidebarOpen ? 'hidden' : ''}`}
        onClick={() => setSidebarOpen(!sidebarOpen)}
        title="Toggle sidebar"
      >
        <BsLayoutSidebarInset />
      </button>

      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <h2>Today's Apps</h2>
          <div className="sidebar-header-right">
            <button 
              className="sidebar-toggle sidebar-toggle-inside" 
              onClick={() => setSidebarOpen(!sidebarOpen)}
              title="Close sidebar"
            >
              <BsLayoutSidebarInset />
            </button>
          </div>
        </div>

        {/* Contact Clipboard Section */}
        <div className="contact-clipboard">
          <h3>Quick Copy</h3>
          <div className="contact-icons">
            <button 
              className="contact-icon"
              onClick={() => copyToClipboard(contactInfo.linkedin, 'linkedin')}
              title="Copy LinkedIn URL"
            >
              <FiLinkedin />
              {copiedItem === 'linkedin' && <span className="copied-tooltip">Copied!</span>}
            </button>
            <button 
              className="contact-icon"
              onClick={() => copyToClipboard(contactInfo.github, 'github')}
              title="Copy GitHub URL"
            >
              <FiGithub />
              {copiedItem === 'github' && <span className="copied-tooltip">Copied!</span>}
            </button>
            <button 
              className="contact-icon"
              onClick={() => copyToClipboard(contactInfo.website, 'website')}
              title="Copy Website URL"
            >
              <FiGlobe />
              {copiedItem === 'website' && <span className="copied-tooltip">Copied!</span>}
            </button>
            <button 
              className="contact-icon"
              onClick={() => copyToClipboard(contactInfo.email, 'email')}
              title="Copy Email"
            >
              <HiOutlineAtSymbol />
              {copiedItem === 'email' && <span className="copied-tooltip">Copied!</span>}
            </button>
          </div>
        </div>

        <div className="sidebar-content">
          {todayApplications.length === 0 ? (
            <p className="empty-state">No applications yet. Start by generating your first tailored documents!</p>
          ) : (
            <ul className="apps-list">
              {todayApplications.map((app) => (
                <li key={app.id} className="app-item">
                  <div className="app-title">{app.title}</div>
                  <div className="app-meta">
                    <span className="app-type">{app.type.replace('_', ' ')}</span>
                    <span className="app-time">{app.timestamp}</span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="sidebar-footer">
          <div className="app-count">{todayApplications.length} application{todayApplications.length !== 1 ? 's' : ''} today</div>
        </div>
      </aside>

      <div className={`app-wrapper ${sidebarOpen ? 'sidebar-open' : ''}`}>
        <div className="glass-card">
          <div className="header">
            <h1 className="title">Resume Tailor</h1>
            <p className="subtitle">Generate customized resumes and cover letters</p>
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
                    Cover Letter
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