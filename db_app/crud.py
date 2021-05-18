from db_app.database import User, Note
from db_app.serializers import UserSchema, NoteSchema
from utils.hash_password import hash_password


def create_user(username, password):
    hashed_password = hash_password(password)
    new_user = User(username=username, password=hashed_password)
    new_user.save(force_insert=True)
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


def find_user(username, password):
    try:
        user_id = User.select().where(User.username == username, User.password == password).get().id
        return user_id
    except User.DoesNotExist:
        return False

def create_note(name, user_id):
    new_note = Note(name=name, user=user_id)
    new_note.save(force_insert=True)
    new_note = {
        "id": new_note.id,
        "name": new_note.name,
        "user": new_note.user.id
    }
    schema = NoteSchema()
    new_note = schema.dump(new_note)
    return new_note


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
