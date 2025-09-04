from mongoengine import (
    Document, EmailField, StringField, ListField, BooleanField, DateTimeField
)
import datetime

class User(Document):
    meta = {
        "collection": "user",
        "db_alias": "default"
    }

    email = EmailField(required=True, unique=True)
    hashed_password = StringField(required=True)

    avatar = StringField(default="")
    name = StringField()
    phone = StringField()
    address = StringField()
    position = StringField()

    roles = ListField(StringField(), default=["user"])  
    permissions = ListField(StringField(), default=[])

    is_active = BooleanField(default=True)

    created_at = DateTimeField(default=datetime.datetime.utcnow)
    updated_at = DateTimeField(default=datetime.datetime.utcnow)

    def save(self, *args, **kwargs):
        """Tự động cập nhật updated_at"""
        self.updated_at = datetime.datetime.utcnow()
        return super(User, self).save(*args, **kwargs)
