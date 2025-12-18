# Template Selection User Guide

## 🎨 Overview

ResuAI now includes 7 professional resume templates to choose from when exporting your resume. Each template has a unique design and purpose to match different career goals.

---

## 📋 Available Templates

### 1. **Auto CV** (Default) 🤖
- **Best For**: ATS-friendly applications, corporate jobs
- **Style**: Modern, clean, two-column layout
- **Features**: 
  - Excellent for Applicant Tracking Systems
  - Professional color scheme
  - Clear section hierarchy
  - Skills displayed with proficiency levels

### 2. **Anti CV** 🎨
- **Best For**: Creative roles, startups, unique positions
- **Style**: Story-driven, narrative format
- **Features**:
  - Focus on personality and journey
  - Creative section names ("My Story", "Superpowers")
  - Bold typography
  - Stands out from traditional resumes

### 3. **Ethan's Template** 💼
- **Best For**: Traditional corporate, finance, consulting
- **Style**: Professional two-column with sidebar
- **Features**:
  - Classic professional look
  - Contact info in left sidebar
  - Clean typography
  - Conservative design

### 4. **RenderCV Classic** 🎓
- **Best For**: Academic positions, research roles
- **Style**: LaTeX-inspired, academic format
- **Features**:
  - Resembles LaTeX documents
  - Formal and traditional
  - Ideal for academia
  - Publication-ready

### 5. **RenderCV Engineering** ⚙️
- **Best For**: Technical roles, engineering positions
- **Style**: Data-driven, technical focus
- **Features**:
  - Emphasizes technical skills
  - Project-centric layout
  - Tech-friendly formatting
  - Metrics highlighted

### 6. **RenderCV sb2nov** 💻
- **Best For**: Tech industry, software development
- **Style**: Compact GitHub-style
- **Features**:
  - Inspired by popular GitHub template
  - Maximizes content density
  - Modern tech aesthetic
  - Open-source community favorite

### 7. **Yuan's Template** ✨
- **Best For**: Minimalist preference, design roles
- **Style**: Elegant, clean, spacious
- **Features**:
  - Beautiful minimalist design
  - Generous white space
  - Elegant typography
  - Sophisticated look

---

## 🚀 How to Use Templates

### Step 1: Navigate to Dashboard
1. Log in to your ResuAI account
2. Go to the Dashboard
3. View your saved resumes

### Step 2: Export with Template Selection
1. Click the **Download** button on any resume card
2. The **Export Modal** will open
3. Browse through the available templates in the grid view
4. Click on a template to select it
   - Selected template will show a blue border and checkmark
   - Template details will appear at the bottom

### Step 3: Choose Theme Color (Optional)
1. Scroll to the **Theme Color** section
2. Select from 8 professional colors:
   - Blue (default)
   - Green
   - Purple
   - Red
   - Orange
   - Teal
   - Pink
   - Indigo

### Step 4: Export
1. Click **Export as PDF** or **Export as DOCX**
2. Wait for the download to complete
3. Your resume will be saved as: `{resume_title}_{template_name}.pdf`

---

## 💡 Tips for Choosing Templates

### For Corporate Jobs
- **Best Choice**: Auto CV, Ethan's Template, RenderCV Classic
- **Why**: ATS-friendly, professional, traditional

### For Tech Jobs
- **Best Choice**: RenderCV Engineering, RenderCV sb2nov, Auto CV
- **Why**: Technical focus, modern, developer-friendly

### For Creative Roles
- **Best Choice**: Anti CV, Yuan's Template
- **Why**: Unique design, personality-driven, artistic

### For Academic Positions
- **Best Choice**: RenderCV Classic
- **Why**: Traditional academic format, publication-ready

### For Startups
- **Best Choice**: Anti CV, RenderCV sb2nov, Yuan's Template
- **Why**: Modern, unique, shows personality

---

## 🎨 Theme Color Guide

### Professional Colors
- **Blue** (#3B82F6): Trust, reliability, tech (default)
- **Indigo** (#6366F1): Professional, corporate, stable

### Creative Colors
- **Purple** (#8B5CF6): Creative, innovative, unique
- **Pink** (#EC4899): Design, creative, bold

### Tech Colors
- **Teal** (#14B8A6): Modern, tech, startup
- **Green** (#10B981): Growth, positive, fresh

### Bold Colors
- **Orange** (#F59E0B): Energetic, friendly, approachable
- **Red** (#EF4444): Bold, confident, leadership

---

## ⚙️ Technical Details

### Export Formats
- **PDF**: Universal compatibility, preserves formatting
- **DOCX**: Editable in Word, can be further customized

### Template Parameters
- All templates support theme color customization
- Colors apply to headings, section dividers, and accents
- Layout and structure remain consistent per template

### File Naming
- Format: `{resume_title}_{template_id}.{format}`
- Example: `Software_Engineer_Resume_auto_cv.pdf`

---

## 🔧 Troubleshooting

### Template Not Loading
1. Refresh the page
2. Check backend is running
3. Verify API endpoint: `http://localhost:8000/templates/`

### Export Failed
1. Ensure backend is running
2. Check console for errors
3. Verify resume ID is valid
4. Try different template

### Preview Not Showing
1. Select a template first
2. Ensure valid resume data exists
3. Check network tab for API errors

---

## 🆘 Need Help?

### Common Issues

**Q: Can I preview templates before exporting?**
A: Yes! The template selector shows template icons and descriptions. Click to see details.

**Q: Can I change the template after exporting?**
A: Yes! Export the same resume with a different template anytime.

**Q: Do templates affect ATS compatibility?**
A: Auto CV, Ethan's Template, and RenderCV templates are ATS-friendly. Anti CV and Yuan's may have lower ATS scores.

**Q: Can I customize template layouts?**
A: Currently templates have fixed layouts. You can customize content and theme colors.

### Support
- Check `Docs/TEMPLATES.md` for developer documentation
- See `Docs/TEMPLATE_QUICKSTART.md` for quick reference
- Report issues through the dashboard

---

## 🎯 Best Practices

1. **Match Industry**: Choose template based on target industry
2. **Test Multiple**: Export with 2-3 templates to compare
3. **Consider ATS**: Use Auto CV for online applications
4. **Personality**: Use creative templates for personal brand
5. **Consistency**: Use same template for related applications

---

## 📈 Template Comparison

| Template | ATS Score | Creativity | Best For |
|----------|-----------|------------|----------|
| Auto CV | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Corporate, Tech |
| Anti CV | ⭐⭐ | ⭐⭐⭐⭐⭐ | Creative, Startups |
| Ethan's | ⭐⭐⭐⭐ | ⭐⭐ | Finance, Consulting |
| RenderCV Classic | ⭐⭐⭐⭐⭐ | ⭐⭐ | Academia, Research |
| RenderCV Engineering | ⭐⭐⭐⭐ | ⭐⭐⭐ | Engineering, Tech |
| RenderCV sb2nov | ⭐⭐⭐⭐ | ⭐⭐⭐ | Software Dev |
| Yuan's | ⭐⭐⭐ | ⭐⭐⭐⭐ | Design, Minimal |

---

## 🚀 Quick Start

```
1. Dashboard → Select Resume → Click Download
2. Choose Template → Pick Color → Export PDF
3. Download Complete! ✅
```

That's it! Your professional resume is ready to send. 🎉
