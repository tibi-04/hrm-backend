from pydantic import BaseModel
from typing import Optional
from datetime import date

class LeaveBase(BaseModel):
    employee_id: str  
    start_date: date
    end_date: date
    reason: Optional[str] = None
    status: Optional[str] = "Pending"

class LeaveCreate(LeaveBase):
    pass

class LeaveUpdate(LeaveBase):
    pass

class LeaveOut(LeaveBase):
    id: str
    class Config:
        from_attributes = True
        
