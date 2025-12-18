from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from bson import ObjectId
import json
from database.connection import get_database
from routes.auth import get_current_user
from config import settings

# AI imports
try:
    import openai
    openai.api_key = settings.OPENAI_API_KEY
except ImportError:
    openai = None

try:
    import google.generativeai as genai
    if settings.GEMINI_API_KEY:
        genai.configure(api_key=settings.GEMINI_API_KEY)
except ImportError:
    genai = None

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = None


class ChatRequest(BaseModel):
    message: str
    resume_id: Optional[str] = None
    context: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    response: str
    resume_data: Optional[Dict[str, Any]] = None
    action: Optional[str] = None  # "update", "create", "none"


# System prompt for the AI assistant
SYSTEM_PROMPT = """You are ResuAI, an expert resume-building AI assistant. Your job is to help users create professional, ATS-optimized resumes through natural conversation.

GUIDELINES:
1. Ask guided questions to extract structured information (experience, education, skills, etc.)
2. When users provide information, extract it into JSON format
3. Be professional but friendly and conversational
4. Provide actionable suggestions for improvement
5. Format content for maximum ATS compatibility
6. Use strong action verbs and quantifiable achievements
7. Keep responses concise and clear

AVAILABLE ACTIONS:
- Extract information and return structured JSON
- Enhance existing content (make it more professional, concise, or impactful)
- Add new sections or entries
- Remove or modify content
- Provide feedback and suggestions

When extracting resume data, return it in this JSON structure:
{
  "personal_info": {"name": "", "email": "", "phone": "", "location": "", "linkedin": "", "github": ""},
  "objective": "",
  "summary": "",
  "experience": [{"company": "", "position": "", "start_date": "", "end_date": "", "current": false, "achievements": []}],
  "education": [{"institution": "", "degree": "", "field_of_study": "", "start_date": "", "end_date": "", "grade": ""}],
  "skills": [],
  "projects": [{"name": "", "description": "", "technologies": [], "url": ""}],
  "certifications": [{"name": "", "issuer": "", "date": "", "url": ""}]
}

Always be helpful and guide users through the resume building process step by step."""


async def call_ai(messages: List[Dict[str, str]], provider: str = "openai") -> str:
    """Call AI API (OpenAI or Gemini)"""
    
    if provider == "openai" and openai:
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"OpenAI API error: {str(e)}"
            )
    
    elif provider == "gemini" and genai:
        try:
            model = genai.GenerativeModel('gemini-pro')
            # Convert messages to Gemini format
            prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Gemini API error: {str(e)}"
            )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service not configured. Please set OPENAI_API_KEY or GEMINI_API_KEY"
        )


def extract_json_from_response(text: str) -> Optional[Dict]:
    """Extract JSON from AI response if present"""
    try:
        # Look for JSON in code blocks
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            json_str = text[start:end].strip()
            return json.loads(json_str)
        
        # Look for JSON objects
        if "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            json_str = text[start:end]
            return json.loads(json_str)
        
        return None
    except:
        return None


@router.post("/respond", response_model=ChatResponse)
async def chat_respond(
    chat_request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Handle chat message and return AI response"""
    db = get_database()
    
    # Build conversation history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Add context from previous messages
    for msg in chat_request.context[-10:]:  # Last 10 messages for context
        messages.append({
            "role": msg.role,
            "content": msg.content
        })
    
    # Add current resume data if resume_id is provided
    resume_context = None
    if chat_request.resume_id:
        if ObjectId.is_valid(chat_request.resume_id):
            resume = await db.resumes.find_one({"_id": ObjectId(chat_request.resume_id)})
            if resume and resume["user_id"] == str(current_user["_id"]):
                resume_context = resume.get("data", {})
                messages.append({
                    "role": "system",
                    "content": f"Current resume data: {json.dumps(resume_context, default=str)}"
                })
    
    # Add user's message
    messages.append({
        "role": "user",
        "content": chat_request.message
    })
    
    # Get AI response
    ai_response = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    # Extract JSON data if present
    extracted_data = extract_json_from_response(ai_response)
    
    # Determine action
    action = "none"
    if extracted_data:
        action = "update"
    
    return ChatResponse(
        response=ai_response,
        resume_data=extracted_data,
        action=action
    )


@router.post("/enhance", response_model=Dict[str, str])
async def enhance_text(
    text: str,
    style: str = "professional",  # professional, concise, impactful
    current_user: dict = Depends(get_current_user)
):
    """Enhance a piece of text (description, summary, etc.)"""
    
    enhancement_prompts = {
        "professional": "Rewrite the following text to sound more professional and polished while maintaining the same meaning:",
        "concise": "Rewrite the following text to be more concise and impactful, removing unnecessary words:",
        "impactful": "Rewrite the following text to be more impactful using strong action verbs and quantifiable results:"
    }
    
    prompt = enhancement_prompts.get(style, enhancement_prompts["professional"])
    
    messages = [
        {"role": "system", "content": "You are an expert resume writer. Enhance the given text according to the instructions."},
        {"role": "user", "content": f"{prompt}\n\nText: {text}"}
    ]
    
    enhanced = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    return {"original": text, "enhanced": enhanced.strip()}


@router.post("/suggestions")
async def get_suggestions(
    resume_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get AI suggestions for improving a resume"""
    db = get_database()
    
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
    
    resume_data = resume.get("data", {})
    
    messages = [
        {"role": "system", "content": "You are an expert resume reviewer. Provide specific, actionable suggestions to improve this resume."},
        {"role": "user", "content": f"Review this resume and provide 5-7 specific suggestions for improvement:\n\n{json.dumps(resume_data, default=str)}"}
    ]
    
    suggestions = await call_ai(messages, provider=settings.AI_PROVIDER)
    
    return {"suggestions": suggestions}
