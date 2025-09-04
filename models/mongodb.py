from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()  

MONGO_DETAILS = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["DACNKTCNTT"]  

# Các collection giữ nguyên
employee_collection = database.get_collection("employees")
candidate_collection = database.get_collection("candidates")
department_collection = database.get_collection("departments")
attendance_collection = database.get_collection("attendance")
leave_collection = database.get_collection("leave")
payroll_collection = database.get_collection("payroll")
performance_collection = database.get_collection("performance")
report_collection = database.get_collection("reports")
notification_collection = database.get_collection("notifications")
reward_collection = database.get_collection("rewards")
contract_collection = database.get_collection("contracts")