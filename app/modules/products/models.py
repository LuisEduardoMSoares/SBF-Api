from app.modules.providers.models import Provider
import sqlalchemy as db

from sqlalchemy.orm import relationship

from ...db.engine import Base
from ...db.base import BaseMixin

from ..associations.models import ProductProvider


class ProductImage(BaseMixin, Base):
    __tablename__ = 'support_products_image'
    
    product_id = db.Column(db.Integer, db.ForeignKey('base_products.id'), primary_key=True)
    image_data = db.Column(db.TEXT, default="R0lGODdhAQABAPAAAP8AAAAAACwAAAAAAQABAAACAkQBADs=")

    product = relationship("Product", lazy="joined", back_populates="image")


class Product(BaseMixin, Base):
    __tablename__ = 'base_products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    size = db.Column(db.String, nullable=False)
    inventory = db.Column(db.Integer, nullable=False)
    description = db.Column(db.TEXT)
    weight = db.Column(db.Float)
    # TODO: Store directly in Base64 or create a support_image table with one2one relatitionship
    # image = db.Column(db.String)
    
    is_deleted = db.Column(db.Boolean, default=False) # To maintain consistency in the system, the current product must exists.

    # User Foreign key
    created_by = db.Column(db.Integer, db.ForeignKey('base_users.id'), nullable=False)

    # Relationships
    image = relationship("ProductImage", lazy="joined", back_populates="product")
    user = relationship("User", lazy="select", back_populates="products_created", uselist=False)
    providers = relationship("Provider", secondary=ProductProvider, back_populates="products")