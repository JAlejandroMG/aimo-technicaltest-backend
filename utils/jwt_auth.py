import os
from datetime import datetime

import jwt
from bottle import HTTPResponse
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')


def jwt_encode(user_id, username):
    payload = {"id": user_id, "username": username}
    jwt_encoded = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jwt_encoded


def jwt_decode(encoded):
    try:
        jwt_decoded = jwt.decode(encoded, SECRET_KEY, algorithms="HS256", headers=None, json_encoder=None)
        return jwt_decoded
    except jwt.DecodeError:
        raise HTTPResponse(body="No cuenta con las credenciales requeridas.", status=401)
    except jwt.ExpiredSignatureError:
        raise HTTPResponse(body="Su token ha expirado.", status=401)
