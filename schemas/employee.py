from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None 
    address: Optional[str] = None  
    department_id: Optional[str] = None
    position: Optional[str] = None
    hire_date: Optional[date] = None
    date_of_birth: Optional[date] = None
    skills: Optional[List[str]] = []
    experience_years: Optional[int] = 0
    photo_data: Optional[str] = None
    work_schedule: Optional[str] = None  # Lịch làm việc chi tiết


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeOut(EmployeeBase):
    id: str
    photo_data: Optional[str] = None

    class Config:
        from_attributes = True
        validate_by_name = True


class DepartmentExperienceStat(BaseModel):
    department_id: str
    average_experience: float
    employee_count: int

class DepartmentExperienceStatsResponse(BaseModel):
    stats: List[DepartmentExperienceStat]

class AverageEmployeeCountResponse(BaseModel):
    average_employee_count: float

class DepartmentExpDetailStat(BaseModel):
    average: float
    min: float
    max: float
    list: List[float]

class SuggestionResponse(BaseModel):
    suggest: str
    reason: str 