from datetime import datetime

async def update_attendance_analysis(employee_id: str):
    emp_obj_id = ObjectId(employee_id)
    await employee_collection.update_one(
        {"_id": emp_obj_id},
        {"$inc": {"attendance_count": 1}, "$set": {"last_attendance": datetime.utcnow()}}
    )
from config.mongodb import employee_collection
from bson import ObjectId
from typing import List, Dict

async def get_employee_count_by_department() -> List[Dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "count": {"$sum": 1}
            }
        },
        {
            "$project": {
                "_id": 0,
                "department": "$_id",
                "count": 1
            }
        }
    ]
    result = await employee_collection.aggregate(pipeline).to_list(length=None)
    return result
