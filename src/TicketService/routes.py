from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from models import TicketCreate, TicketUpdate, TicketResponse, CommentCreate, FeedbackCreate, Comment
from database import tickets_collection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/create", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket: TicketCreate, user_id: str = Query(...)):
    logger.info(f"Creating ticket: {ticket.title}")
    
    ticket_dict = ticket.model_dump()
    ticket_dict["reported_by"] = user_id
    ticket_dict["status"] = "pending"
    ticket_dict["comments"] = []
    ticket_dict["feedback"] = None
    ticket_dict["created_at"] = datetime.utcnow()
    ticket_dict["updated_at"] = datetime.utcnow()
    
    result = await tickets_collection.insert_one(ticket_dict)
    created_ticket = await tickets_collection.find_one({"_id": result.inserted_id})
    
    created_ticket["_id"] = str(created_ticket["_id"])
    return TicketResponse(**created_ticket)

@router.get("/list", response_model=List[TicketResponse])
async def get_tickets(
    tenant_id: Optional[str] = None,
    user_id: Optional[str] = None,
    status: Optional[str] = None
):
    logger.info(f"Fetching tickets - tenant_id: {tenant_id}, user_id: {user_id}, status: {status}")
    
    query = {}
    if tenant_id:
        query["tenant_id"] = tenant_id
    if user_id:
        query["reported_by"] = user_id
    if status:
        query["status"] = status
    
    tickets = []
    async for ticket in tickets_collection.find(query).sort("created_at", -1):
        ticket["_id"] = str(ticket["_id"])
        tickets.append(TicketResponse(**ticket))
    
    return tickets

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: str):
    logger.info(f"Fetching ticket: {ticket_id}")
    
    try:
        ticket = await tickets_collection.find_one({"_id": ObjectId(ticket_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID format"
        )
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    ticket["_id"] = str(ticket["_id"])
    return TicketResponse(**ticket)

@router.patch("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(ticket_id: str, ticket_update: TicketUpdate):
    logger.info(f"Updating ticket: {ticket_id}")
    
    try:
        obj_id = ObjectId(ticket_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID format"
        )
    
    update_data = ticket_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update"
        )
    
    update_data["updated_at"] = datetime.utcnow()
    
    result = await tickets_collection.update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    updated_ticket = await tickets_collection.find_one({"_id": obj_id})
    updated_ticket["_id"] = str(updated_ticket["_id"])
    return TicketResponse(**updated_ticket)

@router.post("/{ticket_id}/comments", response_model=TicketResponse)
async def add_comment(ticket_id: str, comment: CommentCreate):
    logger.info(f"Adding comment to ticket: {ticket_id}")
    
    try:
        obj_id = ObjectId(ticket_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID format"
        )
    
    new_comment = Comment(
        user_id=comment.user_id,
        message=comment.message,
        created_at=datetime.utcnow()
    )
    
    result = await tickets_collection.update_one(
        {"_id": obj_id},
        {
            "$push": {"comments": new_comment.model_dump()},
            "$set": {"updated_at": datetime.utcnow()}
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    updated_ticket = await tickets_collection.find_one({"_id": obj_id})
    updated_ticket["_id"] = str(updated_ticket["_id"])
    return TicketResponse(**updated_ticket)

@router.post("/{ticket_id}/feedback", response_model=TicketResponse)
async def add_feedback(ticket_id: str, feedback: FeedbackCreate):
    logger.info(f"Adding feedback to ticket: {ticket_id}")
    
    try:
        obj_id = ObjectId(ticket_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid ticket ID format"
        )
    
    feedback_data = feedback.model_dump()
    feedback_data["created_at"] = datetime.utcnow()
    
    result = await tickets_collection.update_one(
        {"_id": obj_id},
        {
            "$set": {
                "feedback": feedback_data,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )
    
    updated_ticket = await tickets_collection.find_one({"_id": obj_id})
    updated_ticket["_id"] = str(updated_ticket["_id"])
    return TicketResponse(**updated_ticket)