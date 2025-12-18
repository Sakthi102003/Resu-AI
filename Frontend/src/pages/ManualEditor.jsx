import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import {
  ArrowLeft,
  Download,
  Save,
  Plus,
  Trash2,
  Award,
  Briefcase,
  Sparkles,
} from 'lucide-react'
import toast from 'react-hot-toast'
import { resumeAPI, aiAPI } from '../Services/api'
import ResumePreview from '../components/resumepreview'
import ResumeScoreCard from '../components/ResumeScoreCard'
import JobRecommendation from '../components/jobRecommendation'

export default function ManualEditor() {
  const { resumeId } = useParams()
  const navigate = useNavigate()
  const isNew = resumeId === 'new'

  const [isSaving, setIsSaving] = useState(false)
  const [isAiProcessing, setIsAiProcessing] = useState(false)
  const [showScore, setShowScore] = useState(false)
  const [showJobs, setShowJobs] = useState(false)
  const [atsScore, setAtsScore] = useState(null)
  const [jobRecommendations, setJobRecommendations] = useState([])
  const [currentResumeId, setCurrentResumeId] = useState(isNew ? null : resumeId)
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [selectedColor, setSelectedColor] = useState(null)

  const [resumeData, setResumeData] = useState({
    title: 'My Resume',
    personal_info: {
      name: '',
      email: '',
      phone: '',
      location: '',
      linkedin: '',
      website: '',
    },
    summary: '',
    experience: [],
    education: [],
    skills: [],
    certifications: [],
    projects: [],
  })

  useEffect(() => {
    if (!isNew && resumeId) {
      loadResume()
    }
  }, [resumeId, isNew])

  const loadResume = async () => {
    try {
      const response = await resumeAPI.getById(resumeId)
      const loadedData = response.data.data || {}
      
      // Store template and color info
      setSelectedTemplate(response.data.template || 'auto_cv')
      setSelectedColor(response.data.theme_color || '#3B82F6')
      
      // Merge loaded data with default structure to ensure all fields exist
      setResumeData({
        title: response.data.title || 'My Resume',
        personal_info: loadedData.personal_info || {
          name: '',
          email: '',
          phone: '',
          location: '',
          linkedin: '',
          website: '',
        },
        summary: loadedData.summary || '',
        experience: loadedData.experience || [],
        education: loadedData.education || [],
        skills: loadedData.skills || [],
        certifications: loadedData.certifications || [],
        projects: loadedData.projects || [],
      })
      
      console.log('Resume loaded:', response.data)
    } catch (error) {
      console.error('Load resume error:', error)
      toast.error('Failed to load resume')
      navigate('/dashboard')
    }
  }

  const handleSave = async () => {
    setIsSaving(true)
    try {
      const payload = {
        title: resumeData.title,
        data: { ...resumeData },
      }
      delete payload.data.title

      console.log('Saving resume with payload:', payload)

      if (isNew || !currentResumeId) {
        const response = await resumeAPI.create(payload)
        setCurrentResumeId(response.data.id)
        toast.success('Resume created successfully!')
        navigate(`/editor/manual/${response.data.id}`, { replace: true })
      } else {
        await resumeAPI.update(currentResumeId, payload)
        toast.success('Resume saved successfully!')
      }
    } catch (error) {
      console.error('Save error:', error)
      console.error('Error response:', error.response?.data)
      toast.error(error.response?.data?.message || 'Failed to save resume')
    } finally {
      setIsSaving(false)
    }
  }

  const handleExportPDF = async () => {
    if (!currentResumeId) {
      toast.error('Please save the resume first')
      return
    }

    try {
      // Export with the currently selected template (no override)
      const response = await resumeAPI.exportPDF(currentResumeId, null)
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${resumeData.title}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('PDF downloaded!')
    } catch (error) {
      toast.error('Failed to export PDF')
    }
  }

  const handleCalculateScore = async () => {
    if (!currentResumeId) {
      toast.error('Please save the resume first')
      return
    }

    setShowScore(true)
    try {
      const response = await aiAPI.atsScore(currentResumeId)
      setAtsScore(response.data)
    } catch (error) {
      toast.error('Failed to calculate ATS score')
    }
  }

  const handleGetJobRecommendations = async () => {
    if (!currentResumeId) {
      toast.error('Please save the resume first')
      return
    }

    setShowJobs(true)
    try {
      const response = await aiAPI.jobRecommend(currentResumeId)
      setJobRecommendations(response.data)
    } catch (error) {
      toast.error('Failed to get job recommendations')
    }
  }

  const updateField = (field, value) => {
    setResumeData({ ...resumeData, [field]: value })
  }

  const updatePersonalInfo = (field, value) => {
    setResumeData({
      ...resumeData,
      personal_info: { ...resumeData.personal_info, [field]: value },
    })
  }

  const addExperience = () => {
    setResumeData({
      ...resumeData,
      experience: [
        ...resumeData.experience,
        {
          company: '',
          position: '',
          location: '',
          start_date: '',
          end_date: '',
          current: false,
          description: [],
        },
      ],
    })
  }

  const updateExperience = (index, field, value) => {
    const newExperience = [...resumeData.experience]
    newExperience[index] = { ...newExperience[index], [field]: value }
    setResumeData({ ...resumeData, experience: newExperience })
  }

  const removeExperience = (index) => {
    setResumeData({
      ...resumeData,
      experience: resumeData.experience.filter((_, i) => i !== index),
    })
  }

  const addExperiencePoint = (expIndex) => {
    const newExperience = [...resumeData.experience]
    newExperience[expIndex].description = [
      ...newExperience[expIndex].description,
      '',
    ]
    setResumeData({ ...resumeData, experience: newExperience })
  }

  const updateExperiencePoint = (expIndex, pointIndex, value) => {
    const newExperience = [...resumeData.experience]
    newExperience[expIndex].description[pointIndex] = value
    setResumeData({ ...resumeData, experience: newExperience })
  }

  const removeExperiencePoint = (expIndex, pointIndex) => {
    const newExperience = [...resumeData.experience]
    newExperience[expIndex].description = newExperience[
      expIndex
    ].description.filter((_, i) => i !== pointIndex)
    setResumeData({ ...resumeData, experience: newExperience })
  }

  const addEducation = () => {
    setResumeData({
      ...resumeData,
      education: [
        ...resumeData.education,
        {
          institution: '',
          degree: '',
          field: '',
          graduation_date: '',
          gpa: '',
        },
      ],
    })
  }

  const updateEducation = (index, field, value) => {
    const newEducation = [...resumeData.education]
    newEducation[index] = { ...newEducation[index], [field]: value }
    setResumeData({ ...resumeData, education: newEducation })
  }

  const removeEducation = (index) => {
    setResumeData({
      ...resumeData,
      education: resumeData.education.filter((_, i) => i !== index),
    })
  }

  const addSkill = () => {
    setResumeData({
      ...resumeData,
      skills: [...resumeData.skills, { category: '', items: [] }],
    })
  }

  const updateSkill = (index, field, value) => {
    const newSkills = [...resumeData.skills]
    newSkills[index] = { ...newSkills[index], [field]: value }
    setResumeData({ ...resumeData, skills: newSkills })
  }

  const removeSkill = (index) => {
    setResumeData({
      ...resumeData,
      skills: resumeData.skills.filter((_, i) => i !== index),
    })
  }

  const addProject = () => {
    setResumeData({
      ...resumeData,
      projects: [
        ...resumeData.projects,
        {
          name: '',
          description: '',
          technologies: [],
          url: '',
        },
      ],
    })
  }

  const updateProject = (index, field, value) => {
    const newProjects = [...resumeData.projects]
    newProjects[index] = { ...newProjects[index], [field]: value }
    setResumeData({ ...resumeData, projects: newProjects })
  }

  const removeProject = (index) => {
    setResumeData({
      ...resumeData,
      projects: resumeData.projects.filter((_, i) => i !== index),
    })
  }

  const addCertification = () => {
    setResumeData({
      ...resumeData,
      certifications: [
        ...resumeData.certifications,
        {
          name: '',
          issuer: '',
          date: '',
          credential_id: '',
        },
      ],
    })
  }

  const updateCertification = (index, field, value) => {
    const newCertifications = [...resumeData.certifications]
    newCertifications[index] = { ...newCertifications[index], [field]: value }
    setResumeData({ ...resumeData, certifications: newCertifications })
  }

  const removeCertification = (index) => {
    setResumeData({
      ...resumeData,
      certifications: resumeData.certifications.filter((_, i) => i !== index),
    })
  }

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              type="button"
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div className="flex items-center gap-3">
              <input
                type="text"
                value={resumeData.title}
                onChange={(e) => updateField('title', e.target.value)}
                className="text-xl font-bold text-gray-900 bg-transparent border-b-2 border-transparent hover:border-gray-300 focus:border-primary-500 outline-none transition"
                placeholder="Resume Title"
              />
              {selectedTemplate && (
                <div className="flex items-center gap-2 px-3 py-1 bg-primary-50 border border-primary-200 rounded-lg">
                  <div 
                    className="w-3 h-3 rounded-full" 
                    style={{ backgroundColor: selectedColor || '#3B82F6' }}
                  />
                  <span className="text-xs font-semibold text-primary-700 uppercase">
                    {selectedTemplate.replace(/_/g, ' ')}
                  </span>
                </div>
              )}
            </div>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => navigate('/')}
              className="hidden lg:flex items-center gap-2 px-3 py-2 text-lg font-bold text-gray-900 hover:text-primary-600 transition-colors"
            >
              <Sparkles className="w-5 h-5" />
              ResuAI
            </button>
            <button
              type="button"
              onClick={handleSave}
              disabled={isSaving}
              className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition disabled:opacity-50"
            >
              <Save className="w-4 h-4" />
              <span className="hidden sm:inline">
                {isSaving ? 'Saving...' : 'Save'}
              </span>
            </button>
            <button
              type="button"
              onClick={async () => {
                // AI Assist: send current resume data to the AI enhance endpoint and merge results
                if (isAiProcessing) return
                setIsAiProcessing(true)
                try {
                  const payload = { resume: resumeData }
                  const response = await aiAPI.enhance(payload)
                  const enhanced = response.data || {}
                  // Merge enhanced fields into resumeData defensively
                  setResumeData((prev) => ({ ...prev, ...enhanced }))
                  toast.success('AI suggestions applied')
                } catch (error) {
                  toast.error('AI assist failed')
                } finally {
                  setIsAiProcessing(false)
                }
              }}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              <Sparkles className="w-4 h-4" />
              <span className="hidden sm:inline">
                {isAiProcessing ? 'Processing...' : 'AI Assist'}
              </span>
            </button>
            <button
              type="button"
              onClick={handleCalculateScore}
              className="flex items-center gap-2 px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition"
            >
              <Award className="w-4 h-4" />
              <span className="hidden sm:inline">ATS Score</span>
            </button>
            <button
              type="button"
              onClick={handleGetJobRecommendations}
              className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
            >
              <Briefcase className="w-4 h-4" />
              <span className="hidden sm:inline">Jobs</span>
            </button>
            <button
              type="button"
              onClick={handleExportPDF}
              className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition"
            >
              <Download className="w-4 h-4" />
              <span className="hidden sm:inline">Export PDF</span>
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Form Section */}
        <div className="w-1/2 overflow-y-auto p-6">
          <div className="max-w-4xl mx-auto space-y-6">
            {/* Template Info Banner */}
            {selectedTemplate && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-gradient-to-r from-primary-600 to-purple-600 text-white p-4 rounded-lg shadow-lg"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                      <span className="text-xl">✨</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-sm">
                        Template: {selectedTemplate.replace(/_/g, ' ').toUpperCase()}
                      </h3>
                      <p className="text-xs text-primary-100">
                        Fill in your details below. Your resume will use the <strong>{selectedTemplate.replace(/_/g, ' ')}</strong> template when downloaded.
                      </p>
                    </div>
                  </div>
                  <div 
                    className="w-8 h-8 rounded-full border-2 border-white shadow-md"
                    style={{ backgroundColor: selectedColor }}
                    title="Theme Color"
                  />
                </div>
              </motion.div>
            )}

            {/* Personal Information */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="card"
            >
              <h2 className="text-xl font-bold mb-4">Personal Information</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Full Name"
                  value={resumeData.personal_info.name}
                  onChange={(e) => updatePersonalInfo('name', e.target.value)}
                  className="input"
                />
                <input
                  type="email"
                  placeholder="Email"
                  value={resumeData.personal_info.email}
                  onChange={(e) => updatePersonalInfo('email', e.target.value)}
                  className="input"
                />
                <input
                  type="tel"
                  placeholder="Phone"
                  value={resumeData.personal_info.phone}
                  onChange={(e) => updatePersonalInfo('phone', e.target.value)}
                  className="input"
                />
                <input
                  type="text"
                  placeholder="Location"
                  value={resumeData.personal_info.location}
                  onChange={(e) =>
                    updatePersonalInfo('location', e.target.value)
                  }
                  className="input"
                />
                <input
                  type="url"
                  placeholder="LinkedIn URL"
                  value={resumeData.personal_info.linkedin}
                  onChange={(e) =>
                    updatePersonalInfo('linkedin', e.target.value)
                  }
                  className="input"
                />
                <input
                  type="url"
                  placeholder="Website/Portfolio"
                  value={resumeData.personal_info.website}
                  onChange={(e) =>
                    updatePersonalInfo('website', e.target.value)
                  }
                  className="input"
                />
              </div>
            </motion.div>

            {/* Summary */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="card"
            >
              <h2 className="text-xl font-bold mb-4">Career Objective / Professional Summary</h2>
              <textarea
                placeholder="Write a brief, keyword-rich summary targeted toward cybersecurity and development..."
                value={resumeData.summary}
                onChange={(e) => updateField('summary', e.target.value)}
                className="input min-h-[120px]"
              />
            </motion.div>

            {/* Skills - MOVED UP */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Technical Skills</h2>
                <button type="button" onClick={addSkill} className="btn btn-primary">
                  <Plus className="w-4 h-4 mr-1" />
                  Add Skill Category
                </button>
              </div>
              <div className="space-y-4">
                {resumeData.skills.map((skill, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <input
                        type="text"
                        placeholder="Category (e.g., Programming Languages)"
                        value={skill.category}
                        onChange={(e) =>
                          updateSkill(index, 'category', e.target.value)
                        }
                        className="input flex-1 mr-2"
                      />
                      <button
                        type="button"
                        onClick={() => removeSkill(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    <input
                      type="text"
                      placeholder="Skills (comma-separated, e.g., Python, JavaScript, React)"
                      value={skill.items.join(', ')}
                      onChange={(e) =>
                        updateSkill(
                          index,
                          'items',
                          e.target.value.split(',').map((s) => s.trim())
                        )
                      }
                      className="input"
                    />
                  </div>
                ))}
                {resumeData.skills.length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    No skills added yet. Click "Add Skill Category" to get started.
                  </p>
                )}
              </div>
            </motion.div>

            {/* Projects - MOVED UP */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Projects</h2>
                <button type="button" onClick={addProject} className="btn btn-primary">
                  <Plus className="w-4 h-4 mr-1" />
                  Add Project
                </button>
              </div>
              <div className="space-y-4">
                {resumeData.projects.map((project, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="font-semibold">Project {index + 1}</h3>
                      <button
                        type="button"
                        onClick={() => removeProject(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="space-y-3">
                      <input
                        type="text"
                        placeholder="Project Name"
                        value={project.name}
                        onChange={(e) =>
                          updateProject(index, 'name', e.target.value)
                        }
                        className="input"
                      />
                      <textarea
                        placeholder="Description"
                        value={project.description}
                        onChange={(e) =>
                          updateProject(index, 'description', e.target.value)
                        }
                        className="input min-h-[80px]"
                      />
                      <input
                        type="text"
                        placeholder="Technologies (comma-separated)"
                        value={project.technologies.join(', ')}
                        onChange={(e) =>
                          updateProject(
                            index,
                            'technologies',
                            e.target.value.split(',').map((s) => s.trim())
                          )
                        }
                        className="input"
                      />
                      <input
                        type="url"
                        placeholder="Project URL (Optional)"
                        value={project.url}
                        onChange={(e) =>
                          updateProject(index, 'url', e.target.value)
                        }
                        className="input"
                      />
                    </div>
                  </div>
                ))}
                {resumeData.projects.length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    No projects added yet. Click "Add Project" to get started.
                  </p>
                )}
              </div>
            </motion.div>

            {/* Experience / Internship Experience */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Internship / Work Experience</h2>
                <button type="button" onClick={addExperience} className="btn btn-primary">
                  <Plus className="w-4 h-4 mr-1" />
                  Add Experience
                </button>
              </div>
              <div className="space-y-4">
                {resumeData.experience.map((exp, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="font-semibold">Experience {index + 1}</h3>
                      <button
                        type="button"
                        onClick={() => removeExperience(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                      <input
                        type="text"
                        placeholder="Company"
                        value={exp.company}
                        onChange={(e) =>
                          updateExperience(index, 'company', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Position"
                        value={exp.position}
                        onChange={(e) =>
                          updateExperience(index, 'position', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Location"
                        value={exp.location}
                        onChange={(e) =>
                          updateExperience(index, 'location', e.target.value)
                        }
                        className="input"
                      />
                      <div className="flex gap-2">
                        <input
                          type="text"
                          placeholder="Start Date"
                          value={exp.start_date}
                          onChange={(e) =>
                            updateExperience(index, 'start_date', e.target.value)
                          }
                          className="input flex-1"
                        />
                        <input
                          type="text"
                          placeholder="End Date"
                          value={exp.end_date}
                          onChange={(e) =>
                            updateExperience(index, 'end_date', e.target.value)
                          }
                          className="input flex-1"
                          disabled={exp.current}
                        />
                      </div>
                    </div>
                    <label className="flex items-center gap-2 mb-3">
                      <input
                        type="checkbox"
                        checked={exp.current}
                        onChange={(e) =>
                          updateExperience(index, 'current', e.target.checked)
                        }
                      />
                      <span className="text-sm">Currently working here</span>
                    </label>
                    <div className="space-y-2">
                      <div className="flex items-center justify-between">
                        <label className="text-sm font-medium">
                          Key Achievements
                        </label>
                        <button
                          type="button"
                          onClick={() => addExperiencePoint(index)}
                          className="text-xs text-primary-600 hover:text-primary-700"
                        >
                          + Add Point
                        </button>
                      </div>
                      {exp.description.map((point, pointIndex) => (
                        <div key={pointIndex} className="flex gap-2">
                          <input
                            type="text"
                            placeholder="Achievement or responsibility"
                            value={point}
                            onChange={(e) =>
                              updateExperiencePoint(
                                index,
                                pointIndex,
                                e.target.value
                              )
                            }
                            className="input flex-1"
                          />
                          <button
                            type="button"
                            onClick={() =>
                              removeExperiencePoint(index, pointIndex)
                            }
                            className="text-red-500 hover:text-red-700"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
                {resumeData.experience.length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    No experience added yet. Click "Add Experience" to get started.
                  </p>
                )}
              </div>
            </motion.div>

            {/* Certifications */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Certifications</h2>
                <button type="button" onClick={addCertification} className="btn btn-primary">
                  <Plus className="w-4 h-4 mr-1" />
                  Add Certification
                </button>
              </div>
              <div className="space-y-4">
                {resumeData.certifications.map((cert, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="font-semibold">Certification {index + 1}</h3>
                      <button
                        type="button"
                        onClick={() => removeCertification(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <input
                        type="text"
                        placeholder="Certification Name"
                        value={cert.name}
                        onChange={(e) =>
                          updateCertification(index, 'name', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Issuing Organization"
                        value={cert.issuer}
                        onChange={(e) =>
                          updateCertification(index, 'issuer', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Date Obtained"
                        value={cert.date}
                        onChange={(e) =>
                          updateCertification(index, 'date', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Credential ID (Optional)"
                        value={cert.credential_id || ''}
                        onChange={(e) =>
                          updateCertification(index, 'credential_id', e.target.value)
                        }
                        className="input"
                      />
                    </div>
                  </div>
                ))}
                {resumeData.certifications.length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    No certifications added yet. Click "Add Certification" to get started.
                  </p>
                )}
              </div>
            </motion.div>

            {/* Education - MOVED TO END */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold">Education</h2>
                <button type="button" onClick={addEducation} className="btn btn-primary">
                  <Plus className="w-4 h-4 mr-1" />
                  Add Education
                </button>
              </div>
              <div className="space-y-4">
                {resumeData.education.map((edu, index) => (
                  <div key={index} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="font-semibold">Education {index + 1}</h3>
                      <button
                        type="button"
                        onClick={() => removeEducation(index)}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <input
                        type="text"
                        placeholder="Institution"
                        value={edu.institution}
                        onChange={(e) =>
                          updateEducation(index, 'institution', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Degree"
                        value={edu.degree}
                        onChange={(e) =>
                          updateEducation(index, 'degree', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Field of Study"
                        value={edu.field}
                        onChange={(e) =>
                          updateEducation(index, 'field', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="Graduation Date"
                        value={edu.graduation_date}
                        onChange={(e) =>
                          updateEducation(index, 'graduation_date', e.target.value)
                        }
                        className="input"
                      />
                      <input
                        type="text"
                        placeholder="GPA (Optional)"
                        value={edu.gpa}
                        onChange={(e) =>
                          updateEducation(index, 'gpa', e.target.value)
                        }
                        className="input"
                      />
                    </div>
                  </div>
                ))}
                {resumeData.education.length === 0 && (
                  <p className="text-gray-500 text-center py-4">
                    No education added yet. Click "Add Education" to get started.
                  </p>
                )}
              </div>
            </motion.div>
          </div>
        </div>

        {/* Preview Section */}
        <div className="w-1/2 border-l border-gray-200 bg-white overflow-y-auto">
          <div className="p-4 sticky top-0 bg-white border-b border-gray-200 z-10">
            <h3 className="text-lg font-semibold">Live Preview</h3>
          </div>
          <div className="p-4">
            <ResumePreview data={resumeData} />
          </div>
        </div>
      </div>

      {/* Modals */}
      {showScore && (
        <ResumeScoreCard score={atsScore} onClose={() => setShowScore(false)} />
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
