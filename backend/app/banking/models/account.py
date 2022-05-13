from backend.app import db
from backend.app.core.models.mixins import SaveableModelMixin, JsonableMixin
from backend.app.banking.models.transaction import Transaction


class Account(SaveableModelMixin, JsonableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(20), unique=True, nullable=False)

    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", foreign_keys=[owner_id],
                            back_populates="accounts")
    outcome_transactions = db.relationship(Transaction, back_populates='origin_account',
                                           foreign_keys="Transaction.origin_account_id")
    income_transactions = db.relationship(Transaction, back_populates='origin_account',
                                          foreign_keys="Transaction.dest_account_id")
    balance = db.Column(db.Integer, nullable=False)
