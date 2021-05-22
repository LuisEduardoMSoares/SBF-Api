import sqlalchemy as db

from sqlalchemy.orm import relationship
from passlib.hash import pbkdf2_sha256

from ...db.engine import Base
from ...db.base import BaseMixin


class User(BaseMixin, Base):
    __tablename__ = 'base_users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    admin = db.Column("is_admin", db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)

    # Relationships
    products_created = relationship("Product", lazy="select", back_populates="user")
    providers_created = relationship("Provider", lazy="select", back_populates="user")
    transactions = relationship("Transaction", lazy="select", back_populates="user")
    

    def hash_password(self) -> None:
        self.password = pbkdf2_sha256.hash(self.password)

    def verify_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)