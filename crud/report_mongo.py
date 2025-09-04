from models.mongodb import report_collection
from schemas.report import ReportCreate, ReportUpdate, ReportOut
from typing import List, Optional
from bson import ObjectId
from datetime import date

def report_helper(rp) -> dict:
    return {
        "id": str(rp["_id"]),
        "title": rp["title"],
        "created_at": str(rp.get("created_at")) if rp.get("created_at") else None,
        "content": rp.get("content"),
        "type": rp.get("type"),
        "value": rp.get("value", 0),
    }

async def get_reports() -> List[dict]:
    reports = []
    async for rp in report_collection.find():
        reports.append(report_helper(rp))
    return reports

async def get_report(report_id: str) -> Optional[dict]:
    rp = await report_collection.find_one({"_id": ObjectId(report_id)})
    if rp:
        return report_helper(rp)
    return None

async def create_report(rp: ReportCreate) -> dict:
    rp_dict = rp.dict()

    if isinstance(rp_dict.get("created_at"), date):
        rp_dict["created_at"] = str(rp_dict["created_at"])

    result = await report_collection.insert_one(rp_dict)
    new_rp = await report_collection.find_one({"_id": result.inserted_id})
    return report_helper(new_rp)

async def update_report(report_id: str, rp: ReportUpdate) -> Optional[dict]:
    rp_dict = {k: v for k, v in rp.dict().items() if v is not None}

    if isinstance(rp_dict.get("created_at"), date):
        rp_dict["created_at"] = str(rp_dict["created_at"])

    await report_collection.update_one({"_id": ObjectId(report_id)}, {"$set": rp_dict})
    updated = await report_collection.find_one({"_id": ObjectId(report_id)})
    if updated:
        return report_helper(updated)
    return None

async def delete_report(report_id: str) -> bool:
    result = await report_collection.delete_one({"_id": ObjectId(report_id)})
    return result.deleted_count == 1
