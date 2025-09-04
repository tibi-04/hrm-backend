from pydantic import BaseModel
from typing import Optional
from datetime import date

class ReportBase(BaseModel):
    title: str
    created_at: Optional[date] = None
    content: Optional[str] = None
    type: Optional[str] = None
    value: Optional[float] = 0

class ReportCreate(ReportBase):
    pass

class ReportUpdate(ReportBase):
    pass

class ReportOut(ReportBase):
    id: str
    class Config:
        from_attributes = True
        
