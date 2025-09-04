from fastapi import APIRouter, HTTPException
from typing import List
from schemas.payroll import PayrollOut
from models.payroll import Payroll

router = APIRouter(prefix="/payroll_all", tags=["Payroll (MongoDB)"])

@router.get("/", response_model=List[PayrollOut])
async def list_payroll_all():
    payrolls = Payroll.objects.all()
    return [PayrollOut(**payroll.to_mongo().to_dict(), id=str(payroll.id)) for payroll in payrolls]
