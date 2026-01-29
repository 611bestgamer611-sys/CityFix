from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from bson import ObjectId
from models import NotificationCreate, NotificationResponse
from database import notifications_collection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/send", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def send_notification(notification: NotificationCreate):
    logger.info(f"Sending notification to user: {notification.user_id}")
    
    notification_dict = notification.model_dump()
    notification_dict["read"] = False
    notification_dict["created_at"] = datetime.utcnow()
    
    result = await notifications_collection.insert_one(notification_dict)
    created_notification = await notifications_collection.find_one({"_id": result.inserted_id})
    
    created_notification["_id"] = str(created_notification["_id"])
    return NotificationResponse(**created_notification)

@router.get("/user/{user_id}", response_model=List[NotificationResponse])
async def get_user_notifications(user_id: str, unread_only: bool = False):
    logger.info(f"Fetching notifications for user: {user_id}")
    
    query = {"user_id": user_id}
    if unread_only:
        query["read"] = False
    
    notifications = []
    async for notification in notifications_collection.find(query).sort("created_at", -1):
        notification["_id"] = str(notification["_id"])
        notifications.append(NotificationResponse(**notification))
    
    return notifications

@router.patch("/{notification_id}/read")
async def mark_as_read(notification_id: str):
    logger.info(f"Marking notification as read: {notification_id}")
    
    try:
        obj_id = ObjectId(notification_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid notification ID format"
        )
    
    result = await notifications_collection.update_one(
        {"_id": obj_id},
        {"$set": {"read": True}}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    updated_notification = await notifications_collection.find_one({"_id": obj_id})
    updated_notification["_id"] = str(updated_notification["_id"])
    
    return NotificationResponse(**updated_notification)