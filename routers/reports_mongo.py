from fastapi import APIRouter, HTTPException
from typing import List
from crud.report_mongo import (
    get_reports, get_report, create_report,
    update_report, delete_report
)
from schemas.report import ReportCreate, ReportUpdate, ReportOut

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/", response_model=List[ReportOut])
async def list_reports():
    return await get_reports()

@router.post("/", response_model=ReportOut)
async def add_report(rp: ReportCreate):
    return await create_report(rp)

@router.put("/{report_id}/", response_model=ReportOut)
async def edit_report(report_id: str, rp: ReportUpdate):
    updated = await update_report(report_id, rp)
    if not updated:
        raise HTTPException(status_code=404, detail="Không tìm thấy báo cáo")
    return updated

@router.delete("/{report_id}/")
async def remove_report(report_id: str):
    ok = await delete_report(report_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Không tìm thấy báo cáo")
    return {"success": True}
