from fastapi import APIRouter, HTTPException, status
from app.schemas.result_schema import ResultCreate, ResultResponse
from app.services.result_service import ResultService
from typing import List

router = APIRouter()

@router.post("/", response_model=ResultResponse, status_code=status.HTTP_201_CREATED)
async def create_result(result_data: ResultCreate):
    
    try:
        result = await ResultService.create_result(result_data)
        
        result["_id"] = str(result["_id"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating result: {str(e)}"
        )

@router.get("/", response_model=List[ResultResponse])
async def get_all_results():
    
    try:
        results = await ResultService.get_all_results()
        
        for result in results:
            result["_id"] = str(result["_id"])
        
        return results
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching results: {str(e)}"
        )

@router.get("/{result_id}", response_model=ResultResponse)
async def get_result(result_id: str):
    
    result = await ResultService.get_result_by_id(result_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found"
        )
    
    result["_id"] = str(result["_id"])
    
    return result
