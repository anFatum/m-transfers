from http import HTTPStatus

from flask import request
from flask_restplus import Resource
from werkzeug.exceptions import abort, HTTPException

from backend.app.auth.utils.decorators import login_required, roles_required
from backend.app.banking.models.transaction import Transaction
from backend.app.banking.services.transaction.transaction_service import create_transaction, get_transaction_by_id, \
    transaction_query_filter
from backend.app.banking.utils.dto import TransactionDto
from backend.app.banking.utils.parsers.transaction_parsers import transaction_filter_parser
from backend.app.core.parsers.request_parsers import authentication_parser
from backend.app.core.utils.iterable_utils import delete_none_keys
from backend.app.core.utils.logger import get_logger
from backend.app.core.utils.querying import map_query_to_json

api = TransactionDto.api
transaction_model = TransactionDto.transaction_model
logger = get_logger("app")


@api.route("s")
class TransactionList(Resource):

    @api.doc("list_transactions", responses={
        HTTPStatus.UNAUTHORIZED: "Unauthorized",
        HTTPStatus.BAD_REQUEST: "Bad Request",
        HTTPStatus.NOT_FOUND: "Users or groups not found"
    })
    @api.expect(transaction_filter_parser)
    @api.marshal_with(transaction_model, as_list=True, code=HTTPStatus.OK)
    @roles_required('admin')
    def get(self, user):
        """
        Get list of all transactions (available only for admin user).
        """
        args = transaction_filter_parser.parse_args()
        query = Transaction.query
        try:
            query = transaction_query_filter.filter(query, delete_none_keys(args))
            accounts = query.all()
            return map_query_to_json(accounts), HTTPStatus.OK
        except Exception as e:
            if isinstance(e, HTTPException):
                raise e
            logger.exception(e)
            abort(HTTPStatus.BAD_REQUEST, "Invalid query parameter")

    @api.doc("make_transaction",
             responses={
                 HTTPStatus.BAD_REQUEST: "Bad Request",
                 HTTPStatus.NOT_FOUND: "Resource is not found"
             },
             body=transaction_model,
             parser=authentication_parser)
    @api.expect(transaction_model, validate=True)
    @api.marshal_with(transaction_model,
                      code=HTTPStatus.CREATED,
                      description="Transaction was successfully created")
    @login_required
    def post(self, user):
        """
        Makes a transaction between accounts (if has enough balance).
        Non admin users can transfer money only from their accounts
        """
        new_transaction = create_transaction(user, {
            "origin_account_id": request.json.get("origin_account_id"),
            "dest_account_id": request.json.get("dest_account_id"),
            "amount": request.json.get("amount"),
            "comment": request.json.get("comment")
        })
        return new_transaction.to_json(), HTTPStatus.CREATED


@api.route("/<int:transaction_id>")
class UsersDetailView(Resource):

    @api.doc("transaction_detail",
             responses={
                 HTTPStatus.UNAUTHORIZED: "Unauthorized",
                 HTTPStatus.BAD_REQUEST: "Bad Request"
             },
             parser=authentication_parser)
    @api.expect(authentication_parser)
    @api.marshal_with(transaction_model, code=HTTPStatus.OK)
    @roles_required('admin')
    def get(self, user, transaction_id: int):
        """
        Returns details of a transaction. Admin role required
        """
        transaction = get_transaction_by_id(transaction_id)
        return transaction.to_json(), HTTPStatus.OK
