from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user_data_schema import ParseResumeRequest, ParseResumeResponse
from app.services.user_data_service import UserDataService
from app.api.dependencies.auth_dependency import require_admin
from typing import List

router = APIRouter()

@router.post("/parse", response_model=ParseResumeResponse, status_code=status.HTTP_201_CREATED)
async def parse_resume(request: ParseResumeRequest):
    
    try:
        user_data = await UserDataService.parse_and_store_resume(request.applicantId)
        
        user_data["_id"] = str(user_data["_id"])
        user_data["applicantId"] = str(user_data["applicantId"])
        
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
    
    user_data = await UserDataService.get_parsed_data(applicant_id)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parsed resume data not found. Please parse the resume first."
        )
    
    user_data["_id"] = str(user_data["_id"])
    user_data["applicantId"] = str(user_data["applicantId"])
    
    if "rawResumeText" in user_data:
        del user_data["rawResumeText"]
    
    return user_data

@router.get("/my-candidates", response_model=List[ParseResumeResponse])
async def get_my_candidates(current_user: dict = Depends(require_admin)):
    try:
        admin_id = str(current_user["_id"])
        
        user_data_list = await UserDataService.get_user_data_by_admin(admin_id)
        
        for user_data in user_data_list:
            user_data["_id"] = str(user_data["_id"])
            user_data["applicantId"] = str(user_data["applicantId"])
            
            if "rawResumeText" in user_data:
                del user_data["rawResumeText"]
        
        return user_data_list
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching candidates: {str(e)}"
        )
