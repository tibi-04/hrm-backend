from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class CandidateBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None 
    skills: List[str] = Field(default_factory=list)
    experience_years: int = 0
    status: str = "Chờ phê duyệt"
    position: Optional[str] = None  
    department_id: Optional[str] = None 
    department_name: Optional[str] = None
    date_of_birth: Optional[str] = None  
    resume_link: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_years: Optional[int] = None
    status: Optional[str] = None
    position: Optional[str] = None  
    department_id: Optional[str] = None  
    date_of_birth: Optional[str] = None  
    resume_link: Optional[str] = None

class CandidateOut(CandidateBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True