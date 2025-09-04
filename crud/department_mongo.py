from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut
from typing import List, Optional
from bson import ObjectId

load_dotenv()

MONGO_DETAILS = os.getenv("MONGODB_URI")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["DACNKTCNTT"] 
department_collection = db["departments"]

def department_helper(dep) -> dict:
    return {
        "id": str(dep["_id"]),
        "name": dep["name"],
    }

async def get_departments() -> List[dict]:
    departments = []
    async for dep in department_collection.find():
        departments.append(department_helper(dep))
    return departments

async def get_department(department_id: str) -> Optional[dict]:
    dep = await department_collection.find_one({"_id": ObjectId(department_id)})
    if dep:
        return department_helper(dep)
    return None

async def create_department(dep: DepartmentCreate) -> dict:
    dep_dict = dep.dict()
    result = await department_collection.insert_one(dep_dict)
    new_dep = await department_collection.find_one({"_id": result.inserted_id})
    return department_helper(new_dep)

async def update_department(department_id: str, dep: DepartmentUpdate) -> Optional[dict]:
    dep_dict = {k: v for k, v in dep.dict().items() if v is not None}
    await department_collection.update_one({"_id": ObjectId(department_id)}, {"$set": dep_dict})
    updated = await department_collection.find_one({"_id": ObjectId(department_id)})
    if updated:
        return department_helper(updated)
    return None

async def delete_department(department_id: str) -> bool:
    result = await department_collection.delete_one({"_id": ObjectId(department_id)})
    return result.deleted_count == 1