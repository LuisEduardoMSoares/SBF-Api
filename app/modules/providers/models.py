import sqlalchemy as db

from sqlalchemy.orm import relationship

from ...db.engine import Base
from ...db.base import BaseMixin


class Provider(BaseMixin, Base):
    __tablename__ = 'base_providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120))
    contact_name = db.Column(db.String(100))
    
    # To maintain consistency in the system, the current product must exists.
    is_deleted = db.Column(db.Boolean, default=False)

    # User Foreign key
    created_by = db.Column(db.Integer, db.ForeignKey('base_users.id'), nullable=False)

    # Relationships
    user = relationship("User", lazy="select", back_populates="providers_created", uselist=False)