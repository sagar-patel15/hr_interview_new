from app.models.user import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from passlib.context import CryptContext
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings
from app.core.database import db
from typing import Optional
from bson import ObjectId

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    """Authentication service for user management"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a plain text password (truncate to 72 bytes for bcrypt)"""
        # Bcrypt has a maximum password length of 72 bytes
        password_bytes = password.encode('utf-8')[:72]
        return pwd_context.hash(password_bytes.decode('utf-8'))
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash (truncate to 72 bytes for bcrypt)"""
        # Bcrypt has a maximum password length of 72 bytes
        password_bytes = plain_password.encode('utf-8')[:72]
        return pwd_context.verify(password_bytes.decode('utf-8'), hashed_password)
    
    @staticmethod
    async def get_user_by_email(email: str) -> Optional[dict]:
        """Get user by email from database"""
        users_collection = db.db["users"]
        user = await users_collection.find_one({"email": email})
        return user
    
    @staticmethod
    async def create_user(user_data: UserCreate) -> dict:
        """Create a new user in the database"""
        # Check if user already exists
        existing_user = await AuthService.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash the password
        hashed_password = AuthService.hash_password(user_data.password)
        
        # Create user object
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            mobile_number=user_data.mobile_number,
            password=hashed_password,
            company_name=user_data.company_name,
            role=user_data.role,
            status=user_data.status,
            profile_photo=user_data.profile_photo
        )
        
        # Insert into database
        users_collection = db.db["users"]
        result = await users_collection.insert_one(user.to_dict())
        
        # Get the created user
        created_user = await users_collection.find_one({"_id": result.inserted_id})
        return created_user
    
    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    async def authenticate_user(login_data: UserLogin) -> dict:
        """Authenticate user with email and password"""
        user = await AuthService.get_user_by_email(login_data.email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not AuthService.verify_password(login_data.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    
    @staticmethod
    async def login_user(login_data: UserLogin) -> dict:
        """Login user and return token with user data"""
        user = await AuthService.authenticate_user(login_data)
        
        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = AuthService.create_access_token(
            data={
                "sub": user["email"],
                "user_id": str(user["_id"]),
                "role": user["role"]
            },
            expires_delta=access_token_expires
        )
        
        # Convert ObjectId to string for response
        user["_id"] = str(user["_id"])
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user
        }
