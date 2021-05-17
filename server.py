from bottle import run, request, post, get, response
from json import dumps

from marshmallow import ValidationError

from db_app.crud import *
from db_app.database import *
from utils.serializers import UserSchema, NoteSchema

db.connect()
db.create_tables([User, Note])
db.close()


@post('/users')
def users():
    username = request.forms.get('username')
    password = request.forms.get('password')
    user_data = {"username": username, "password": password}
    try:
        UserSchema().load(user_data)
        db.connect()
        new_user = create_user(username, password)
        db.close()
        """response.content_type = 'application/json'
        return dumps(new_user)"""
        return new_user
    except ValidationError as error:
        return error.messages


@get('/users')
def users():
    db.connect()
    all_users = get_all_users()
    db.close()
    response.content_type = 'application/json'
    return dumps(all_users)


@post('/notes')
def notes():
    name = request.forms.get('name')
    user = request.forms.get('user')
    note_data = {"name": name, "user": user}
    try:
        NoteSchema().load(note_data)
        db.connect()
        new_note = create_note(name, user)
        db.close()
        """response.content_type = 'application/json'
        return dumps(new_note)"""
        return new_note
    except ValidationError as error:
        return error.messages


@get('/notes')
def notes():
    db.connect()
    all_notes = get_all_notes()
    db.close()
    response.content_type = 'application/json'
    return dumps(all_notes)


@get('/notes/<user_id>')
def notes(user_id):
    db.connect()
    all_user_notes = get_user_notes(user_id)
    db.close()
    response.content_type = 'application/json'
    return dumps(all_user_notes)


run(host='localhost', port=8000)
