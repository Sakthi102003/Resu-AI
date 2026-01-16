import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  Plus,
  FileText,
  LogOut,
  User,
  Download,
  Trash2,
  Edit,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { useAuthStore } from '../Services/auth'
import { resumeAPI } from '../Services/api'

export default function Dashboard() {
  const navigate = useNavigate()
  const { user, logout } = useAuthStore()
  const [resumes, setResumes] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadResumes()
  }, [])

  const loadResumes = async () => {
    try {
      const response = await resumeAPI.getAll()
      setResumes(response.data)
    } catch (error) {
      toast.error('Failed to load resumes')
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreateResume = () => {
    navigate('/template-selection')
  }

  const handleDeleteResume = async (id) => {
    if (!confirm('Are you sure you want to delete this resume?')) return

    try {
      await resumeAPI.delete(id)
      toast.success('Resume deleted')
      loadResumes()
    } catch (error) {
      toast.error('Failed to delete resume')
    }
  }

  const handleExportPDF = async (id, title) => {
    try {
      const response = await resumeAPI.exportPDF(id, null)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${title}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('PDF downloaded!')
    } catch (error) {
      toast.error('Failed to export PDF')
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
    toast.success('Logged out successfully')
  }

  return (
    <div className="min-h-screen bg-transparent font-sans text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-40 bg-cyber-background/80 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity group"
            >
              <div className="w-10 h-10 bg-gradient-to-br from-cyber-primary to-cyber-secondary flex items-center justify-center rounded-lg shadow-glow-sm">
                <span className="text-black font-black text-xl">R</span>
              </div>
              <h1 className="text-2xl font-bold text-white tracking-tighter">ResuAI</h1>
            </button>
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/profile')}
                className="flex items-center gap-2 px-4 py-2 text-gray-300 hover:text-white hover:bg-white/5 rounded-full transition-all text-sm font-medium"
              >
                <User className="w-4 h-4" />
                <span className="hidden sm:inline">{user?.full_name || user?.email}</span>
              </button>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded-full transition-all text-sm font-medium"
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        {/* Welcome Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12"
        >
          <h2 className="text-3xl font-bold text-white mb-2">
            Welcome back, <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-primary to-cyber-secondary">{user?.full_name?.split(' ')[0] || 'User'}</span>
          </h2>
          <p className="text-gray-400 font-mono text-sm max-w-2xl">
            Workspace active. Ready to deploy career assets.
          </p>
        </motion.div>

        {/* Create New Resume Card */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="md:col-span-3"
          >
            <button
              onClick={handleCreateResume}
              className="w-full glass-card hover:bg-white/5 transition-all duration-300 flex flex-col items-center justify-center gap-4 py-16 rounded-2xl group border border-white/10 hover:border-cyber-primary/50 hover:shadow-glow-sm"
            >
              <div className="w-16 h-16 rounded-full bg-cyber-primary/10 flex items-center justify-center group-hover:scale-110 transition-transform border border-cyber-primary/20">
                <Plus className="w-8 h-8 text-cyber-primary" />
              </div>
              <div className="text-center">
                <span className="text-2xl font-bold text-white tracking-wide block mb-2">
                  Initialize New Resume
                </span>
                <span className="text-sm text-gray-400 font-mono px-4 max-w-md block">
                  Select a holographic template and begin the generation sequence
                </span>
              </div>
            </button>
          </motion.div>
        </div>

        {/* Resumes Grid */}
        <div className="space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <FileText className="w-5 h-5 text-cyber-secondary" />
              Active Projects
            </h3>
          </div>

          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="w-8 h-8 border-2 border-cyber-primary border-t-transparent rounded-full animate-spin" />
            </div>
          ) : resumes.length === 0 ? (
            <div className="text-center py-16 glass-card rounded-2xl border border-white/5 border-dashed">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-white/5 flex items-center justify-center">
                <FileText className="w-8 h-8 text-gray-500" />
              </div>
              <h3 className="text-lg font-medium text-white mb-2">
                No active projects found
              </h3>
              <p className="text-gray-500 font-mono text-sm">
                Begin by initializing a new resume sequence above
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {resumes.map((resume, index) => (
                <motion.div
                  key={resume.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="glass-card p-6 rounded-xl hover:bg-white/5 transition-all border border-white/10 hover:border-cyber-secondary/30 group"
                >
                  <div className="flex items-start justify-between mb-6">
                    <div className="flex-1">
                      <h3 className="text-lg font-bold text-white mb-1 truncate pr-2 group-hover:text-cyber-secondary transition-colors">
                        {resume.title}
                      </h3>
                      <p className="text-xs text-gray-500 font-mono">
                        Last sync: {new Date(resume.updated_at).toLocaleDateString()}
                      </p>
                    </div>
                    {resume.ats_score && (
                      <div className={`px-2 py-1 rounded text-xs font-bold font-mono ${resume.ats_score >= 80 ? 'bg-green-500/20 text-green-400' :
                          resume.ats_score >= 60 ? 'bg-yellow-500/20 text-yellow-400' :
                            'bg-red-500/20 text-red-400'
                        }`}>
                        {resume.ats_score}%
                      </div>
                    )}
                  </div>

                  <div className="grid grid-cols-3 gap-3">
                    <button
                      onClick={() => navigate(`/editor/latex/${resume.id}`)}
                      className="col-span-1 flex flex-col items-center justify-center gap-1 py-3 rounded-lg bg-white/5 hover:bg-white/10 hover:text-cyber-primary transition-all text-xs font-medium text-gray-400"
                    >
                      <Edit className="w-4 h-4" />
                      Edit
                    </button>
                    <button
                      onClick={() => handleExportPDF(resume.id, resume.title)}
                      className="col-span-1 flex flex-col items-center justify-center gap-1 py-3 rounded-lg bg-white/5 hover:bg-white/10 hover:text-cyber-secondary transition-all text-xs font-medium text-gray-400"
                    >
                      <Download className="w-4 h-4" />
                      PDF
                    </button>
                    <button
                      onClick={() => handleDeleteResume(resume.id)}
                      className="col-span-1 flex flex-col items-center justify-center gap-1 py-3 rounded-lg bg-white/5 hover:bg-red-500/20 hover:text-red-400 transition-all text-xs font-medium text-gray-400"
                    >
                      <Trash2 className="w-4 h-4" />
                      Delete
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
