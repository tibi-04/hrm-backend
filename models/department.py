# models/department.py
from mongoengine import Document, StringField, ListField, ReferenceField
from models.employee import Employee  
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class Department(Document):
    meta = {"collection": "departments", "db_alias": "default"}

    name = StringField(required=True, unique=True)
    employees = ListField(ReferenceField(Employee))  

class Department(BaseModel):
    id: str = Field(alias="_id")
    name: str
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
    
    @classmethod
    async def find_all(cls):
        pass