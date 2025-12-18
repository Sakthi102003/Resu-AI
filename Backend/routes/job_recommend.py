from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from routes.ai_enhance import recommend_jobs, JobRecommendRequest
from routes.auth import get_current_user

router = APIRouter(prefix="/jobs", tags=["Job Recommendations"])


class JobSearchRequest(BaseModel):
    resume_id: str
    keywords: Optional[List[str]] = []
    location: Optional[str] = None
    job_type: Optional[str] = "full-time"


@router.post("/recommend")
async def get_job_recommendations(
    request: JobRecommendRequest,
    current_user: dict = Depends(get_current_user)
):
    """Get AI-powered job recommendations based on resume"""
    return await recommend_jobs(request, current_user)


@router.get("/trending")
async def get_trending_jobs(
    industry: str = "Technology",
    current_user: dict = Depends(get_current_user)
):
    """Get trending job titles in an industry"""
    # This could be enhanced with real job market data
    trending_by_industry = {
        "Technology": [
            "AI/ML Engineer",
            "Full Stack Developer",
            "DevOps Engineer",
            "Data Scientist",
            "Cloud Architect"
        ],
        "Finance": [
            "Financial Analyst",
            "Investment Banker",
            "Risk Manager",
            "Portfolio Manager",
            "Compliance Officer"
        ],
        "Healthcare": [
            "Nurse Practitioner",
            "Healthcare Administrator",
            "Medical Coder",
            "Clinical Research Coordinator",
            "Health Informatics Specialist"
        ],
        "Marketing": [
            "Digital Marketing Manager",
            "Content Strategist",
            "SEO Specialist",
            "Brand Manager",
            "Growth Hacker"
        ]
    }
    
    return {
        "industry": industry,
        "trending_jobs": trending_by_industry.get(industry, trending_by_industry["Technology"])
    }
