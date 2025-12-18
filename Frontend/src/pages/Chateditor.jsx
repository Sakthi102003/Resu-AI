import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  Send,
  ArrowLeft,
  Download,
  Sparkles,
  Award,
  Briefcase,
  Loader,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { resumeAPI, chatAPI, aiAPI } from '../Services/api'
import ResumePreview from '../components/resumepreview'
import ResumeScoreCard from '../components/ResumeScoreCard'
import JobRecommendation from '../components/jobRecommendation'

export default function ChatEditor() {
  const { resumeId } = useParams()
  const navigate = useNavigate()
  const messagesEndRef = useRef(null)

  const [resume, setResume] = useState(null)
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content:
        "Hi! I'm your AI resume assistant. I'll help you create a professional, ATS-optimized resume. Let's start by telling me about your most recent role or experience. What position did you hold?",
      timestamp: new Date(),
    },
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSending, setIsSending] = useState(false)
  const [showScore, setShowScore] = useState(false)
  const [showJobs, setShowJobs] = useState(false)
  const [atsScore, setAtsScore] = useState(null)
  const [jobRecommendations, setJobRecommendations] = useState([])

  useEffect(() => {
    if (resumeId) {
      loadResume()
    }
  }, [resumeId])

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const loadResume = async () => {
    setIsLoading(true)
    try {
      const response = await resumeAPI.getById(resumeId)
      setResume(response.data)
    } catch (error) {
      toast.error('Failed to load resume')
      navigate('/dashboard')
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || isSending) return

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInputMessage('')
    setIsSending(true)

    try {
      const response = await chatAPI.respond({
        message: inputMessage,
        resume_id: resumeId,
        context: messages.slice(-6),
      })

      const assistantMessage = {
        role: 'assistant',
        content: response.data.response,
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])

      // Update resume if AI extracted data
      if (response.data.resume_data && resumeId) {
        await resumeAPI.update(resumeId, {
          data: {
            ...resume?.data,
            ...response.data.resume_data,
          },
        })
        loadResume()
      }
    } catch (error) {
      toast.error('Failed to send message')
      const errorMessage = {
        role: 'assistant',
        content: "Sorry, I couldn't process that. Please try again.",
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsSending(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleCalculateScore = async () => {
    if (!resumeId) return

    setShowScore(true)
    try {
      const response = await aiAPI.atsScore(resumeId)
      setAtsScore(response.data)
    } catch (error) {
      toast.error('Failed to calculate ATS score')
    }
  }

  const handleGetJobRecommendations = async () => {
    if (!resumeId) return

    setShowJobs(true)
    try {
      const response = await aiAPI.jobRecommend(resumeId)
      setJobRecommendations(response.data)
    } catch (error) {
      toast.error('Failed to get job recommendations')
    }
  }

  const handleExportPDF = async () => {
    if (!resumeId) return

    try {
      // Export with the currently selected template (no override)
      const response = await resumeAPI.exportPDF(resumeId, null)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${resume?.title || 'resume'}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('PDF downloaded!')
    } catch (error) {
      toast.error('Failed to export PDF')
    }
  }

  if (isLoading) {
    return (
      <div className="h-screen flex items-center justify-center">
        <div className="spinner" />
      </div>
    )
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50 font-sans">
      {/* Header */}
      <header className="bg-white border-b-2 border-black px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-brutal-yellow border-2 border-transparent hover:border-black transition-all"
            >
              <ArrowLeft className="w-5 h-5 text-black" />
            </button>
            <div>
              <h1 className="text-xl font-black text-black uppercase">
                {resume?.title || 'New Resume'}
              </h1>
              <p className="text-sm text-black font-mono">
                Chat with AI to build your resume
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate('/')}
              className="hidden sm:flex items-center gap-2 px-3 py-2 text-lg font-black text-black hover:text-brutal-blue transition-colors uppercase"
            >
              <div className="w-6 h-6 bg-black flex items-center justify-center border-2 border-black">
                <span className="text-white text-xs font-bold">R</span>
              </div>
              ResuAI
            </button>
            <button
              onClick={handleCalculateScore}
              className="flex items-center gap-2 px-4 py-2 bg-brutal-yellow text-black border-2 border-black shadow-neo hover:shadow-none hover:translate-x-[2px] hover:translate-y-[2px] transition-all font-bold uppercase text-sm"
            >
              <Award className="w-4 h-4" />
              <span className="hidden sm:inline">ATS Score</span>
            </button>
            <button
              onClick={handleGetJobRecommendations}
              className="flex items-center gap-2 px-4 py-2 bg-brutal-green text-black border-2 border-black shadow-neo hover:shadow-none hover:translate-x-[2px] hover:translate-y-[2px] transition-all font-bold uppercase text-sm"
            >
              <Briefcase className="w-4 h-4" />
              <span className="hidden sm:inline">Jobs</span>
            </button>
            <button
              onClick={handleExportPDF}
              className="flex items-center gap-2 px-4 py-2 bg-black text-white border-2 border-black shadow-neo hover:bg-white hover:text-black hover:shadow-none hover:translate-x-[2px] hover:translate-y-[2px] transition-all font-bold uppercase text-sm"
            >
              <Download className="w-4 h-4" />
              <span className="hidden sm:inline">Export PDF</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Chat Section */}
        <div className="w-1/2 flex flex-col bg-gray-50">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            <AnimatePresence>
              {messages.map((message, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0 }}
                  className={`flex ${
                    message.role === 'user' ? 'justify-end' : 'justify-start'
                  }`}
                >
                  <div
                    className={`max-w-[80%] p-4 border-2 border-black shadow-neo-sm ${
                      message.role === 'user'
                        ? 'bg-brutal-blue text-black'
                        : 'bg-white text-black'
                    }`}
                  >
                    {message.role === 'assistant' && (
                      <div className="flex items-center gap-2 mb-2 border-b-2 border-black pb-1">
                        <Sparkles className="w-4 h-4 text-black" />
                        <span className="text-xs font-black uppercase text-black">
                          AI Assistant
                        </span>
                      </div>
                    )}
                    <p className="whitespace-pre-wrap font-mono text-sm">{message.content}</p>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            {isSending && (
              <div className="flex justify-start">
                <div className="bg-white border-2 border-black p-4 shadow-neo-sm">
                  <div className="flex items-center gap-2">
                    <Loader className="w-4 h-4 animate-spin text-black" />
                    <span className="text-sm text-black font-mono">AI is thinking...</span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="border-t-2 border-black bg-white p-4">
            <div className="flex gap-2">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message... (e.g., 'I worked as a Software Engineer at Google')"
                className="flex-1 input font-mono"
                disabled={isSending}
              />
              <button
                onClick={handleSendMessage}
                disabled={isSending || !inputMessage.trim()}
                className="btn bg-black text-white hover:bg-gray-800 px-6 disabled:opacity-50"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
            <p className="text-xs text-black font-mono mt-2">
              💡 Tip: Be specific about your experience, achievements, and skills for
              better results
            </p>
          </div>
        </div>

        {/* Preview Section */}
        <div className="w-1/2 border-l-2 border-black bg-white overflow-y-auto">
          <div className="p-4 sticky top-0 bg-white border-b-2 border-black z-10 flex justify-between items-center">
            <h3 className="text-lg font-black uppercase">Live Preview</h3>
            <div className="text-xs font-mono bg-brutal-yellow px-2 py-1 border border-black">
              Auto-updating
            </div>
          </div>
          <div className="p-4">
            {resume && <ResumePreview data={resume.data} />}
          </div>
        </div>
      </div>

      {/* Modals */}
      {showScore && (
        <ResumeScoreCard
          score={atsScore}
          onClose={() => setShowScore(false)}
        />
      )}
      {showJobs && (
        <JobRecommendation
          jobs={jobRecommendations}
          onClose={() => setShowJobs(false)}
        />
      )}
    </div>
  )
}
