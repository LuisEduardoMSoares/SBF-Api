import sqlalchemy as db

from sqlalchemy.orm import relationship

from ...db.engine import Base
from ...db.base import BaseMixin


class TransactionProduct(BaseMixin, Base):
    __tablename__ = 'base_transactions_products'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    # Transaction and Product Foreign keys
    transaction_id = db.Column(db.Integer, db.ForeignKey('base_transactions.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('base_products.id'), nullable=False)

    # Relationships
    transactions = relationship('Transaction', back_populates='products_transaction', uselist=False)

    # Define Indexes
    __table_args__ = (
        db.Index('combined_single_value', transaction_id, product_id),
    )