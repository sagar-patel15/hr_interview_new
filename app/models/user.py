from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import Field
from app.models.enum import UserRole, UserStatus

class User:
    """User model for MongoDB with Motor"""
    
    def __init__(
        self,
        full_name: str,
        email: str,
        mobile_number: str,
        password: str,
        company_name: str,
        role: UserRole = UserRole.admin,
        status: UserStatus = UserStatus.active,
        profile_photo: Optional[str] = None,
        _id: Optional[ObjectId] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = _id or ObjectId()
        self.full_name = full_name
        self.email = email
        self.mobile_number = mobile_number
        self.password = password
        self.company_name = company_name
        self.role = role if isinstance(role, str) else role.value
        self.status = status if isinstance(status, str) else status.value
        self.profile_photo = profile_photo
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert user object to dictionary for MongoDB"""
        return {
            "_id": self._id,
            "full_name": self.full_name,
            "email": self.email,
            "mobile_number": self.mobile_number,
            "password": self.password,
            "company_name": self.company_name,
            "role": self.role,
            "status": self.status,
            "profile_photo": self.profile_photo,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'User':
        """Create user object from MongoDB document"""
        return User(
            _id=data.get("_id"),
            full_name=data["full_name"],
            email=data["email"],
            mobile_number=data["mobile_number"],
            password=data["password"],
            company_name=data["company_name"],
            role=data.get("role", UserRole.admin.value),
            status=data.get("status", UserStatus.active.value),
            profile_photo=data.get("profile_photo"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
