from db_app.serializers import UserSchema
from utils.jwt_auth import jwt_decode


def get_user_id(bearer_token):
    token = bearer_token.lstrip("Bearer")
    token = token.strip()
    jwt_authentication = jwt_decode(token)
    jwt_authentication = UserSchema().load(jwt_authentication, partial=("password",))
    user_id = jwt_authentication.id
    return user_id
