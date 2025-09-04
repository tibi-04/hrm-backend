from models.mongodb import leave_collection
from schemas.leave import LeaveCreate, LeaveUpdate, LeaveOut
from typing import List, Optional
from bson import ObjectId

def leave_helper(lv) -> dict:
    return {
        "id": str(lv["_id"]),
        "employee_id": lv["employee_id"],
        "start_date": str(lv["start_date"]),
        "end_date": str(lv["end_date"]),
        "reason": lv.get("reason"),
        "status": lv.get("status", "Pending"),
    }

async def get_leaves() -> List[dict]:
    leaves = []
    async for lv in leave_collection.find():
        leaves.append(leave_helper(lv))
    return leaves

async def get_leave(leave_id: str) -> Optional[dict]:
    lv = await leave_collection.find_one({"_id": ObjectId(leave_id)})
    if lv:
        return leave_helper(lv)
    return None

async def create_leave(lv: LeaveCreate) -> dict:
    import datetime
    lv_dict = lv.dict()
    for field in ["start_date", "end_date"]:
        if field in lv_dict and isinstance(lv_dict[field], datetime.date) and not isinstance(lv_dict[field], datetime.datetime):
            lv_dict[field] = datetime.datetime.combine(lv_dict[field], datetime.time())
    result = await leave_collection.insert_one(lv_dict)
    new_lv = await leave_collection.find_one({"_id": result.inserted_id})
    return leave_helper(new_lv)

async def update_leave(leave_id: str, lv: LeaveUpdate) -> Optional[dict]:
    lv_dict = {k: v for k, v in lv.dict().items() if v is not None}
    await leave_collection.update_one({"_id": ObjectId(leave_id)}, {"$set": lv_dict})
    updated = await leave_collection.find_one({"_id": ObjectId(leave_id)})
    if updated:
        return leave_helper(updated)
    return None

async def delete_leave(leave_id: str) -> bool:
    result = await leave_collection.delete_one({"_id": ObjectId(leave_id)})
    return result.deleted_count == 1
