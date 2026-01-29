from fastapi import APIRouter, UploadFile, File, Query
from typing import Optional
import httpx
from config import MEDIA_SERVICE_URL

router = APIRouter()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = Query(...),
    ticket_id: Optional[str] = Query(None)
):
    async with httpx.AsyncClient() as client:
        files = {"file": (file.filename, await file.read(), file.content_type)}
        params = {"user_id": user_id}
        if ticket_id:
            params["ticket_id"] = ticket_id
        
        response = await client.post(
            f"{MEDIA_SERVICE_URL}/media/upload",
            files=files,
            params=params
        )
        return response.json()

@router.get("/{file_id}")
async def get_file(file_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MEDIA_SERVICE_URL}/media/{file_id}")
        return response.content

@router.delete("/{file_id}")
async def delete_file(file_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{MEDIA_SERVICE_URL}/media/{file_id}")
        return response.json()