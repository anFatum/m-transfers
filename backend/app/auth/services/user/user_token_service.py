from http import HTTPStatus

import jwt
from flask import request, current_app
from parse import parse
from werkzeug.exceptions import abort, Unauthorized, HTTPException

from backend.app.auth.models.user import User
from backend.app.auth.services.user.user_service import get_user_by_id
from backend.app.core.utils.logger import get_logger
from backend.app.auth.utils.auth_provider import get_auth_provider

logger = get_logger("app")

def get_user_from_token() -> User:
    """
    Gets user from JWT passed as header parameter
    :return: user retrieved from token
    :rtype: User
    """
    token = retrieve_token()
    user = authentication_token_parser(token)
    if not user:
        abort(HTTPStatus.UNAUTHORIZED, "Invalid user data")
    return user


def retrieve_token_from_headers() -> str:
    """
    Method gets the token from request headers
    Token should be set in Authorization header and
    be the Bearer token format.
    :return: Token received from headers
    :rtype: str
    """
    header = request.headers.get("Authorization")
    try:
        # Retrieve the Bearer token
        parse_result = parse('Bearer {}', header)
    except (TypeError, ValueError) as e:
        logger.exception(e)
        abort(HTTPStatus.UNAUTHORIZED, "No authentication provided")
    if not parse_result:
        logger.error("Wrong token type")
        abort(HTTPStatus.BAD_REQUEST, "Wrong format for header")
    return parse_result[0]


def retrieve_token_from_cookies():
    """
    Method gets the token from request cookies
    Token should be set as CF_Authorization cookie
    :return: Token received from headers
    :rtype: str
    """
    token = request.cookies.get("CF_Authorization")
    if not token:
        logger.exception("No CF_Authorization cookies found")
        abort(HTTPStatus.UNAUTHORIZED, "No authentication provided")
    return token


def retrieve_token() -> str:
    """
    Method tries to get authorization token from headers first,
    and then tries to get it from cookies
    :return: Authorization token
    :rtype: str
    """
    try:
        token = retrieve_token_from_headers()
    except Unauthorized:
        token = retrieve_token_from_cookies()
    return token


def authentication_token_parser(token: str) -> User:
    """
    Gets the user data from JWT token after its validation
    :param token: request Authentication header
    :type token: str
    :return: User info retrieved from token
    :rtype: User
    """
    try:
        auth_provider = get_auth_provider(current_app.config["AUTH_TYPE"])
        user = auth_provider.validate_token(token)
        user = get_user_by_id(user.get('id'))
        return user
    except (jwt.exceptions.DecodeError,
            jwt.InvalidAudienceError,
            jwt.InvalidIssuerError,
            jwt.ExpiredSignatureError) as e:
        abort(HTTPStatus.UNAUTHORIZED, str(e))
    except HTTPException as e:
        logger.exception(e)
        raise e
    except Exception as e:
        logger.exception(e)
        abort(HTTPStatus.UNAUTHORIZED, "Invalid token")