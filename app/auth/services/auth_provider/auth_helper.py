from http import HTTPStatus

import jwt
from flask import current_app
from werkzeug.exceptions import abort
from bcrypt import checkpw


def validate_token(token):
    try:
        return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.DecodeError as e:
        return None


def retrieve_token(email, password):
    from app.auth.services.user.user_service import get_user_by_email

    test_user = get_user_by_email(email)
    correct_password = checkpw(password.encode('utf-8'), test_user.pw_hash.encode("utf-8"))
    if not correct_password:
        abort(HTTPStatus.UNAUTHORIZED)
    user_token = jwt.encode(test_user.to_json(), current_app.config['SECRET_KEY'])
    return user_token


def get_user_info(user):
    return user
