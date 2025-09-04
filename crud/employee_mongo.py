from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import datetime
from typing import List, Optional
from schemas.employee import EmployeeCreate, EmployeeUpdate
import base64
from PIL import Image
from io import BytesIO
import numpy as np

def prepare_photo_data(photo_data: str) -> str:
    """Chuyển ảnh base64 thành RGB và mã hóa lại"""
    try:
        photo_bytes = base64.b64decode(photo_data)
        image = Image.open(BytesIO(photo_bytes)).convert("RGB")

        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"[PHOTO_PROCESS_ERROR] {e}")
        return None

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGO_DB", "DACNKTCNTT")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]
employee_collection = db["employees"]

def skills_to_list(skills) -> List[str]:
    if isinstance(skills, list):
        return [str(s).strip() for s in skills if str(s).strip()]
    if isinstance(skills, str):
        return [s.strip() for s in skills.split(",") if s.strip()]
    return []

def employee_doc_to_dict(emp) -> dict:
    if not emp or "_id" not in emp:
        return None
    
    department_id = emp.get("department_id")
    
    return {
        "id": str(emp["_id"]),
        "name": emp.get("name", ""),
        "email": emp.get("email", ""),
        "phone": emp.get("phone", None),
        "address": emp.get("address", None),
        "department_id": str(department_id) if department_id else None,  # Chuyển ObjectId thành string
        "position": emp.get("position", ""),
        "hire_date": emp.get("hire_date"), 
        "date_of_birth": emp.get("date_of_birth"),
        "skills": skills_to_list(emp.get("skills", [])),
        "experience_years": emp.get("experience_years", 0),
        "photo_url": emp.get("photo_url", ""),
        "photo_data": emp.get("photo_data", None),
        "work_schedule": emp.get("work_schedule", "")
    }

def convert_dates(emp_dict: dict):
    for field in ["hire_date", "date_of_birth"]:
        if isinstance(emp_dict.get(field), datetime.date):
            emp_dict[field] = emp_dict[field].isoformat()
    return emp_dict

async def get_employees() -> List[dict]:
    employees = []
    async for emp in employee_collection.find():
        emp_dict = employee_doc_to_dict(emp)
        if emp_dict:
            employees.append(emp_dict)
    return employees

async def get_employee(employee_id: str) -> Optional[dict]:
    if not ObjectId.is_valid(employee_id):
        return None
    emp = await employee_collection.find_one({"_id": ObjectId(employee_id)})
    return employee_doc_to_dict(emp) if emp else None

async def create_employee(emp: EmployeeCreate) -> dict:
    emp_dict = emp.dict(exclude_unset=True)
    emp_dict.pop("id", None)
    emp_dict.pop("_id", None)

    if emp_dict.get("department_id") and ObjectId.is_valid(emp_dict["department_id"]):
        emp_dict["department_id"] = ObjectId(emp_dict["department_id"])

    emp_dict["skills"] = skills_to_list(emp_dict.get("skills", []))
    emp_dict = convert_dates(emp_dict)

    if emp_dict.get("photo_data"):
        fixed_photo = prepare_photo_data(emp_dict["photo_data"])
        if fixed_photo:
            emp_dict["photo_data"] = fixed_photo
        else:
            emp_dict.pop("photo_data")  
    result = await employee_collection.insert_one(emp_dict)
    new_emp = await employee_collection.find_one({"_id": result.inserted_id})
    return employee_doc_to_dict(new_emp)

async def update_employee(employee_id: str, emp: EmployeeUpdate) -> Optional[dict]:
    if not ObjectId.is_valid(employee_id):
        return None

    emp_dict = {k: v for k, v in emp.dict().items() if v is not None}

    if "department_id" in emp_dict and ObjectId.is_valid(emp_dict["department_id"]):
        emp_dict["department_id"] = ObjectId(emp_dict["department_id"])

    if "skills" in emp_dict:
        emp_dict["skills"] = skills_to_list(emp_dict["skills"])

    emp_dict = convert_dates(emp_dict)

    if emp_dict.get("photo_data"):
        fixed_photo = prepare_photo_data(emp_dict["photo_data"])
        if fixed_photo:
            emp_dict["photo_data"] = fixed_photo
        else:
            emp_dict.pop("photo_data")

    await employee_collection.update_one({"_id": ObjectId(employee_id)}, {"$set": emp_dict})
    updated = await employee_collection.find_one({"_id": ObjectId(employee_id)})
    return employee_doc_to_dict(updated) if updated else None

async def delete_employee(employee_id: str) -> bool:
    if not ObjectId.is_valid(employee_id):
        return False
    result = await employee_collection.delete_one({"_id": ObjectId(employee_id)})
    return result.deleted_count == 1

async def fix_department_ids():
    """Chuyển tất cả department_id đang là string thành ObjectId (nếu hợp lệ)."""
    async for emp in employee_collection.find({"department_id": {"$type": "string"}}):
        dept_id = emp.get("department_id")
        if ObjectId.is_valid(dept_id):
            await employee_collection.update_one(
                {"_id": emp["_id"]},
                {"$set": {"department_id": ObjectId(dept_id)}}
            )

async def get_employee_by_email(email: str) -> Optional[dict]:
    """Tìm employee theo email"""
    emp = await employee_collection.find_one({"email": email})
    return employee_doc_to_dict(emp) if emp else None