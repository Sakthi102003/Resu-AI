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
  Sparkles,
  FileCode,
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
    // Navigate to template selection page
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
      // Export with the resume's stored template (no override)
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
    <div className="min-h-screen bg-gray-50 font-sans">
      {/* Header */}
      <header className="bg-white border-b-2 border-black">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/')}
              className="flex items-center gap-3 hover:opacity-80 transition-opacity group"
            >
              <div className="w-10 h-10 bg-black flex items-center justify-center shadow-neo-sm group-hover:shadow-none group-hover:translate-x-[2px] group-hover:translate-y-[2px] transition-all border-2 border-black">
                <span className="text-white font-bold text-xl">R</span>
              </div>
              <h1 className="text-2xl font-black text-black uppercase tracking-tighter">ResuAI</h1>
            </button>
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/profile')}
                className="flex items-center gap-2 px-4 py-2 text-black border-2 border-transparent hover:border-black hover:bg-brutal-yellow transition-all font-bold uppercase text-sm"
              >
                <User className="w-5 h-5" />
                <span className="hidden sm:inline">{user?.full_name || user?.email}</span>
              </button>
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 text-black border-2 border-transparent hover:border-black hover:bg-brutal-red hover:text-white transition-all font-bold uppercase text-sm"
              >
                <LogOut className="w-5 h-5" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8 border-l-4 border-black pl-6 py-2 bg-white">
          <h2 className="text-3xl font-black text-black mb-2 uppercase">
            Welcome back, {user?.full_name?.split(' ')[0] || 'there'}! 👋
          </h2>
          <p className="text-black font-mono">
            Create and manage your AI-powered resumes
          </p>
        </div>

        {/* Create New Resume Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:col-span-3"
          >
            <button
              onClick={handleCreateResume}
              className="w-full bg-white border-2 border-black shadow-neo hover:shadow-none hover:translate-x-[4px] hover:translate-y-[4px] transition-all flex flex-col items-center justify-center gap-3 py-12 group"
            >
              <div className="w-20 h-20 bg-brutal-green border-2 border-black rounded-full flex items-center justify-center group-hover:scale-110 transition-transform">
                <Plus className="w-10 h-10 text-black" />
              </div>
              <span className="text-2xl font-black text-black uppercase tracking-wider">
                Create New Resume
              </span>
              <span className="text-base text-black font-mono px-4 max-w-md">
                Select your template and theme, then build your professional resume
              </span>
            </button>
          </motion.div>
        </div>

        {/* Resumes Grid */}
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="spinner" />
          </div>
        ) : resumes.length === 0 ? (
          <div className="text-center py-12 border-2 border-black bg-white shadow-neo">
            <FileText className="w-16 h-16 text-black mx-auto mb-4" />
            <h3 className="text-xl font-black text-black mb-2 uppercase">
              No resumes yet
            </h3>
            <p className="text-black font-mono mb-6">
              Create your first resume using our AI-powered chat interface
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
                className="bg-white border-2 border-black shadow-neo p-6 hover:shadow-neo-lg transition-all group"
              >
                <div className="flex items-start justify-between mb-4 border-b-2 border-black pb-4">
                  <div className="flex-1">
                    <h3 className="text-lg font-black text-black mb-1 uppercase truncate pr-2">
                      {resume.title}
                    </h3>
                    <p className="text-xs text-black font-mono">
                      Updated {new Date(resume.updated_at).toLocaleDateString()}
                    </p>
                    {resume.ats_score && (
                      <div className="mt-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-black uppercase bg-brutal-yellow px-2 py-0.5 border border-black">
                            ATS Score
                          </span>
                          <span
                            className={`text-sm font-black ${
                              resume.ats_score >= 80
                                ? 'text-green-600'
                                : resume.ats_score >= 60
                                ? 'text-yellow-600'
                                : 'text-red-600'
                            }`}
                          >
                            {resume.ats_score}/100
                          </span>
                        </div>
                      </div>
                    )}
                  </div>
                  <div className="w-10 h-10 bg-brutal-blue border-2 border-black flex items-center justify-center">
                    <FileText className="w-6 h-6 text-black" />
                  </div>
                </div>

                <div className="flex flex-wrap gap-2">
                  <button
                    onClick={() => navigate(`/editor/latex/${resume.id}`)}
                    className="flex-1 btn bg-black text-white hover:bg-gray-800"
                  >
                    <Edit className="w-4 h-4 inline mr-1" />
                    Edit
                  </button>
                  <button
                    onClick={() => handleExportPDF(resume.id, resume.title)}
                    className="btn bg-white text-black hover:bg-brutal-green"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                  <button
                    onClick={() => handleDeleteResume(resume.id)}
                    className="btn bg-white text-black hover:bg-brutal-red hover:text-white"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}
