# 🚀 ResuAI Deployment Guide

Complete guide to deploy ResuAI to production.

---

## 📋 Pre-Deployment Checklist

- [ ] MongoDB Atlas account created
- [ ] OpenAI or Gemini API key obtained
- [ ] Domain name (optional)
- [ ] GitHub repository set up
- [ ] Environment variables documented

---

## 🗄️ Database Setup (MongoDB Atlas)

### 1. Create MongoDB Atlas Account
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a new cluster (free tier available)

### 2. Configure Database
```
1. Click "Connect" on your cluster
2. Add your IP address (or 0.0.0.0/0 for all IPs)
3. Create database user with password
4. Get connection string
```

### 3. Connection String Format
```
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/resuai_db?retryWrites=true&w=majority
```

**Save this for deployment!**

---

## 🔧 Backend Deployment (Railway)

### Option 1: Railway (Recommended - Easy)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Select `Backend` folder as root

3. **Add Environment Variables**
   ```env
   MONGODB_URL=your-mongodb-atlas-url
   SECRET_KEY=your-secret-key
   OPENAI_API_KEY=your-openai-key
   AI_PROVIDER=openai
   ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
   ```

4. **Configure Build**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Get your backend URL: `https://your-app.railway.app`

### Option 2: Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect GitHub repository
   - Root Directory: `Backend`

3. **Configure Service**
   ```
   Name: resuai-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**
   Same as Railway above

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment

---

## 🎨 Frontend Deployment (Vercel)

### 1. Create Vercel Account
- Go to https://vercel.com
- Sign up with GitHub

### 2. Import Project
- Click "Add New..." → "Project"
- Import your GitHub repository
- Root Directory: `Frontend`

### 3. Configure Build Settings
```
Framework Preset: Vite
Build Command: npm run build
Output Directory: dist
Install Command: npm install
```

### 4. Add Environment Variables
```env
VITE_API_URL=https://your-backend.railway.app
```

### 5. Deploy
- Click "Deploy"
- Wait for build to complete
- Get your URL: `https://your-app.vercel.app`

### 6. Update Backend CORS
Go back to Railway/Render and update:
```env
ALLOWED_ORIGINS=https://your-app.vercel.app
```

---

## 🌐 Custom Domain (Optional)

### For Frontend (Vercel)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed

### For Backend (Railway)
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records

---

## 🔐 Environment Variables Reference

### Backend (.env)
```env
# Application
APP_NAME=ResuAI
APP_VERSION=1.0.0
DEBUG=False

# Database
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/resuai_db

# Security
SECRET_KEY=your-very-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# AI Services
OPENAI_API_KEY=sk-your-openai-key
# OR
GEMINI_API_KEY=your-gemini-key
AI_PROVIDER=openai

# CORS
ALLOWED_ORIGINS=https://your-frontend.vercel.app,https://your-custom-domain.com
```

### Frontend (.env)
```env
VITE_API_URL=https://your-backend.railway.app
```

---

## 🧪 Testing Deployment

### 1. Test Backend
```bash
curl https://your-backend.railway.app/health
# Should return: {"status": "healthy"}

curl https://your-backend.railway.app/
# Should return: API info
```

### 2. Test Frontend
1. Open `https://your-frontend.vercel.app`
2. Try to register/login
3. Create a resume
4. Test AI chat
5. Export PDF

---

## 📊 Monitoring & Logs

### Railway
- Go to your project → Deployments
- Click on latest deployment
- View logs in real-time

### Vercel
- Go to your project → Deployments
- Click on latest deployment
- View Function Logs

### MongoDB Atlas
- Go to Clusters → Metrics
- Monitor database usage
- Set up alerts

---

## 🔄 Continuous Deployment

### Automatic Deployment
Both Railway and Vercel automatically deploy when you push to GitHub!

```bash
git add .
git commit -m "Update feature"
git push origin main
```

Your app will automatically rebuild and deploy.

---

## 💰 Cost Estimates (Free Tier)

| Service | Free Tier | Paid Plans Start At |
|---------|-----------|---------------------|
| MongoDB Atlas | 512MB storage | $9/month |
| Railway | $5 credit/month | $10/month |
| Vercel | 100GB bandwidth | $20/month |
| OpenAI API | Pay per use | ~$0.002/1K tokens |
| **Total** | **~$5-10/month** | Scales with usage |

---

## 🚨 Common Deployment Issues

### Issue: CORS Error
**Solution:** Make sure `ALLOWED_ORIGINS` includes your frontend URL

### Issue: MongoDB Connection Failed
**Solution:** 
- Check connection string format
- Verify IP whitelist (0.0.0.0/0 allows all)
- Check username/password

### Issue: OpenAI API Error
**Solution:**
- Verify API key is correct
- Check API usage limits
- Ensure billing is set up

### Issue: Build Failed
**Solution:**
- Check requirements.txt versions
- Verify Python version (3.9+)
- Check Node version (18+)

### Issue: 502 Bad Gateway
**Solution:**
- Check backend logs
- Verify start command is correct
- Ensure port binding to $PORT

---

## 📈 Performance Optimization

### Backend
1. **Enable Redis Caching** (optional)
   ```python
   # Cache AI responses for common queries
   ```

2. **Database Indexing**
   ```python
   # Add indexes on frequently queried fields
   await db.resumes.create_index("user_id")
   ```

3. **Rate Limiting**
   ```python
   # Install slowapi
   pip install slowapi
   ```

### Frontend
1. **Code Splitting**
   - Already configured with Vite

2. **Image Optimization**
   - Use WebP format
   - Lazy loading

3. **CDN**
   - Vercel automatically uses CDN

---

## 🔒 Security Checklist

### Before Going Live
- [ ] Change SECRET_KEY to strong random value
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS only
- [ ] Whitelist specific IPs in MongoDB
- [ ] Enable rate limiting
- [ ] Set up error logging
- [ ] Regular dependency updates
- [ ] Backup database regularly

---

## 📱 Mobile Responsiveness

The app is already responsive! Test on:
- [ ] Desktop (Chrome, Firefox, Safari)
- [ ] Tablet (iPad, Android)
- [ ] Mobile (iPhone, Android)

---

## 🎉 Launch Checklist

### Final Steps Before Launch
- [ ] Test all features in production
- [ ] Verify AI responses
- [ ] Test PDF/DOCX export
- [ ] Check mobile responsiveness
- [ ] Set up analytics (optional)
- [ ] Create backup of database
- [ ] Document admin procedures
- [ ] Prepare user documentation

### Post-Launch
- [ ] Monitor error logs
- [ ] Track API usage
- [ ] Gather user feedback
- [ ] Plan feature updates
- [ ] Set up uptime monitoring

---

## 🆘 Support & Maintenance

### Regular Tasks
- **Weekly:** Check error logs
- **Monthly:** Review API costs
- **Quarterly:** Update dependencies
- **Annually:** Renew domains/certificates

### Backup Strategy
1. MongoDB Atlas automatic backups
2. Code in GitHub
3. Environment variables documented

---

## 🚀 You're Ready to Deploy!

Follow this guide step-by-step and you'll have a production-ready app in about 30 minutes!

**Questions?** Check the logs first, they usually tell you what's wrong.

**Good luck with your launch! 🎉**
