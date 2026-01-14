import os
import shutil
import httpx
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from bson import ObjectId
from ...core.database import db
from ...schemas.login_code import CodeValidate, ValidationResponse
from datetime import datetime

router = APIRouter()

# Ensure recordings directory exists
RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

@router.post("/validate-code", response_model=ValidationResponse)
async def validate_code(request: CodeValidate):
    code_doc = await db.db.login_codes.find_one({"code": request.code})
    
    if not code_doc:
        return ValidationResponse(valid=False, message="Invalid login code")
    
    if code_doc["is_used"]:
        return ValidationResponse(valid=False, message="This code has already been used")
    
    # Mark as used
    await db.db.login_codes.update_one(
        {"code": request.code},
        {
            "$set": {
                "is_used": True,
                "used_at": datetime.utcnow()
            }
        }
    )
    
    return ValidationResponse(
        valid=True, 
        message="Code validated successfully",
        candidate_name=code_doc.get("candidate_name"),
        uid=str(code_doc["_id"])
    )

from retell import Retell
from ...core.config import settings

retell = Retell(api_key=settings.RETELL_API_KEY)

@router.post("/retell/create-web-call")
async def create_retell_web_call():
    try:
        # Check if API key is set
        if not settings.RETELL_API_KEY:
            # Fallback to the proxy if API key is not provided, 
            # but warn that this is not the official way.
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://agent.intelligens.app/api/retell/create-web-call",
                    json={"agentId": "agent_9f1f95bdc1e8caef6c4d35080a"}
                )
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail="Failed to connect to interview service"
                    )
                return response.json()

        # Official Retell SDK call
        call_response = retell.call.create_web_call(
            agent_id="agent_9f1f95bdc1e8caef6c4d35080a"
        )
        return {
            "access_token": call_response.access_token,
            "call_id": call_response.call_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/save-recording")
async def save_recording(
    file: UploadFile = File(...), 
    candidate_name: str = Form("unknown"),
    uid: str = Form("unknown")
):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{candidate_name}_{timestamp}.mp4"
        
        # Initialize GridFS
        fs = AsyncIOMotorGridFSBucket(db.db)
        
        # Upload to GridFS
        file_id = await fs.upload_from_stream(
            filename,
            file.file,
            metadata={"candidate_name": candidate_name, "uid": uid}
        )
        
        # Save metadata to MongoDB
        recording_doc = {
            "candidate_name": candidate_name,
            "uid": uid,
            "filename": filename,
            "gridfs_id": file_id,
            "created_at": datetime.utcnow()
        }
        result = await db.db.video_recording.insert_one(recording_doc)
        recording_id = str(result.inserted_id)
        
        # Unique URL for the recording
        recording_url = f"/api/recordings/{recording_id}"
        
        await db.db.video_recording.update_one(
            {"_id": result.inserted_id},
            {"$set": {"url": recording_url}}
        )
            
        return {
            "message": "Recording saved successfully", 
            "filename": filename,
            "recording_id": recording_id,
            "url": recording_url
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save recording: {str(e)}"
        )

@router.get("/recordings/{recording_id}")
async def get_recording(recording_id: str):
    try:
        # Get metadata
        recording = await db.db.video_recording.find_one({"_id": ObjectId(recording_id)})
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        # Initialize GridFS
        fs = AsyncIOMotorGridFSBucket(db.db)
        
        # Open download stream
        grid_out = await fs.open_download_stream(recording["gridfs_id"])
        
        return StreamingResponse(
            grid_out,
            media_type="video/mp4",
            headers={"Content-Disposition": f"inline; filename={recording['filename']}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve recording: {str(e)}"
        )

@router.get("/recordings")
async def list_recordings():
    try:
        # Get all recordings from MongoDB
        recordings = []
        cursor = db.db.video_recording.find().sort("created_at", -1)
        
        async for recording in cursor:
            recordings.append({
                "id": str(recording["_id"]),
                "candidate_name": recording.get("candidate_name", "Unknown"),
                "filename": recording.get("filename", ""),
                "url": recording.get("url", ""),
                "created_at": recording.get("created_at").isoformat() if recording.get("created_at") else None,
                "uid": recording.get("uid", "")
            })
        
        return {"recordings": recordings, "total": len(recordings)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list recordings: {str(e)}"
        )

@router.delete("/recordings/{recording_id}")
async def delete_recording(recording_id: str):
    try:
        # Get recording metadata
        recording = await db.db.video_recording.find_one({"_id": ObjectId(recording_id)})
        if not recording:
            raise HTTPException(status_code=404, detail="Recording not found")
        
        # Initialize GridFS
        fs = AsyncIOMotorGridFSBucket(db.db)
        
        # Delete file from GridFS
        gridfs_id = recording.get("gridfs_id")
        if gridfs_id:
            try:
                await fs.delete(gridfs_id)
            except Exception as e:
                print(f"Warning: Failed to delete GridFS file: {e}")
        
        # Delete metadata from MongoDB
        await db.db.video_recording.delete_one({"_id": ObjectId(recording_id)})
        
        return {
            "message": "Recording deleted successfully",
            "recording_id": recording_id,
            "filename": recording.get("filename", "")
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete recording: {str(e)}"
        )
