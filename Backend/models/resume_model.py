from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    field: Optional[str] = None  # Alternative field name
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    graduation_date: Optional[str] = None  # Alternative date format
    grade: Optional[str] = None
    gpa: Optional[str] = None  # Alternative grade field
    description: Optional[str] = None


class Experience(BaseModel):
    company: str
    position: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current: bool = False
    description: Optional[Any] = None  # Can be str or List[str]
    achievements: List[str] = []


class Project(BaseModel):
    name: str
    description: Optional[str] = None
    technologies: List[str] = []
    url: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


class Certification(BaseModel):
    name: str
    issuer: str
    date: Optional[str] = None
    url: Optional[str] = None
    credential_id: Optional[str] = None


class SkillCategory(BaseModel):
    category: str
    items: List[str] = []


class ResumeData(BaseModel):
    personal_info: Dict[str, Any] = {}
    objective: Optional[str] = None
    summary: Optional[str] = None
    education: List[Education] = []
    experience: List[Experience] = []
    skills: List[Any] = []  # Can be List[str] or List[SkillCategory]
    projects: List[Project] = []
    certifications: List[Certification] = []
    languages: List[str] = []
    awards: List[str] = []
    custom_sections: Dict[str, Any] = {}


class ResumeCreate(BaseModel):
    title: str = "My Resume"
    data: ResumeData = ResumeData()
    template: str = "auto_cv"  # Updated default to match template system
    theme_color: str = "#3B82F6"


class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    data: Optional[ResumeData] = None
    template: Optional[str] = None
    theme_color: Optional[str] = None


class ResumeInDB(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: str
    title: str = "My Resume"
    data: ResumeData
    template: str = "auto_cv"  # Updated default to match template system
    theme_color: str = "#3B82F6"
    ats_score: Optional[int] = None
    version: int = 1
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ResumeResponse(BaseModel):
    id: str
    user_id: str
    title: str
    data: ResumeData
    template: str
    theme_color: str
    ats_score: Optional[int] = None
    version: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
