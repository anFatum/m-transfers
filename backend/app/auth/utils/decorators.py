from functools import wraps
from typing import Iterable

from backend.app.auth.services.user.user_token_service import get_user_from_token
from backend.app.core.utils.logger import get_logger

logger = get_logger("app")


def login_required(f):
    """
    Decorator function that checks if user is logged in
    by validating the JWT
    :param f: function we are wrapping
    :type f: callable
    :return: decorated_function
    :rtype: callable
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_user_from_token()
        return f(*args, user, **kwargs)

    return decorated_function


def roles_required(*roles: str):
    """
    Decorator function that checks if user is logged in
    and has all roles passed in by validating the JWT
    :param roles: roles that user needs to have
    :type roles: Iterable
    :return: decorated_function
    :rtype: callable
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_user_from_token()
            user.check_permissions_or_401(roles)
            return f(*args, user, **kwargs)

        return decorated_function

    return decorator

