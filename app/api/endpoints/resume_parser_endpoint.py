from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_data_schema import ParseResumeRequest, ParseResumeResponse
from app.services.user_data_service import UserDataService
from app.api.dependencies.auth_dependency import require_admin
from typing import List

router = APIRouter()

@router.post("/parse", response_model=ParseResumeResponse, status_code=status.HTTP_201_CREATED)
async def parse_resume(request: ParseResumeRequest):
    """
    Parse resume and extract structured information
    
    Fetches resume PDF from applicants collection, extracts text,
    parses candidate information, and stores in user_data collection.
    
    - **applicantId**: ID of the applicant whose resume to parse
    
    Returns parsed candidate data including:
    - Full name, email, phone, LinkedIn URL
    - Skills, education, experience
    - Total years of experience
    """
    try:
        # Parse and store resume
        user_data = await UserDataService.parse_and_store_resume(request.applicantId)
        
        # Convert ObjectIds to strings
        user_data["_id"] = str(user_data["_id"])
        user_data["applicantId"] = str(user_data["applicantId"])
        
        # Don't return rawResumeText in response (too large)
        if "rawResumeText" in user_data:
            del user_data["rawResumeText"]
        
        return user_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while parsing resume: {str(e)}"
        )


@router.get("/parsed/{applicant_id}", response_model=ParseResumeResponse)
async def get_parsed_resume(applicant_id: str):
    """
    Get parsed resume data for an applicant
    
    Retrieves previously parsed resume data from user_data collection.
    
    - **applicant_id**: ID of the applicant
    """
    user_data = await UserDataService.get_parsed_data(applicant_id)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parsed resume data not found. Please parse the resume first."
        )
    
    # Convert ObjectIds to strings
    user_data["_id"] = str(user_data["_id"])
    user_data["applicantId"] = str(user_data["applicantId"])
    
    # Don't return rawResumeText in response
    if "rawResumeText" in user_data:
        del user_data["rawResumeText"]
    
    return user_data


@router.get("/my-candidates", response_model=List[ParseResumeResponse])
async def get_my_candidates(current_user: dict = Depends(require_admin)):
    try:
        # Get admin ID from token
        admin_id = str(current_user["_id"])
        
        # Fetch all user data for this admin
        user_data_list = await UserDataService.get_user_data_by_admin(admin_id)
        
        # Convert ObjectIds to strings and remove rawResumeText
        for user_data in user_data_list:
            user_data["_id"] = str(user_data["_id"])
            user_data["applicantId"] = str(user_data["applicantId"])
            
            # Don't return rawResumeText in response (too large)
            if "rawResumeText" in user_data:
                del user_data["rawResumeText"]
        
        return user_data_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching candidates: {str(e)}"
        )
