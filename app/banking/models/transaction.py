from app import db
from app.core.models.mixins import SaveableModelMixin, TimestampMixin


class Transaction(SaveableModelMixin, TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    origin_account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    origin_account = db.relationship("Account", foreign_keys=[origin_account_id],
                                     back_populates="transactions")

    dest_account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    dest_account = db.relationship("Account", foreign_keys=[dest_account_id])

    amount = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=True)
