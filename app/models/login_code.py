from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class LoginCode(BaseModel):
    code: str
    is_used: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    used_at: Optional[datetime] = None
    candidate_name: Optional[str] = None
