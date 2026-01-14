from datetime import datetime
from typing import Optional
from bson import ObjectId
from app.models.enum import EmploymentType, WorkMode

class Job:

    def __init__(
        self,
        jobTitle: str,
        jobDescription: str,
        employmentType: EmploymentType,
        experienceRequired: str,
        jobLocation: str,
        workMode: WorkMode,
        vacancies: int,
        createdBy: ObjectId,
        _id: Optional[ObjectId] = None,
        createdAt: Optional[datetime] = None,
        updatedAt: Optional[datetime] = None
    ):
        self._id = _id or ObjectId()
        self.jobTitle = jobTitle
        self.jobDescription = jobDescription
        self.employmentType = employmentType if isinstance(employmentType, str) else employmentType.value
        self.experienceRequired = experienceRequired
        self.jobLocation = jobLocation
        self.workMode = workMode if isinstance(workMode, str) else workMode.value
        self.vacancies = vacancies
        self.createdBy = createdBy
        self.createdAt = createdAt or datetime.utcnow()
        self.updatedAt = updatedAt or datetime.utcnow()
        self.deletedAt = None
    
    def to_dict(self) -> dict:
        
        return {
            "_id": self._id,
            "jobTitle": self.jobTitle,
            "jobDescription": self.jobDescription,
            "employmentType": self.employmentType,
            "experienceRequired": self.experienceRequired,
            "jobLocation": self.jobLocation,
            "workMode": self.workMode,
            "vacancies": self.vacancies,
            "createdBy": self.createdBy,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
            "deletedAt": self.deletedAt
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Job':
        
        job = Job(
            _id=data.get("_id"),
            jobTitle=data["jobTitle"],
            jobDescription=data["jobDescription"],
            employmentType=data["employmentType"],
            experienceRequired=data["experienceRequired"],
            jobLocation=data["jobLocation"],
            workMode=data["workMode"],
            vacancies=data["vacancies"],
            createdBy=data["createdBy"],
            createdAt=data.get("createdAt"),
            updatedAt=data.get("updatedAt")
        )
        job.deletedAt = data.get("deletedAt")
        return job
