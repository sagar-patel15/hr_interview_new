from pydantic import BaseModel, Field, field_validator, HttpUrl
from typing import Optional
from datetime import datetime

class ApplicantCreate(BaseModel):
    """Schema for creating an application"""
    linkedinUrl: Optional[HttpUrl] = Field(None, description="LinkedIn profile URL (optional)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "linkedinUrl": "https://linkedin.com/in/johndoe"
            }
        }


class ApplicantResponse(BaseModel):
    """Schema for applicant response"""
    id: str = Field(..., alias="_id", description="Application ID")
    jobId: str
    jobTitle: str
    linkedinUrl: Optional[str] = None
    adminId: str
    createdAt: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "jobId": "507f1f77bcf86cd799439012",
                "jobTitle": "Backend Developer",
                "linkedinUrl": "https://linkedin.com/in/johndoe",
                "adminId": "507f1f77bcf86cd799439099",
                "createdAt": "2024-01-01T00:00:00"
            }
        }
