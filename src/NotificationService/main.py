import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes import router

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="CityFix Notification Service",
    description="Notification management service for CityFix",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/notify", tags=["Notifications"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "notification"}

@app.on_event("startup")
async def startup_event():
    logger.info("Notification Service starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Notification Service shutting down...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8006))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)