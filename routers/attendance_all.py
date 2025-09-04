
from fastapi import APIRouter, HTTPException
from typing import List
from schemas.attendance import AttendanceOut
from models.attendance import Attendance  # MongoEngine model

router = APIRouter(prefix="/attendance_all", tags=["AttendanceAll"])

@router.get("/", response_model=List[AttendanceOut])
async def list_attendance_all(skip: int = 0, limit: int = 100):
    try:
        attendances = Attendance.objects.skip(skip).limit(limit)
        return [
            {
                "id": str(att.id),
                "employee_id": str(att.employee_id),
                "date": att.date,
                "status": att.status,
                "check_in": att.check_in,
                "check_out": att.check_out,
                "note": att.note
            }
            for att in attendances
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching attendance: {str(e)}")