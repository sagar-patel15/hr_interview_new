from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
from app.models.enum import UserRole, UserStatus

class UserCreate(BaseModel):
    
    full_name: str = Field(..., min_length=2, description="Full name of the user")
    email: EmailStr = Field(..., description="Email address")
    mobile_number: str = Field(..., description="Mobile number (10 digits)")
    profile_photo: Optional[str] = Field(None, description="Profile photo URL (optional)")
    password: str = Field(..., min_length=8, description="Password (minimum 8 characters)")
    confirm_password: str = Field(..., description="Confirm password")
    role: UserRole = Field(default=UserRole.admin, description="User role")
    status: UserStatus = Field(default=UserStatus.active, description="User status")
    company_name: str = Field(..., min_length=2, description="Company name")
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        return v.strip()
    
    @field_validator('mobile_number')
    @classmethod
    def validate_mobile_number(cls, v: str) -> str:
        cleaned = v.replace(' ', '').replace('-', '')
        if not cleaned.isdigit():
            raise ValueError('Mobile number must contain only digits')
        if len(cleaned) != 10:
            raise ValueError('Mobile number must be exactly 10 digits')
        return cleaned
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @field_validator('company_name')
    @classmethod
    def validate_company_name(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError('Company name must be at least 2 characters long')
        return v.strip()
    
    @model_validator(mode='after')
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "mobile_number": "9876543210",
                "profile_photo": "https://example.com/photo.jpg",
                "password": "securepass123",
                "confirm_password": "securepass123",
                "role": "admin",
                "status": "active",
                "company_name": "Tech Corp"
            }
        }

class UserLogin(BaseModel):
    
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "securepass123"
            }
        }

class UserResponse(BaseModel):
    
    id: str = Field(..., alias="_id", description="User ID")
    full_name: str
    email: EmailStr
    mobile_number: str
    profile_photo: Optional[str] = None
    role: UserRole
    status: UserStatus
    company_name: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "mobile_number": "9876543210",
                "profile_photo": "https://example.com/photo.jpg",
                "role": "admin",
                "status": "active",
                "company_name": "Tech Corp",
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }

class Token(BaseModel):
    
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    
    email: Optional[str] = None
    user_id: Optional[str] = None
    role: Optional[str] = None

class LoginResponse(BaseModel):
    
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "_id": "507f1f77bcf86cd799439011",
                    "full_name": "John Doe",
                    "email": "john.doe@example.com",
                    "mobile_number": "9876543210",
                    "role": "admin",
                    "status": "active",
                    "company_name": "Tech Corp"
                }
            }
        }
