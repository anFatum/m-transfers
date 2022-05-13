from flask_restplus import Namespace, fields
from backend.app.auth.utils.dto import UserDto


class AccountDto:
    api = Namespace("Account API", path="/account", description="Account related operations")
    account_model = api.model("Account", {
        "id": fields.String(readonly=True),
        "account_number": fields.String(readonly=True),
        "owner": fields.Nested(UserDto.user_model, skip_none=True, readonly=True),
        "owner_id": fields.Integer(),
        "balance": fields.Integer(),
        "outcome_transactions": fields.List(fields.Raw()),
        "income_transactions": fields.List(fields.Raw())
    })


class TransactionDto:
    api = Namespace("Transaction API", path="/transaction", description="Transaction related operations")
    transaction_model = api.model("Transaction", {
        "id": fields.String(readonly=True),
        "origin_account_id": fields.Integer(required=True),
        "dest_account_id": fields.Integer(required=True),
        "amount": fields.Integer(required=True),
        "comment": fields.String(),
        "created_at": fields.String()
    })
