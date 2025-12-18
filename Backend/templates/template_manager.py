"""Template Manager - Centralized template selection and generation"""

from io import BytesIO
from typing import Dict, Any
from .latex_template_processor import LaTeXTemplateProcessor
from .yuan_template import YuanTemplate  # Fallback for yuan
from .rendercv_classic import RenderCVClassicTemplate  # Python-based fallback


class TemplateManager:
    """Manages all resume templates"""
    
    TEMPLATES = {
        'auto_cv': {
            'name': 'Auto CV',
            'description': 'Modern, automated, ATS-friendly template with clean design',
            'best_for': 'General applications, ATS systems',
            'icon': '🤖',
            'category': 'Modern',
            'ats_friendly': True,
            'preview_image': '/templates/auto_cv.png'
        },
        'anti_cv': {
            'name': 'Anti CV',
            'description': 'Unconventional, creative, story-driven format that stands out',
            'best_for': 'Creative roles, startups, unique positions',
            'icon': '🎨',
            'category': 'Creative',
            'ats_friendly': False,
            'preview_image': '/templates/anti_cv.png'
        },
        'ethan': {
            'name': 'Ethan\'s Resume',
            'description': 'Clean, professional, two-column layout for business settings',
            'best_for': 'Business professionals, consultants',
            'icon': '💼',
            'category': 'Professional',
            'ats_friendly': True,
            'preview_image': '/templates/ethan.png'
        },
        'rendercv_classic': {
            'name': 'RenderCV Classic',
            'description': 'Academic, traditional, LaTeX-inspired professional format',
            'best_for': 'Academic positions, research roles',
            'icon': '🎓',
            'category': 'Academic',
            'ats_friendly': True,
            'preview_image': '/templates/rendercv_classic.png',
            'fallback_class': RenderCVClassicTemplate
        },
        'yuan': {
            'name': 'Yuan\'s Resume',
            'description': 'Minimalist, elegant, sophisticated design for executives',
            'best_for': 'Executive positions, senior roles',
            'icon': '✨',
            'category': 'Executive',
            'ats_friendly': True,
            'preview_image': '/templates/yuan.png',
        },
    }
    
    @classmethod
    def generate_resume(cls, resume_data: Dict[str, Any], template_name: str = "auto_cv", 
                       theme_color: str = "#3B82F6") -> BytesIO:
        """Generate a resume using the specified template"""
        import logging
        logger = logging.getLogger(__name__)
        
        # Check if template has a fallback class (for templates without .tex files)
        template_info = cls.TEMPLATES.get(template_name, cls.TEMPLATES['auto_cv'])
        if 'fallback_class' in template_info:
            logger.info(f"Using Python-based fallback template for {template_name}")
            template_class = template_info['fallback_class']
            template = template_class(theme_color=theme_color)
            return template.generate(resume_data)
        
        # Use LaTeX template processor for templates with .tex files
        logger.info(f"Attempting LaTeX compilation for {template_name}")
        return LaTeXTemplateProcessor.generate(resume_data, template_name, theme_color)
    
    @classmethod
    def list_templates(cls) -> list:
        """List all available templates"""
        return [
            {
                'id': key,
                'name': value['name'],
                'description': value['description'],
                'best_for': value['best_for'],
                'icon': value.get('icon', '📄'),
                'category': value.get('category', 'General'),
                'ats_friendly': value.get('ats_friendly', True),
                'preview_image': value.get('preview_image', f'/templates/{key}.png')
            }
            for key, value in cls.TEMPLATES.items()
        ]
    
    @classmethod
    def get_template_info(cls, template_name: str) -> Dict[str, str]:
        """Get information about a specific template"""
        template_info = cls.TEMPLATES.get(template_name, cls.TEMPLATES['auto_cv'])
        return {
            'name': template_info['name'],
            'description': template_info['description'],
            'best_for': template_info['best_for']
        }


def generate_resume_pdf(resume_data: Dict[str, Any], template: str = "auto_cv", 
                       theme_color: str = "#3B82F6") -> BytesIO:
    """Main function to generate PDF resume with template"""
    return TemplateManager.generate_resume(resume_data, template, theme_color)
