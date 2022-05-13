from http import HTTPStatus

from bcrypt import hashpw, gensalt
from flask_sqlalchemy import BaseQuery
from werkzeug.exceptions import abort

from app.auth.models.user import User, UserRoles
from app.core.utils.logger import get_logger
from app.core.utils.querying import QueryFilter

logger = get_logger("app")


def hash_password(password: str) -> bytes:
    """
    Method to hash provided by user password
    :param password: str
    :return: hashed password
    :rtype: bytes
    """
    salt = gensalt()
    hashed_pass = hashpw(
        password.encode('utf-8'),
        salt
    )
    return hashed_pass


def get_user_by_email(user_email: str) -> User:
    """
    Method retrieves user from database by the email.
    If not found raises Not found
    :param user_email: user email
    :type user_email: str
    :return: found User object
    :rtype: User
    """
    return User.query.filter_by(email=user_email).first_or_404(
        description=f"User with email {user_email} not found")


def get_user_by_id(user_id: int) -> User:
    """
    Method retrieves user from database by id.
    If not found raises 404 Error
    :param user_id: user data with id and groups
    :type user_id: id
    :return: found User object
    :rtype: User
    """
    return User.query.filter_by(id=user_id).first_or_404()


def raise_if_invalid_roles(user: User):
    """
    Raises BAD REQUEST error if the user is provided with
    invalid roles not present in UserRoles enum
    :param user: user that's about to be created
    :return: None
    """
    if user.has_invalid_roles():
        abort(HTTPStatus.BAD_REQUEST,
              f"Valid roles are: {', '.join(UserRoles.values())}")


def create_user(user_data: dict) -> User:
    """
    Method creates new user object
    :param user_data: that comes from request
    :type user_data: dict
    :return: created User object
    :rtype: User
    """
    hashed_pw = hash_password(user_data.get("password"))
    new_user = User(
        email=user_data.get("email"),
        roles=";".join(user_data.get("roles", [])),
        name=user_data.get("name"),
        pw_hash=hashed_pw.decode("utf-8")
    )
    raise_if_invalid_roles(new_user)
    new_user = new_user.save()
    if isinstance(new_user, User):
        return new_user
    abort(HTTPStatus.BAD_REQUEST, new_user.get("err", "Unknown error occured"))


def _filter_by_email(query: BaseQuery, args: dict) -> BaseQuery:
    """
    Filter Users by their email.
    Returns filtered query
    :param query: QuerySet that needs to be filtered
    :type query: BaseQuery
    :param args: Data retrieved from client
    :type args: dict
    :return: Filtered QuerySet on status
    :rtype: BaseQuery
    """
    email = args['email']
    return query.filter_by(email=email)


# Query filter object that will query Test Request objects
user_query_filter = QueryFilter(
    [_filter_by_email],
    User
)
