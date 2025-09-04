from models.mongodb import performance_collection
from schemas.performance import PerformanceCreate, PerformanceUpdate
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

def performance_helper(pf) -> dict:
    return {
        "id": str(pf["_id"]),
        "employee_id": pf["employee_id"],
        "review_date": pf["review_date"].strftime("%Y-%m-%d") if pf.get("review_date") else None,
        "score": pf["score"],
        "comment": pf.get("comment"),
    }

async def get_performances() -> List[dict]:
    performances = []
    async for pf in performance_collection.find():
        performances.append(performance_helper(pf))
    return performances

async def get_performance(performance_id: str) -> Optional[dict]:
    pf = await performance_collection.find_one({"_id": ObjectId(performance_id)})
    if pf:
        return performance_helper(pf)
    return None

async def create_performance(pf: PerformanceCreate) -> dict:
    pf_dict = pf.dict()
    if isinstance(pf_dict["review_date"], datetime) is False:
        pf_dict["review_date"] = datetime.combine(pf_dict["review_date"], datetime.min.time())
    result = await performance_collection.insert_one(pf_dict)
    new_pf = await performance_collection.find_one({"_id": result.inserted_id})
    return performance_helper(new_pf)

async def update_performance(performance_id: str, pf: PerformanceUpdate) -> Optional[dict]:
    pf_dict = {k: v for k, v in pf.dict().items() if v is not None}
    if "review_date" in pf_dict:
        pf_dict["review_date"] = datetime.combine(pf_dict["review_date"], datetime.min.time())
    await performance_collection.update_one({"_id": ObjectId(performance_id)}, {"$set": pf_dict})
    updated = await performance_collection.find_one({"_id": ObjectId(performance_id)})
    if updated:
        return performance_helper(updated)
    return None

async def delete_performance(performance_id: str) -> bool:
    result = await performance_collection.delete_one({"_id": ObjectId(performance_id)})
    return result.deleted_count == 1
