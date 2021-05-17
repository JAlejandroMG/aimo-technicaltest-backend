from db_app.database import User, Note
from utils.serializers import UserSchema, NoteSchema


def create_user(username, password):
    new_user = User(username=username, password=password)
    new_user.save(force_insert=True)
    """new_user = {
        "id": f'{new_user.id}',
        "username": new_user.username
    }"""
    schema = UserSchema(only=("id", "username"))
    new_user = schema.dump(new_user)
    return new_user


def get_all_users():
    all_users = User.select()
    all_users_json = []
    for user in all_users:
        all_users_json.append({
            "id": str(user.id),
            "username": user.username
        })
    return all_users_json


def create_note(name, user):
    new_note = Note(name=name, user=user)
    new_note.save(force_insert=True)
    new_note = {
        "id": new_note.id,
        "name": new_note.name,
        "user": new_note.user.id
    }
    schema = NoteSchema()
    new_note = schema.dump(new_note)
    return new_note


def get_all_notes():
    """all_notes = list(Note.select())
    print(all_notes)"""
    all_notes = Note.select()
    all_notes_json = []
    for note in all_notes:
        all_notes_json.append({
            "id": str(note.id),
            "name": note.name,
            "user": str(note.user.id)
        })
    """schema = NoteSchema(many=True)
    all_notes = schema.dump(all_notes)
    return all_notes"""
    return all_notes_json


def get_user_notes(user_id):
    all_user_notes = Note.filter(Note.user == user_id)
    all_user_notes_json = []
    for note in all_user_notes:
        all_user_notes_json.append({
            "id": str(note.id),
            "name": note.name,
            "user": str(note.user.id)
        })
    return all_user_notes_json
