from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class AttendanceType(str, Enum):
    check_in = "check-in"
    check_out = "check-out"

class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"

class AttendanceBase(BaseModel):
    employee_id: str
    employee_name: str
    department: str
    date: str
    type: AttendanceType
    status: AttendanceStatus = AttendanceStatus.present
    reason: Optional[str] = None
    has_permission: bool = False
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    employee_id: Optional[str] = None
    employee_name: Optional[str] = None
    department: Optional[str] = None
    date: Optional[str] = None
    type: Optional[AttendanceType] = None
    status: Optional[AttendanceStatus] = None
    reason: Optional[str] = None
    has_permission: Optional[bool] = None
    check_in_time: Optional[str] = None
    check_out_time: Optional[str] = None

class AttendanceOut(AttendanceBase):
    id: str

    class Config:
        from_attributes = True