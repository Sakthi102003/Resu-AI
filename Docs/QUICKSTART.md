# 🚀 Quick Start Guide - ResuAI

Get ResuAI up and running in 5 minutes!

## Prerequisites

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB running (local or Atlas)
- [ ] OpenAI API key or Google Gemini API key

---

## Step 1: Backend Setup (2 minutes)

```powershell
# Navigate to backend
cd Backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env file with your settings (important!)
# Required fields:
#   MONGODB_URL=mongodb://localhost:27017
#   OPENAI_API_KEY=your-openai-key-here
#   SECRET_KEY=generate-with-openssl-rand-hex-32

# Start backend server
python main.py
```

✅ Backend running at: http://localhost:8000
📚 API Docs: http://localhost:8000/docs

---

## Step 2: Frontend Setup (2 minutes)

```powershell
# Open NEW terminal
# Navigate to frontend
cd Frontend

# Install dependencies
npm install

# Create .env file
echo VITE_API_URL=http://localhost:8000 > .env

# Start frontend
npm run dev
```

✅ Frontend running at: http://localhost:5173

---

## Step 3: Test the Application (1 minute)

1. Open http://localhost:5173 in your browser
2. Click "Sign Up" and create an account
3. Create your first resume
4. Start chatting with AI!

Example first message:
```
"I'm a Software Engineer with 5 years of experience at Google. I worked on cloud infrastructure and led a team of 3 developers."
```

---

## 🎯 Quick Tips

### Get Better Results
- Be specific with achievements and numbers
- Mention technologies and tools you used
- Include time periods and locations
- Use the "Enhance" button to improve text

### AI Commands to Try
- "Add my AWS certification"
- "Make this sound more professional"
- "Add a project where I built a React app"
- "Shorten my experience section"
- "Calculate my ATS score"
- "Recommend jobs for me"

### Keyboard Shortcuts
- `Enter` - Send message
- `Shift + Enter` - New line in message
- `Ctrl + K` - Focus search/input

---

## 🔧 Troubleshooting

### Backend Issues

**Error: "MongoDB connection failed"**
```powershell
# Make sure MongoDB is running
# Or update MONGODB_URL in .env to use Atlas:
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/resuai_db
```

**Error: "OpenAI API error"**
```powershell
# Verify your API key in .env
OPENAI_API_KEY=sk-your-actual-key-here

# Or switch to Gemini:
AI_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-key
```

### Frontend Issues

**Error: "Network Error"**
```powershell
# Ensure backend is running on port 8000
# Check VITE_API_URL in .env:
VITE_API_URL=http://localhost:8000
```

**Dependencies installation failed**
```powershell
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 Next Steps

1. ✅ Create your first resume
2. ✅ Calculate ATS score
3. ✅ Get job recommendations
4. ✅ Export to PDF
5. ✅ Try different writing styles
6. ✅ Build multiple resume versions

---

## 🆘 Need Help?

- Check the full README.md for detailed documentation
- Visit http://localhost:8000/docs for API documentation
- Report issues on GitHub

---

## 🎉 You're All Set!

Start building amazing resumes with AI assistance!

**Happy Resume Building! 🚀**
