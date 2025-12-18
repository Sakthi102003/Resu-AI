# 🚀 ResuAI - AI-Powered Chat-Based Resume Builder

> **⚠️ Project Status: Under Active Development**  
> This project is currently under construction. Some features may be incomplete or subject to change.

Build professional, ATS-optimized resumes through natural conversation with AI. ResuAI is a full-stack application that combines the power of AI (OpenAI GPT or Google Gemini) with an intuitive chat interface to help users create perfect resumes.

![ResuAI](https://img.shields.io/badge/Version-1.0.0-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![AI](https://img.shields.io/badge/AI-Powered-purple)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

---

## ✨ Features

### 🤖 AI-Powered Chat Interface
- Natural conversation with AI to build your resume
- AI extracts structured data from your descriptions
- Context-aware responses and suggestions
- Real-time resume preview

### 📊 ATS Optimization
- Calculate ATS compatibility score (0-100)
- Get detailed feedback on improvements
- Identify missing keywords
- Optimize content for applicant tracking systems

### 💼 Job Recommendations
- AI suggests suitable job positions based on your resume
- Match percentage for each recommendation
- Required skills and qualifications
- Personalized fit analysis

### 🎨 Professional Export
- Export to PDF format
- Export to DOCX (Microsoft Word)
- Clean, professional formatting

### 📝 Resume Management
- Create multiple resumes
- Version tracking
- Edit and update anytime
- Secure cloud storage

### 🔧 AI Enhancements
- Rewrite text professionally
- Grammar and spell checking
- Keyword suggestions
- Multiple writing styles (professional, concise, impactful)

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework
- **MongoDB Atlas** - Cloud database
- **OpenAI GPT / Google Gemini** - AI language models
- **JWT** - Secure authentication
- **python-docx & reportlab** - Document generation
- **Motor** - Async MongoDB driver

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **TailwindCSS** - Styling
- **Framer Motion** - Animations
- **Axios** - API calls
- **React Query** - State management
- **Zustand** - Auth state
- **React Router** - Navigation

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB (local or Atlas)
- OpenAI API Key OR Google Gemini API Key

### Backend Setup

1. **Clone the repository**
```bash
cd ResuAI/Backend
```

2. **Create virtual environment**
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
# Copy example env file
cp .env.example .env

# Edit .env file with your settings:
# - MONGODB_URL=mongodb://localhost:27017
# - OPENAI_API_KEY=your-key-here (or GEMINI_API_KEY)
# - SECRET_KEY (generate with: openssl rand -hex 32)
```

5. **Run the server**
```bash
python main.py
# Or with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../Frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create environment file**
```bash
# Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

4. **Run development server**
```bash
npm run dev
```

Frontend will be available at: `http://localhost:5173`

---

## 🎯 Usage

### 1. Register/Login
- Create an account or sign in
- Your profile information will be used as defaults in resumes

### 2. Create Resume
- Click "Create New Resume" on the dashboard
- Start chatting with the AI assistant
- Answer questions about your experience, education, skills

### 3. Build Through Chat
Example conversation:
```
AI: Tell me about your most recent role.
You: I worked as a Software Engineer at Google for 3 years.

AI: Great! What were your key responsibilities and achievements?
You: I developed microservices, led a team of 5, and improved performance by 40%.

AI: Excellent! I've added that to your experience. Now, tell me about your education...
```

### 4. Optimize & Export
- Calculate ATS score
- Get improvement suggestions
- View job recommendations
- Export to PDF or DOCX

---

## 📁 Project Structure

```
ResuAI/
├── Backend/
│   ├── config.py                 # Configuration settings
│   ├── main.py                   # FastAPI application
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example             # Environment template
│   ├── database/
│   │   └── connection.py        # MongoDB connection
│   ├── models/
│   │   ├── user_model.py        # User Pydantic models
│   │   └── resume_model.py      # Resume Pydantic models
│   ├── routes/
│   │   ├── auth.py              # Authentication endpoints
│   │   ├── resume.py            # Resume CRUD endpoints
│   │   ├── chat.py              # AI chat endpoints
│   │   ├── ai_enhance.py        # AI enhancement features
│   │   └── job_recommend.py     # Job recommendations
│   └── utils/
│       ├── pdf_generator.py     # PDF export
│       ├── docx_generator.py    # DOCX export
│       ├── ats_scorer.py        # ATS scoring algorithm
│       └── resume_parser.py     # Resume parsing
│
└── Frontend/
    ├── package.json             # Node dependencies
    ├── vite.config.js           # Vite configuration
    ├── tailwind.config.js       # TailwindCSS config
    ├── index.html               # HTML entry point
    └── src/
        ├── main.jsx             # React entry point
        ├── app.jsx              # Main App component
        ├── index.css            # Global styles
        ├── Services/
        │   ├── api.js           # API client
        │   └── auth.js          # Auth state management
        ├── pages/
        │   ├── login.jsx        # Login/Register page
        │   ├── Dashboard.jsx    # Dashboard page
        │   ├── Chateditor.jsx   # Chat editor page
        │   └── Profile.jsx      # Profile page
        └── components/
            ├── resumepreview.jsx      # Resume preview
            ├── ResumeScoreCard.jsx    # ATS score display
            └── jobRecommendation.jsx  # Job recommendations
```

---

## 🔌 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (form data)
- `POST /auth/login/json` - Login (JSON)
- `GET /auth/me` - Get current user
- `PUT /auth/me` - Update user profile

### Resume Management
- `POST /resume/` - Create resume
- `GET /resume/` - Get all resumes
- `GET /resume/{id}` - Get specific resume
- `PUT /resume/{id}` - Update resume
- `DELETE /resume/{id}` - Delete resume

### Chat & AI
- `POST /chat/respond` - Chat with AI
- `POST /chat/enhance` - Enhance text
- `POST /chat/suggestions` - Get suggestions

### AI Features
- `POST /ai/enhance` - Enhance text with style
- `POST /ai/ats-score` - Calculate ATS score
- `POST /ai/job-recommend` - Get job recommendations
- `POST /ai/grammar-check` - Check grammar
- `POST /ai/keywords` - Suggest keywords

### Export
- `POST /resume/export/pdf` - Export as PDF
- `POST /resume/export/docx` - Export as DOCX
- `POST /resume/upload` - Upload & parse resume

---

## 🔐 Environment Variables

### Backend (.env)
```env
# Required
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-your-key  # OR
GEMINI_API_KEY=your-key

# Optional
AI_PROVIDER=openai  # or "gemini"
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

---

## 🎨 Screenshots

### Dashboard
Create and manage multiple resumes with ATS scores and quick actions.

### Chat Editor
Build your resume through natural conversation with AI assistance.

### ATS Score
Get detailed feedback on your resume's ATS compatibility.

### Job Recommendations
Discover perfect job matches based on your skills and experience.

---

## � Documentation

Comprehensive documentation is available in the **[Docs/](./Docs/)** folder:

### Getting Started
- **[Quickstart Guide](./Docs/QUICKSTART.md)** - Get up and running quickly
- **[Project Summary](./Docs/PROJECT_SUMMARY.md)** - Overview and architecture
- **[Project Checklist](./Docs/PROJECT_CHECKLIST.md)** - Development milestones

### Development & Testing
- **[API Testing Guide](./Docs/API_TESTING.md)** - Test all API endpoints

### Deployment
- **[Deployment Guide](./Docs/DEPLOYMENT.md)** - Production deployment steps
- **[Firebase Setup](./Docs/FIREBASE_SETUP.md)** - Firebase integration

📖 **[View All Documentation](./Docs/README.md)**

---

## � Deployment

### Backend (Railway/Render)
1. Create account on Railway or Render
2. Connect your repository
3. Add environment variables
4. Deploy!

### Frontend (Vercel/Netlify)
1. Create account on Vercel or Netlify
2. Connect your repository
3. Set build command: `npm run build`
4. Set output directory: `dist`
5. Add environment variable: `VITE_API_URL`
6. Deploy!

📖 Detailed deployment guide: [Docs/DEPLOYMENT.md](./Docs/DEPLOYMENT.md)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 🆘 Support

- 📖 Check the [Documentation](./Docs/README.md)
- 🐛 Report bugs via GitHub Issues
- 💬 Questions? Check existing issues or create a new one

---

**Built with ❤️ using FastAPI, React, and AI**
