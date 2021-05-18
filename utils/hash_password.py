import hashlib


def hash_password(password):
    hash_func = hashlib.sha256()
    encoded_password = password.encode()
    hash_func.update(encoded_password)
    hashed_password = hash_func.hexdigest()
    return hashed_password
