import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیمات API
API_KEY = os.getenv("API_KEY")
EXA_ENDPOINT = os.getenv("EXA_ENDPOINT")

# تنظیمات FastAPI
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 9000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
