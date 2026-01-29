import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://admin:admin123@localhost:27017/cityfix?authSource=admin")

client = AsyncIOMotorClient(MONGODB_URL)
db = client.cityfix

tickets_collection = db.tickets
operators_collection = db.operators

async def get_database():
    return db