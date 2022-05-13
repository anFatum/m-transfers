from http import HTTPStatus

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import abort, HTTPException

from backend.app.auth.models.user import User
from backend.app.core.utils.querying import map_query_to_json
from backend.app.auth.services.user.user_service import user_query_filter, create_user, get_user_by_id
from backend.app.auth.utils.decorators import login_required
from backend.app.auth.utils.dto import UserDto
from backend.app.auth.utils.parsers.user_parsers import user_filter_parser
from backend.app.core.parsers.request_parsers import authentication_parser
from backend.app.core.utils.iterable_utils import delete_none_keys
from backend.app.core.utils.logger import get_logger

api = UserDto.api
user_model = UserDto.user_model
logger = get_logger("app")


@api.route("s")
class UsersList(Resource):

    @api.doc("list_user", responses={
        HTTPStatus.UNAUTHORIZED: "Unauthorized",
        HTTPStatus.BAD_REQUEST: "Bad Request",
        HTTPStatus.NOT_FOUND: "Users or groups not found"
    })
    @api.expect(user_filter_parser)
    @api.marshal_with(user_model, as_list=True, code=HTTPStatus.OK)
    @login_required
    def get(self, user):
        """
        Get list of registered users.
        """
        args = user_filter_parser.parse_args()
        query = User.query
        try:
            query = user_query_filter.filter(query, delete_none_keys(args))
            users = query.all()
            return map_query_to_json(users), HTTPStatus.OK
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.exception(e)
            abort(HTTPStatus.BAD_REQUEST, "Invalid query parameter")

    @api.doc("add_user",
             responses={
                 HTTPStatus.BAD_REQUEST: "Bad Request",
                 HTTPStatus.NOT_FOUND: "Users or groups not found"
             },
             body=user_model)
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_model,
                      code=HTTPStatus.CREATED,
                      description="User was successfully created")
    def post(self):
        """
        Creates a user
        """
        new_user = create_user(request.json)
        return new_user.to_json(), HTTPStatus.CREATED


@api.route("")
class UsersDetailView(Resource):

    @api.doc("current_user_detail",
             responses={
                 HTTPStatus.UNAUTHORIZED: "Unauthorized",
                 HTTPStatus.BAD_REQUEST: "Bad Request"
             },
             parser=authentication_parser)
    @api.expect(authentication_parser)
    @api.marshal_with(user_model, code=HTTPStatus.OK)
    @login_required
    def get(self, user: User):
        """
        Returns current logged user data
        """
        user = user.to_json()
        return user, HTTPStatus.OK


@api.route("/<int:user_id>")
class UsersDetailView(Resource):

    @api.doc("user_detail",
             responses={
                 HTTPStatus.UNAUTHORIZED: "Unauthorized",
                 HTTPStatus.BAD_REQUEST: "Bad Request"
             },
             parser=authentication_parser)
    @api.expect(authentication_parser)
    @api.marshal_with(user_model, code=HTTPStatus.OK)
    @login_required
    def get(self, user: User, user_id: int):
        """
        Returns user with provided id or 404 if not found
        """
        user = get_user_by_id(user_id)
        return user.to_json(), HTTPStatus.OK
