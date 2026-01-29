from fastapi import APIRouter, Request, Query
from typing import Optional
import httpx
from config import TICKET_SERVICE_URL

router = APIRouter()

@router.post("/create")
async def create_ticket(request: Request, user_id: str = Query(...)):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(
            f"{TICKET_SERVICE_URL}/tickets/create",
            json=body,
            params={"user_id": user_id}
        )
        return response.json()

@router.get("/list")
async def get_tickets(
    tenant_id: Optional[str] = None,
    user_id: Optional[str] = None,
    status: Optional[str] = None
):
    async with httpx.AsyncClient() as client:
        params = {}
        if tenant_id:
            params["tenant_id"] = tenant_id
        if user_id:
            params["user_id"] = user_id
        if status:
            params["status"] = status
        
        response = await client.get(f"{TICKET_SERVICE_URL}/tickets/list", params=params)
        return response.json()

@router.get("/{ticket_id}")
async def get_ticket(ticket_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{TICKET_SERVICE_URL}/tickets/{ticket_id}")
        return response.json()

@router.patch("/{ticket_id}")
async def update_ticket(ticket_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.patch(f"{TICKET_SERVICE_URL}/tickets/{ticket_id}", json=body)
        return response.json()

@router.post("/{ticket_id}/comments")
async def add_comment(ticket_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{TICKET_SERVICE_URL}/tickets/{ticket_id}/comments", json=body)
        return response.json()

@router.post("/{ticket_id}/feedback")
async def add_feedback(ticket_id: str, request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{TICKET_SERVICE_URL}/tickets/{ticket_id}/feedback", json=body)
        return response.json()