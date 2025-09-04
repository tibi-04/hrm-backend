# models/performance.py
from mongoengine import Document, StringField, FloatField, DateField

class Performance(Document):
    meta = {"collection": "performance", "db_alias": "default"}

    employee_id = StringField(required=True) 
    review_date = DateField(required=True)
    score = FloatField(required=True)
    comment = StringField()
