import sqlalchemy as db

from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256

from ...db.engine import Base
from ...db.base import BaseMixin

from .schemas import TransactionTypeEnum


class Transaction(BaseMixin, Base):
    __tablename__ = 'base_transactions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(TransactionTypeEnum), nullable=False)
    description = db.Column(db.TEXT)
    quantity = db.Column(db.Integer, nullable=False)
    # TODO: Adicionar um campo data para a transação
    
    # Foreign keys from Product, Provider and User
    product_id = db.Column(db.Integer, db.ForeignKey('base_products.id'), nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('base_providers.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('base_users.id'), nullable=False)

    # Relationships
    product = relationship("Product", lazy="select", uselist=False)
    provider = relationship("Provider", lazy="select", uselist=False)
    user = relationship("User", lazy="select", back_populates="transactions", uselist=False)