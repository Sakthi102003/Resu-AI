import { motion } from 'framer-motion'
import { Mail, Phone, MapPin, Linkedin, Github, Globe } from 'lucide-react'

export default function ResumePreview({ data }) {
  if (!data) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p>Start chatting to build your resume!</p>
      </div>
    )
  }

  const personalInfo = data.personal_info || {}
  const experience = data.experience || []
  const education = data.education || []
  const skills = data.skills || []
  const projects = data.projects || []
  const certifications = data.certifications || []

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="bg-white p-8 shadow-lg rounded-lg text-sm"
      style={{ fontFamily: 'Georgia, serif' }}
    >
      {/* Header */}
      <div className="text-center border-b-2 border-primary-600 pb-4 mb-6">
        {personalInfo.name && (
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {personalInfo.name}
          </h1>
        )}
        <div className="flex flex-wrap justify-center gap-3 text-gray-600 text-xs">
          {personalInfo.email && (
            <div className="flex items-center gap-1">
              <Mail className="w-3 h-3" />
              {personalInfo.email}
            </div>
          )}
          {personalInfo.phone && (
            <div className="flex items-center gap-1">
              <Phone className="w-3 h-3" />
              {personalInfo.phone}
            </div>
          )}
          {personalInfo.location && (
            <div className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {personalInfo.location}
            </div>
          )}
        </div>
        {(personalInfo.linkedin || personalInfo.github || personalInfo.portfolio) && (
          <div className="flex flex-wrap justify-center gap-3 text-primary-600 text-xs mt-2">
            {personalInfo.linkedin && (
              <div className="flex items-center gap-1">
                <Linkedin className="w-3 h-3" />
                LinkedIn
              </div>
            )}
            {personalInfo.github && (
              <div className="flex items-center gap-1">
                <Github className="w-3 h-3" />
                GitHub
              </div>
            )}
            {personalInfo.portfolio && (
              <div className="flex items-center gap-1">
                <Globe className="w-3 h-3" />
                Portfolio
              </div>
            )}
          </div>
        )}
      </div>

      {/* Summary/Objective */}
      {(data.summary || data.objective) && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-primary-700 border-b border-gray-300 pb-1 mb-2">
            {data.summary ? 'CAREER OBJECTIVE / PROFESSIONAL SUMMARY' : 'OBJECTIVE'}
          </h2>
          <p className="text-gray-700 text-xs leading-relaxed">
            {data.summary || data.objective}
          </p>
        </div>
      )}

      {/* Skills - MOVED UP */}
      {skills.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-primary-700 border-b border-gray-300 pb-1 mb-2">
            TECHNICAL SKILLS
          </h2>
          {skills.map((skill, index) => {
            // Handle both object format {category, items} and string format
            if (skill && typeof skill === 'object' && skill !== null && 'category' in skill) {
              return (
                <div key={index} className="mb-2">
                  <h3 className="font-semibold text-gray-800 text-xs mb-1">
                    {skill.category || 'Skills'}
                  </h3>
                  <div className="flex flex-wrap gap-2">
                    {Array.isArray(skill.items) && skill.items.length > 0 && skill.items.map((item, idx) => (
                      item && (
                        <span
                          key={idx}
                          className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs"
                        >
                          {item}
                        </span>
                      )
                    ))}
                  </div>
                </div>
              )
            }
            // Fallback for string format
            return (
              <span
                key={index}
                className="px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs inline-block mb-2 mr-2"
              >
                {String(skill)}
              </span>
            )
          })}
        </div>
      )}

      {/* Projects - MOVED UP */}
      {projects.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-primary-700 border-b border-gray-300 pb-1 mb-3">
            PROJECTS
          </h2>
          {projects.map((project, index) => (
            <div key={index} className="mb-2">
              <h3 className="font-bold text-gray-900 text-sm">
                {project.name}
              </h3>
              {project.description && (
                <p className="text-gray-600 text-xs mb-1">
                  {project.description}
                </p>
              )}
              {project.technologies && project.technologies.length > 0 && (
                <p className="text-xs text-gray-600">
                  <span className="font-semibold">Technologies:</span>{' '}
                  {project.technologies.join(', ')}
                </p>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Experience / Internship Experience */}
      {experience.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-primary-700 border-b border-gray-300 pb-1 mb-3">
            INTERNSHIP / WORK EXPERIENCE
          </h2>
          {experience.map((exp, index) => (
            <div key={index} className="mb-3">
              <div className="flex justify-between items-start mb-1">
                <div>
                  <h3 className="font-bold text-gray-900 text-sm">
                    {exp.position}
                  </h3>
                  <p className="text-gray-700 text-xs">{exp.company}</p>
                </div>
                <span className="text-xs text-gray-600 italic">
                  {exp.start_date} - {exp.current ? 'Present' : exp.end_date}
                </span>
              </div>
              {exp.description && (
                <>
                  {/* Handle description as array or string */}
                  {Array.isArray(exp.description) ? (
                    exp.description.length > 0 && (
                      <ul className="list-disc list-inside text-xs text-gray-700 space-y-1">
                        {exp.description.map((point, idx) => (
                          <li key={idx}>{point}</li>
                        ))}
                      </ul>
                    )
                  ) : (
                    <p className="text-gray-600 text-xs mb-1">{exp.description}</p>
                  )}
                </>
              )}
              {exp.achievements && exp.achievements.length > 0 && (
                <ul className="list-disc list-inside text-xs text-gray-700 space-y-1">
                  {exp.achievements.map((achievement, idx) => (
                    <li key={idx}>{achievement}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Certifications */}
      {certifications.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-primary-700 border-b border-gray-300 pb-1 mb-2">
            CERTIFICATIONS
          </h2>
          {certifications.map((cert, index) => (
            <div key={index} className="mb-1">
              <p className="text-xs text-gray-700">
                <span className="font-bold">{cert.name}</span> - {cert.issuer}
                {cert.date && ` (${cert.date})`}
              </p>
            </div>
          ))}
        </div>
      )}

      {/* Education - MOVED TO END */}
      {education.length > 0 && (
        <div className="mb-6">
          <h2 className="text-lg font-bold text-primary-700 border-b border-gray-300 pb-1 mb-3">
            EDUCATION
          </h2>
          {education.map((edu, index) => (
            <div key={index} className="mb-2">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-gray-900 text-sm">
                    {edu.degree}
                    {(edu.field_of_study || edu.field) && ` in ${edu.field_of_study || edu.field}`}
                  </h3>
                  <p className="text-gray-700 text-xs">{edu.institution}</p>
                  {(edu.grade || edu.gpa) && (
                    <p className="text-gray-600 text-xs">GPA: {edu.grade || edu.gpa}</p>
                  )}
                </div>
                {(edu.start_date || edu.end_date || edu.graduation_date) && (
                  <span className="text-xs text-gray-600 italic">
                    {edu.graduation_date || `${edu.start_date || ''} - ${edu.end_date || ''}`}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </motion.div>
  )
}
