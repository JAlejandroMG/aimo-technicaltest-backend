import uuid

from peewee import *

db = SqliteDatabase('tt_backend.db')


class BaseModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True, null=False)
    password = CharField(null=False)


class Note(BaseModel):
    name = CharField(null=False)
    user = ForeignKeyField(User, null=False)
