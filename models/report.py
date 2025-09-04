from mongoengine import Document, StringField, DateTimeField, FloatField
import datetime

class Report(Document):
    title = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    content = StringField()
    type = StringField() 
    value = FloatField(default=0)

    meta = {
        'collection': 'reports'
    }
