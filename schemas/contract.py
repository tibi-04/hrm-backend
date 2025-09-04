from pydantic import BaseModel
from typing import Optional
from datetime import date

class ContractBase(BaseModel):
    employee_id: str
    contract_type: str  
    start_date: date
    end_date: date
    status: Optional[str] = "Active" 
    note: Optional[str] = None
    salary: Optional[float] = None
    position: Optional[str] = None

class ContractCreate(ContractBase):
    pass

class ContractUpdate(BaseModel):
    employee_id: Optional[str] = None
    contract_type: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    note: Optional[str] = None
    salary: Optional[float] = None
    position: Optional[str] = None

class ContractOut(ContractBase):
    id: str
    
    class Config:
        from_attributes = True