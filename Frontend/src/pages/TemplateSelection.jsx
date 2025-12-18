import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, ArrowRight, Palette, Check } from 'lucide-react';
import toast from 'react-hot-toast';
import { templateAPI, resumeAPI } from '../Services/api';
import { useAuthStore } from '../Services/auth';
import { getSampleResumeData } from '../utils/sampleData';

export default function TemplateSelection() {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState('auto_cv');
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await templateAPI.getAll();
      setTemplates(response.data);
    } catch (error) {
      console.error('Failed to fetch templates:', error);
      toast.error('Failed to load templates');
    } finally {
      setLoading(false);
    }
  };

  const handleContinue = async () => {
    setCreating(true);
    try {
      // Get sample data for the selected template
      const sampleData = getSampleResumeData(selectedTemplate);
      
      // Merge user's basic info with sample data
      const resumeData = {
        ...sampleData,
        personal_info: {
          ...sampleData.personal_info,
          name: user?.full_name || sampleData.personal_info.name,
          email: user?.email || sampleData.personal_info.email,
          phone: user?.phone || sampleData.personal_info.phone,
        },
      };

      // Create resume with selected template, color, and sample data
      const response = await resumeAPI.create({
        title: `Resume ${new Date().toLocaleDateString()}`,
        template: selectedTemplate,
        theme_color: '#3B82F6',
        data: resumeData,
      });
      
      toast.success('Template selected! Now build your resume.');
      // Navigate to latex editor with the new resume
      navigate(`/editor/latex/${response.data.id}`);
    } catch (error) {
      console.error('Failed to create resume:', error);
      toast.error('Failed to create resume');
      setCreating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-200 border-t-primary-600 mx-auto mb-3"></div>
          <p className="text-gray-600">Loading templates...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-purple-50 to-pink-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Dashboard</span>
            </button>
            <h1 className="text-2xl font-bold text-gray-900">Choose Your Template & Theme</h1>
            <div className="w-32" /> {/* Spacer for centering */}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Step Indicator */}
        <div className="mb-12">
          <div className="flex items-center justify-center gap-4">
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-full bg-primary-600 text-white flex items-center justify-center font-bold">
                1
              </div>
              <span className="font-semibold text-gray-900">Select Template</span>
            </div>
            <div className="w-16 h-1 bg-gray-300"></div>
            <div className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-full bg-gray-300 text-gray-600 flex items-center justify-center font-bold">
                2
              </div>
              <span className="font-semibold text-gray-600">Edit Resume</span>
            </div>
          </div>
        </div>

        {/* Templates Section */}
        <section className="mb-12">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">Select a Resume Template</h2>
            <p className="text-gray-600">Choose a professional template that fits your style</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {templates.map((template, index) => (
              <motion.div
                key={template.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                onClick={() => setSelectedTemplate(template.id)}
                className={`relative cursor-pointer rounded-xl border-4 transition-all transform hover:scale-[1.02] overflow-hidden ${
                  selectedTemplate === template.id
                    ? 'border-primary-600 bg-white shadow-2xl ring-4 ring-primary-200'
                    : 'border-gray-200 bg-white hover:border-primary-300 hover:shadow-lg'
                }`}
              >
                {/* Selected Badge */}
                {selectedTemplate === template.id && (
                  <div className="absolute top-3 right-3 z-10">
                    <div className="w-10 h-10 rounded-full bg-primary-600 flex items-center justify-center shadow-lg">
                      <Check className="w-5 h-5 text-white" />
                    </div>
                  </div>
                )}

                {/* Template Preview Image */}
                <div className="relative bg-gray-100 overflow-hidden" style={{ height: '280px' }}>
                  <img
                    src={`/templates/${template.id}.png`}
                    alt={`${template.name} preview`}
                    className="w-full h-full object-cover object-top"
                    onError={(e) => {
                      // Fallback to icon if image not found
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                  {/* Fallback Icon (hidden by default) */}
                  <div 
                    className="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100"
                    style={{ display: 'none' }}
                  >
                    <span className="text-8xl">{template.icon || '📄'}</span>
                  </div>
                  
                  {/* Hover Overlay */}
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent opacity-0 hover:opacity-100 transition-opacity flex items-end justify-center pb-4">
                    <span className="text-white font-semibold text-sm">Click to Select</span>
                  </div>
                </div>

                {/* Template Info */}
                <div className="p-5">
                  <h3 className="font-bold text-lg text-gray-900 mb-2 flex items-center gap-2">
                    <span className="text-xl">{template.icon || '📄'}</span>
                    {template.name}
                  </h3>
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {template.description}
                  </p>
                  <div className="flex flex-wrap gap-2">
                    <span className="text-xs px-3 py-1 bg-primary-100 rounded-full text-primary-700 font-medium">
                      {template.category}
                    </span>
                    {template.ats_friendly && (
                      <span className="text-xs px-3 py-1 bg-green-100 text-green-700 rounded-full font-medium">
                        ✓ ATS
                      </span>
                    )}
                  </div>
                  <p className="text-xs text-gray-500 mt-3">
                    <span className="font-medium">Best for:</span> {template.best_for}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </section>

        {/* Current Selection Summary */}
        <div className="bg-white rounded-2xl shadow-xl border-2 border-primary-200 p-8 max-w-3xl mx-auto mb-8">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-xl font-bold text-gray-900">Your Selection</h3>
            <Palette className="w-6 h-6 text-primary-600" />
          </div>
          <div className="grid md:grid-cols-1 gap-6">
            <div className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
              <span className="text-4xl">
                {templates.find((t) => t.id === selectedTemplate)?.icon || '📄'}
              </span>
              <div>
                <div className="text-xs text-gray-500 uppercase font-semibold mb-1">Template</div>
                <div className="font-bold text-gray-900">
                  {templates.find((t) => t.id === selectedTemplate)?.name || 'Auto CV'}
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="text-center">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleContinue}
            disabled={creating}
            className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white text-lg font-bold rounded-xl shadow-lg hover:shadow-2xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {creating ? (
              <>
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
                Creating Resume...
              </>
            ) : (
              <>
                Continue to Editor
                <ArrowRight className="w-6 h-6" />
              </>
            )}
          </motion.button>
          
        </div>
      </main>
    </div>
  );
}
