from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class EducationItem(BaseModel):
    """Schema for education entry"""
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "degree": "B.Tech in Computer Science",
                "institution": "IIT Delhi",
                "year": "2015-2019"
            }
        }


class ExperienceItem(BaseModel):
    """Schema for experience entry"""
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "company": "Google",
                "role": "Software Engineer",
                "duration": "2020-2023",
                "description": "Worked on backend systems"
            }
        }


class ParsedResumeData(BaseModel):
    """Schema for parsed resume data"""
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedinUrl: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    totalExperienceYears: Optional[float] = None
    rawResumeText: str


class ParseResumeRequest(BaseModel):
    """Schema for parse resume request"""
    applicantId: str = Field(..., description="Applicant ID to parse resume for")
    
    class Config:
        json_schema_extra = {
            "example": {
                "applicantId": "507f1f77bcf86cd799439011"
            }
        }


class ParseResumeResponse(BaseModel):
    """Schema for parse resume response"""
    id: str = Field(..., alias="_id", description="User data ID")
    applicantId: str
    fullName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedinUrl: Optional[str] = None
    skills: List[str]
    education: List[EducationItem]
    experience: List[ExperienceItem]
    totalExperienceYears: Optional[float] = None
    createdAt: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439013",
                "applicantId": "507f1f77bcf86cd799439011",
                "fullName": "John Doe",
                "email": "john.doe@example.com",
                "phone": "9876543210",
                "linkedinUrl": "https://linkedin.com/in/johndoe",
                "skills": ["Python", "FastAPI", "MongoDB"],
                "education": [],
                "experience": [],
                "totalExperienceYears": 3.5,
                "createdAt": "2024-01-13T00:00:00"
            }
        }
