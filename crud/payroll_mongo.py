from models.mongodb import payroll_collection
from schemas.payroll import PayrollCreate, PayrollUpdate, PayrollOut
from typing import List, Optional
from bson import ObjectId

def payroll_helper(pr) -> dict:
    return {
        "id": str(pr["_id"]),
        "employee_id": pr["employee_id"],
        "month": pr["month"],
        "base_salary": pr["base_salary"],
        "bonus": pr.get("bonus", 0),
        "deduction": pr.get("deduction", 0),
        "total": pr["total"],
    }

async def get_payrolls() -> List[dict]:
    payrolls = []
    async for pr in payroll_collection.find():
        payrolls.append(payroll_helper(pr))
    return payrolls

async def get_payroll(payroll_id: str) -> Optional[dict]:
    pr = await payroll_collection.find_one({"_id": ObjectId(payroll_id)})
    if pr:
        return payroll_helper(pr)
    return None

async def create_payroll(pr: PayrollCreate) -> dict:
    pr_dict = pr.dict()
    result = await payroll_collection.insert_one(pr_dict)
    new_pr = await payroll_collection.find_one({"_id": result.inserted_id})
    return payroll_helper(new_pr)

async def update_payroll(payroll_id: str, pr: PayrollUpdate) -> Optional[dict]:
    pr_dict = {k: v for k, v in pr.dict().items() if v is not None}
    await payroll_collection.update_one({"_id": ObjectId(payroll_id)}, {"$set": pr_dict})
    updated = await payroll_collection.find_one({"_id": ObjectId(payroll_id)})
    if updated:
        return payroll_helper(updated)
    return None

async def delete_payroll(payroll_id: str) -> bool:
    result = await payroll_collection.delete_one({"_id": ObjectId(payroll_id)})
    return result.deleted_count == 1
