from app.models.user_data import UserData
from app.schemas.user_data_schema import ParsedResumeData
from app.services.resume_parser import ResumeParser
from app.core.database import db
from fastapi import HTTPException, status
from bson import ObjectId
from typing import Optional, List

class UserDataService:
    """Service for user data operations (parsed resumes)"""
    
    @staticmethod
    async def get_applicant_resume(applicant_id: str) -> Optional[bytes]:
        """
        Fetch resume binary from applicants collection
        Args:
            applicant_id: Applicant ID
        Returns:
            Resume binary data or None if not found
        """
        if not ObjectId.is_valid(applicant_id):
            return None
        
        applicants_collection = db.db["applicants"]
        applicant = await applicants_collection.find_one(
            {"_id": ObjectId(applicant_id)},
            {"resume": 1}  # Only fetch resume field
        )
        
        if not applicant or "resume" not in applicant:
            return None
        
        return applicant["resume"]
    
    @staticmethod
    async def parse_and_store_resume(applicant_id: str) -> dict:
        """
        Parse resume and store in user_data collection
        Args:
            applicant_id: Applicant ID to parse resume for
        Returns:
            Parsed user data document
        """
        # Step 1: Fetch resume binary
        resume_binary = await UserDataService.get_applicant_resume(applicant_id)
        
        if not resume_binary:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Applicant or resume not found"
            )
        
        # Step 2: Parse resume
        parsed_data = ResumeParser.parse_resume(resume_binary)
        
        # Step 3: Create user data object
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
            rawResumeText=parsed_data["rawResumeText"]
        )
        
        # Step 4: Store in database
        user_data_collection = db.db["user_data"]
        
        # Check if already parsed (optional: allow re-parsing)
        existing = await user_data_collection.find_one({"applicantId": ObjectId(applicant_id)})
        
        if existing:
            # Update existing record
            await user_data_collection.update_one(
                {"applicantId": ObjectId(applicant_id)},
                {"$set": user_data.to_dict()}
            )
            result = await user_data_collection.find_one({"applicantId": ObjectId(applicant_id)})
        else:
            # Insert new record
            result = await user_data_collection.insert_one(user_data.to_dict())
            result = await user_data_collection.find_one({"_id": result.inserted_id})
        
        return result
    
    @staticmethod
    async def get_parsed_data(applicant_id: str) -> Optional[dict]:
        """
        Get parsed data for an applicant
        Args:
            applicant_id: Applicant ID
        Returns:
            Parsed user data or None if not found
        """
        if not ObjectId.is_valid(applicant_id):
            return None
        
        user_data_collection = db.db["user_data"]
        user_data = await user_data_collection.find_one(
            {"applicantId": ObjectId(applicant_id)}
        )
        
        return user_data
    
    @staticmethod
    async def get_user_data_by_admin(admin_id: str) -> List[dict]:
        """
        Get all user data (parsed resumes) created by a specific admin
        Args:
            admin_id: Admin ID (as string)
        Returns:
            List of user data documents
        """
        user_data_collection = db.db["user_data"]
        
        # Query by adminId (stored as string)
        cursor = user_data_collection.find({"adminId": admin_id})
        user_data_list = await cursor.to_list(length=1000)  # Max 1000 results
        
        return user_data_list
