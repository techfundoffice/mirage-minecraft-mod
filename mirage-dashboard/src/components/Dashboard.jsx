import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  Upload, 
  Video, 
  Play, 
  Download, 
  RefreshCw, 
  CheckCircle, 
  XCircle, 
  Clock,
  Sparkles,
  TrendingUp
} from 'lucide-react'
import axios from 'axios'
import './Dashboard.css'

// Use environment variable or detect sandbox environment
const API_URL = import.meta.env.VITE_API_URL || 
  (window.location.hostname.includes('sandbox') 
    ? `${window.location.protocol}//${window.location.hostname.replace('5173', '5000')}/api`
    : 'http://localhost:5000/api')

function Dashboard() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [videoUrl, setVideoUrl] = useState('')
  const [selectedStyle, setSelectedStyle] = useState('minecraft')
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isDownloadingFromUrl, setIsDownloadingFromUrl] = useState(false)
  const queryClient = useQueryClient()

  // Check URL parameters on mount
  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search)
    const urlParam = urlParams.get('url')
    const styleParam = urlParams.get('style')
    
    if (urlParam) {
      setVideoUrl(decodeURIComponent(urlParam))
    }
    if (styleParam && ['minecraft', 'anime', 'cyberpunk', 'default'].includes(styleParam)) {
      setSelectedStyle(styleParam)
    }
  }, [])

  // Fetch available styles
  const { data: styles = [] } = useQuery({
    queryKey: ['styles'],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/styles`)
      return response.data
    }
  })

  // Fetch jobs
  const { data: jobs = [], refetch: refetchJobs } = useQuery({
    queryKey: ['jobs'],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/jobs`)
      return response.data
    },
    refetchInterval: 2000 // Poll every 2 seconds
  })

  // Fetch stats
  const { data: stats } = useQuery({
    queryKey: ['stats'],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/stats`)
      return response.data
    },
    refetchInterval: 5000
  })

  // Upload mutation
  const uploadMutation = useMutation({
    mutationFn: async (file) => {
      const formData = new FormData()
      formData.append('video', file)
      
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setUploadProgress(progress)
        }
      })
      return response.data
    },
    onSuccess: (data) => {
      // Automatically create job after upload
      createJobMutation.mutate({
        input_file: data.filename,
        style: selectedStyle
      })
    }
  })

  // Create job mutation
  const createJobMutation = useMutation({
    mutationFn: async (jobData) => {
      const response = await axios.post(`${API_URL}/jobs`, jobData)
      return response.data
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['jobs'])
      setSelectedFile(null)
      setUploadProgress(0)
    }
  })

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
    }
  }

  const handleUpload = () => {
    if (selectedFile) {
      uploadMutation.mutate(selectedFile)
    }
  }

  const handleUrlDownload = async () => {
    if (!videoUrl) {
      alert('Please enter a video URL')
      return
    }

    setIsDownloadingFromUrl(true)
    try {
      // Download video from URL
      const response = await axios.get(videoUrl, {
        responseType: 'blob',
        onDownloadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          setUploadProgress(progress)
        }
      })

      // Create a file from the blob
      const filename = videoUrl.split('/').pop().split('?')[0] || 'video.mp4'
      const file = new File([response.data], filename, { type: 'video/mp4' })

      // Upload the file
      uploadMutation.mutate(file)
      setVideoUrl('')
    } catch (error) {
      console.error('Failed to download from URL:', error)
      alert('Failed to download video from URL. Please check the URL and try again.')
      setUploadProgress(0)
    } finally {
      setIsDownloadingFromUrl(false)
    }
  }

  const handleDownload = async (jobId) => {
    try {
      // Fetch the video file
      const response = await axios.get(`${API_URL}/jobs/${jobId}/download`, {
        responseType: 'blob'
      })
      
      // Create a blob URL
      const blob = new Blob([response.data], { type: 'video/mp4' })
      const url = window.URL.createObjectURL(blob)
      
      // Create a temporary link and trigger download
      const link = document.createElement('a')
      link.href = url
      
      // Get filename from Content-Disposition header or use default
      const contentDisposition = response.headers['content-disposition']
      let filename = `mirage_video_${jobId}.mp4`
      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename=(.+)/)
        if (filenameMatch) {
          filename = filenameMatch[1].replace(/['"]/g, '')
        }
      }
      
      link.download = filename
      document.body.appendChild(link)
      link.click()
      
      // Cleanup
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
    } catch (error) {
      console.error('Download failed:', error)
      alert('Failed to download video. Please try again.')
    }
  }

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="status-icon success" />
      case 'failed':
        return <XCircle className="status-icon error" />
      case 'processing':
        return <RefreshCw className="status-icon processing spin" />
      default:
        return <Clock className="status-icon pending" />
    }
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return 'success'
      case 'failed':
        return 'error'
      case 'processing':
        return 'processing'
      default:
        return 'pending'
    }
  }

  return (
    <div className="dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="logo">
            <Sparkles size={32} />
            <h1>Mirage Workflow Dashboard</h1>
          </div>
          <p className="subtitle">Transform videos with AI-powered style transfer</p>
        </div>
      </header>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">
            <Video size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.total_jobs || 0}</div>
            <div className="stat-label">Total Jobs</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon success">
            <CheckCircle size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.completed || 0}</div>
            <div className="stat-label">Completed</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon processing">
            <RefreshCw size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.processing || 0}</div>
            <div className="stat-label">Processing</div>
          </div>
        </div>
        
        <div className="stat-card">
          <div className="stat-icon error">
            <XCircle size={24} />
          </div>
          <div className="stat-content">
            <div className="stat-value">{stats?.failed || 0}</div>
            <div className="stat-label">Failed</div>
          </div>
        </div>
      </div>

      {/* Upload Section */}
      <div className="upload-section">
        <h2>Create New Transformation</h2>
        
        {/* Style Selection */}
        <div className="style-selector">
          <h3>Select Style</h3>
          <div className="styles-grid">
            {styles.map((style) => (
              <div
                key={style.id}
                className={`style-card ${selectedStyle === style.id ? 'selected' : ''}`}
                onClick={() => setSelectedStyle(style.id)}
              >
                <div className="style-preview">
                  <Sparkles size={32} />
                </div>
                <h4>{style.name}</h4>
                <p>{style.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* File Upload */}
        <div className="upload-controls">
          <div className="file-input-wrapper">
            <input
              type="file"
              id="video-upload"
              accept="video/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
            <label htmlFor="video-upload" className="file-input-label">
              <Upload size={20} />
              {selectedFile ? selectedFile.name : 'Choose Video File'}
            </label>
          </div>

          <button
            className="upload-button"
            onClick={handleUpload}
            disabled={!selectedFile || uploadMutation.isPending}
          >
            {uploadMutation.isPending ? (
              <>
                <RefreshCw size={20} className="spin" />
                Uploading... {uploadProgress}%
              </>
            ) : (
              <>
                <Play size={20} />
                Start Transformation
              </>
            )}
          </button>
        </div>

        {/* URL Input */}
        <div className="url-input-section">
          <h3>Or Load from URL</h3>
          <div className="url-controls">
            <input
              type="text"
              className="url-input"
              placeholder="Enter video URL (e.g., https://example.com/video.mp4)"
              value={videoUrl}
              onChange={(e) => setVideoUrl(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleUrlDownload()}
            />
            <button
              className="upload-button"
              onClick={handleUrlDownload}
              disabled={!videoUrl || isDownloadingFromUrl || uploadMutation.isPending}
            >
              {isDownloadingFromUrl ? (
                <>
                  <RefreshCw size={20} className="spin" />
                  Downloading... {uploadProgress}%
                </>
              ) : (
                <>
                  <Download size={20} />
                  Load from URL
                </>
              )}
            </button>
          </div>
          <p className="url-hint">
            💡 Tip: You can prepopulate the URL by adding ?url=VIDEO_URL&style=STYLE to the page URL
          </p>
        </div>

        {uploadMutation.isError && (
          <div className="error-message">
            Error: {uploadMutation.error.message}
          </div>
        )}
      </div>

      {/* Jobs List */}
      <div className="jobs-section">
        <div className="section-header">
          <h2>Transformation Jobs</h2>
          <button className="refresh-button" onClick={() => refetchJobs()}>
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>

        {jobs.length === 0 ? (
          <div className="empty-state">
            <Video size={48} />
            <p>No jobs yet. Upload a video to get started!</p>
          </div>
        ) : (
          <div className="jobs-grid">
            {jobs.map((job) => (
              <div key={job.id} className="job-card">
                <div className="job-header">
                  <div className="job-info">
                    {getStatusIcon(job.status)}
                    <div>
                      <h4>{job.input_file}</h4>
                      <p className="job-style">{job.style} style</p>
                    </div>
                  </div>
                  <span className={`job-status ${getStatusColor(job.status)}`}>
                    {job.status}
                  </span>
                </div>

                {job.status === 'processing' && (
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${job.progress}%` }}
                    />
                  </div>
                )}

                <div className="job-meta">
                  <span>Created: {new Date(job.created_at).toLocaleString()}</span>
                  {job.completed_at && (
                    <span>Completed: {new Date(job.completed_at).toLocaleString()}</span>
                  )}
                </div>

                {job.error && (
                  <div className="job-error">
                    Error: {job.error}
                  </div>
                )}

                {job.status === 'completed' && (
                  <button 
                    className="download-button"
                    onClick={() => handleDownload(job.id)}
                  >
                    <Download size={16} />
                    Download Result
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
