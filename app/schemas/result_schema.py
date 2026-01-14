from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Union

class ResultCreate(BaseModel):
    """Schema for creating an interview result"""
    fullName: str = Field(..., min_length=2)
    appliedRole: str
    interviewDate: Union[datetime, str]  # Can be datetime or string like "Not discussed"
    interviewDuration: str
    previousRejections: int = Field(..., ge=0)
    experienceLevel: str
    currentRole: str
    company: str
    skills: str
    decision: str
    shortSummary: str
    detailedSummary: str
    mode: str
    interviewer: str
    reviewDate: Union[datetime, str]  # Can be datetime or string
    age: int = Field(..., ge=18, le=100)
    status: str
    currentCTC: str
    expectedCTC: str
    followUpNotes: str
    scoreTech: int = Field(..., ge=0, le=10)
    scoreProblemSolving: int = Field(..., ge=0, le=10)
    scoreCommunication: int = Field(..., ge=0, le=10)
    scoreSystemDesign: int = Field(..., ge=0, le=10)
    scoreCultureFit: int = Field(..., ge=0, le=10)
    scoreRedFlags: int = Field(..., ge=0, le=10)
    strengths: str
    weaknesses: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "fullName": "Uma Sharma",
                "appliedRole": "Senior Developer",
                "interviewDate": "2025-09-10T00:00:00.000Z",
                "interviewDuration": "Approximately 15 minutes",
                "previousRejections": 0,
                "experienceLevel": "Senior (6+ years)",
                "currentRole": "Senior Developer (Full-stack)",
                "company": "Not discussed",
                "skills": "React.js|Redux|Node.js",
                "decision": "MAYBE",
                "shortSummary": "Strong technical skills",
                "detailedSummary": "Detailed assessment...",
                "mode": "Phone",
                "interviewer": "Emma (AI Agent)",
                "reviewDate": "2025-12-06T00:00:00.000Z",
                "age": 34,
                "status": "Further Review",
                "currentCTC": "Not discussed",
                "expectedCTC": "Not discussed",
                "followUpNotes": "Clarify experience",
                "scoreTech": 7,
                "scoreProblemSolving": 6,
                "scoreCommunication": 7,
                "scoreSystemDesign": 8,
                "scoreCultureFit": 6,
                "scoreRedFlags": 0,
                "strengths": "Strong technical knowledge",
                "weaknesses": "Communication gaps"
            }
        }


class ResultResponse(BaseModel):
    """Schema for result response"""
    id: str = Field(..., alias="_id")
    fullName: str
    appliedRole: str
    interviewDate: Union[datetime, str]  # Can be datetime or string
    interviewDuration: str
    previousRejections: int
    experienceLevel: str
    currentRole: str
    company: str
    skills: str
    decision: str
    shortSummary: str
    detailedSummary: str
    mode: str
    interviewer: str
    reviewDate: Union[datetime, str]  # Can be datetime or string
    age: int
    status: str
    currentCTC: str
    expectedCTC: str
    followUpNotes: str
    scoreTech: int
    scoreProblemSolving: int
    scoreCommunication: int
    scoreSystemDesign: int
    scoreCultureFit: int
    scoreRedFlags: int
    strengths: str
    weaknesses: str
    createdAt: Optional[datetime] = None  # Optional for backward compatibility
    
    class Config:
        from_attributes = True
        populate_by_name = True
