from fastapi import APIRouter, HTTPException, status, UploadFile, File, Query
from fastapi.responses import FileResponse
from datetime import datetime
from bson import ObjectId
import os
import uuid
from database import media_collection
from config import UPLOAD_DIR, MAX_FILE_SIZE, ALLOWED_EXTENSIONS
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

def get_file_extension(filename: str) -> str:
    return filename.split(".")[-1].lower() if "." in filename else ""

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    ticket_id: str = Query(None),
    user_id: str = Query(...)
):
    logger.info(f"Uploading file: {file.filename}")
    
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided"
        )
    
    file_extension = get_file_extension(file.filename)
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File too large. Max size: {MAX_FILE_SIZE} bytes"
        )
    
    file_id = str(uuid.uuid4())
    file_name = f"{file_id}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, file_name)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    media_doc = {
        "file_id": file_id,
        "filename": file.filename,
        "stored_filename": file_name,
        "url": f"/media/{file_id}",
        "ticket_id": ticket_id,
        "uploaded_by": user_id,
        "size": len(contents),
        "content_type": file.content_type,
        "created_at": datetime.utcnow()
    }
    
    await media_collection.insert_one(media_doc)
    
    return {
        "file_id": file_id,
        "filename": file.filename,
        "url": f"/media/{file_id}",
        "size": len(contents)
    }

@router.get("/{file_id}")
async def get_file(file_id: str):
    logger.info(f"Retrieving file: {file_id}")
    
    media_doc = await media_collection.find_one({"file_id": file_id})
    
    if not media_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    file_path = os.path.join(UPLOAD_DIR, media_doc["stored_filename"])
    
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )
    
    return FileResponse(
        file_path,
        media_type=media_doc.get("content_type", "application/octet-stream"),
        filename=media_doc["filename"]
    )

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    logger.info(f"Deleting file: {file_id}")
    
    media_doc = await media_collection.find_one({"file_id": file_id})
    
    if not media_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    file_path = os.path.join(UPLOAD_DIR, media_doc["stored_filename"])
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    await media_collection.delete_one({"file_id": file_id})
    
    return {"message": "File deleted successfully"}