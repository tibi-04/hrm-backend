from fastapi import APIRouter
from config.mongodb import employee_collection
from bson import ObjectId

router = APIRouter(prefix="/api/analytics")

@router.get("/employees-by-department")
async def get_employees_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "count": {"$sum": 1}}},
        {"$project": {"department": "$_id", "count": 1, "_id": 0}}
    ]
    result = await employee_collection.aggregate(pipeline).to_list(length=None)
    return result