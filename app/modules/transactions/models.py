import sqlalchemy as db

from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256

from ...db.engine import Base
from ...db.base import BaseMixin


class Transaction(BaseMixin, Base):
    __tablename__ = 'base_transactions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    product_id = db.Column(db.Integer, db.ForeignKey('base_products.id'))
    provider_id = db.Column(db.Integer, db.ForeignKey('base_providers.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('base_users.id'))

    # Relationships
    product = relationship("Product", lazy="select")
    provider = relationship("Provider", lazy="select")
    user = relationship("User", lazy="select", back_populates="transactions")