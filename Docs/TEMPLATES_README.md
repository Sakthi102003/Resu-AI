# 🎨 Resume Templates - Quick Guide

ResuAI now includes **7 professional resume templates** optimized for different industries and roles!

## Available Templates

| Template | Style | Best For |
|----------|-------|----------|
| **Auto CV** | Modern, ATS-friendly | General applications, corporate |
| **Anti CV** | Creative, story-driven | Creative roles, startups |
| **Ethan's Resume** | Professional two-column | Business, consulting |
| **RenderCV Classic** | Academic, traditional | Research, faculty positions |
| **RenderCV Engineering** | Technical, data-driven | Engineering, STEM |
| **RenderCV sb2nov** | Compact, GitHub-style | Software engineers |
| **Yuan's Resume** | Minimalist, elegant | Executive, senior roles |

## Quick Start

### List Templates
```bash
curl http://localhost:8000/templates/
```

### Export with Template
```bash
curl -X POST \
  "http://localhost:8000/resume/export/pdf?resume_id=YOUR_ID&template=yuan" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -o resume.pdf
```

### Test Templates
```bash
cd Backend
python test_templates.py --all
```

## Documentation

- 📚 **Full Guide**: [TEMPLATES.md](./TEMPLATES.md)
- ⚡ **Quick Reference**: [TEMPLATE_QUICKSTART.md](./TEMPLATE_QUICKSTART.md)
- 🔧 **Implementation Details**: [TEMPLATE_IMPLEMENTATION.md](./TEMPLATE_IMPLEMENTATION.md)
- 👩‍💻 **Developer Guide**: [Backend/templates/README.md](../Backend/templates/README.md)

## Template Preview

Each template offers:
- ✅ Professional, print-ready PDFs
- ✅ Customizable theme colors
- ✅ ATS compatibility (most templates)
- ✅ Mobile and desktop viewing
- ✅ Optimized layouts

## Usage Example

```python
from templates.template_manager import TemplateManager

# Generate resume with Auto CV template
pdf = TemplateManager.generate_resume(
    resume_data=your_resume_data,
    template_name="auto_cv",
    theme_color="#3B82F6"
)

# Save to file
with open("resume.pdf", "wb") as f:
    f.write(pdf.getvalue())
```

## Need Help?

- Check the [TEMPLATES.md](./TEMPLATES.md) for detailed information
- Run `python test_templates.py --list` to see all templates
- See [sample_data.py](../Backend/templates/sample_data.py) for example resume formats

---

**New to ResuAI?** Start with the main [README.md](../README.md)
