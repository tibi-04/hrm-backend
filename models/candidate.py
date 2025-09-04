# models/candidate.py
from mongoengine import Document, StringField, IntField, ListField, DateTimeField
from datetime import datetime

class Candidate(Document):
    meta = {"collection": "candidates", "db_alias": "default"}

    name = StringField(required=True)
    email = StringField(required=True, unique=True)
    phone = StringField()
    address = StringField()
    skills = ListField(StringField()) 
    experience_years = IntField(default=0)
    status = StringField(default="Chờ phê duyệt")
    position = StringField()  
    department_id = StringField()  
    date_of_birth = StringField()  
    resume_link = StringField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)