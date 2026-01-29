from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: str
    message: str
    type: str = Field(default="info", pattern="^(info|warning|success|error)$")
    ticket_id: Optional[str] = None

class NotificationResponse(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    message: str
    type: str
    ticket_id: Optional[str] = None
    read: bool
    created_at: datetime
    
    class Config:
        populate_by_name = True
        from_attributes = True