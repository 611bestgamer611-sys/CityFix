import os
from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
ADMIN_SERVICE_URL = os.getenv("ADMIN_SERVICE_URL", "http://localhost:8002")
TICKET_SERVICE_URL = os.getenv("TICKET_SERVICE_URL", "http://localhost:8003")
MEDIA_SERVICE_URL = os.getenv("MEDIA_SERVICE_URL", "http://localhost:8004")
GEO_SERVICE_URL = os.getenv("GEO_SERVICE_URL", "http://localhost:8005")
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8006")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")