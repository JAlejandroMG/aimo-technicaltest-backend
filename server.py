from bottle import run, route, request, post, get, response
from json import dumps

from db_app.crud import *
from db_app.database import *

db.connect()
db.create_tables([User, Note])
db.close()


@post('/users')
def users():
    db.connect()
    username = request.forms.get('username')
    password = request.forms.get('password') + "NotReallyHashed"
    new_user = create_user(username, password)
    new_user_json = {
        "id": f'{new_user.id}',
        "username": new_user.username
    }
    response.content_type = 'application/json'
    db.close()
    return dumps(new_user_json)


@get('/users')
def users():
    db.connect()
    all_users = get_all_users()
    all_users_json = []
    for user in all_users:
        all_users_json.append({
            "id": str(user.id),
            "username": user.username
        })
    response.content_type = 'application/json'
    db.close()
    return dumps(all_users_json)


@post('/notes')
def notes():
    db.connect()
    name = request.forms.get('name')
    user = request.forms.get('user')
    new_note = create_note(name, user)
    new_note_json = {
        "id": f'{new_note.id}',
        "name": new_note.name,
        "user": f'{new_note.user.id}'
    }
    response.content_type = 'application/json'
    db.close()
    return dumps(new_note_json)


@get('/notes')
def notes():
    db.connect()
    all_notes = get_all_notes()
    all_notes_json = []
    for note in all_notes:
        all_notes_json.append({
            "id": str(note.id),
            "name": note.name,
            "user": f'{note.user.id}'
        })
    response.content_type = 'application/json'
    db.close()
    return dumps(all_notes_json)


@get('/notes/<user_id>')
def notes(user_id):
    db.connect()
    all_user_notes = get_user_notes(user_id)
    all_user_notes_json = []
    for note in all_user_notes:
        all_user_notes_json.append({
            "id": str(note.id),
            "name": note.name,
            "user": f'{note.user.id}'
        })
    response.content_type = 'application/json'
    db.close()
    return dumps(all_user_notes_json)


run(host='localhost', port=8000)
