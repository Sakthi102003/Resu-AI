import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import api from '../Services/api';

export default function TemplateSelector({ onSelectTemplate, currentTemplate = 'auto_cv' }) {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(currentTemplate);
  const [loading, setLoading] = useState(true);
  const [showPreview, setShowPreview] = useState(false);

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await api.get('/templates/');
      setTemplates(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching templates:', error);
      setLoading(false);
    }
  };

  const handleSelectTemplate = (templateId) => {
    setSelectedTemplate(templateId);
    if (onSelectTemplate) {
      onSelectTemplate(templateId);
    }
  };

  const getTemplateIcon = (templateId) => {
    const icons = {
      auto_cv: '🤖',
      anti_cv: '🎨',
      ethan: '💼',
      rendercv_classic: '🎓',
      rendercv_engineering: '⚙️',
      rendercv_sb2nov: '💻',
      yuan: '✨'
    };
    return icons[templateId] || '📄';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Choose Template</h3>
        <span className="text-sm text-gray-500">{templates.length} templates</span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map((template) => (
          <motion.div
            key={template.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`
              relative cursor-pointer border-2 border-black p-4 transition-all
              ${selectedTemplate === template.id
                ? 'bg-brutal-yellow shadow-neo'
                : 'bg-white hover:bg-brutal-pink hover:shadow-neo-sm'
              }
            `}
            onClick={() => handleSelectTemplate(template.id)}
          >
            {/* Selected Badge */}
            {selectedTemplate === template.id && (
              <div className="absolute top-2 right-2">
                <span className="inline-flex items-center px-2 py-1 border-2 border-black text-xs font-bold bg-white text-black shadow-neo-sm">
                  ✓ SELECTED
                </span>
              </div>
            )}

            {/* Template Icon */}
            <div className="text-4xl mb-3">{getTemplateIcon(template.id)}</div>

            {/* Template Info */}
            <h4 className="font-bold text-black mb-1 uppercase tracking-wide">{template.name}</h4>
            <p className="text-sm text-black mb-2 font-mono">{template.description}</p>
            <p className="text-xs text-black border-t-2 border-black pt-2 mt-2">
              <span className="font-bold">BEST FOR:</span> {template.best_for}
            </p>
          </motion.div>
        ))}
      </div>

      {/* Template Details */}
      {selectedTemplate && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white border-2 border-black shadow-neo p-4"
        >
          <div className="flex items-start justify-between">
            <div>
              <h4 className="font-bold text-black mb-1 uppercase">
                {templates.find(t => t.id === selectedTemplate)?.name}
              </h4>
              <p className="text-sm text-black font-mono">
                {templates.find(t => t.id === selectedTemplate)?.description}
              </p>
            </div>
            <button
              onClick={() => setShowPreview(true)}
              className="text-sm px-4 py-2 bg-black text-white font-bold hover:bg-gray-800 transition-colors border-2 border-transparent hover:border-black"
            >
              PREVIEW
            </button>
          </div>
        </motion.div>
      )}
    </div>
  );
}
