import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from config import CORS_ORIGINS
from middleware import LoggingMiddleware
from routers import auth, admin, tickets, media, geo, notifications

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="CityFix API Gateway",
    description="Orchestrator/API Gateway for CityFix microservices",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(admin.router, prefix="/admin", tags=["Administration"])
app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])
app.include_router(media.router, prefix="/media", tags=["Media"])
app.include_router(geo.router, prefix="/geo", tags=["Geolocation"])
app.include_router(notifications.router, prefix="/notify", tags=["Notifications"])

@app.get("/")
async def root():
    return {
        "service": "CityFix API Gateway",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "orchestrator"}

@app.on_event("startup")
async def startup_event():
    logger.info("Orchestrator starting up...")
    logger.info(f"CORS Origins: {CORS_ORIGINS}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Orchestrator shutting down...")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)