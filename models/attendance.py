from mongoengine import Document, StringField, DateTimeField, BooleanField, ReferenceField
from datetime import datetime
from enum import Enum


class AttendanceType(Enum):
    CHECK_IN = "check-in"
    CHECK_OUT = "check-out"


class AttendanceStatus(Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

class Attendance(Document):
    meta = {"collection": "attendance", "db_alias": "default"}

    employee = ReferenceField("Employee", required=False)


    employee_id = StringField(required=True)    
    employee_name = StringField(required=True)  
    department = StringField(required=True)     
    
    date = DateTimeField(default=datetime.utcnow) 
    type = StringField(required=True, choices=[t.value for t in AttendanceType])  
    status = StringField(required=True, choices=[s.value for s in AttendanceStatus])  
    
    reason = StringField()                        
    has_permission = BooleanField(default=False)  
