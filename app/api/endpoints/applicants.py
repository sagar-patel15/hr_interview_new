from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from app.schemas.applicant_schema import ApplicantCreate, ApplicantResponse
from app.services.applicant_service import ApplicantService
from app.api.dependencies.auth_dependency import require_admin
from pydantic import HttpUrl
from typing import Optional

router = APIRouter()

@router.post("/{job_id}/apply", response_model=ApplicantResponse, status_code=status.HTTP_201_CREATED)
async def apply_for_job(
    job_id: str,
    resume: UploadFile = File(...),
    linkedinUrl: Optional[str] = Form(None),
    current_user: dict = Depends(require_admin)
):

    try:
        validated_url = None
        if linkedinUrl:
            try:
                validated_url = HttpUrl(linkedinUrl)
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid LinkedIn URL format"
                )
        
        applicant_data = ApplicantCreate(linkedinUrl=validated_url)
        
        applicant = await ApplicantService.create_application(
            job_id,
            applicant_data,
            resume,
            str(current_user["_id"])  # Pass admin ID from JWT token
        )
        
        applicant["_id"] = str(applicant["_id"])
        
        return applicant
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while submitting application: {str(e)}"
        )
