from fastapi import APIRouter, Request, Query
import httpx
from config import NOTIFICATION_SERVICE_URL

router = APIRouter()

@router.post("/send")
async def send_notification(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{NOTIFICATION_SERVICE_URL}/notify/send", json=body)
        return response.json()

@router.get("/user/{user_id}")
async def get_user_notifications(user_id: str, unread_only: bool = Query(False)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{NOTIFICATION_SERVICE_URL}/notify/user/{user_id}",
            params={"unread_only": unread_only}
        )
        return response.json()

@router.patch("/{notification_id}/read")
async def mark_as_read(notification_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{NOTIFICATION_SERVICE_URL}/notify/{notification_id}/read")
        return response.json()