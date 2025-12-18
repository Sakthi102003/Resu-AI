import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Check, Palette, FileText, X } from 'lucide-react';
import toast from 'react-hot-toast';
import { templateAPI } from '../Services/api';

export default function TemplatePanel({ selectedTemplate, onTemplateChange }) {
  const [templates, setTemplates] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [expandedSection, setExpandedSection] = useState('templates'); // 'templates' only
  const [isCollapsed, setIsCollapsed] = useState(false);

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
      setIsLoading(false);
    }
  };

  const handleTemplateSelect = (templateId) => {
    onTemplateChange(templateId);
    const templateName = templates.find(t => t.id === templateId)?.name;
    toast.success(`✨ Template: ${templateName}`, {
      icon: templates.find(t => t.id === templateId)?.icon,
    });
  };

  const toggleExpand = (section) => {
    if (expandedSection === section) {
      setExpandedSection(null);
    } else {
      setExpandedSection(section);
    }
  };

  if (isLoading) {
    return (
      <div className="h-full flex items-center justify-center bg-gradient-to-br from-primary-50 to-purple-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-200 border-t-primary-600 mx-auto mb-3"></div>
          <p className="text-sm text-gray-600">Loading templates...</p>
        </div>
      </div>
    );
  }

  if (isCollapsed) {
    return (
      <div className="h-full w-12 bg-gradient-to-b from-primary-600 to-purple-600 flex flex-col items-center py-4 gap-4">
        <button
          onClick={() => setIsCollapsed(false)}
          className="p-2 bg-white/20 hover:bg-white/30 rounded-lg transition text-white"
          title="Expand Panel"
        >
          <FileText className="w-5 h-5" />
        </button>
        <div className="flex-1" />
        <button
          className="p-2 bg-white/20 rounded-lg text-white"
          title="Templates"
        >
          <span className="text-xs">7</span>
        </button>
      </div>
    );
  }

  return (
    <div className="h-full w-80 flex flex-col bg-gradient-to-br from-white via-primary-50/30 to-purple-50/30 border-l-4 border-primary-500 shadow-2xl">
      {/* Header */}
      <div className="relative bg-gradient-to-r from-primary-600 to-purple-600 text-white p-6 shadow-lg">
        <button
          onClick={() => setIsCollapsed(true)}
          className="absolute top-4 right-4 p-1 hover:bg-white/20 rounded transition"
          title="Collapse Panel"
        >
          <X className="w-4 h-4" />
        </button>
        <div className="flex items-center gap-3 mb-2">
          <div className="p-2 bg-white/20 rounded-lg">
            <FileText className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold">Customize Resume</h2>
            <p className="text-xs text-primary-100">Choose your perfect style</p>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {/* Templates Section */}
        <div className="bg-white/80 backdrop-blur-sm m-3 rounded-xl shadow-lg overflow-hidden">
          <button
            onClick={() => toggleExpand('templates')}
            className="w-full px-4 py-4 flex items-center justify-between bg-gradient-to-r from-primary-500 to-primary-600 text-white hover:from-primary-600 hover:to-primary-700 transition"
          >
            <span className="font-bold text-base flex items-center gap-2">
              <FileText className="w-5 h-5" />
              Templates ({templates.length})
            </span>
            <motion.div
              animate={{ rotate: expandedSection === 'templates' ? 180 : 0 }}
              transition={{ duration: 0.3 }}
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </motion.div>
          </button>

          <AnimatePresence>
            {expandedSection === 'templates' && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                transition={{ duration: 0.3 }}
                className="px-3 py-3 space-y-2 max-h-[600px] overflow-y-auto"
              >
                {templates.map((template, index) => (
                  <motion.button
                    key={template.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    onClick={() => handleTemplateSelect(template.id)}
                    className={`w-full text-left p-3 rounded-lg border-2 transition-all transform hover:scale-[1.02] ${
                      selectedTemplate === template.id
                        ? 'border-primary-500 bg-gradient-to-r from-primary-50 to-purple-50 shadow-md'
                        : 'border-gray-200 hover:border-primary-300 bg-white hover:shadow-sm'
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <span className="text-2xl">{template.icon || '📄'}</span>
                          <span className="font-bold text-sm text-gray-900">
                            {template.name}
                          </span>
                        </div>
                        <p className="text-xs text-gray-600 leading-relaxed line-clamp-2">
                          {template.description}
                        </p>
                        <div className="flex items-center gap-1.5 mt-2 flex-wrap">
                          <span className="text-xs px-2 py-0.5 bg-primary-100 rounded-full text-primary-700 font-medium">
                            {template.category}
                          </span>
                          {template.ats_friendly && (
                            <span className="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full font-medium">
                              ✓ ATS
                            </span>
                          )}
                        </div>
                      </div>
                      {selectedTemplate === template.id && (
                        <div className="flex-shrink-0">
                          <div className="p-1 bg-primary-500 rounded-full">
                            <Check className="w-4 h-4 text-white" />
                          </div>
                        </div>
                      )}
                    </div>
                  </motion.button>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      {/* Footer with Current Selection */}
      <div className="p-4 bg-gradient-to-r from-gray-800 to-gray-900 text-white shadow-inner">
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <span className="text-xl">
              {templates.find((t) => t.id === selectedTemplate)?.icon || '📄'}
            </span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold truncate">
                {templates.find((t) => t.id === selectedTemplate)?.name || 'Auto CV'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
