from marshmallow import Schema, fields, validate


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str(required=True, validate=validate.Length(min=1))
    password = fields.Str(required=True, validate=validate.Length(min=8))


class NoteSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True, validate=validate.Length(min=1))
    user = fields.Str(required=True, error_messages={"required": "Se requiere el id del usuario"})
