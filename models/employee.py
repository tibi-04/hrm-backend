# models/employee.py
from mongoengine import Document, StringField, EmailField, DateTimeField
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class Employee(Document):
    meta = {"collection": "employees", "db_alias": "default"}

    name = StringField(required=True)
    email = EmailField(required=True, unique=True)
    phone = StringField() 
    address = StringField()  
    department = StringField(required=True)
    position = StringField() 
    hire_date = DateTimeField(default=datetime.utcnow)
    work_schedule = StringField()  # Lịch làm việc chi tiết (dạng JSON: '{"start": "08:00", "end": "17:00"}')

class Employee(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: str
    phone: Optional[str] = None  
    address: Optional[str] = None  
    department_id: Optional[str] = None
    position: str
    hire_date: str
    skills: list[str] = []
    experience_years: int = 0
    date_of_birth: Optional[str] = None
    photo_url: Optional[str] = None
    photo_data: Optional[str] = None
    work_schedule: Optional[str] = None  # Lịch làm việc chi tiết (dạng JSON: '{"start": "08:00", "end": "17:00"}')
    
    class Config:
        validate_by_name = True
        json_encoders = {ObjectId: str}
    
    @classmethod
    async def find_all(cls):
        pass