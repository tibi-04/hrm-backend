from sqlalchemy.orm import Session
from models.attendance import Attendance
from schemas.attendance import AttendanceCreate, AttendanceUpdate
from typing import List, Optional
from datetime import date

def get_attendances(db: Session, skip: int = 0, limit: int = 100) -> List[Attendance]:
    return db.query(Attendance).offset(skip).limit(limit).all()
def get_attendance(db: Session, attendance_id: str) -> Optional[Attendance]:
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()

def create_attendance(db: Session, att: AttendanceCreate) -> Attendance:
    import uuid
    db_att = Attendance(
        id=str(uuid.uuid4()),
        employee_id=att.employee_id,
        date=att.date,
        status=att.status
    )
    db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return db_att

def delete_attendance(db: Session, attendance_id: str) -> bool:
    db_att = get_attendance(db, attendance_id)
    if not db_att:
        return False
    db.delete(db_att)
    db.commit()
    return True
