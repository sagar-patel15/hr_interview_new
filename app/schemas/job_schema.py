from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.enum import EmploymentType, WorkMode

class JobCreate(BaseModel):
    
    jobTitle: str = Field(..., min_length=3, description="Job title")
    jobDescription: str = Field(..., min_length=50, description="Full job description")
    employmentType: EmploymentType = Field(..., description="Employment type")
    experienceRequired: str = Field(..., min_length=3, description="Experience required (e.g., 2-5 years)")
    jobLocation: str = Field(..., min_length=3, description="Job location")
    workMode: WorkMode = Field(..., description="Work mode")
    vacancies: int = Field(..., ge=1, description="Number of vacancies")
    
    @field_validator('jobTitle')
    @classmethod
    def validate_job_title(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError('Job title must be at least 3 characters long')
        return v.strip()
    
    @field_validator('jobDescription')
    @classmethod
    def validate_job_description(cls, v: str) -> str:
        if not v or len(v.strip()) < 50:
            raise ValueError('Job description must be at least 50 characters long')
        return v.strip()
    
    @field_validator('experienceRequired')
    @classmethod
    def validate_experience(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError('Experience required must be at least 3 characters long')
        return v.strip()
    
    @field_validator('jobLocation')
    @classmethod
    def validate_location(cls, v: str) -> str:
        if not v or len(v.strip()) < 3:
            raise ValueError('Job location must be at least 3 characters long')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "jobTitle": "Backend Developer",
                "jobDescription": "We are looking for an experienced backend developer to join our team...",
                "employmentType": "full_time",
                "experienceRequired": "2-5 years",
                "jobLocation": "Remote",
                "workMode": "remote",
                "vacancies": 3
            }
        }

class JobResponse(BaseModel):
    
    id: str = Field(..., alias="_id", description="Job ID")
    jobTitle: str
    jobDescription: str
    employmentType: EmploymentType
    experienceRequired: str
    jobLocation: str
    workMode: WorkMode
    vacancies: int
    createdBy: str
    createdAt: datetime
    updatedAt: datetime
    totalCandidates: Optional[int] = 0
    
    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "jobTitle": "Backend Developer",
                "jobDescription": "We are looking for...",
                "employmentType": "full_time",
                "experienceRequired": "2-5 years",
                "jobLocation": "Remote",
                "workMode": "remote",
                "vacancies": 3,
                "createdBy": "507f1f77bcf86cd799439012",
                "createdAt": "2024-01-01T00:00:00",
                "updatedAt": "2024-01-01T00:00:00"
            }
        }
