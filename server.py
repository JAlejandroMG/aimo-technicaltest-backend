import json

from bottle import app, run, request, post, get, response, HTTPResponse, hook
from json import dumps

from bottle_cors_plugin import cors_plugin
from marshmallow import ValidationError

from db_app.crud import *
from db_app.database import db, User, Note
from db_app.serializers import UserSchema, NoteSchema
from utils.jwt_auth import jwt_encode
from utils.user_id import get_user_id

db.connect()
db.create_tables([User, Note])
db.close()


@post('/v1/users')
def users():
    username = request.forms.get('username')
    password = request.forms.get('password')
    user_data = {"username": username, "password": password}
    try:
        UserSchema().load(user_data)
        db.connect()
        new_user = create_user(username, password)
        db.close()
        return new_user
    except ValidationError as error:
        return error.messages


@get('/v1/users')
def users():
    db.connect()
    all_users = get_all_users()
    db.close()
    response.content_type = 'application/json'
    return dumps(all_users)


@post('/v1/login')
def login():
    body = request.body.read()
    body = str(body).lstrip("b'")
    body = str(body).rstrip("'")
    body = json.loads(body)
    username = body['username']
    password = body['password']
    hashed_password = hash_password(password)
    db.connect()
    user_id = find_user(username, hashed_password)
    db.close()
    if not user_id:
        return HTTPResponse(body="No cuenta con las credenciales requeridas.", status=400)
    jwt_token = jwt_encode(str(user_id), username)
    jwt_token = str(jwt_token).lstrip("b'")
    jwt_token = str(jwt_token).rstrip("'")
    body = json.dumps({"token": jwt_token})
    response.content_type = 'application/json'
    print(body)
    return HTTPResponse(body=body, status=200)


@post('/v1/notes')
def notes():
    bearer_token = request.get_header('Authorization')
    user_id = get_user_id(bearer_token)
    name = request.forms.get('name')
    try:
        note_data = NoteSchema().load({"name": name}, partial=("id", "user",))
        db.connect()
        new_note = create_note(note_data.name, user_id)
        db.close()
        return new_note
    except ValidationError as error:
        return error.messages


@get('/v1/notes')
def notes():
    bearer_token = request.get_header('Authorization')
    user_id = get_user_id(bearer_token)
    db.connect()
    all_notes = get_user_notes(user_id)
    db.close()
    response.content_type = 'application/json'
    return dumps(all_notes)


app = app()
app.install(cors_plugin('*'))


allow_origin = '*'
allow_methods = 'PUT,GET'
allow_headers = 'Authorization, Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@hook('after_request')
def enable_cors():
    response.headers['Acces-Control-Allow-Origin'] = allow_origin
    response.headers['Acces-Control-Allow-Methods'] = allow_methods
    response.headers['Acces-Control-Allow-Headers'] = allow_headers


run(host='localhost', port=8000)
