import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/app/uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "10485760"))
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}

os.makedirs(UPLOAD_DIR, exist_ok=True)