import { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  ArrowLeft,
  Download,
  Save,
  Play,
  FileCode,
  Sparkles,
  Award,
  Briefcase,
} from 'lucide-react';
import toast from 'react-hot-toast';
import { resumeAPI, templateAPI, aiAPI } from '../Services/api';
import ResumeScoreCard from '../components/ResumeScoreCard';
import JobRecommendation from '../components/jobRecommendation';

export default function LatexEditor() {
  const { resumeId } = useParams();
  const navigate = useNavigate();
  const isNew = resumeId === 'new';

  const [isSaving, setIsSaving] = useState(false);
  const [isCompiling, setIsCompiling] = useState(false);
  const [showScore, setShowScore] = useState(false);
  const [showJobs, setShowJobs] = useState(false);
  const [atsScore, setAtsScore] = useState(null);
  const [jobRecommendations, setJobRecommendations] = useState([]);
  const [currentResumeId, setCurrentResumeId] = useState(isNew ? null : resumeId);
  const [selectedTemplate, setSelectedTemplate] = useState('auto_cv');
  const [selectedColor, setSelectedColor] = useState('#3B82F6');
  const [pdfPreview, setPdfPreview] = useState(null);

  const [resumeTitle, setResumeTitle] = useState('My Resume');
  const [latexContent, setLatexContent] = useState('');
  const textareaRef = useRef(null);

  // Generate default LaTeX template based on selected template
  const getDefaultLatexTemplate = () => {
    // This returns a simplified JSON-compatible format
    // The actual LaTeX compilation uses the real template files
    return `% Resume Data in LaTeX-style format
% Edit the content below - it will be automatically converted to JSON

\\name{Your Full Name}
\\email{your.email@example.com}
\\phone{+1-234-567-8900}
\\location{City, State, Country}
\\linkedin{linkedin.com/in/yourprofile}
\\github{github.com/yourusername}
\\website{yourwebsite.com}

\\summary{
  Results-driven professional with X+ years of experience in [your field]. 
  Proven expertise in [key skills] with a track record of [achievements]. 
  Passionate about [your interests] and committed to delivering high-quality solutions.
}

\\experience{
  \\item{
    \\position{Senior Software Engineer}
    \\company{Tech Company Inc}
    \\dates{Jan 2022 -- Present}
    \\location{San Francisco, CA}
    \\description{
      • Led development of microservices architecture serving 1M+ daily users
      • Mentored team of 5 junior developers, improving code quality by 40%
      • Implemented CI/CD pipeline reducing deployment time from 2hrs to 15min
      • Collaborated with product team to define technical requirements
    }
  }
  \\item{
    \\position{Software Engineer}
    \\company{Startup Solutions}
    \\dates{Jun 2020 -- Dec 2021}
    \\location{New York, NY}
    \\description{
      • Built RESTful APIs using Python/Django and Node.js
      • Designed and implemented database schemas for scalability
      • Integrated third-party payment systems (Stripe, PayPal)
      • Reduced API response time by 60% through optimization
    }
  }
  \\item{
    \\position{Junior Developer}
    \\company{Digital Agency}
    \\dates{Jul 2018 -- May 2020}
    \\location{Austin, TX}
    \\description{
      • Developed responsive web applications using React and Vue.js
      • Fixed bugs and implemented new features based on client feedback
      • Participated in agile development process and daily standups
    }
  }
}

\\education{
  \\item{
    \\degree{Master of Science in Computer Science}
    \\institution{Stanford University}
    \\dates{2016 -- 2018}
    \\location{Stanford, CA}
    \\gpa{3.9/4.0}
    \\coursework{Machine Learning, Distributed Systems, Algorithms}
  }
  \\item{
    \\degree{Bachelor of Science in Computer Science}
    \\institution{University of California, Berkeley}
    \\dates{2012 -- 2016}
    \\location{Berkeley, CA}
    \\gpa{3.7/4.0}
    \\honors{Dean's List, Cum Laude}
  }
}

\\skills{
  \\category{Languages}{Python, JavaScript, TypeScript, Java, C++, SQL, Go}
  \\category{Frontend}{React, Vue.js, Angular, HTML5, CSS3, Tailwind CSS}
  \\category{Backend}{Node.js, Django, FastAPI, Express, Spring Boot}
  \\category{Databases}{PostgreSQL, MongoDB, Redis, MySQL, DynamoDB}
  \\category{DevOps}{Docker, Kubernetes, AWS, GCP, Jenkins, GitHub Actions}
  \\category{Tools}{Git, VS Code, Postman, Figma, Jira, Slack}
}

\\projects{
  \\item{
    \\title{E-Commerce Platform}
    \\dates{2023}
    \\description{Full-stack marketplace with real-time inventory management and payment processing}
    \\tech{React, Node.js, PostgreSQL, Stripe API, AWS}
    \\url{github.com/yourusername/ecommerce-platform}
    \\highlights{• Handles 10K+ transactions/month • 99.9% uptime}
  }
  \\item{
    \\title{AI-Powered Chat Application}
    \\dates{2023}
    \\description{Real-time chat app with AI-powered message suggestions and sentiment analysis}
    \\tech{React, FastAPI, OpenAI API, WebSocket, MongoDB}
    \\url{github.com/yourusername/ai-chat}
    \\highlights{• 5K+ active users • Real-time message processing}
  }
  \\item{
    \\title{Portfolio Analytics Dashboard}
    \\dates{2022}
    \\description{Interactive dashboard for tracking investment portfolio performance}
    \\tech{Vue.js, Python, D3.js, PostgreSQL}
    \\url{yourwebsite.com/portfolio}
    \\highlights{• Real-time data visualization • Custom analytics engine}
  }
}

\\certifications{
  \\item{AWS Certified Solutions Architect - Associate}{Amazon Web Services}{2023}
  \\item{Professional Scrum Master I (PSM I)}{Scrum.org}{2023}
  \\item{MongoDB Certified Developer}{MongoDB University}{2022}
}

% Optional sections - uncomment to use:
%
% \\awards{
%   \\item{Best Innovation Award}{Company Hackathon 2023}{For developing AI-powered tool}
%   \\item{Dean's List}{University Name}{All 4 years}
% }
%
% \\publications{
%   \\item{Title of Paper}{Conference/Journal Name}{2023}{Co-author}{DOI or URL}
% }
%
% \\languages{
%   \\item{English}{Native}
%   \\item{Spanish}{Professional Working Proficiency}
%   \\item{French}{Elementary Proficiency}
% }
`;
  };

  useEffect(() => {
    if (!isNew && resumeId) {
      loadResume();
    } else if (isNew) {
      // Set default sample content for new resumes
      setLatexContent(getDefaultLatexTemplate());
    }
  }, [resumeId, isNew]);

  const loadResume = async () => {
    try {
      const response = await resumeAPI.getById(resumeId);
      setResumeTitle(response.data.title || 'My Resume');
      setSelectedTemplate(response.data.template || 'auto_cv');
      setSelectedColor(response.data.theme_color || '#3B82F6');
      
      console.log('Resume loaded:', response.data);
      
      // Convert JSON resume data to LaTeX format
      const latexCode = jsonToLatex(response.data.data);
      setLatexContent(latexCode);
    } catch (error) {
      console.error('Load resume error:', error);
      toast.error('Failed to load resume');
      navigate('/dashboard');
    }
  };

  const jsonToLatex = (data) => {
    let latex = '% Resume Data in LaTeX-style format\n\n';

    // Personal Info
    if (data.personal_info) {
      const info = data.personal_info;
      if (info.name) latex += `\\name{${info.name}}\n`;
      if (info.email) latex += `\\email{${info.email}}\n`;
      if (info.phone) latex += `\\phone{${info.phone}}\n`;
      if (info.location) latex += `\\location{${info.location}}\n`;
      if (info.linkedin) latex += `\\linkedin{${info.linkedin}}\n`;
      if (info.github) latex += `\\github{${info.github}}\n`;
      if (info.website) latex += `\\website{${info.website}}\n`;
      latex += '\n';
    }

    // Summary
    if (data.summary) {
      latex += `\\summary{\n  ${data.summary}\n}\n\n`;
    }

    // Experience
    if (data.experience && data.experience.length > 0) {
      latex += '\\experience{\n';
      data.experience.forEach(exp => {
        latex += '  \\item{\n';
        latex += `    \\position{${exp.position || 'Position'}}\n`;
        latex += `    \\company{${exp.company || 'Company'}}\n`;
        latex += `    \\dates{${exp.start_date || ''} -- ${exp.end_date || 'Present'}}\n`;
        if (exp.location) latex += `    \\location{${exp.location}}\n`;
        if (exp.description) {
          const desc = Array.isArray(exp.description) 
            ? exp.description.map(d => `      • ${d}`).join('\n')
            : `      ${exp.description}`;
          latex += `    \\description{\n${desc}\n    }\n`;
        }
        latex += '  }\n';
      });
      latex += '}\n\n';
    }

    // Education
    if (data.education && data.education.length > 0) {
      latex += '\\education{\n';
      data.education.forEach(edu => {
        latex += '  \\item{\n';
        const degree = edu.degree || 'Degree';
        const field = edu.field_of_study || edu.field || '';
        latex += `    \\degree{${degree}${field ? ' in ' + field : ''}}\n`;
        latex += `    \\institution{${edu.institution || 'Institution'}}\n`;
        latex += `    \\dates{${edu.start_date || ''} -- ${edu.end_date || edu.graduation_date || ''}}\n`;
        if (edu.gpa || edu.grade) latex += `    \\gpa{${edu.gpa || edu.grade}}\n`;
        latex += '  }\n';
      });
      latex += '}\n\n';
    }

    // Skills
    if (data.skills && data.skills.length > 0) {
      latex += '\\skills{\n';
      data.skills.forEach(skill => {
        if (typeof skill === 'object' && skill.category) {
          latex += `  \\category{${skill.category}}{${skill.items.join(', ')}}\n`;
        } else {
          latex += `  ${skill}\n`;
        }
      });
      latex += '}\n\n';
    }

    // Projects
    if (data.projects && data.projects.length > 0) {
      latex += '\\projects{\n';
      data.projects.forEach(proj => {
        latex += '  \\item{\n';
        latex += `    \\title{${proj.name}}\n`;
        if (proj.description) latex += `    \\description{${proj.description}}\n`;
        if (proj.technologies) latex += `    \\tech{${proj.technologies.join(', ')}}\n`;
        if (proj.url) latex += `    \\url{${proj.url}}\n`;
        latex += '  }\n';
      });
      latex += '}\n\n';
    }

    // Certifications
    if (data.certifications && data.certifications.length > 0) {
      latex += '\\certifications{\n';
      data.certifications.forEach(cert => {
        latex += `  \\item{${cert.name}}{${cert.issuer}}{${cert.date || ''}}\n`;
      });
      latex += '}\n';
    }

    return latex;
  };

  const latexToJson = (latexCode) => {
    const data = {
      personal_info: {},
      summary: '',
      experience: [],
      education: [],
      skills: [],
      projects: [],
      certifications: [],
    };

    // Extract personal info
    const nameMatch = latexCode.match(/\\name\s*\{([^}]+)\}/);
    if (nameMatch) data.personal_info.name = nameMatch[1];

    const emailMatch = latexCode.match(/\\email\s*\{([^}]+)\}/);
    if (emailMatch) data.personal_info.email = emailMatch[1];

    const phoneMatch = latexCode.match(/\\phone\s*\{([^}]+)\}/);
    if (phoneMatch) data.personal_info.phone = phoneMatch[1];

    const locationMatch = latexCode.match(/\\location\s*\{([^}]+)\}/);
    if (locationMatch) data.personal_info.location = locationMatch[1];

    const linkedinMatch = latexCode.match(/\\linkedin\s*\{([^}]+)\}/);
    if (linkedinMatch) data.personal_info.linkedin = linkedinMatch[1];

    const githubMatch = latexCode.match(/\\github\s*\{([^}]+)\}/);
    if (githubMatch) data.personal_info.github = githubMatch[1];

    const websiteMatch = latexCode.match(/\\website\s*\{([^}]+)\}/);
    if (websiteMatch) data.personal_info.website = websiteMatch[1];

    // Extract summary
    const summaryMatch = latexCode.match(/\\summary\{([^}]+)\}/s);
    if (summaryMatch) data.summary = summaryMatch[1].trim();

    // Extract experience
    const experienceMatch = latexCode.match(/\\experience\{([\s\S]*?)\n\}/);
    if (experienceMatch) {
      const expContent = experienceMatch[1];
      const items = expContent.split('\\item{');
      items.slice(1).forEach(item => {
        const exp = {};
        const posMatch = item.match(/\\position\{([^}]+)\}/);
        if (posMatch) exp.position = posMatch[1];
        const compMatch = item.match(/\\company\{([^}]+)\}/);
        if (compMatch) exp.company = compMatch[1];
        const datesMatch = item.match(/\\dates\{([^}]+)\}/);
        if (datesMatch) {
          const dates = datesMatch[1].split('--');
          exp.start_date = dates[0]?.trim();
          exp.end_date = dates[1]?.trim();
        }
        const locMatch = item.match(/\\location\{([^}]+)\}/);
        if (locMatch) exp.location = locMatch[1];
        const descMatch = item.match(/\\description\{([\s\S]*?)\n\s+\}/);
        if (descMatch) {
          const desc = descMatch[1].trim();
          exp.description = desc.split('\n').map(line => line.trim().replace(/^•\s*/, '')).filter(Boolean);
        }
        data.experience.push(exp);
      });
    }

    // Extract education
    const educationMatch = latexCode.match(/\\education\{([\s\S]*?)\n\}/);
    if (educationMatch) {
      const eduContent = educationMatch[1];
      const items = eduContent.split('\\item{');
      items.slice(1).forEach(item => {
        const edu = {};
        const degMatch = item.match(/\\degree\{([^}]+)\}/);
        if (degMatch) {
          const degParts = degMatch[1].split(' in ');
          edu.degree = degParts[0];
          if (degParts[1]) edu.field_of_study = degParts[1];
        }
        const instMatch = item.match(/\\institution\{([^}]+)\}/);
        if (instMatch) edu.institution = instMatch[1];
        const datesMatch = item.match(/\\dates\{([^}]+)\}/);
        if (datesMatch) {
          const dates = datesMatch[1].split('--');
          edu.start_date = dates[0]?.trim();
          edu.graduation_date = dates[1]?.trim();
        }
        const gpaMatch = item.match(/\\gpa\{([^}]+)\}/);
        if (gpaMatch) edu.gpa = gpaMatch[1];
        data.education.push(edu);
      });
    }

    // Extract skills
    const skillsMatch = latexCode.match(/\\skills\{([\s\S]*?)\n\}/);
    if (skillsMatch) {
      const skillContent = skillsMatch[1];
      const categories = skillContent.matchAll(/\\category\{([^}]+)\}\{([^}]+)\}/g);
      for (const match of categories) {
        data.skills.push({
          category: match[1],
          items: match[2].split(',').map(s => s.trim()),
        });
      }
    }

    // Extract projects
    const projectsMatch = latexCode.match(/\\projects\{([\s\S]*?)\n\}/);
    if (projectsMatch) {
      const projContent = projectsMatch[1];
      const items = projContent.split('\\item{');
      items.slice(1).forEach(item => {
        const proj = {};
        const titleMatch = item.match(/\\title\{([^}]+)\}/);
        if (titleMatch) proj.name = titleMatch[1];
        const descMatch = item.match(/\\description\{([^}]+)\}/);
        if (descMatch) proj.description = descMatch[1];
        const techMatch = item.match(/\\tech\{([^}]+)\}/);
        if (techMatch) proj.technologies = techMatch[1].split(',').map(t => t.trim());
        const urlMatch = item.match(/\\url\{([^}]+)\}/);
        if (urlMatch) proj.url = urlMatch[1];
        data.projects.push(proj);
      });
    }

    // Extract certifications
    const certsMatch = latexCode.match(/\\certifications\{([\s\S]*?)\n\}/);
    if (certsMatch) {
      const certContent = certsMatch[1];
      const items = certContent.matchAll(/\\item\{([^}]+)\}\{([^}]+)\}\{([^}]*)\}/g);
      for (const match of items) {
        data.certifications.push({
          name: match[1],
          issuer: match[2],
          date: match[3],
        });
      }
    }

    return data;
  };

  const handleSave = async () => {
    setIsSaving(true);
    try {
      // Convert LaTeX to JSON
      const resumeData = latexToJson(latexContent);

      const payload = {
        title: resumeTitle,
        data: resumeData,
      };

      if (isNew || !currentResumeId) {
        const response = await resumeAPI.create(payload);
        setCurrentResumeId(response.data.id);
        toast.success('Resume created successfully!');
        navigate(`/editor/latex/${response.data.id}`, { replace: true });
      } else {
        await resumeAPI.update(currentResumeId, payload);
        toast.success('Resume saved successfully!');
      }
    } catch (error) {
      console.error('Save error:', error);
      toast.error(error.response?.data?.message || 'Failed to save resume');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCompile = async () => {
    setIsCompiling(true);
    try {
      // Convert LaTeX to JSON first
      const resumeData = latexToJson(latexContent);
      
      console.log('Compiling with data:', resumeData);
      console.log('Template:', selectedTemplate);
      console.log('Color:', selectedColor);
      
      // Generate preview
      const response = await templateAPI.preview(selectedTemplate, resumeData, selectedColor);
      
      console.log('Preview response:', response);
      console.log('Response data type:', typeof response.data);
      console.log('Response data size:', response.data.size);
      
      // Verify we got a valid PDF blob
      if (!response.data || response.data.size === 0) {
        throw new Error('Received empty PDF response');
      }
      
      // Create blob URL for preview
      const blob = new Blob([response.data], { type: 'application/pdf' });
      console.log('Created blob:', blob);
      console.log('Blob size:', blob.size);
      console.log('Blob type:', blob.type);
      
      const url = URL.createObjectURL(blob);
      console.log('Created blob URL:', url);
      
      // Clean up old preview URL if exists
      if (pdfPreview) {
        URL.revokeObjectURL(pdfPreview);
      }
      
      setPdfPreview(url);
      toast.success('Compiled successfully!');
    } catch (error) {
      console.error('Compile error:', error);
      console.error('Error response:', error.response);
      toast.error(error.response?.data?.detail || error.message || 'Failed to compile preview');
    } finally {
      setIsCompiling(false);
    }
  };

  const handleExportPDF = async () => {
    if (!currentResumeId) {
      toast.error('Please save the resume first');
      return;
    }

    try {
      const response = await resumeAPI.exportPDF(currentResumeId, null);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${resumeTitle}.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      toast.success('PDF downloaded!');
    } catch (error) {
      toast.error('Failed to export PDF');
    }
  };

  const handleCalculateScore = async () => {
    if (!currentResumeId) {
      toast.error('Please save the resume first');
      return;
    }

    setShowScore(true);
    try {
      const response = await aiAPI.atsScore(currentResumeId);
      setAtsScore(response.data);
    } catch (error) {
      toast.error('Failed to calculate ATS score');
    }
  };

  const handleGetJobRecommendations = async () => {
    if (!currentResumeId) {
      toast.error('Please save the resume first');
      return;
    }

    setShowJobs(true);
    try {
      const response = await aiAPI.jobRecommendations(currentResumeId);
      setJobRecommendations(response.data);
    } catch (error) {
      toast.error('Failed to get job recommendations');
    }
  };

  // Insert tab character on Tab key
  const handleKeyDown = (e) => {
    if (e.key === 'Tab') {
      e.preventDefault();
      const start = e.target.selectionStart;
      const end = e.target.selectionEnd;
      const newContent = latexContent.substring(0, start) + '  ' + latexContent.substring(end);
      setLatexContent(newContent);
      setTimeout(() => {
        textareaRef.current.selectionStart = textareaRef.current.selectionEnd = start + 2;
      }, 0);
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200 px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 hover:bg-gray-100 rounded-lg transition"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <FileCode className="w-5 h-5 text-primary-600" />
            <input
              type="text"
              value={resumeTitle}
              onChange={(e) => setResumeTitle(e.target.value)}
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
          <div className="flex items-center gap-2">
            <button
              onClick={() => navigate('/')}
              className="hidden lg:flex items-center gap-2 px-3 py-2 text-lg font-bold text-gray-900 hover:text-primary-600 transition-colors"
            >
              <Sparkles className="w-5 h-5" />
              ResuAI
            </button>
            <button
              onClick={handleCompile}
              disabled={isCompiling}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition disabled:opacity-50"
            >
              <Play className="w-4 h-4" />
              <span className="hidden sm:inline">
                {isCompiling ? 'Compiling...' : 'Compile'}
              </span>
            </button>
            <button
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
              onClick={handleCalculateScore}
              className="flex items-center gap-2 px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 transition"
            >
              <Award className="w-4 h-4" />
              <span className="hidden sm:inline">ATS Score</span>
            </button>
            <button
              onClick={handleGetJobRecommendations}
              className="flex items-center gap-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition"
            >
              <Briefcase className="w-4 h-4" />
              <span className="hidden sm:inline">Jobs</span>
            </button>
            <button
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
        {/* LaTeX Editor */}
        <div className="w-1/2 flex flex-col bg-gray-900">
          <div className="p-3 bg-gray-800 border-b border-gray-700 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="text-sm font-semibold text-gray-300">LaTeX Source Code</span>
              {selectedTemplate && (
                <div className="flex items-center gap-2 px-2 py-1 bg-gray-700 rounded">
                  <div 
                    className="w-2 h-2 rounded-full" 
                    style={{ backgroundColor: selectedColor }}
                  />
                  <span className="text-xs text-gray-300">
                    Template: {selectedTemplate.replace(/_/g, ' ').toUpperCase()}
                  </span>
                </div>
              )}
            </div>
            <span className="text-xs text-gray-400">Press Tab for indentation</span>
          </div>
          <textarea
            ref={textareaRef}
            value={latexContent}
            onChange={(e) => setLatexContent(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 p-4 bg-gray-900 text-green-400 font-mono text-sm resize-none outline-none"
            style={{ 
              tabSize: 2,
              lineHeight: '1.6',
              fontFamily: 'Monaco, Consolas, "Courier New", monospace'
            }}
            spellCheck={false}
          />
        </div>

        {/* PDF Preview */}
        <div className="w-1/2 border-l border-gray-200 bg-white overflow-hidden flex flex-col">
          <div className="p-4 bg-white border-b border-gray-200">
            <h3 className="text-lg font-semibold">PDF Preview</h3>
            <p className="text-xs text-gray-500 mt-1">Click "Compile" to generate preview</p>
          </div>
          <div className="flex-1 overflow-auto bg-gray-100">
            {pdfPreview ? (
              <iframe
                src={`${pdfPreview}#toolbar=0`}
                className="w-full h-full border-0"
                title="Resume Preview"
                style={{ minHeight: '600px' }}
              />
            ) : (
              <div className="h-full flex items-center justify-center text-gray-400">
                <div className="text-center">
                  <FileCode className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>No preview yet</p>
                  <p className="text-sm mt-2">Click "Compile" to generate PDF</p>
                </div>
              </div>
            )}
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
  );
}
