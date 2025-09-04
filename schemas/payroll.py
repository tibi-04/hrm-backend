
from pydantic import BaseModel
from typing import Optional

class PayrollBase(BaseModel):
    employee_id: str  # Lưu tên nhân viên
    month: str  # YYYY-MM
    base_salary: float
    bonus: Optional[float] = 0
    deduction: Optional[float] = 0
    total: float

class PayrollCreate(PayrollBase):
    pass

class PayrollUpdate(PayrollBase):
    pass

class PayrollOut(PayrollBase):
    id: str
    class Config:
        from_attributes = True
