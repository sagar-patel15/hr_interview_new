from datetime import datetime
from typing import Optional
from bson import ObjectId

class Applicant:
    """Applicant model for MongoDB with Motor"""
    
    def __init__(
        self,
        jobId: str,
        jobTitle: str,
        linkedinUrl: Optional[str],
        resume: bytes,
        adminId: str,  # ID of admin who created this application
        _id: Optional[ObjectId] = None,
        createdAt: Optional[datetime] = None
    ):
        self._id = _id or ObjectId()
        self.jobId = jobId
        self.jobTitle = jobTitle
        self.linkedinUrl = linkedinUrl
        self.resume = resume
        self.adminId = adminId
        self.createdAt = createdAt or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert applicant object to dictionary for MongoDB"""
        return {
            "_id": self._id,
            "jobId": self.jobId,
            "jobTitle": self.jobTitle,
            "linkedinUrl": self.linkedinUrl,
            "resume": self.resume,
            "adminId": self.adminId,
            "createdAt": self.createdAt
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Applicant':
        """Create applicant object from MongoDB document"""
        return Applicant(
            _id=data.get("_id"),
            jobId=data["jobId"],
            jobTitle=data["jobTitle"],
            linkedinUrl=data.get("linkedinUrl"),
            resume=data["resume"],
            adminId=data["adminId"],
            createdAt=data.get("createdAt")
        )
