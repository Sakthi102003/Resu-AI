# 🎨 LaTeX Editor - Complete Guide

## ✨ Overview

ResuAI now includes a **LaTeX-style editor** that works exactly like Overleaf! Write resume content using LaTeX-like commands, compile to see preview, and export to PDF with any template.

---

## 🚀 Quick Start

### Create Resume with LaTeX Editor

1. **Dashboard** → Click **"LaTeX Editor"** card (green)
2. **Write LaTeX code** in left panel
3. **Click "Compile"** to see PDF preview
4. **Select template** from right panel
5. **Click "Save"** to save resume
6. **Click "Export PDF"** to download

---

## 📝 LaTeX Command Reference

### Personal Information
```latex
\name{Your Full Name}
\email{your.email@example.com}
\phone{+1-234-567-8900}
\location{City, State}
\linkedin{linkedin.com/in/yourprofile}
\github{github.com/yourusername}
```

### Summary/Objective
```latex
\summary{
  Brief professional summary highlighting your expertise and value proposition.
  Keep it concise and impactful.
}
```

### Experience Section
```latex
\experience{
  \item{
    \position{Software Engineer}
    \company{Tech Company Inc}
    \dates{Jan 2020 -- Present}
    \location{San Francisco, CA}
    \description{
      • Led development of microservices architecture
      • Improved system performance by 40%
      • Mentored 3 junior developers
    }
  }
  \item{
    \position{Junior Developer}
    \company{Startup Corp}
    \dates{Jun 2018 -- Dec 2019}
    \location{New York, NY}
    \description{
      • Built RESTful APIs using Python/Django
      • Implemented CI/CD pipelines with Jenkins
    }
  }
}
```

### Education Section
```latex
\education{
  \item{
    \degree{Bachelor of Science in Computer Science}
    \institution{University Name}
    \dates{2014 -- 2018}
    \gpa{3.8/4.0}
  }
  \item{
    \degree{Master of Science in Software Engineering}
    \institution{Tech University}
    \dates{2018 -- 2020}
    \gpa{3.9/4.0}
  }
}
```

### Skills Section
```latex
\skills{
  \category{Languages}{Python, JavaScript, Java, C++, SQL}
  \category{Frameworks}{React, Django, FastAPI, Node.js, Spring}
  \category{Tools}{Git, Docker, Kubernetes, AWS, Jenkins}
  \category{Databases}{PostgreSQL, MongoDB, Redis}
}
```

### Projects Section
```latex
\projects{
  \item{
    \title{E-commerce Platform}
    \description{Full-stack web application with real-time features}
    \tech{React, Django, PostgreSQL, Redis, AWS}
    \url{github.com/yourusername/project}
  }
  \item{
    \title{Machine Learning Pipeline}
    \description{Automated ML pipeline for data processing}
    \tech{Python, TensorFlow, Docker, Kubernetes}
    \url{github.com/yourusername/ml-pipeline}
  }
}
```

### Certifications Section
```latex
\certifications{
  \item{AWS Certified Solutions Architect}{Amazon Web Services}{2023}
  \item{Professional Scrum Master I}{Scrum.org}{2022}
  \item{Google Cloud Professional}{Google}{2021}
}
```

---

## 🎨 Complete Example

```latex
% Resume Data in LaTeX-style format

\name{John Doe}
\email{john.doe@email.com}
\phone{+1-555-123-4567}
\location{San Francisco, CA}
\linkedin{linkedin.com/in/johndoe}
\github{github.com/johndoe}

\summary{
  Full-stack software engineer with 5+ years of experience building scalable 
  web applications. Specialized in React, Python, and cloud technologies. 
  Passionate about creating user-centric solutions and mentoring junior developers.
}

\experience{
  \item{
    \position{Senior Software Engineer}
    \company{TechCorp Inc}
    \dates{Jan 2021 -- Present}
    \location{San Francisco, CA}
    \description{
      • Led development of microservices architecture serving 1M+ users
      • Reduced API response time by 60% through optimization
      • Mentored team of 4 junior developers
      • Implemented automated testing, increasing code coverage to 95%
    }
  }
  \item{
    \position{Software Engineer}
    \company{StartupXYZ}
    \dates{Jun 2019 -- Dec 2020}
    \location{San Francisco, CA}
    \description{
      • Built RESTful APIs using Python/Django
      • Developed responsive frontend with React
      • Implemented CI/CD pipelines with Docker and Jenkins
      • Contributed to open-source projects
    }
  }
  \item{
    \position{Junior Developer}
    \company{WebSolutions LLC}
    \dates{Jan 2018 -- May 2019}
    \location{New York, NY}
    \description{
      • Developed web applications using MERN stack
      • Collaborated with designers on UI/UX
      • Fixed bugs and improved code quality
    }
  }
}

\education{
  \item{
    \degree{Bachelor of Science in Computer Science}
    \institution{Stanford University}
    \dates{2014 -- 2018}
    \gpa{3.8/4.0}
  }
}

\skills{
  \category{Languages}{Python, JavaScript, TypeScript, Java, SQL}
  \category{Frameworks}{React, Django, FastAPI, Node.js, Express}
  \category{Tools}{Git, Docker, Kubernetes, AWS, Jenkins, Terraform}
  \category{Databases}{PostgreSQL, MongoDB, Redis, MySQL}
}

\projects{
  \item{
    \title{E-commerce Platform}
    \description{Full-stack platform with real-time inventory management}
    \tech{React, Django, PostgreSQL, Redis, AWS}
    \url{github.com/johndoe/ecommerce}
  }
  \item{
    \title{Task Management App}
    \description{Collaborative task management with real-time updates}
    \tech{React, Node.js, MongoDB, Socket.io}
    \url{github.com/johndoe/taskapp}
  }
  \item{
    \title{Weather Dashboard}
    \description{Real-time weather data visualization}
    \tech{React, Python, FastAPI, Chart.js}
    \url{github.com/johndoe/weather}
  }
}

\certifications{
  \item{AWS Certified Solutions Architect}{Amazon Web Services}{2023}
  \item{Professional Scrum Master I}{Scrum.org}{2022}
  \item{Docker Certified Associate}{Docker Inc}{2021}
}
```

---

## 🎯 LaTeX Editor Features

### 1. **Syntax Highlighting**
- Green text on dark background (terminal-style)
- Monospace font for code
- Easy to read and edit

### 2. **Tab Support**
- Press `Tab` to indent (adds 2 spaces)
- Helps maintain clean code structure

### 3. **Live Compilation**
- Click "Compile" to generate PDF preview
- See changes immediately
- Preview shown in center panel

### 4. **Template Selection**
- Choose from 7 professional templates
- Select theme colors
- Changes applied on next compile

### 5. **Auto-Save**
- Save button stores LaTeX code
- Template and color saved with resume
- Resume persists across sessions

---

## 🏗️ Layout Structure

```
┌────────────────────────────────────────────────────────────────────┐
│ Header: [Back] [Title] [Compile] [Save] [ATS] [Jobs] [Export]     │
├────────────────────┬───────────────────┬───────────────────────────┤
│                    │                   │                           │
│  LaTeX Editor      │   PDF Preview     │    Template Panel         │
│  ┌──────────────┐  │  ┌─────────────┐  │   ┌──────────────────┐   │
│  │ Source Code  │  │  │             │  │   │ Templates (7)    │   │
│  │              │  │  │   Resume    │  │   │ ├─ 🤖 Auto CV ✓ │   │
│  │ \name{...}   │  │  │   PDF       │  │   │ ├─ 🎨 Anti CV    │   │
│  │ \email{...}  │  │  │   Preview   │  │   │ └─ ... (all 7)  │   │
│  │ \experience{ │  │  │             │  │   │                  │   │
│  │   \item{...} │  │  │             │  │   │ Theme Colors     │   │
│  │   ...        │  │  │             │  │   │ [🔵][🟢][🟣][🔴]│   │
│  │ }            │  │  │             │  │   └──────────────────┘   │
│  └──────────────┘  │  └─────────────┘  │                           │
│  (Flex-1)          │  (1/3)            │   (w-64)                  │
└────────────────────┴───────────────────┴───────────────────────────┘
```

---

## 🔧 How It Works

### Frontend Flow
```javascript
1. User writes LaTeX code
2. Click "Compile"
3. LaTeX → JSON conversion (latexToJson)
4. Send JSON to backend preview API
5. Backend generates PDF with selected template
6. Display PDF in iframe
```

### Save Flow
```javascript
1. User clicks "Save"
2. LaTeX → JSON conversion
3. Save to database with template & color
4. Resume persisted
```

### Export Flow
```javascript
1. User clicks "Export PDF"
2. Uses stored template from database
3. Backend generates final PDF
4. Download file
```

---

## 📊 LaTeX to JSON Conversion

### Input (LaTeX)
```latex
\name{John Doe}
\email{john@example.com}
\experience{
  \item{
    \position{Software Engineer}
    \company{TechCorp}
    \dates{2020 -- Present}
    \description{
      • Built scalable applications
      • Improved performance
    }
  }
}
```

### Output (JSON)
```json
{
  "personal_info": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "experience": [
    {
      "position": "Software Engineer",
      "company": "TechCorp",
      "start_date": "2020",
      "end_date": "Present",
      "description": [
        "Built scalable applications",
        "Improved performance"
      ]
    }
  ]
}
```

---

## 💡 Tips & Best Practices

### 1. **Use Bullet Points**
```latex
\description{
  • Use bullet points for clarity
  • Keep each point concise
  • Start with strong action verbs
}
```

### 2. **Consistent Date Format**
```latex
% Good
\dates{Jan 2020 -- Dec 2021}
\dates{2020 -- 2021}

% Avoid mixing formats
```

### 3. **Organize Skills by Category**
```latex
\skills{
  \category{Languages}{Python, Java}
  \category{Frameworks}{React, Django}
  % Better than flat list
}
```

### 4. **Include URLs**
```latex
\projects{
  \item{
    \title{Project Name}
    \url{github.com/user/project}  % Always include
  }
}
```

### 5. **Compile Frequently**
- Compile after major changes
- Check PDF preview
- Catch errors early

---

## 🎨 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Tab` | Insert indentation (2 spaces) |
| `Ctrl+S` / `Cmd+S` | Save resume (coming soon) |
| `Ctrl+Enter` | Compile preview (coming soon) |

---

## 🐛 Common Issues & Solutions

### Issue 1: Preview Not Showing
**Solution**: Click "Compile" button first

### Issue 2: Template Not Applied
**Solution**: 
1. Select template in right panel
2. Save resume
3. Compile again

### Issue 3: LaTeX Syntax Error
**Solution**: Check for:
- Missing closing `}`
- Unclosed `\item{`
- Mismatched brackets

### Issue 4: Description Not Formatting
**Solution**: Use bullet points `•` or line breaks:
```latex
\description{
  • Point 1
  • Point 2
}
```

---

## 🔄 Migration from Other Editors

### From Form Editor
1. Open existing resume in LaTeX editor
2. LaTeX code auto-generated from JSON
3. Edit LaTeX directly
4. Save and compile

### From Chat Editor
1. Export resume data
2. Open in LaTeX editor
3. Converted to LaTeX format
4. Continue editing

---

## 📦 Files Structure

### New Component
- `Frontend/src/pages/LatexEditor.jsx` - Main LaTeX editor component

### Updated Files
- `Frontend/src/app.jsx` - Added `/editor/latex/:resumeId` route
- `Frontend/src/pages/Dashboard.jsx` - Added LaTeX editor creation card

### Reused Components
- `TemplatePanel.jsx` - Template and color selection
- `ResumeScoreCard.jsx` - ATS score display
- `JobRecommendation.jsx` - Job recommendations

---

## ✅ Features Checklist

✅ LaTeX-style code editor  
✅ Syntax highlighting (green on dark)  
✅ Tab indentation support  
✅ PDF preview with compile button  
✅ Template selection (7 templates)  
✅ Theme color picker (8 colors)  
✅ Save LaTeX code to database  
✅ Auto-conversion LaTeX ↔ JSON  
✅ Export to PDF with selected template  
✅ ATS score calculation  
✅ Job recommendations  
✅ Full Overleaf-style workflow  

---

## 🎯 User Benefits

1. **Professional LaTeX Experience** - Like Overleaf, but for resumes
2. **Full Control** - Write exactly what you want
3. **Template Flexibility** - Switch templates anytime
4. **Fast Editing** - No form fields, just code
5. **Version Control Ready** - LaTeX code is text-based
6. **Portable** - Copy/paste LaTeX anywhere

---

## 🚀 Future Enhancements

### Planned Features
- [ ] Syntax error highlighting
- [ ] Auto-completion for commands
- [ ] Keyboard shortcuts (Ctrl+S, Ctrl+Enter)
- [ ] LaTeX snippets library
- [ ] Collaborative editing
- [ ] Version history
- [ ] LaTeX export option
- [ ] Import from .tex files

---

## 🎉 Summary

The LaTeX Editor provides a **professional code-based approach** to resume creation:

- **Write LaTeX** → **Compile** → **See PDF** → **Export**
- Works exactly like Overleaf
- No forms, just code
- Full template support
- Professional workflow

Perfect for developers and technical professionals who prefer coding over form-filling! 🚀

---

## 📞 Quick Reference

### Dashboard → LaTeX Editor
```
Dashboard → Click "LaTeX Editor" (green card) → Start writing
```

### Basic Resume Structure
```latex
\name{Name}
\email{email}
\summary{Summary}
\experience{\item{...}}
\education{\item{...}}
\skills{\category{...}{...}}
```

### Workflow
```
Write → Compile → Preview → Select Template → Save → Export
```

**Ready to create professional resumes with LaTeX!** ✨
