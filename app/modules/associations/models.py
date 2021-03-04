import sqlalchemy as db

from ...db.engine import Base


ProductProvider = db.Table('association_products_providers', Base.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('base_products.id')),
    db.Column('provider_id', db.Integer, db.ForeignKey('base_providers.id'))
)