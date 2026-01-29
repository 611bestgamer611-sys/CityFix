from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class Location(BaseModel):
    lat: float
    lon: float
    address: Optional[str] = None

class MunicipalityCreate(BaseModel):
    name: str
    location: Location
    admin_id: str

class MunicipalityResponse(BaseModel):
    id: str = Field(alias="_id")
    name: str
    location: Location
    admin_id: str
    created_at: datetime
    
    class Config:
        populate_by_name = True
        from_attributes = True

class Stats(BaseModel):
    total_tickets: int
    pending_tickets: int
    in_progress_tickets: int
    completed_tickets: int
    total_municipalities: int
    total_users: int
    tickets_by_category: Dict[str, int]
    tickets_by_municipality: Dict[str, int]