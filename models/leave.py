# models/leave.py
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class Leave(Document):
    meta = {"collection": "leaves", "db_alias": "default"}

    employee_id = StringField(required=True)  
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)
    reason = StringField()
    status = StringField(default="Pending")  
    created_at = DateTimeField(default=datetime.utcnow)
