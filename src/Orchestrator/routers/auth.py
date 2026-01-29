from fastapi import APIRouter, Request
import httpx
from config import AUTH_SERVICE_URL

router = APIRouter()

@router.post("/register")
async def register(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/register", json=body)
        return response.json()

@router.post("/login")
async def login(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/login", json=body)
        return response.json()

@router.get("/me")
async def get_me(request: Request):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": request.headers.get("Authorization", "")}
        response = await client.get(f"{AUTH_SERVICE_URL}/auth/me", headers=headers)
        return response.json()

@router.post("/logout")
async def logout():
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{AUTH_SERVICE_URL}/auth/logout")
        return response.json()