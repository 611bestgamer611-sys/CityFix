from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from models import MunicipalityCreate, MunicipalityResponse, Stats
from database import municipalities_collection, tickets_collection, users_collection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/municipalities", response_model=List[MunicipalityResponse])
async def get_municipalities():
    logger.info("Fetching all municipalities")
    municipalities = []
    async for municipality in municipalities_collection.find():
        municipality["_id"] = str(municipality["_id"])
        municipalities.append(MunicipalityResponse(**municipality))
    return municipalities

@router.post("/municipalities", response_model=MunicipalityResponse, status_code=status.HTTP_201_CREATED)
async def create_municipality(municipality: MunicipalityCreate):
    logger.info(f"Creating municipality: {municipality.name}")
    
    existing = await municipalities_collection.find_one({"name": municipality.name})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Municipality with this name already exists"
        )
    
    municipality_dict = municipality.model_dump()
    municipality_dict["created_at"] = datetime.utcnow()
    
    result = await municipalities_collection.insert_one(municipality_dict)
    created = await municipalities_collection.find_one({"_id": result.inserted_id})
    
    created["_id"] = str(created["_id"])
    return MunicipalityResponse(**created)

@router.get("/stats", response_model=Stats)
async def get_stats():
    logger.info("Fetching statistics")
    
    total_tickets = await tickets_collection.count_documents({})
    pending_tickets = await tickets_collection.count_documents({"status": "pending"})
    in_progress_tickets = await tickets_collection.count_documents({"status": "in_progress"})
    completed_tickets = await tickets_collection.count_documents({"status": "completed"})
    total_municipalities = await municipalities_collection.count_documents({})
    total_users = await users_collection.count_documents({})
    
    tickets_by_category = {}
    categories_cursor = tickets_collection.aggregate([
        {"$group": {"_id": "$category", "count": {"$sum": 1}}}
    ])
    async for cat in categories_cursor:
        tickets_by_category[cat["_id"]] = cat["count"]
    
    tickets_by_municipality = {}
    municipalities_cursor = tickets_collection.aggregate([
        {"$group": {"_id": "$tenant_id", "count": {"$sum": 1}}}
    ])
    async for mun in municipalities_cursor:
        tickets_by_municipality[str(mun["_id"])] = mun["count"]
    
    return Stats(
        total_tickets=total_tickets,
        pending_tickets=pending_tickets,
        in_progress_tickets=in_progress_tickets,
        completed_tickets=completed_tickets,
        total_municipalities=total_municipalities,
        total_users=total_users,
        tickets_by_category=tickets_by_category,
        tickets_by_municipality=tickets_by_municipality
    )

@router.get("/tickets/all")
async def get_all_tickets():
    logger.info("Fetching all tickets across municipalities")
    tickets = []
    async for ticket in tickets_collection.find().sort("created_at", -1):
        ticket["_id"] = str(ticket["_id"])
        tickets.append(ticket)
    return tickets