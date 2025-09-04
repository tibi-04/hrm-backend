from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from models.payroll import Payroll
from schemas.payroll import PayrollCreate, PayrollUpdate, PayrollOut

router = APIRouter(prefix="/payroll", tags=["Payroll (MongoDB)"])

@router.get("/", response_model=List[PayrollOut])
async def list_payroll():
    payrolls = Payroll.objects.all()
    return [PayrollOut(**pr.to_mongo().to_dict(), id=str(pr.id)) for pr in payrolls]

@router.get("/{payroll_id}", response_model=PayrollOut)
async def get_payroll(payroll_id: str):
    if not ObjectId.is_valid(payroll_id):
        raise HTTPException(status_code=400, detail="Invalid payroll ID format")
    pr = Payroll.objects(id=payroll_id).first()
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll not found")
    return PayrollOut(**pr.to_mongo().to_dict(), id=str(pr.id))

@router.post("/", response_model=PayrollOut, status_code=status.HTTP_201_CREATED)
async def create_payroll(payroll: PayrollCreate):
    new_pr = Payroll(**payroll.dict())
    new_pr.save()
    return PayrollOut(**new_pr.to_mongo().to_dict(), id=str(new_pr.id))

@router.put("/{payroll_id}", response_model=PayrollOut)
async def update_payroll(payroll_id: str, payroll: PayrollUpdate):
    if not ObjectId.is_valid(payroll_id):
        raise HTTPException(status_code=400, detail="Invalid payroll ID format")
    pr = Payroll.objects(id=payroll_id).first()
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll not found")
    pr.update(**payroll.dict(exclude_unset=True))
    pr.reload()
    return PayrollOut(**pr.to_mongo().to_dict(), id=str(pr.id))

@router.delete("/{payroll_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_payroll(payroll_id: str):
    if not ObjectId.is_valid(payroll_id):
        raise HTTPException(status_code=400, detail="Invalid payroll ID format")
    pr = Payroll.objects(id=payroll_id).first()
    if not pr:
        raise HTTPException(status_code=404, detail="Payroll not found")
    pr.delete()
    return None
