from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.job_schema import JobCreate, JobResponse
from app.services.job_service import JobService
from app.api.dependencies.auth_dependency import require_admin
from typing import List

router = APIRouter()

@router.post("/", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_data: JobCreate,
    current_user: dict = Depends(require_admin)
):
    try:
        job = await JobService.create_job(job_data, str(current_user["_id"]))
        # Convert ObjectId to string for response
        job["_id"] = str(job["_id"])
        job["createdBy"] = str(job["createdBy"])
        return job
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating job: {str(e)}"
        )


@router.get("/", response_model=List[JobResponse])
async def get_all_jobs():
    """
    Get all jobs
    
    Public endpoint - no authentication required
    """
    try:
        jobs = await JobService.get_all_jobs()
        # Convert ObjectIds to strings
        for job in jobs:
            job["_id"] = str(job["_id"])
            job["createdBy"] = str(job["createdBy"])
        return jobs
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching jobs: {str(e)}"
        )


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: str):
    """
    Get job by ID
    
    Public endpoint - no authentication required
    """
    job = await JobService.get_job_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    
    # Convert ObjectIds to strings
    job["_id"] = str(job["_id"])
    job["createdBy"] = str(job["createdBy"])
    return job


@router.delete("/{job_id}", status_code=status.HTTP_200_OK)
async def delete_job(
    job_id: str,
    current_user: dict = Depends(require_admin)
):

    try:
        # Check if job exists first
        job = await JobService.get_job_by_id(job_id)
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
            
        success = await JobService.delete_job(job_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found or already deleted"
            )
            
        return {"message": "Job deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting job: {str(e)}"
        )
