# Resume Templates

This directory contains all resume template implementations for ResuAI.

## Architecture

```
templates/
├── __init__.py              # Package exports
├── base_template.py         # Base template class
├── template_manager.py      # Template manager and registry
├── auto_cv.py              # Auto CV template
├── anti_cv.py              # Anti CV template
├── ethan_template.py       # Ethan's template
├── rendercv_classic.py     # RenderCV Classic theme
├── rendercv_engineering.py # RenderCV Engineering theme
├── rendercv_sb2nov.py      # RenderCV sb2nov theme
└── yuan_template.py        # Yuan's template
```

## Base Template

All templates extend `BaseTemplate` which provides:
- Page size configuration
- Margin configuration
- PDF document creation
- Common utilities (hex_to_rgb)

## Creating a New Template

1. Create a new file: `my_template.py`

```python
from .base_template import BaseTemplate
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer
from typing import Dict, Any

class MyTemplate(BaseTemplate):
    """My custom template"""
    
    def _get_margins(self):
        """Override to customize margins (right, left, top, bottom)"""
        return (0.75, 0.75, 0.75, 0.75)
    
    def generate(self, resume_data: Dict[str, Any]):
        """Generate the resume PDF"""
        doc = self.create_doc()
        elements = []
        styles = self._create_styles()
        
        # Add your template logic here
        personal_info = resume_data.get('personal_info', {})
        if personal_info.get('name'):
            elements.append(Paragraph(personal_info['name'], styles['name']))
        
        # ... more template code ...
        
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
    
    def _create_styles(self):
        """Create custom styles for this template"""
        styles = {}
        styles['name'] = ParagraphStyle(
            'Name',
            fontName='Helvetica-Bold',
            fontSize=24,
            # ... more style properties
        )
        return styles
```

2. Register in `template_manager.py`:

```python
from .my_template import MyTemplate

class TemplateManager:
    TEMPLATES = {
        # ... existing templates ...
        'my_template': {
            'class': MyTemplate,
            'name': 'My Template',
            'description': 'Description of my template',
            'best_for': 'Who should use this template'
        }
    }
```

## Template Guidelines

### Structure
- Always start with personal info header
- Use consistent spacing (Spacer objects)
- Implement responsive layouts
- Consider single-page optimization

### Typography
- Use Helvetica for sans-serif
- Use Times for serif
- Keep font sizes between 8-24pt
- Maintain consistent leading (line spacing)

### Colors
- Use `self.theme_color` for branding
- Support hex color customization
- Use grayscale for secondary text
- Maintain good contrast ratios

### Layout
- Use Tables for alignment
- Apply proper margins/padding
- Consider printer margins
- Test with various content lengths

### Data Handling
- Check for optional fields
- Handle both list and string formats
- Provide fallbacks for missing data
- Support multiple data structures

## Testing Templates

```python
# Test individual template
from templates.auto_cv import AutoCVTemplate

template = AutoCVTemplate(theme_color="#3B82F6")
pdf = template.generate(sample_resume_data)

with open('test.pdf', 'wb') as f:
    f.write(pdf.getvalue())
```

```python
# Test through manager
from templates.template_manager import TemplateManager

pdf = TemplateManager.generate_resume(
    resume_data=sample_data,
    template_name='auto_cv',
    theme_color='#FF6B6B'
)
```

## Sample Resume Data Structure

```python
{
    "personal_info": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-234-567-8900",
        "location": "City, State",
        "linkedin": "linkedin.com/in/johndoe",
        "github": "github.com/johndoe",
        "website": "johndoe.com"
    },
    "summary": "Professional summary text...",
    "objective": "Career objective text...",
    "experience": [
        {
            "position": "Software Engineer",
            "company": "Tech Corp",
            "location": "San Francisco, CA",
            "start_date": "Jan 2020",
            "end_date": "Present",
            "current": True,
            "description": ["Achievement 1", "Achievement 2"],
            "achievements": ["Additional achievement"]
        }
    ],
    "education": [
        {
            "degree": "Bachelor of Science",
            "field_of_study": "Computer Science",
            "institution": "University Name",
            "location": "City, State",
            "graduation_date": "May 2019",
            "gpa": "3.8/4.0"
        }
    ],
    "skills": [
        {
            "category": "Languages",
            "items": ["Python", "JavaScript", "Go"]
        },
        {
            "category": "Frameworks",
            "items": ["React", "Django", "FastAPI"]
        }
    ],
    "projects": [
        {
            "name": "Project Name",
            "description": "Project description...",
            "technologies": ["Python", "React"],
            "url": "github.com/project"
        }
    ],
    "certifications": [
        {
            "name": "AWS Certified Solutions Architect",
            "issuer": "Amazon Web Services",
            "date": "2023"
        }
    ],
    "awards": ["Award 1", "Award 2"],
    "languages": ["English (Native)", "Spanish (Fluent)"]
}
```

## Best Practices

1. **Consistency**: Maintain visual consistency throughout
2. **Readability**: Prioritize clear, readable text
3. **ATS-Friendly**: Avoid complex graphics for ATS templates
4. **Mobile-Friendly**: Consider PDF rendering on mobile
5. **Print-Ready**: Test printing on physical paper
6. **Accessibility**: Ensure good contrast and font sizes
7. **Performance**: Optimize for fast generation
8. **Error Handling**: Handle missing or malformed data gracefully

## Maintenance

When updating templates:
- Test with various resume lengths
- Verify page breaks work correctly
- Check spacing consistency
- Test with different theme colors
- Validate with real resume data
- Test PDF viewer compatibility

## Resources

- ReportLab Documentation: https://www.reportlab.com/docs/reportlab-userguide.pdf
- LaTeX Resume Examples: https://www.overleaf.com/gallery/tagged/cv
- ATS Guidelines: https://www.jobscan.co/blog/ats-resume-template/
- Typography Best Practices: https://practicaltypography.com/
