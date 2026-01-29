from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Location(BaseModel):
    lat: float
    lon: float
    address: Optional[str] = None

class TicketCreate(BaseModel):
    title: str
    description: str
    location: Location
    category: str
    tenant_id: str
    images: Optional[List[str]] = []

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    category: Optional[str] = None
    assigned_to: Optional[str] = None

class Comment(BaseModel):
    user_id: str
    message: str
    created_at: datetime

class TicketResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    location: Location
    status: str
    category: str
    reported_by: str
    assigned_to: Optional[str] = None
    images: List[str] = []
    tenant_id: str
    comments: List[Comment] = []
    feedback: Optional[dict] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        from_attributes = True

class CommentCreate(BaseModel):
    message: str
    user_id: str

class FeedbackCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = None