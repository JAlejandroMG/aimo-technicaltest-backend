from db_app.database import User, Note


def create_user(username, password):
    new_user = User(username=username, password=password)
    new_user.save(force_insert=True)
    return new_user


def get_all_users():
    return User.select()


def create_note(name, user):
    new_note = Note(name=name, user=user)
    new_note.save(force_insert=True)
    return new_note


def get_all_notes():
    return Note.select()


def get_user_notes(user_id):
    return Note.filter(Note.user == user_id)
