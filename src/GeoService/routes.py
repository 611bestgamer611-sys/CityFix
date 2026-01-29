from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List
from geopy.geocoders import Nominatim
from database import municipalities_collection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

geolocator = Nominatim(user_agent="cityfix_geoservice")

class GeocodeRequest(BaseModel):
    address: str

class GeocodeResponse(BaseModel):
    lat: float
    lon: float
    address: str
    display_name: str

class ReverseGeocodeRequest(BaseModel):
    lat: float
    lon: float

class ReverseGeocodeResponse(BaseModel):
    address: str
    display_name: str
    lat: float
    lon: float

class BoundaryResponse(BaseModel):
    municipality_id: str
    name: str
    bounds: Optional[dict] = None

@router.post("/geocode", response_model=GeocodeResponse)
async def geocode_address(request: GeocodeRequest):
    logger.info(f"Geocoding address: {request.address}")
    
    try:
        location = geolocator.geocode(request.address)
        
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Address not found"
            )
        
        return GeocodeResponse(
            lat=location.latitude,
            lon=location.longitude,
            address=request.address,
            display_name=location.address
        )
    except Exception as e:
        logger.error(f"Geocoding error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Geocoding service error"
        )

@router.post("/reverse-geocode", response_model=ReverseGeocodeResponse)
async def reverse_geocode(request: ReverseGeocodeRequest):
    logger.info(f"Reverse geocoding: {request.lat}, {request.lon}")
    
    try:
        location = geolocator.reverse(f"{request.lat}, {request.lon}")
        
        if not location:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Location not found"
            )
        
        return ReverseGeocodeResponse(
            address=location.address,
            display_name=location.address,
            lat=request.lat,
            lon=request.lon
        )
    except Exception as e:
        logger.error(f"Reverse geocoding error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Reverse geocoding service error"
        )

@router.get("/map/tiles")
async def get_map_tiles():
    return {
        "tile_url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "attribution": "© OpenStreetMap contributors",
        "max_zoom": 19
    }

@router.get("/boundaries", response_model=List[BoundaryResponse])
async def get_boundaries():
    logger.info("Fetching municipality boundaries")
    
    boundaries = []
    async for municipality in municipalities_collection.find():
        boundary = BoundaryResponse(
            municipality_id=str(municipality["_id"]),
            name=municipality["name"],
            bounds=municipality.get("bounds")
        )
        boundaries.append(boundary)
    
    return boundaries