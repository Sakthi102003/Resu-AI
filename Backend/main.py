import sys
import os

# Add the parent directory to Python path for proper imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from bson import ObjectId
import io

from config import settings
from database.connection import Database
from routes import auth, resume, ai_enhance, chat, job_recommend, templates
from utils.pdf_generator import generate_pdf_resume
from utils.docx_generator import generate_docx_resume
from utils.resume_parser import parse_pdf_resume, parse_docx_resume
from templates.template_manager import TemplateManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events for startup and shutdown"""
    # Startup
    await Database.connect_db()
    yield
    # Shutdown
    await Database.close_db()


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Chat-Based Resume Builder",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Include routers
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(chat.router)
app.include_router(ai_enhance.router)
app.include_router(job_recommend.router)
app.include_router(templates.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ResuAI API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/resume/export/pdf")
async def export_pdf(
    resume_id: str,
    template: str = None,  # Optional override, uses resume's stored template by default
    current_user: dict = Depends(auth.get_current_user)
):
    """Export resume as PDF - uses resume's stored template by default"""
    db = Database.get_db()
    
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID"
        )
    
    resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    
    if not resume or resume["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Use resume's stored template, or override if specified
    selected_template = template or resume.get("template", "auto_cv")
    
    # Use new template system
    try:
        pdf_buffer = TemplateManager.generate_resume(
            resume_data=resume["data"],
            template_name=selected_template,
            theme_color=resume.get("theme_color", "#3B82F6")
        )
    except Exception as e:
        # Fallback to old system if template fails
        pdf_buffer = generate_pdf_resume(
            resume["data"],
            template=resume.get("template", "modern"),
            theme_color=resume.get("theme_color", "#3B82F6")
        )
    
    # Return as streaming response
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={resume.get('title', 'resume')}.pdf"
        }
    )


@app.post("/resume/export/docx")
async def export_docx(
    resume_id: str,
    current_user: dict = Depends(auth.get_current_user)
):
    """Export resume as DOCX"""
    db = Database.get_db()
    
    if not ObjectId.is_valid(resume_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid resume ID"
        )
    
    resume = await db.resumes.find_one({"_id": ObjectId(resume_id)})
    
    if not resume or resume["user_id"] != str(current_user["_id"]):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Generate DOCX
    docx_buffer = generate_docx_resume(
        resume["data"],
        template=resume.get("template", "modern"),
        theme_color=resume.get("theme_color", "#3B82F6")
    )
    
    # Return as streaming response
    return StreamingResponse(
        docx_buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={
            "Content-Disposition": f"attachment; filename={resume.get('title', 'resume')}.docx"
        }
    )


@app.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: dict = Depends(auth.get_current_user)
):
    """Upload and parse existing resume"""
    
    # Check file type
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF and DOCX files are supported"
        )
    
    # Save file temporarily
    content = await file.read()
    temp_path = f"/tmp/{file.filename}"
    
    with open(temp_path, "wb") as f:
        f.write(content)
    
    # Parse based on file type
    try:
        if file.filename.endswith('.pdf'):
            parsed_data = parse_pdf_resume(temp_path)
        else:
            parsed_data = parse_docx_resume(temp_path)
        
        return {
            "message": "Resume parsed successfully",
            "data": parsed_data,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse resume: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
