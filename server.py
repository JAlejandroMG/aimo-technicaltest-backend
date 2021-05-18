from bottle import run, request, post, get, response, HTTPResponse
from json import dumps

from marshmallow import ValidationError

from db_app.crud import *
from db_app.database import db, User, Note
from db_app.serializers import UserSchema, NoteSchema
from utils.jwt_auth import jwt_encode, jwt_decode

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


@post('/login')
def login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    hashed_password = hash_password(password)
    db.connect()
    user_id = find_user(username, hashed_password)
    db.close()
    if not user_id:
        raise HTTPResponse(body="No cuenta con las credenciales requeridas.", status=400)
    jwt_token = jwt_encode(str(user_id), username)
    jwt_token = str(jwt_token).lstrip("b'")
    jwt_token = str(jwt_token).rstrip("'")
    return HTTPResponse(body={"token": jwt_token}, status=200)


@post('/decode')
def decode():
    token = request.forms.get('token')
    jwt_authentication = jwt_decode(token)
    print(jwt_authentication)


@post('/notes')
def notes():
    bearer_token = request.get_header('Authorization')
    bearer_token = bearer_token.lstrip("Bearer")
    bearer_token = bearer_token.strip()
    jwt_authentication = jwt_decode(bearer_token)
    jwt_authentication = UserSchema().load(jwt_authentication, partial=("password",))
    user = jwt_authentication.id
    name = request.forms.get('name')
    """user_id = request.forms.get('user_id')
    note_data = {"name": name, "user": user}"""
    pass
    try:
        note_data = NoteSchema().load({"name": name}, partial=("id", "user",))
        db.connect()
        new_note = create_note(note_data.name, user)
        db.close()
        return new_note
    except ValidationError as error:
        return error.messages


@get('/notes')
def notes():
    bearer_token = request.get_header('Authorization')
    bearer_token = bearer_token.lstrip("Bearer")
    bearer_token = bearer_token.strip()
    #print(bearer_token)
    #token = request.forms.get('token')
    #jwt_authentication = jwt_decode(token)
    jwt_authentication = jwt_decode(bearer_token)
    jwt_authentication = UserSchema().load(jwt_authentication, partial=("password",))
    user = jwt_authentication.id
    #print(jwt_authentication)
    db.connect()
    all_notes = get_user_notes(user)
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
