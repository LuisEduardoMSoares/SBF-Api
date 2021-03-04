import sqlalchemy as db

from sqlalchemy.orm import relationship

from ...db.engine import Base
from ...db.base import BaseMixin

from ..associations.models import ProductProvider


class Provider(BaseMixin, Base):
    __tablename__ = 'base_providers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    products = relationship(
        "Product",
        secondary=ProductProvider,
        back_populates="providers"
    )