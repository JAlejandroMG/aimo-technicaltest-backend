from marshmallow import Schema, fields, validate, post_load

from db_app.database import User, Note


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=8))

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class NoteSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    user = fields.Str(required=True, error_messages={"required": "Se requiere el id del usuario"})

    @post_load
    def make_note(self, data, **kwargs):
        return Note(**data)
