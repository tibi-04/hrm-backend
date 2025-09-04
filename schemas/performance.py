from pydantic import BaseModel
from typing import Optional
from datetime import date

class PerformanceBase(BaseModel):
    employee_id: str
    review_date: date
    score: float
    comment: Optional[str] = None

class PerformanceCreate(PerformanceBase):
    pass

class PerformanceUpdate(PerformanceBase):
    pass

class PerformanceOut(PerformanceBase):
    id: str
    class Config:
        from_attributes = True
        
