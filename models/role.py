from mongoengine import Document, StringField, ListField, ReferenceField
from .permission import Permission

class Role(Document):
    name = StringField(required=True, unique=True)
    permissions = ListField(ReferenceField(Permission))

    meta = {
        'collection': 'role'
    }
