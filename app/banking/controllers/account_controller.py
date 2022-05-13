from http import HTTPStatus

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import abort, HTTPException

from app.auth.utils.decorators import login_required
from app.banking.models.account import Account
from app.banking.services.account.account_service import create_account, account_query_filter, get_account_by_id
from app.banking.utils.constants import INITIAL_USER_BALANCE
from app.banking.utils.dto import AccountDto
from app.banking.utils.parsers.account_parsers import account_filter_parser
from app.core.parsers.request_parsers import authentication_parser
from app.core.utils.iterable_utils import delete_none_keys
from app.core.utils.logger import get_logger
from app.core.utils.querying import map_query_to_json

api = AccountDto.api
account_model = AccountDto.account_model
logger = get_logger("app")


@api.route("s")
class UsersList(Resource):

    @api.doc("list_accounts", responses={
        HTTPStatus.UNAUTHORIZED: "Unauthorized",
        HTTPStatus.BAD_REQUEST: "Bad Request",
        HTTPStatus.NOT_FOUND: "Users or groups not found"
    })
    @api.expect(account_filter_parser)
    @api.marshal_with(account_model, as_list=True, code=HTTPStatus.OK)
    @login_required
    def get(self, user):
        """
        Get list of registered users.
        """
        args = account_filter_parser.parse_args()
        query = Account.query
        if not user.check_permissions(['admin']):
            args['owner_id'] = user.id
        try:
            query = account_query_filter.filter(query, delete_none_keys(args))
            accounts = query.all()
            return map_query_to_json(accounts), HTTPStatus.OK
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.exception(e)
            abort(HTTPStatus.BAD_REQUEST, "Invalid query parameter")

    @api.doc("open_account",
             responses={
                 HTTPStatus.BAD_REQUEST: "Bad Request",
                 HTTPStatus.NOT_FOUND: "Users or groups not found"
             },
             body=account_model,
             parser=authentication_parser)
    @api.expect(account_model, validate=True)
    @api.marshal_with(account_model,
                      code=HTTPStatus.CREATED,
                      description="User was successfully created")
    @login_required
    def post(self, user):
        """
        Creates a account for a user (if admin role can create account for any user)
        """
        initial_balance = INITIAL_USER_BALANCE
        owner_id = user.id
        if user.check_permissions(["admin"]):
            owner_id = request.json.get('owner_id', owner_id)
            initial_balance = request.json.get('balance', initial_balance)
        return create_account(owner_id, initial_balance).to_json(), HTTPStatus.CREATED


@api.route("/<int:account_id>")
class UsersDetailView(Resource):

    @api.doc("account_detail",
             responses={
                 HTTPStatus.UNAUTHORIZED: "Unauthorized",
                 HTTPStatus.BAD_REQUEST: "Bad Request"
             },
             parser=authentication_parser)
    @api.expect(authentication_parser)
    @api.marshal_with(account_model, code=HTTPStatus.OK)
    @login_required
    def get(self, user, account_id: int):
        """
        Returns user with provided id or 404 if not found
        """
        account = get_account_by_id(account_id)
        if not user.check_permissions(["admin"]) and not account.owner_id == user.id:
            abort(HTTPStatus.UNAUTHORIZED)
        return account.to_json(), HTTPStatus.OK
