import string
import random
from fastapi import APIRouter, HTTPException, status
from ...core.database import db
from ...models.login_code import LoginCode
from ...schemas.login_code import CodeCreate, CodeResponse

router = APIRouter()

def generate_random_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

@router.post("/generate-code", response_model=CodeResponse)
async def generate_code(request: CodeCreate):
    max_retries = 5
    for _ in range(max_retries):
        code = generate_random_code()
        existing = await db.db.login_codes.find_one({"code": code})
        if not existing:
            break
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate a unique code"
        )
    
    login_code = LoginCode(code=code, candidate_name=request.candidate_name)
    await db.db.login_codes.insert_one(login_code.dict())
    
    return login_code
