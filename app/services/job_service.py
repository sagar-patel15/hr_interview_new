from app.models.job import Job
from app.schemas.job_schema import JobCreate, JobResponse
from fastapi import HTTPException, status
from app.core.database import db
from typing import Optional, List
from bson import ObjectId

from datetime import datetime

class JobService:

    @staticmethod
    async def create_job(job_data: JobCreate, admin_id: str) -> dict:
        
        job = Job(
            jobTitle=job_data.jobTitle,
            jobDescription=job_data.jobDescription,
            employmentType=job_data.employmentType,
            experienceRequired=job_data.experienceRequired,
            jobLocation=job_data.jobLocation,
            workMode=job_data.workMode,
            vacancies=job_data.vacancies,
            createdBy=ObjectId(admin_id)
        )
        
        jobs_collection = db.db["jobs"]
        result = await jobs_collection.insert_one(job.to_dict())
        
        created_job = await jobs_collection.find_one({"_id": result.inserted_id})
        return created_job
    
    @staticmethod
    async def get_job_by_id(job_id: str) -> Optional[dict]:
        
        if not ObjectId.is_valid(job_id):
            return None
        
        jobs_collection = db.db["jobs"]
        job = await jobs_collection.find_one({
            "_id": ObjectId(job_id),
            "deletedAt": None
        })
        
        if job:
            applicants_collection = db.db["applicants"]
            count = await applicants_collection.count_documents({"jobId": job_id})
            job["totalCandidates"] = count
            
        return job
    
    @staticmethod
    async def get_all_jobs() -> List[dict]:
        jobs_collection = db.db["jobs"]
        applicants_collection = db.db["applicants"]
        
        jobs = await jobs_collection.find({"deletedAt": None}).to_list(length=100)
        
        for job in jobs:
            job_id_str = str(job["_id"])
            count = await applicants_collection.count_documents({"jobId": job_id_str})
            job["totalCandidates"] = count
            
        return jobs

    @staticmethod
    async def delete_job(job_id: str) -> bool:
        
        if not ObjectId.is_valid(job_id):
            return False
            
        jobs_collection = db.db["jobs"]
        
        result = await jobs_collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"deletedAt": datetime.utcnow()}}
        )
        
        return result.modified_count > 0
