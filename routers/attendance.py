from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.database import SessionLocal
from schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceOut
from crud import attendance as crud_attendance

router = APIRouter(prefix="/attendance", tags=["Attendance"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[AttendanceOut])
def list_attendance(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_attendance.get_attendances(db, skip=skip, limit=limit)

@router.get("/{attendance_id}", response_model=AttendanceOut)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    att = crud_attendance.get_attendance(db, attendance_id)
    if not att:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return att

@router.post("/", response_model=AttendanceOut, status_code=status.HTTP_201_CREATED)
def create_attendance(att: AttendanceCreate, db: Session = Depends(get_db)):
    return crud_attendance.create_attendance(db, att)

@router.put("/{attendance_id}", response_model=AttendanceOut)
def update_attendance(attendance_id: int, att: AttendanceUpdate, db: Session = Depends(get_db)):
    updated = crud_attendance.update_attendance(db, attendance_id, att)
    if not updated:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return updated

@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    ok = crud_attendance.delete_attendance(db, attendance_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return None
