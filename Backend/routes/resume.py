from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
from models.resume_model import ResumeCreate, ResumeUpdate, ResumeResponse, ResumeInDB
from database.connection import get_database
from routes.auth import get_current_user

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(resume: ResumeCreate, current_user: dict = Depends(get_current_user)):
    """Create a new resume"""
    db = get_database()
    
    # Create resume document
    resume_dict = resume.model_dump()
    resume_dict["user_id"] = str(current_user["_id"])
    resume_dict["created_at"] = datetime.utcnow()
    resume_dict["updated_at"] = datetime.utcnow()
    resume_dict["version"] = 1
    resume_dict["ats_score"] = None
    
    result = await db.resumes.insert_one(resume_dict)
    created_resume = await db.resumes.find_one({"_id": result.inserted_id})
    
    # Update user's resume_ids
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$push": {"resume_ids": str(result.inserted_id)}}
    )
    
    # Convert to response
    created_resume["id"] = str(created_resume["_id"])
    return ResumeResponse(**created_resume)


@router.get("/", response_model=List[ResumeResponse])
async def get_all_resumes(current_user: dict = Depends(get_current_user)):
    """Get all resumes for current user"""
    db = get_database()
    
    resumes = await db.resumes.find({"user_id": str(current_user["_id"])}).to_list(100)
    
    # Convert to response
    for resume in resumes:
        resume["id"] = str(resume["_id"])
    
    return [ResumeResponse(**resume) for resume in resumes]


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(resume_id: str, current_user: dict = Depends(get_current_user)):
    """Get a specific resume"""
    db = get_database()
    
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID"
        )
    
    resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Check ownership
    if resume["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resume"
        )
    
    resume["id"] = str(resume["_id"])
    return ResumeResponse(**resume)


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: str,
    resume_update: ResumeUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update a resume"""
    db = get_database()
    
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID"
        )
    
    # Find resume
    resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Check ownership
    if resume["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this resume"
        )
    
    # Update resume
    update_dict = resume_update.model_dump(exclude_unset=True)
    update_dict["updated_at"] = datetime.utcnow()
    update_dict["version"] = resume.get("version", 1) + 1
    
    await db.resumes.update_one(
        {"_id": ObjectId(resume_id)},
        {"$set": update_dict}
    )
    
    updated_resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    updated_resume["id"] = str(updated_resume["_id"])
    return ResumeResponse(**updated_resume)


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(resume_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a resume"""
    db = get_database()
    
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID"
        )
    
    # Find resume
    resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Check ownership
    if resume["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this resume"
        )
    
    # Delete resume
    await db.resumes.delete_one({"_id": ObjectId(resume_id)})
    
    # Remove from user's resume_ids
    await db.users.update_one(
        {"_id": current_user["_id"]},
        {"$pull": {"resume_ids": resume_id}}
    )
    
    return None
