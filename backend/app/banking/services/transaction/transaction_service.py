from http import HTTPStatus

from flask_sqlalchemy import BaseQuery
from werkzeug.exceptions import abort

from app.banking.models.transaction import Transaction
from app.auth.models.user import User
from app.core.utils.querying import QueryFilter
from app.banking.services.account.account_service import get_account_by_id


def create_transaction(user: User, transaction_data: dict) -> Transaction:
    """
    Method creates new account object
    :param user:
    :param transaction_data: transaction date to save
    :type transaction_data: dict
    :return: created account object
    :rtype: Account
    """
    _validate_transaction(user, transaction_data)
    new_transaction = Transaction(
        origin_account_id=transaction_data.get("origin_account_id"),
        dest_account_id=transaction_data.get("dest_account_id"),
        amount=transaction_data.get("amount"),
        comment=transaction_data.get("comment")
    )
    new_transaction = new_transaction.save()
    if isinstance(new_transaction, Transaction):
        return new_transaction
    abort(HTTPStatus.BAD_REQUEST, new_transaction.get("err", "Unknown error occured"))


def _validate_transaction(user: User, transaction_data: dict):
    origin_account = get_account_by_id(transaction_data.get("origin_account_id"))
    dest_account = get_account_by_id(transaction_data.get("dest_account_id"))
    transaction_amount = transaction_data.get('amount')
    if origin_account.id == dest_account.id:
        abort(HTTPStatus.BAD_REQUEST, "Malformed request, cannot transfer funds on the same account!")
    if origin_account.balance < transaction_amount:
        abort(HTTPStatus.BAD_REQUEST, "You have not enough funds!")
    if not user.check_permissions(['admin']) and not user.id == origin_account.owner_id:
        abort(HTTPStatus.UNAUTHORIZED, "You can tranfer money only from your account!")
    origin_account.balance -= transaction_amount
    dest_account.balance += transaction_amount


def get_transaction_by_id(transaction_id: int) -> Transaction:
    """
    Method retrieves an account from database by id.
    If not found raises 404 Error
    :param transaction_id: account id
    :type transaction_id: id
    :return: found Account object
    :rtype: Account
    """
    return Transaction.query.filter_by(id=transaction_id).first_or_404()


def _filter_by_origin_account(query: BaseQuery, args: dict) -> BaseQuery:
    """
    Filter Accounts by their account number.
    Returns filtered query
    :param query: QuerySet that needs to be filtered
    :type query: BaseQuery
    :param args: Data retrieved from client
    :type args: dict
    :return: Filtered QuerySet on status
    :rtype: BaseQuery
    """
    origin_account_id = args['origin_account_id']
    return query.filter_by(origin_account_id=origin_account_id)


def _filter_by_dest_account(query: BaseQuery, args: dict) -> BaseQuery:
    """
    Filter Accounts by their account number.
    Returns filtered query
    :param query: QuerySet that needs to be filtered
    :type query: BaseQuery
    :param args: Data retrieved from client
    :type args: dict
    :return: Filtered QuerySet on status
    :rtype: BaseQuery
    """
    dest_account_id = args['dest_account_id']
    return query.filter_by(origin_account_id=dest_account_id)


# Query filter object that will query Account objects
transaction_query_filter = QueryFilter(
    [_filter_by_origin_account,
     _filter_by_dest_account],
    Transaction
)
