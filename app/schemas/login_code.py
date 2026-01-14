from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CodeCreate(BaseModel):
    candidate_name: Optional[str] = None

class CodeValidate(BaseModel):
    code: str

class CodeResponse(BaseModel):
    code: str
    is_used: bool
    created_at: datetime
    candidate_name: Optional[str] = None

class ValidationResponse(BaseModel):
    valid: bool
    message: str
    candidate_name: Optional[str] = None
    uid: Optional[str] = None
