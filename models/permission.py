from mongoengine import Document, StringField

class Permission(Document):
    name = StringField(required=True, unique=True)

    meta = {
        'collection': 'permission'
    }
