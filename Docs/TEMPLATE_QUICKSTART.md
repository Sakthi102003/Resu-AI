# Resume Template System - Quick Reference

## Quick Start

### 1. List Available Templates

```bash
curl http://localhost:8000/templates/
```

### 2. Generate Resume with Template

```python
from templates.template_manager import TemplateManager

# Your resume data
resume_data = {
    "personal_info": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1-234-567-8900",
        "location": "San Francisco, CA",
        "linkedin": "linkedin.com/in/johndoe",
        "github": "github.com/johndoe"
    },
    "summary": "Experienced software engineer...",
    "experience": [...],
    "education": [...],
    "skills": [
        {"category": "Languages", "items": ["Python", "JavaScript", "Go"]},
        {"category": "Frameworks", "items": ["React", "FastAPI", "Django"]}
    ],
    "projects": [...]
}

# Generate with Auto CV template
pdf = TemplateManager.generate_resume(
    resume_data=resume_data,
    template_name="auto_cv",
    theme_color="#3B82F6"
)

# Save to file
with open("resume.pdf", "wb") as f:
    f.write(pdf.getvalue())
```

## Template IDs

- `auto_cv` - Modern, ATS-friendly
- `anti_cv` - Creative, unconventional
- `ethan` - Professional two-column
- `rendercv_classic` - Academic LaTeX style
- `rendercv_engineering` - Technical focus
- `rendercv_sb2nov` - GitHub compact style
- `yuan` - Minimalist elegant

## API Usage

### Export Resume with Template

```javascript
// POST /resume/export/pdf?resume_id=xxx&template=yuan
fetch('/resume/export/pdf?resume_id=12345&template=yuan', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer ' + token
  }
})
.then(response => response.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  window.open(url);
});
```

### Preview Template

```javascript
// POST /templates/auto_cv/preview
fetch('/templates/auto_cv/preview', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + token
  },
  body: JSON.stringify({
    resume_data: yourResumeData,
    theme_color: '#FF6B6B'
  })
})
.then(response => response.blob())
.then(blob => {
  const url = URL.createObjectURL(blob);
  window.open(url);
});
```

## Template Selection by Role

| Your Role | Use This Template |
|-----------|------------------|
| Software Developer | `rendercv_sb2nov` or `rendercv_engineering` |
| Product Manager | `ethan` or `auto_cv` |
| Designer | `anti_cv` or `yuan` |
| Data Scientist | `rendercv_engineering` |
| Academic/PhD | `rendercv_classic` |
| Executive | `yuan` |
| Entry Level | `auto_cv` |

## Color Customization

All templates support custom theme colors:

```python
# Default blue
pdf = TemplateManager.generate_resume(data, "ethan", "#3B82F6")

# Custom colors
pdf = TemplateManager.generate_resume(data, "yuan", "#2ECC71")  # Green
pdf = TemplateManager.generate_resume(data, "anti_cv", "#E74C3C")  # Red
pdf = TemplateManager.generate_resume(data, "auto_cv", "#9B59B6")  # Purple
```

## Frontend Integration Example

```jsx
// React Component
import { useState, useEffect } from 'react';

function TemplateSelector({ resumeId, onSelect }) {
  const [templates, setTemplates] = useState([]);
  const [selected, setSelected] = useState('auto_cv');
  
  useEffect(() => {
    fetch('/templates/')
      .then(r => r.json())
      .then(data => setTemplates(data));
  }, []);
  
  const handleExport = async () => {
    const response = await fetch(
      `/resume/export/pdf?resume_id=${resumeId}&template=${selected}`,
      { method: 'POST', headers: { 'Authorization': `Bearer ${token}` }}
    );
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    window.open(url);
  };
  
  return (
    <div>
      <select value={selected} onChange={e => setSelected(e.target.value)}>
        {templates.map(t => (
          <option key={t.id} value={t.id}>
            {t.name} - {t.description}
          </option>
        ))}
      </select>
      <button onClick={handleExport}>Export PDF</button>
    </div>
  );
}
```

## Testing Templates

```bash
cd Backend

# Test template listing
python -c "
from templates.template_manager import TemplateManager
import json
templates = TemplateManager.list_templates()
print(json.dumps(templates, indent=2))
"

# Test template generation
python -c "
from templates.template_manager import TemplateManager

resume_data = {
    'personal_info': {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '123-456-7890'
    },
    'summary': 'Test summary',
    'skills': ['Python', 'JavaScript'],
    'experience': [],
    'education': []
}

pdf = TemplateManager.generate_resume(resume_data, 'auto_cv')
with open('test_resume.pdf', 'wb') as f:
    f.write(pdf.getvalue())
print('Generated test_resume.pdf')
"
```

## Troubleshooting

### Template not found
- Check template ID spelling
- Use `TemplateManager.list_templates()` to see available templates

### Generation error
- Verify resume_data structure
- Check that all required fields are present
- Ensure theme_color is valid hex format (#RRGGBB)

### PDF not rendering
- Install required dependencies: `pip install reportlab`
- Check console for error messages

## Support

For more details, see:
- Full documentation: `Docs/TEMPLATES.md`
- API docs: http://localhost:8000/docs
- Template source: `Backend/templates/`
