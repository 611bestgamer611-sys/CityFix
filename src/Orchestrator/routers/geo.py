from fastapi import APIRouter, Request
import httpx
from config import GEO_SERVICE_URL

router = APIRouter()

@router.post("/geocode")
async def geocode_address(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{GEO_SERVICE_URL}/geo/geocode", json=body)
        return response.json()

@router.post("/reverse-geocode")
async def reverse_geocode(request: Request):
    async with httpx.AsyncClient() as client:
        body = await request.json()
        response = await client.post(f"{GEO_SERVICE_URL}/geo/reverse-geocode", json=body)
        return response.json()

@router.get("/map/tiles")
async def get_map_tiles():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GEO_SERVICE_URL}/geo/map/tiles")
        return response.json()

@router.get("/boundaries")
async def get_boundaries():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{GEO_SERVICE_URL}/geo/boundaries")
        return response.json()