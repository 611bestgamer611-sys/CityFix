from fastapi import APIRouter, Request
import httpx
from config import ADMIN_SERVICE_URL

router = APIRouter()

@router.get("/municipalities")
async def get_municipalities():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ADMIN_SERVICE_URL}/admin/municipalities")
        return response.json()

@router.post("/municipalities")
async def create_municipality(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{ADMIN_SERVICE_URL}/admin/municipalities", json=body)
        return response.json()

@router.get("/stats")
async def get_stats():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ADMIN_SERVICE_URL}/admin/stats")
        return response.json()

@router.get("/tickets/all")
async def get_all_tickets():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{ADMIN_SERVICE_URL}/admin/tickets/all")
        return response.json()