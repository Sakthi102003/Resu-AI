# Template Examples and Documentation

## Available Resume Templates

ResuAI now offers 7 professional resume templates, each optimized for different use cases and industries:

### 1. **Auto CV** (`auto_cv`)
- **Style**: Modern, automated, ATS-friendly
- **Best For**: General applications, ATS systems, corporate roles
- **Features**:
  - Clean, professional layout
  - Skills-first approach
  - Automatic section ordering
  - High ATS compatibility

### 2. **Anti CV** (`anti_cv`)
- **Style**: Unconventional, creative, story-driven
- **Best For**: Creative roles, startups, unique positions
- **Features**:
  - Narrative format
  - Personal voice and personality
  - Visual hierarchy without formality
  - Achievements over duties

### 3. **Ethan's Resume** (`ethan`)
- **Style**: Clean, professional, two-column layout
- **Best For**: Business professionals, consultants, managers
- **Features**:
  - Two-column design for space utilization
  - Modern typography
  - Clear visual hierarchy
  - Professional appearance

### 4. **RenderCV Classic** (`rendercv_classic`)
- **Style**: Academic, traditional, LaTeX-inspired
- **Best For**: Academic positions, research roles, faculty
- **Features**:
  - Traditional academic style
  - Serif fonts
  - Formal structure
  - Publications support

### 5. **RenderCV EngineeringResume** (`rendercv_engineering`)
- **Style**: Technical, data-driven, results-focused
- **Best For**: Engineering, technical roles, STEM fields
- **Features**:
  - Metrics-driven accomplishments
  - Skills-first approach
  - Clean, scannable layout
  - Technical emphasis

### 6. **RenderCV sb2nov** (`rendercv_sb2nov`)
- **Style**: Compact, information-dense, GitHub style
- **Best For**: Software engineers, developers, tech startups
- **Features**:
  - Single-page optimization
  - Maximum content in minimal space
  - Popular GitHub template style
  - Clear section separation

### 7. **Yuan's Resume** (`yuan`)
- **Style**: Minimalist, elegant, sophisticated
- **Best For**: Executive positions, senior roles, consulting
- **Features**:
  - Minimalist design philosophy
  - Elegant typography
  - Sophisticated color accents
  - Whitespace optimization

## Usage

### API Endpoint

#### List All Templates
```bash
GET /templates/
```

Response:
```json
[
  {
    "id": "auto_cv",
    "name": "Auto CV",
    "description": "Modern, automated, ATS-friendly template",
    "best_for": "General applications, ATS systems"
  },
  ...
]
```

#### Get Template Info
```bash
GET /templates/{template_id}
```

#### Preview Template
```bash
POST /templates/{template_id}/preview
Content-Type: application/json

{
  "resume_data": { ... },
  "theme_color": "#3B82F6"
}
```

### Python Usage

```python
from templates.template_manager import TemplateManager

# List templates
templates = TemplateManager.list_templates()

# Generate resume with template
pdf_buffer = TemplateManager.generate_resume(
    resume_data=your_resume_data,
    template_name="auto_cv",
    theme_color="#3B82F6"
)

# Get template info
info = TemplateManager.get_template_info("rendercv_engineering")
```

### Frontend Integration

```javascript
// Fetch available templates
const templates = await fetch('/templates/').then(r => r.json());

// Generate resume with selected template
const response = await fetch('/resume/export/pdf', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    resume_id: 'your-resume-id',
    template: 'yuan',  // Selected template
    theme_color: '#3B82F6'
  })
});

const blob = await response.blob();
const url = URL.createObjectURL(blob);
window.open(url);
```

## Customization

Each template supports theme color customization. Pass a hex color code:

```python
pdf_buffer = TemplateManager.generate_resume(
    resume_data=data,
    template_name="ethan",
    theme_color="#FF6B6B"  # Custom color
)
```

## Template Selection Guide

| Role Type | Recommended Template | Alternative |
|-----------|---------------------|-------------|
| Software Engineer | `rendercv_sb2nov` | `rendercv_engineering` |
| Data Scientist | `rendercv_engineering` | `auto_cv` |
| Product Manager | `ethan` | `auto_cv` |
| Creative Director | `anti_cv` | `yuan` |
| Academic/Researcher | `rendercv_classic` | `yuan` |
| Executive/C-Level | `yuan` | `ethan` |
| Entry Level | `auto_cv` | `ethan` |
| Startup Founder | `anti_cv` | `yuan` |

## Migration from Old System

If you're using the old `pdf_generator.py`, update your code:

### Old Way:
```python
from utils.pdf_generator import generate_pdf_resume

pdf = generate_pdf_resume(data, template="modern")
```

### New Way:
```python
from templates.template_manager import TemplateManager

pdf = TemplateManager.generate_resume(data, template_name="auto_cv")
```

## Adding Custom Templates

To add a new template:

1. Create a new file in `Backend/templates/` (e.g., `my_template.py`)
2. Extend `BaseTemplate` class
3. Implement `generate()` method
4. Add to `TEMPLATES` dict in `template_manager.py`

Example:
```python
from .base_template import BaseTemplate

class MyTemplate(BaseTemplate):
    def generate(self, resume_data):
        doc = self.create_doc()
        elements = []
        # Your template logic
        doc.build(elements)
        self.buffer.seek(0)
        return self.buffer
```

## Testing

Test template generation:
```bash
# From Backend directory
python -c "
from templates.template_manager import TemplateManager
templates = TemplateManager.list_templates()
for t in templates:
    print(f\"{t['id']}: {t['name']}\")
"
```
