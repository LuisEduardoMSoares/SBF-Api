from app.modules.providers.models import Provider
import sqlalchemy as db

from sqlalchemy.orm import relationship

from ...db.engine import Base
from ...db.base import BaseMixin

from ..associations.models import ProductProvider


class Product(BaseMixin, Base):
    __tablename__ = 'base_products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    providers = relationship(
        "Provider",
        secondary=ProductProvider,
        back_populates="products"
    )