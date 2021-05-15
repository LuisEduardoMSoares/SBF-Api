import sqlalchemy as db

from sqlalchemy.orm import relationship

from typing import List

from ...db.engine import Base
from ...db.base import BaseMixin

from .schemas import TransactionTypeEnum
from .schemas import TransactionProductsData


class Transaction(BaseMixin, Base):
    __tablename__ = 'base_transactions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(TransactionTypeEnum), nullable=False)
    description = db.Column(db.TEXT)
    date = db.Column(db.Date, nullable=False)
    
    # Foreign keys from Provider and User
    provider_id = db.Column(db.Integer, db.ForeignKey('base_providers.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('base_users.id'), nullable=False)

    # Relationships
    products_transaction = relationship('TransactionProduct', lazy='select', back_populates='transactions')
    provider = relationship('Provider', lazy='joined', uselist=False)
    user = relationship('User', lazy='select', back_populates='transactions', uselist=False)

    @property
    def products(self) -> List[TransactionProductsData]:
        return [
            TransactionProductsData.from_orm(product) 
            for product in self.products_transaction
        ]

    @property
    def provider_name(self) -> str:
        return self.provider.name