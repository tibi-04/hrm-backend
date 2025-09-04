from models.mongodb import attendance_collection
from schemas.attendance import AttendanceCreate, AttendanceUpdate
from typing import List, Optional, Dict
from bson import ObjectId
from datetime import datetime

def attendance_helper(att: dict) -> dict:
    return {
        "id": str(att.get("_id", "")),
        "employee_id": str(att.get("employee_id", "")),
        "employee_name": att.get("employee_name", ""),
        "department": att.get("department", ""),
        "date": att.get("date", datetime.utcnow()).isoformat(),
        "type": att.get("type", "check-in"),
        "status": att.get("status", "present"),
        "reason": att.get("reason", ""),
        "has_permission": att.get("has_permission", False),
        "check_in_time": att.get("check_in_time", None),
        "check_out_time": att.get("check_out_time", None),
    }

async def get_attendances() -> List[dict]:
    attendances: List[Dict] = []
    async for att in attendance_collection.find().sort("date", -1):
        attendances.append(attendance_helper(att))
    return attendances

async def get_attendance(attendance_id: str) -> Optional[dict]:
    if not ObjectId.is_valid(attendance_id):
        return None
    att = await attendance_collection.find_one({"_id": ObjectId(attendance_id)})
    return attendance_helper(att) if att else None

async def create_attendance(att: AttendanceCreate) -> dict:
    att_dict = att.dict()
    att_dict["date"] = datetime.fromisoformat(att_dict["date"])
    result = await attendance_collection.insert_one(att_dict)
    new_att = await attendance_collection.find_one({"_id": result.inserted_id})
    return attendance_helper(new_att) if new_att else {}

async def update_attendance(attendance_id: str, att: AttendanceUpdate) -> Optional[dict]:
    if not ObjectId.is_valid(attendance_id):
        return None
    att_dict = {k: v for k, v in att.dict().items() if v is not None}
    if "date" in att_dict:
        att_dict["date"] = datetime.fromisoformat(att_dict["date"])
    if not att_dict:
        return None
    await attendance_collection.update_one(
        {"_id": ObjectId(attendance_id)}, {"$set": att_dict}
    )
    updated = await attendance_collection.find_one({"_id": ObjectId(attendance_id)})
    return attendance_helper(updated) if updated else None

async def delete_attendance(attendance_id: str) -> bool:
    if not ObjectId.is_valid(attendance_id):
        return False
    result = await attendance_collection.delete_one({"_id": ObjectId(attendance_id)})
    return result.deleted_count == 1