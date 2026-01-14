from fastapi import APIRouter

router = APIRouter()
""" - Commented out
@router.get("/recordings")
async def list_recordings():
    recordings = await db.db.video_recording.find().to_list(100)
    for r in recordings:
        r["_id"] = str(r["_id"])
        if "gridfs_id" in r:
            r["gridfs_id"] = str(r["gridfs_id"])
    return recordings
"""
