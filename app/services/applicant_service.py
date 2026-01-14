from app.models.applicant import Applicant
from app.schemas.applicant_schema import ApplicantCreate, ApplicantResponse
from app.services.job_service import JobService
from app.services.resume_parser import ResumeParser
from app.models.user_data import UserData
from fastapi import HTTPException, status, UploadFile
from app.core.database import db
from typing import Optional
from bson import ObjectId

class ApplicantService:

    @staticmethod
    async def create_application(
        job_id: str,
        applicant_data: ApplicantCreate,
        resume_file: UploadFile,
        admin_id: str  # Admin ID from JWT token
    ) -> dict:
        
        job = await JobService.get_job_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        if not resume_file.content_type == "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume must be a PDF file"
            )
        
        resume_bytes = await resume_file.read()
        
        if len(resume_bytes) > 5 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Resume file size must not exceed 5MB"
            )
        
        applicant = Applicant(
            jobId=job_id,
            jobTitle=job["jobTitle"],
            linkedinUrl=str(applicant_data.linkedinUrl) if applicant_data.linkedinUrl else None,
            resume=resume_bytes,
            adminId=admin_id  # Store admin ID
        )
        
        applicants_collection = db.db["applicants"]
        result = await applicants_collection.insert_one(applicant.to_dict())
        
        created_applicant = await applicants_collection.find_one(
            {"_id": result.inserted_id},
            {"resume": 0}  # Exclude binary resume from response
        )
        
        try:
            applicant_id = str(result.inserted_id)
            
            parsed_data = ResumeParser.parse_resume(resume_bytes)
            
            user_data = UserData(
                applicantId=ObjectId(applicant_id),
                fullName=parsed_data["fullName"],
                email=parsed_data["email"],
                phone=parsed_data["phone"],
                linkedinUrl=parsed_data["linkedinUrl"],
                skills=parsed_data["skills"],
                education=parsed_data["education"],
                experience=parsed_data["experience"],
                totalExperienceYears=parsed_data["totalExperienceYears"],
                rawResumeText=parsed_data["rawResumeText"],
                adminId=admin_id  # Store admin ID in user_data
            )
            
            user_data_collection = db.db["user_data"]
            await user_data_collection.insert_one(user_data.to_dict())
            
            print(f"✅ Resume parsed automatically for applicant: {applicant_id}")
        
        except Exception as e:
            print(f"⚠️ Resume parsing failed for applicant {applicant_id}: {str(e)}")
        
        return created_applicant
