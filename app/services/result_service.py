from app.models.result import Result
from app.schemas.result_schema import ResultCreate, ResultResponse
from app.core.database import db
from fastapi import HTTPException, status
from typing import List

class ResultService:
    """Service for interview result operations"""
    
    @staticmethod
    async def create_result(result_data: ResultCreate) -> dict:
        """Create a new interview result"""
        # Create result object
        result = Result(
            fullName=result_data.fullName,
            appliedRole=result_data.appliedRole,
            interviewDate=result_data.interviewDate,
            interviewDuration=result_data.interviewDuration,
            previousRejections=result_data.previousRejections,
            experienceLevel=result_data.experienceLevel,
            currentRole=result_data.currentRole,
            company=result_data.company,
            skills=result_data.skills,
            decision=result_data.decision,
            shortSummary=result_data.shortSummary,
            detailedSummary=result_data.detailedSummary,
            mode=result_data.mode,
            interviewer=result_data.interviewer,
            reviewDate=result_data.reviewDate,
            age=result_data.age,
            status=result_data.status,
            currentCTC=result_data.currentCTC,
            expectedCTC=result_data.expectedCTC,
            followUpNotes=result_data.followUpNotes,
            scoreTech=result_data.scoreTech,
            scoreProblemSolving=result_data.scoreProblemSolving,
            scoreCommunication=result_data.scoreCommunication,
            scoreSystemDesign=result_data.scoreSystemDesign,
            scoreCultureFit=result_data.scoreCultureFit,
            scoreRedFlags=result_data.scoreRedFlags,
            strengths=result_data.strengths,
            weaknesses=result_data.weaknesses
        )
        
        # Insert into database
        results_collection = db.db["results"]
        insert_result = await results_collection.insert_one(result.to_dict())
        
        # Get the created result
        created_result = await results_collection.find_one({"_id": insert_result.inserted_id})
        return created_result
    
    @staticmethod
    async def get_all_results() -> List[dict]:
        """Get all interview results"""
        results_collection = db.db["results"]
        results = await results_collection.find().to_list(length=1000)
        return results
    
    @staticmethod
    async def get_result_by_id(result_id: str) -> dict:
        """Get result by ID"""
        from bson import ObjectId
        
        if not ObjectId.is_valid(result_id):
            return None
        
        results_collection = db.db["results"]
        result = await results_collection.find_one({"_id": ObjectId(result_id)})
        return result
