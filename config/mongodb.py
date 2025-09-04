from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load biến môi trường từ file .env

# Sử dụng biến môi trường
MONGO_URI = os.getenv("MONGODB_URI")

client = AsyncIOMotorClient(MONGO_URI)
db = client["DACNKTCNTT"]  # Đổi tên database theo Atlas

employee_collection = db["employees"]

def get_database():
    return db
