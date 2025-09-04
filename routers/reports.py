from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas.report import ReportCreate, ReportUpdate, ReportOut
from models.report import Report
from bson import ObjectId

router = APIRouter(prefix="/reports", tags=["Reports (MongoDB)"])

@router.get("/", response_model=List[ReportOut])
async def list_reports():
    reports = Report.objects.all()
    return [ReportOut(**rp.to_mongo().to_dict(), id=str(rp.id)) for rp in reports]

@router.get("/{report_id}", response_model=ReportOut)
async def get_report(report_id: str):
    if not ObjectId.is_valid(report_id):
        raise HTTPException(status_code=400, detail="Invalid report ID format")
    rp = Report.objects(id=report_id).first()
    if not rp:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportOut(**rp.to_mongo().to_dict(), id=str(rp.id))

@router.post("/", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
async def create_report(report: ReportCreate):
    new_rp = Report(**report.dict())
    new_rp.save()
    return ReportOut(**new_rp.to_mongo().to_dict(), id=str(new_rp.id))

@router.put("/{report_id}", response_model=ReportOut)
async def update_report(report_id: str, report: ReportUpdate):
    if not ObjectId.is_valid(report_id):
        raise HTTPException(status_code=400, detail="Invalid report ID format")
    rp = Report.objects(id=report_id).first()
    if not rp:
        raise HTTPException(status_code=404, detail="Report not found")
    rp.update(**report.dict(exclude_unset=True))
    rp.reload()
    return ReportOut(**rp.to_mongo().to_dict(), id=str(rp.id))

@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(report_id: str):
    if not ObjectId.is_valid(report_id):
        raise HTTPException(status_code=400, detail="Invalid report ID format")
    deleted = Report.objects(id=report_id).first()
    if not deleted:
        raise HTTPException(status_code=404, detail="Report not found")
    deleted.delete()
    return None
