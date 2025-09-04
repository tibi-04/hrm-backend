# models/payroll.py
from mongoengine import Document, StringField, FloatField, DateTimeField
from datetime import datetime

class Payroll(Document):
    meta = {"collection": "payrolls", "db_alias": "default"}

    employee_id = StringField(required=True)      
    month = StringField(required=True)            
    base_salary = FloatField(required=True)       
    bonus = FloatField(default=0)                 
    deduction = FloatField(default=0)            
    total = FloatField(required=True)             
    created_at = DateTimeField(default=datetime.utcnow)
