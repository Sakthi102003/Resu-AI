from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any
from bson import ObjectId
import json
from database.connection import get_database
from routes.auth import get_current_user
from routes.chat import call_ai
from config import settings

router = APIRouter(prefix="/ai", tags=["AI Enhancement"])


class EnhanceRequest(BaseModel):
    text: str
    style: str = "professional"  # professional, concise, impactful, ats-optimized


class ATSScoreRequest(BaseModel):
    resume_id: str


class ATSScoreResponse(BaseModel):
    score: int
    feedback: str
    missing_keywords: List[str]
    improvements: List[str]


class JobRecommendation(BaseModel):
    title: str
    description: str
    match_percentage: int
    required_skills: List[str]
    why_good_fit: str


class JobRecommendRequest(BaseModel):
    resume_id: str
    preferences: Dict[str, Any] = {}


@router.post("/enhance")
async def enhance_text(
    request: EnhanceRequest,
    current_user: dict = Depends(get_current_user)
):
    """Enhance text with AI"""
    
    style_prompts = {
        "professional": "Rewrite this to sound more professional and polished:",
        "concise": "Make this more concise while keeping the impact:",
        "impactful": "Rewrite this with strong action verbs and quantifiable results:",
        "ats-optimized": "Optimize this for ATS systems with relevant keywords:"
    }
    
    prompt = style_prompts.get(request.style, style_prompts["professional"])
    
    messages = [
        {"role": "system", "content": "You are an expert resume writer."},
        {"role": "user", "content": f"{prompt}\n\n{request.text}"}
    ]
    
    enhanced = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    return {
        "original": request.text,
        "enhanced": enhanced.strip(),
        "style": request.style
    }


@router.post("/ats-score", response_model=ATSScoreResponse)
async def calculate_ats_score(
    request: ATSScoreRequest,
    current_user: dict = Depends(get_current_user)
):
    """Calculate ATS compatibility score for a resume"""
    db = get_database()
    
    if not ObjectId.is_valid(request.resume_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID"
        )
    
    resume = await db.resumes.find_one({"_id": ObjectId(request.resume_id)})
    if not resume or resume["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    resume_data = resume.get("data", {})
    
    # Create prompt for AI to analyze
    messages = [
        {"role": "system", "content": """You are an ATS (Applicant Tracking System) expert. 
Analyze resumes and provide:
1. A score out of 100
2. Detailed feedback
3. Missing important keywords
4. Specific improvements

Return your response in this JSON format:
{
  "score": 85,
  "feedback": "Your resume has good structure...",
  "missing_keywords": ["Python", "AWS", "CI/CD"],
  "improvements": ["Add more quantifiable achievements", "Include technical skills section"]
}"""},
        {"role": "user", "content": f"Analyze this resume for ATS compatibility:\n\n{json.dumps(resume_data, default=str)}"}
    ]
    
    ai_response = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    # Parse JSON response
    try:
        # Extract JSON from response
        if "```json" in ai_response:
            start = ai_response.find("```json") + 7
            end = ai_response.find("```", start)
            json_str = ai_response[start:end].strip()
        else:
            json_str = ai_response
        
        result = json.loads(json_str)
        
        # Update resume with score
        await db.resumes.update_one(
            {"_id": ObjectId(request.resume_id)},
            {"$set": {"ats_score": result["score"]}}
        )
        
        return ATSScoreResponse(**result)
    
    except Exception as e:
        # Fallback if JSON parsing fails
        return ATSScoreResponse(
            score=70,
            feedback=ai_response,
            missing_keywords=[],
            improvements=["Review AI feedback for specific improvements"]
        )


@router.post("/job-recommend", response_model=List[JobRecommendation])
async def recommend_jobs(
    request: JobRecommendRequest,
    current_user: dict = Depends(get_current_user)
):
    """Recommend jobs based on resume"""
    db = get_database()
    
    if not ObjectId.is_valid(request.resume_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID"
        )
    
    resume = await db.resumes.find_one({"_id": ObjectId(request.resume_id)})
    if not resume or resume["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    resume_data = resume.get("data", {})
    
    # Extract key information
    skills = resume_data.get("skills", [])
    experience = resume_data.get("experience", [])
    
    preferences_str = ""
    if request.preferences:
        preferences_str = f"\n\nUser preferences: {json.dumps(request.preferences)}"
    
    messages = [
        {"role": "system", "content": """You are a career advisor AI. Based on a candidate's resume, 
recommend 5 suitable job titles they should apply for.

Return your response in this JSON format:
[
  {
    "title": "Senior Software Engineer",
    "description": "Brief job description",
    "match_percentage": 95,
    "required_skills": ["Python", "AWS", "Docker"],
    "why_good_fit": "Your experience with..."
  }
]"""},
        {"role": "user", "content": f"""Based on this resume, recommend 5 job titles:

Skills: {', '.join(skills)}
Experience: {len(experience)} positions
Latest role: {experience[0].get('position', 'N/A') if experience else 'N/A'}
{preferences_str}

Resume data: {json.dumps(resume_data, default=str)[:1000]}"""}
    ]
    
    ai_response = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    # Parse JSON response
    try:
        if "```json" in ai_response:
            start = ai_response.find("```json") + 7
            end = ai_response.find("```", start)
            json_str = ai_response[start:end].strip()
        else:
            # Try to find JSON array
            start = ai_response.find("[")
            end = ai_response.rfind("]") + 1
            json_str = ai_response[start:end]
        
        recommendations = json.loads(json_str)
        return [JobRecommendation(**rec) for rec in recommendations[:5]]
    
    except Exception as e:
        # Fallback recommendations
        return [
            JobRecommendation(
                title="Software Engineer",
                description="Based on your technical skills and experience",
                match_percentage=80,
                required_skills=skills[:5] if skills else ["Programming"],
                why_good_fit="Your skills align well with this role"
            )
        ]


@router.post("/grammar-check")
async def check_grammar(
    text: str,
    current_user: dict = Depends(get_current_user)
):
    """Check and correct grammar"""
    messages = [
        {"role": "system", "content": "You are a grammar expert. Fix any grammar, spelling, or punctuation errors. Return only the corrected text."},
        {"role": "user", "content": text}
    ]
    
    corrected = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    return {
        "original": text,
        "corrected": corrected.strip(),
        "has_errors": text.strip() != corrected.strip()
    }


@router.post("/keywords")
async def suggest_keywords(
    job_title: str,
    industry: str = "Technology",
    current_user: dict = Depends(get_current_user)
):
    """Suggest relevant keywords for a job title"""
    messages = [
        {"role": "system", "content": "You are an ATS expert. Suggest important keywords for resumes."},
        {"role": "user", "content": f"List 15 important keywords for a {job_title} position in the {industry} industry. Return as a comma-separated list."}
    ]
    
    keywords_text = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    # Parse keywords
    keywords = [k.strip() for k in keywords_text.replace('\n', ',').split(',') if k.strip()]
    
    return {
        "job_title": job_title,
        "industry": industry,
        "keywords": keywords[:15]
    }
