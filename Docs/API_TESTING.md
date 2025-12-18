# API Testing Guide for ResuAI

Test the backend API using curl or your favorite API client.

## Base URL
```
http://localhost:8000
```

---

## 1. Authentication

### Register New User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "phone": "+1234567890"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login/json \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

**Save the access_token from the response!**

### Get Current User
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 2. Resume Management

### Create Resume
```bash
curl -X POST http://localhost:8000/resume/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Professional Resume",
    "data": {
      "personal_info": {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890"
      },
      "skills": ["Python", "JavaScript", "React", "FastAPI"]
    }
  }'
```

### Get All Resumes
```bash
curl -X GET http://localhost:8000/resume/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Specific Resume
```bash
curl -X GET http://localhost:8000/resume/RESUME_ID \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update Resume
```bash
curl -X PUT http://localhost:8000/resume/RESUME_ID \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "summary": "Experienced software engineer with 5+ years..."
    }
  }'
```

---

## 3. AI Chat

### Chat with AI
```bash
curl -X POST http://localhost:8000/chat/respond \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I worked as a Software Engineer at Google for 3 years",
    "resume_id": "RESUME_ID",
    "context": []
  }'
```

### Enhance Text
```bash
curl -X POST "http://localhost:8000/chat/enhance?text=I%20did%20programming&style=professional" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 4. AI Features

### Calculate ATS Score
```bash
curl -X POST http://localhost:8000/ai/ats-score \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "RESUME_ID"
  }'
```

### Get Job Recommendations
```bash
curl -X POST http://localhost:8000/ai/job-recommend \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "RESUME_ID",
    "preferences": {}
  }'
```

### Check Grammar
```bash
curl -X POST "http://localhost:8000/ai/grammar-check?text=I%20is%20a%20engineer" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Keywords
```bash
curl -X POST "http://localhost:8000/ai/keywords?job_title=Software%20Engineer&industry=Technology" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 5. Export

### Export as PDF
```bash
curl -X POST "http://localhost:8000/resume/export/pdf?resume_id=RESUME_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  --output resume.pdf
```

### Export as DOCX
```bash
curl -X POST "http://localhost:8000/resume/export/docx?resume_id=RESUME_ID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  --output resume.docx
```

---

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Login
response = requests.post(f"{BASE_URL}/auth/login/json", json={
    "email": "test@example.com",
    "password": "password123"
})
token = response.json()["access_token"]

headers = {"Authorization": f"Bearer {token}"}

# Create resume
resume = requests.post(f"{BASE_URL}/resume/", headers=headers, json={
    "title": "My Resume",
    "data": {"personal_info": {"name": "John"}}
})
resume_id = resume.json()["id"]

# Chat with AI
chat = requests.post(f"{BASE_URL}/chat/respond", headers=headers, json={
    "message": "Add my Python skills",
    "resume_id": resume_id
})
print(chat.json()["response"])
```

---

## Interactive API Documentation

Visit: **http://localhost:8000/docs**

FastAPI provides an interactive Swagger UI where you can test all endpoints with a nice interface!
