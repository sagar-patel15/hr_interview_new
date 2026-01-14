from datetime import datetime
from typing import Optional, List
from bson import ObjectId

class UserData:
    """User data model for parsed resume information"""
    
    def __init__(
        self,
        applicantId: ObjectId,
        rawResumeText: str,
        adminId: str,  # ID of admin who created the application
        fullName: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        linkedinUrl: Optional[str] = None,
        skills: Optional[List[str]] = None,
        education: Optional[List[dict]] = None,
        experience: Optional[List[dict]] = None,
        totalExperienceYears: Optional[float] = None,
        _id: Optional[ObjectId] = None,
        createdAt: Optional[datetime] = None
    ):
        self._id = _id or ObjectId()
        self.applicantId = applicantId
        self.fullName = fullName
        self.email = email
        self.phone = phone
        self.linkedinUrl = linkedinUrl
        self.skills = skills or []
        self.education = education or []
        self.experience = experience or []
        self.totalExperienceYears = totalExperienceYears
        self.rawResumeText = rawResumeText
        self.adminId = adminId
        self.createdAt = createdAt or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert user data object to dictionary for MongoDB"""
        return {
            "_id": self._id,
            "applicantId": self.applicantId,
            "fullName": self.fullName,
            "email": self.email,
            "phone": self.phone,
            "linkedinUrl": self.linkedinUrl,
            "skills": self.skills,
            "education": self.education,
            "experience": self.experience,
            "totalExperienceYears": self.totalExperienceYears,
            "rawResumeText": self.rawResumeText,
            "adminId": self.adminId,
            "createdAt": self.createdAt
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'UserData':
        """Create user data object from MongoDB document"""
        return UserData(
            _id=data.get("_id"),
            applicantId=data["applicantId"],
            fullName=data.get("fullName"),
            email=data.get("email"),
            phone=data.get("phone"),
            linkedinUrl=data.get("linkedinUrl"),
            skills=data.get("skills", []),
            education=data.get("education", []),
            experience=data.get("experience", []),
            totalExperienceYears=data.get("totalExperienceYears"),
            rawResumeText=data.get("rawResumeText", ""),
            adminId=data["adminId"],
            createdAt=data.get("createdAt")
        )
