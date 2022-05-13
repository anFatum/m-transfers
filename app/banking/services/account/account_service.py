from http import HTTPStatus

from faker import Faker
from werkzeug.exceptions import abort

from app.banking.models.account import Account

from flask_sqlalchemy import BaseQuery
from app.core.utils.querying import QueryFilter

f = Faker()


def create_account(owner_id: int, initial_balance: int) -> Account:
    """
    Method creates new account object
    :param owner_id: account owner id
    :type owner_id: int
    :param initial_balance: initial account balance
    :type initial_balance: int
    :return: created account object
    :rtype: Account
    """
    new_account = Account(
        owner_id=owner_id,
        account_number=f.credit_card_number(),
        balance=initial_balance
    )
    new_account = new_account.save()
    if isinstance(new_account, Account):
        return new_account
    abort(HTTPStatus.BAD_REQUEST, new_account.get("err", "Unknown error occured"))


def get_account_by_id(account_id: int) -> Account:
    """
    Method retrieves user from database by id.
    If not found raises 404 Error
    :param account_id: user data with id and groups
    :type account_id: id
    :return: found User object
    :rtype: User
    """
    return Account.query.filter_by(id=account_id).first_or_404()


def _filter_by_account_number(query: BaseQuery, args: dict) -> BaseQuery:
    """
    Filter Users by their email.
    Returns filtered query
    :param query: QuerySet that needs to be filtered
    :type query: BaseQuerySet
    :param args: Data retrieved from client
    :type args: dict
    :return: Filtered QuerySet on status
    :rtype: BaseQuerySet
    """
    account_number = args['account_number']
    return query.filter_by(account_number=account_number)


def _filter_by_owner_id(query: BaseQuery, args: dict) -> BaseQuery:
    """
    Filter Users by their email.
    Returns filtered query
    :param query: QuerySet that needs to be filtered
    :type query: BaseQuerySet
    :param args: Data retrieved from client
    :type args: dict
    :return: Filtered QuerySet on status
    :rtype: BaseQuerySet
    """
    owner_id = args['owner_id']
    return query.filter_by(owner_id=owner_id)


# Query filter object that will query Test Request objects
account_query_filter = QueryFilter(
    [_filter_by_account_number,
     _filter_by_owner_id],
    Account
)
