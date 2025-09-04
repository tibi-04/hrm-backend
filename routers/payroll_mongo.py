from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.payroll import PayrollCreate, PayrollUpdate, PayrollOut
from crud import payroll_mongo

router = APIRouter(prefix="/payroll", tags=["Payroll"])

@router.get("/", response_model=List[PayrollOut])
async def list_payroll():
    return await payroll_mongo.get_payrolls()

@router.get("/{payroll_id}", response_model=PayrollOut)
async def get_payroll(payroll_id: str):
    pr = await payroll_mongo.get_payroll(payroll_id)
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return pr

@router.post("/", response_model=PayrollOut, status_code=status.HTTP_201_CREATED)
async def create_payroll(pr: PayrollCreate):
    return await payroll_mongo.create_payroll(pr)

@router.put("/{payroll_id}", response_model=PayrollOut)
async def update_payroll(payroll_id: str, pr: PayrollUpdate):
    updated = await payroll_mongo.update_payroll(payroll_id, pr)
    if not updated:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return updated

@router.delete("/{payroll_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payroll(payroll_id: str):
    deleted = await payroll_mongo.delete_payroll(payroll_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return None
