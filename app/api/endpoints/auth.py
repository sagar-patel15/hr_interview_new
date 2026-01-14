from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin, LoginResponse
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate):

    try:
        user = await AuthService.create_user(user_data)
        # Convert ObjectId to string for response
        user["_id"] = str(user["_id"])
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating user: {str(e)}"
        )

@router.post("/login", response_model=LoginResponse)
async def login(login_data: UserLogin):
    """
    Login with email and password
    
    Returns JWT access token and user information
    """
    try:
        result = await AuthService.login_user(login_data)
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during login: {str(e)}"
        )
